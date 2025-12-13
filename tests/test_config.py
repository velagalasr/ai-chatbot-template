"""
Unit tests for configuration loader.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import ConfigLoader


def test_config_loader_initialization():
    """Test that config loader initializes correctly."""
    config = ConfigLoader()
    assert config is not None
    assert config.config is not None


def test_get_llm_config():
    """Test getting LLM configuration."""
    config = ConfigLoader()
    llm_config = config.get_llm_config()
    assert llm_config is not None
    assert 'provider' in llm_config


def test_get_agent_config():
    """Test getting agent configuration."""
    config = ConfigLoader()
    agent_config = config.get_agent_config('default')
    assert agent_config is not None


def test_get_rag_config():
    """Test getting RAG configuration."""
    config = ConfigLoader()
    rag_config = config.get_rag_config()
    assert rag_config is not None
    assert 'vector_db' in rag_config


def test_dot_notation_access():
    """Test accessing config with dot notation."""
    config = ConfigLoader()
    provider = config.get('llm.provider')
    assert provider is not None


if __name__ == "__main__":
    pytest.main([__file__])
