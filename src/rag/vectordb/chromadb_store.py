"""
ChromaDB Vector Database Implementation
"""

from typing import List, Optional
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from ...utils import get_config, get_logger

logger = get_logger(__name__)


class ChromaDBStore:
    """ChromaDB vector store implementation."""
    
    def __init__(self, embeddings):
        """
        Initialize ChromaDB store.
        
        Args:
            embeddings: Embeddings instance
        """
        self.config = get_config()
        self.rag_config = self.config.get_rag_config()
        self.chroma_config = self.rag_config.get('chromadb', {})
        
        self.persist_directory = self.chroma_config.get('persist_directory', './data/chromadb')
        self.collection_name = self.chroma_config.get('collection_name', 'chatbot_docs')
        
        # Ensure directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        self.embeddings = embeddings
        self.vectorstore: Optional[Chroma] = None
        
        # Try to load existing store
        self._load_or_create_store()
    
    def _load_or_create_store(self):
        """Load existing vector store or create new one."""
        try:
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info(f"Loaded ChromaDB store from {self.persist_directory}")
        except Exception as e:
            logger.warning(f"Could not load existing store: {e}. Will create new one when documents are added.")
            self.vectorstore = None
    
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
        
        if self.vectorstore is None:
            # Create new vector store
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )
            logger.info(f"Created new ChromaDB store with {len(documents)} documents")
        else:
            # Add to existing store
            ids = self.vectorstore.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            return ids
        
        return []
    
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
            logger.warning("Vector store not initialized")
            return []
        
        if score_threshold is not None:
            results = self.vectorstore.similarity_search_with_relevance_scores(
                query, k=k
            )
            # Filter by threshold
            filtered_results = [
                doc for doc, score in results
                if score >= score_threshold
            ]
            return filtered_results
        else:
            return self.vectorstore.similarity_search(query, k=k)
    
    def as_retriever(self, **kwargs):
        """
        Get a retriever interface.
        
        Args:
            **kwargs: Additional arguments for retriever
            
        Returns:
            Retriever instance
        """
        if self.vectorstore is None:
            logger.warning("Vector store not initialized")
            return None
        
        search_kwargs = {
            'k': self.rag_config.get('top_k', 5)
        }
        search_kwargs.update(kwargs)
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    def delete_collection(self):
        """Delete the collection."""
        if self.vectorstore:
            self.vectorstore.delete_collection()
            self.vectorstore = None
            logger.info("Deleted ChromaDB collection")
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        if self.vectorstore is None:
            return {"status": "not_initialized", "document_count": 0}
        
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "status": "active",
                "document_count": count,
                "collection_name": self.collection_name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "error": str(e)}
