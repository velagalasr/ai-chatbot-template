"""
FAISS Vector Database Implementation
"""

import pickle
from typing import List, Optional
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from ...utils import get_config, get_logger

logger = get_logger(__name__)


class FAISSStore:
    """FAISS vector store implementation."""
    
    def __init__(self, embeddings):
        """
        Initialize FAISS store.
        
        Args:
            embeddings: Embeddings instance
        """
        self.config = get_config()
        self.rag_config = self.config.get_rag_config()
        self.faiss_config = self.rag_config.get('faiss', {})
        
        self.index_path = self.faiss_config.get('index_path', './data/faiss/index')
        self.index_type = self.faiss_config.get('index_type', 'FlatL2')
        
        # Ensure directory exists
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.embeddings = embeddings
        self.vectorstore: Optional[FAISS] = None
        
        # Try to load existing store
        self._load_store()
    
    def _load_store(self):
        """Load existing vector store."""
        if Path(self.index_path + ".faiss").exists():
            try:
                self.vectorstore = FAISS.load_local(
                    self.index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded FAISS store from {self.index_path}")
            except Exception as e:
                logger.warning(f"Could not load existing store: {e}")
                self.vectorstore = None
        else:
            logger.info("No existing FAISS store found")
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
            self.vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            logger.info(f"Created new FAISS store with {len(documents)} documents")
        else:
            # Add to existing store
            self.vectorstore.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to FAISS")
        
        # Save the store
        self.save()
        
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
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            # Filter by threshold (FAISS returns distance, lower is better)
            # Convert to similarity score (1 / (1 + distance))
            filtered_results = [
                doc for doc, distance in results
                if (1 / (1 + distance)) >= score_threshold
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
    
    def save(self):
        """Save the vector store to disk."""
        if self.vectorstore:
            self.vectorstore.save_local(self.index_path)
            logger.info(f"Saved FAISS store to {self.index_path}")
    
    def delete_store(self):
        """Delete the vector store."""
        if self.vectorstore:
            self.vectorstore = None
        
        # Delete files
        for ext in ['.faiss', '.pkl']:
            file_path = Path(self.index_path + ext)
            if file_path.exists():
                file_path.unlink()
        
        logger.info("Deleted FAISS store")
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        if self.vectorstore is None:
            return {"status": "not_initialized", "document_count": 0}
        
        try:
            # FAISS doesn't have a direct count method
            # Count from docstore
            count = len(self.vectorstore.docstore._dict) if hasattr(self.vectorstore, 'docstore') else 0
            return {
                "status": "active",
                "document_count": count,
                "index_type": self.index_type
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "error": str(e)}
