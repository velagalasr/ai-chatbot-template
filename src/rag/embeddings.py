"""
Embeddings Manager
Handles creation of embeddings for documents.
"""

from typing import Any, List
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

from ..utils import get_config, get_logger

logger = get_logger(__name__)


class EmbeddingsManager:
    """Manages embedding generation for documents."""
    
    def __init__(self):
        """Initialize the embeddings manager."""
        self.config = get_config()
        self.rag_config = self.config.get_rag_config()
        self.embeddings_config = self.rag_config.get('embeddings', {})
        
        self.embeddings = self._create_embeddings()
    
    def _create_embeddings(self) -> Any:
        """
        Create embeddings instance based on configuration.
        
        Returns:
            Embeddings instance
        """
        provider = self.embeddings_config.get('provider', 'openai')
        
        logger.info(f"Creating embeddings with provider: {provider}")
        
        if provider == 'openai':
            return self._create_openai_embeddings()
        elif provider in ['huggingface', 'sentence-transformers']:
            return self._create_huggingface_embeddings()
        else:
            raise ValueError(f"Unsupported embeddings provider: {provider}")
    
    def _create_openai_embeddings(self) -> OpenAIEmbeddings:
        """Create OpenAI embeddings."""
        api_key = self.config.get_api_key(
            self.embeddings_config.get('api_key_env', 'OPENAI_API_KEY')
        )
        
        return OpenAIEmbeddings(
            model=self.embeddings_config.get('model', 'text-embedding-ada-002'),
            openai_api_key=api_key
        )
    
    def _create_huggingface_embeddings(self) -> HuggingFaceEmbeddings:
        """Create HuggingFace/Sentence-Transformers embeddings."""
        hf_config = self.embeddings_config.get('huggingface', {})
        model_name = hf_config.get('model_id', 'sentence-transformers/all-MiniLM-L6-v2')
        
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def get_embeddings(self) -> Any:
        """Get the embeddings instance."""
        return self.embeddings
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of text documents
            
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(text)
