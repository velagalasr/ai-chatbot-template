"""
Document Loader
Handles loading and processing documents for RAG.
"""

import os
from pathlib import Path
from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from langchain_core.documents import Document

from ..utils import get_config, get_logger

logger = get_logger(__name__)


class DocumentLoader:
    """Loads and processes documents for RAG."""
    
    def __init__(self):
        """Initialize the document loader."""
        self.config = get_config()
        self.rag_config = self.config.get_rag_config()
        
        self.document_path = self.rag_config.get('document_path', './data/documents')
        self.supported_formats = self.rag_config.get('supported_formats', ['.txt', '.pdf', '.docx', '.md'])
        self.chunk_size = self.rag_config.get('chunk_size', 1000)
        self.chunk_overlap = self.rag_config.get('chunk_overlap', 200)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
    
    def load_documents(self, file_paths: Optional[List[str]] = None) -> List[Document]:
        """
        Load documents from files.
        
        Args:
            file_paths: Optional list of specific file paths to load.
                       If None, loads all supported files from document_path.
        
        Returns:
            List of Document objects
        """
        if file_paths is None:
            file_paths = self._get_all_document_files()
        
        documents = []
        
        for file_path in file_paths:
            try:
                docs = self._load_single_file(file_path)
                documents.extend(docs)
                logger.info(f"Loaded {len(docs)} documents from {file_path}")
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    def _get_all_document_files(self) -> List[str]:
        """Get all supported document files from the document path."""
        doc_path = Path(self.document_path)
        
        if not doc_path.exists():
            logger.warning(f"Document path does not exist: {doc_path}")
            doc_path.mkdir(parents=True, exist_ok=True)
            return []
        
        files = []
        for ext in self.supported_formats:
            files.extend([str(f) for f in doc_path.rglob(f"*{ext}")])
        
        logger.info(f"Found {len(files)} document files")
        return files
    
    def _load_single_file(self, file_path: str) -> List[Document]:
        """
        Load a single file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of Document objects
        """
        file_ext = Path(file_path).suffix.lower()
        
        # Select appropriate loader
        if file_ext == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif file_ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_ext == '.docx':
            loader = Docx2txtLoader(file_path)
        elif file_ext == '.md':
            loader = UnstructuredMarkdownLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        # Load documents
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata['source'] = file_path
            doc.metadata['file_type'] = file_ext
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
    
    def process_documents(self, file_paths: Optional[List[str]] = None) -> List[Document]:
        """
        Load and split documents in one step.
        
        Args:
            file_paths: Optional list of specific file paths to load
            
        Returns:
            List of processed document chunks
        """
        documents = self.load_documents(file_paths)
        
        if not documents:
            logger.warning("No documents loaded")
            return []
        
        chunks = self.split_documents(documents)
        return chunks
