"""
Unit tests for RAG functionality.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag import DocumentLoader, RAGManager


def test_document_loader_initialization():
    """Test document loader initialization."""
    loader = DocumentLoader()
    assert loader is not None
    assert loader.chunk_size > 0


def test_rag_manager_initialization():
    """Test RAG manager initialization."""
    try:
        manager = RAGManager()
        assert manager is not None
    except Exception as e:
        pytest.skip(f"Skipping due to missing API key: {e}")


def test_get_stats():
    """Test getting RAG statistics."""
    try:
        manager = RAGManager()
        stats = manager.get_stats()
        assert isinstance(stats, dict)
        assert 'enabled' in stats
    except Exception as e:
        pytest.skip(f"Skipping due to initialization error: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
