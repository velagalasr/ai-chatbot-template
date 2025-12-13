"""
Pinecone Vector Database Implementation
"""

from typing import List, Optional
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.schema import Document
import pinecone

from ...utils import get_config, get_logger

logger = get_logger(__name__)


class PineconeStore:
    """Pinecone vector store implementation."""
    
    def __init__(self, embeddings):
        """
        Initialize Pinecone store.
        
        Args:
            embeddings: Embeddings instance
        """
        self.config = get_config()
        self.rag_config = self.config.get_rag_config()
        self.pinecone_config = self.rag_config.get('pinecone', {})
        
        self.index_name = self.pinecone_config.get('index_name', 'chatbot-index')
        self.dimension = self.pinecone_config.get('dimension', 1536)
        self.environment = self.pinecone_config.get('environment', 'gcp-starter')
        
        self.embeddings = embeddings
        self.vectorstore: Optional[LangchainPinecone] = None
        
        # Initialize Pinecone
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and index."""
        try:
            api_key = self.config.get_api_key(
                self.pinecone_config.get('api_key_env', 'PINECONE_API_KEY')
            )
            
            # Initialize Pinecone
            pinecone.init(
                api_key=api_key,
                environment=self.environment
            )
            
            # Check if index exists, create if not
            if self.index_name not in pinecone.list_indexes():
                logger.info(f"Creating Pinecone index: {self.index_name}")
                pinecone.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric='cosine'
                )
            
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []
        
        try:
            if self.vectorstore is None:
                # Create new vector store
                self.vectorstore = LangchainPinecone.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    index_name=self.index_name
                )
                logger.info(f"Created Pinecone store with {len(documents)} documents")
            else:
                # Add to existing store
                ids = self.vectorstore.add_documents(documents)
                logger.info(f"Added {len(documents)} documents to Pinecone")
                return ids
            
            return []
        
        except Exception as e:
            logger.error(f"Error adding documents to Pinecone: {e}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            score_threshold: Minimum similarity score
            
        Returns:
            List of similar documents
        """
        if self.vectorstore is None:
            # Initialize vector store for search
            self.vectorstore = LangchainPinecone.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings
            )
        
        try:
            if score_threshold is not None:
                results = self.vectorstore.similarity_search_with_score(query, k=k)
                # Filter by threshold
                filtered_results = [
                    doc for doc, score in results
                    if score >= score_threshold
                ]
                return filtered_results
            else:
                return self.vectorstore.similarity_search(query, k=k)
        
        except Exception as e:
            logger.error(f"Error searching Pinecone: {e}")
            return []
    
    def as_retriever(self, **kwargs):
        """
        Get a retriever interface.
        
        Args:
            **kwargs: Additional arguments for retriever
            
        Returns:
            Retriever instance
        """
        if self.vectorstore is None:
            self.vectorstore = LangchainPinecone.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings
            )
        
        search_kwargs = {
            'k': self.rag_config.get('top_k', 5)
        }
        search_kwargs.update(kwargs)
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    def delete_index(self):
        """Delete the Pinecone index."""
        try:
            pinecone.delete_index(self.index_name)
            self.vectorstore = None
            logger.info(f"Deleted Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error deleting index: {e}")
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        try:
            index = pinecone.Index(self.index_name)
            stats = index.describe_index_stats()
            
            return {
                "status": "active",
                "document_count": stats.get('total_vector_count', 0),
                "index_name": self.index_name,
                "dimension": self.dimension
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "error": str(e)}
