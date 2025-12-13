"""
Script to initialize vector database with documents.
Run this before starting the chatbot for the first time.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag import RAGManager
from src.utils import setup_logger

logger = setup_logger(name="init_vectordb", level="INFO")


def main():
    """Initialize vector database with documents."""
    logger.info("Starting vector database initialization...")
    
    try:
        # Initialize RAG manager
        rag_manager = RAGManager()
        
        if not rag_manager.enabled:
            logger.warning("RAG is disabled in configuration. Enable it to use vector database.")
            return
        
        # Check current stats
        stats = rag_manager.get_stats()
        logger.info(f"Current stats: {stats}")
        
        # Load and index documents
        logger.info("Loading and indexing documents...")
        count = rag_manager.initialize_documents()
        
        if count > 0:
            logger.info(f"Successfully indexed {count} document chunks")
            
            # Get updated stats
            stats = rag_manager.get_stats()
            logger.info(f"Updated stats: {stats}")
            
            logger.info("✅ Vector database initialization complete!")
        else:
            logger.warning("No documents found to index. Add documents to the configured document path.")
            logger.info("You can still run the chatbot without RAG.")
    
    except Exception as e:
        logger.error(f"Error initializing vector database: {e}")
        logger.error("Please check your configuration and ensure all required API keys are set.")
        sys.exit(1)


if __name__ == "__main__":
    main()
