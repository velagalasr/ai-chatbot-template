"""
RAG System Manager
Manages the complete RAG pipeline.
"""

from typing import Optional, List, Any
from langchain_core.documents import Document

from .document_loader import DocumentLoader
from .embeddings import EmbeddingsManager
from .vectordb import ChromaDBStore, FAISSStore
from ..utils import get_config, get_logger

# Optional import for PineconeStore
try:
    from .vectordb import PineconeStore
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

logger = get_logger(__name__)


class RAGManager:
    """Manages the complete RAG system."""
    
    def __init__(self):
        """Initialize the RAG manager."""
        self.config = get_config()
        self.rag_config = self.config.get_rag_config()
        
        # Check if RAG is enabled
        self.enabled = self.rag_config.get('enabled', True)
        
        if not self.enabled:
            logger.info("RAG is disabled in configuration")
            self.vectorstore = None
            return
        
        # Initialize components
        self.document_loader = DocumentLoader()
        self.embeddings_manager = EmbeddingsManager()
        
        # Initialize vector store
        self.vectorstore = self._create_vectorstore()
    
    def _create_vectorstore(self) -> Any:
        """
        Create vector store based on configuration.
        
        Returns:
            Vector store instance
        """
        vector_db = self.rag_config.get('vector_db', 'chromadb')
        embeddings = self.embeddings_manager.get_embeddings()
        
        logger.info(f"Initializing vector database: {vector_db}")
        
        if vector_db == 'chromadb':
            return ChromaDBStore(embeddings)
        elif vector_db == 'faiss':
            return FAISSStore(embeddings)
        elif vector_db == 'pinecone':
            if not PINECONE_AVAILABLE:
                raise ValueError("Pinecone is not installed. Install with: pip install pinecone-client")
            return PineconeStore(embeddings)
        else:
            raise ValueError(f"Unsupported vector database: {vector_db}")
    
    def initialize_documents(self, file_paths: Optional[List[str]] = None) -> int:
        """
        Load and index documents.
        
        Args:
            file_paths: Optional list of specific files to index
            
        Returns:
            Number of document chunks indexed
        """
        if not self.enabled:
            logger.warning("RAG is disabled")
            return 0
        
        logger.info("Loading and processing documents...")
        
        # Load and split documents
        chunks = self.document_loader.process_documents(file_paths)
        
        if not chunks:
            logger.warning("No documents to index")
            return 0
        
        # Add to vector store
        self.vectorstore.add_documents(chunks)
        
        logger.info(f"Successfully indexed {len(chunks)} document chunks")
        return len(chunks)
    
    def get_retriever(self, **kwargs) -> Optional[Any]:
        """
        Get a retriever for RAG queries.
        
        Args:
            **kwargs: Additional arguments for retriever
            
        Returns:
            Retriever instance or None
        """
        if not self.enabled or not self.vectorstore:
            return None
        
        return self.vectorstore.as_retriever(**kwargs)
    
    def search(
        self,
        query: str,
        k: Optional[int] = None,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            k: Number of results (uses config default if None)
            score_threshold: Minimum similarity score (uses config default if None)
            
        Returns:
            List of relevant documents
        """
        if not self.enabled or not self.vectorstore:
            logger.warning("RAG is not available")
            return []
        
        # Use config defaults if not specified
        if k is None:
            k = self.rag_config.get('top_k', 5)
        if score_threshold is None:
            score_threshold = self.rag_config.get('similarity_threshold', 0.7)
        
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            score_threshold=score_threshold
        )
    
    def get_stats(self) -> dict:
        """
        Get statistics about the RAG system.
        
        Returns:
            Dictionary with RAG statistics
        """
        if not self.enabled:
            return {"enabled": False}
        
        stats = {
            "enabled": True,
            "vector_db": self.rag_config.get('vector_db'),
            "embeddings_provider": self.rag_config.get('embeddings', {}).get('provider')
        }
        
        if self.vectorstore:
            stats.update(self.vectorstore.get_stats())
        
        return stats
    
    def clear_vectorstore(self):
        """Clear all documents from the vector store."""
        if not self.enabled or not self.vectorstore:
            logger.warning("RAG is not available")
            return
        
        vector_db = self.rag_config.get('vector_db', 'chromadb')
        
        if vector_db == 'chromadb':
            self.vectorstore.delete_collection()
        elif vector_db == 'faiss':
            self.vectorstore.delete_store()
        elif vector_db == 'pinecone':
            logger.warning("Pinecone index deletion not automatic. Use delete_index() carefully.")
        
        logger.info("Cleared vector store")
        
        # Reinitialize
        self.vectorstore = self._create_vectorstore()
