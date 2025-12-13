"""
Pytest configuration and fixtures
"""

import pytest
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-123456789")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-key")
    monkeypatch.setenv("COHERE_API_KEY", "test-cohere-key")


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "llm": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000
        },
        "agents": {
            "test_agent": {
                "name": "Test Agent",
                "description": "Test agent for unit tests",
                "system_prompt": "You are a test agent.",
                "use_rag": False,
                "use_tools": False,
                "max_history": 10
            }
        },
        "rag": {
            "enabled": False,
            "vector_db": "chromadb",
            "chunk_size": 500,
            "chunk_overlap": 50
        }
    }


@pytest.fixture
def sample_documents():
    """Sample documents for RAG testing."""
    return [
        {"content": "Artificial intelligence is the simulation of human intelligence by machines.", 
         "metadata": {"source": "test1.txt"}},
        {"content": "Machine learning is a subset of AI that learns from data.",
         "metadata": {"source": "test2.txt"}},
        {"content": "Neural networks are inspired by biological neurons.",
         "metadata": {"source": "test3.txt"}}
    ]


@pytest.fixture
def mock_llm_response(monkeypatch):
    """Mock LLM API responses."""
    class MockResponse:
        def __init__(self, content):
            self.content = content
    
    def mock_invoke(*args, **kwargs):
        return MockResponse("This is a test response from the mock LLM.")
    
    return mock_invoke


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Create sample config.yaml
    config_file = config_dir / "config.yaml"
    config_file.write_text("""
llm:
  provider: "openai"
  model: "gpt-3.5-turbo"
  temperature: 0.7

agents:
  default:
    name: "Test Agent"
    system_prompt: "You are helpful."
    use_rag: false
    use_tools: false

rag:
  enabled: false
""")
    
    return config_dir


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create subdirectories
    (data_dir / "documents").mkdir()
    (data_dir / "chromadb").mkdir()
    (data_dir / "evaluation").mkdir()
    
    return data_dir


# Skip markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires API keys)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: mark test as requiring API keys"
    )


# Auto-skip tests requiring API keys if not set
def pytest_collection_modifyitems(config, items):
    """Automatically skip tests requiring API keys if not available."""
    skip_api = pytest.mark.skip(reason="API key not set")
    
    for item in items:
        if "requires_api_key" in item.keywords:
            if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-test"):
                item.add_marker(skip_api)
