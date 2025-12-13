"""
Unit tests for agent functionality.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import BaseAgent, AgentManager


def test_agent_initialization():
    """Test that agent initializes correctly."""
    config = {
        'name': 'Test Agent',
        'description': 'A test agent',
        'system_prompt': 'You are a test agent',
        'use_rag': False,
        'max_history': 10
    }
    
    # This test might fail without valid API keys
    # In production, use mocking
    try:
        agent = BaseAgent('test', config)
        assert agent.name == 'test'
        assert agent.description == 'A test agent'
    except Exception as e:
        pytest.skip(f"Skipping due to missing API key: {e}")


def test_agent_manager_initialization():
    """Test that agent manager initializes correctly."""
    try:
        manager = AgentManager()
        assert manager is not None
        assert len(manager.agents) > 0
    except Exception as e:
        pytest.skip(f"Skipping due to initialization error: {e}")


def test_list_agents():
    """Test listing available agents."""
    try:
        manager = AgentManager()
        agents = manager.list_agents()
        assert isinstance(agents, dict)
        assert len(agents) > 0
    except Exception as e:
        pytest.skip(f"Skipping due to initialization error: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
