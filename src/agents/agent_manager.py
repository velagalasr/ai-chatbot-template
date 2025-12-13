"""
Agent Manager
Manages multiple agents and handles agent selection.
"""

from typing import Dict, Optional, Any
from ..utils import get_config, get_logger
from .base_agent import BaseAgent

logger = get_logger(__name__)


class AgentManager:
    """Manages multiple chatbot agents."""
    
    def __init__(self, rag_retriever: Optional[Any] = None):
        """
        Initialize the agent manager.
        
        Args:
            rag_retriever: Optional RAG retriever instance for agents
        """
        self.config = get_config()
        self.rag_retriever = rag_retriever
        self.agents: Dict[str, BaseAgent] = {}
        self.current_agent_name: str = "default"
        
        # Load all agents from configuration
        self._load_agents()
    
    def _load_agents(self):
        """Load all agents from configuration."""
        agents_config = self.config.get_all_agents()
        
        # Get global email configuration
        email_config = self.config.get('email', {})
        
        if not agents_config:
            logger.warning("No agents configured. Creating default agent.")
            # Create a basic default agent
            default_config = {
                "name": "Default Assistant",
                "description": "A helpful AI assistant",
                "system_prompt": "You are a helpful AI assistant.",
                "use_rag": True,
                "max_history": 10,
                "email_config": email_config
            }
            agents_config = {"default": default_config}
        
        for agent_name, agent_config in agents_config.items():
            try:
                # Determine if this agent should use RAG
                use_rag = agent_config.get('use_rag', False)
                retriever = self.rag_retriever if use_rag else None
                
                # Add email config to agent config
                if 'email_config' not in agent_config:
                    agent_config['email_config'] = email_config
                
                # Create agent instance
                agent = BaseAgent(
                    name=agent_config.get('name', agent_name),
                    config=agent_config,
                    rag_retriever=retriever
                )
                
                self.agents[agent_name] = agent
                logger.info(f"Loaded agent: {agent_name}")
            
            except Exception as e:
                logger.error(f"Failed to load agent {agent_name}: {e}")
        
        # Ensure we have at least one agent
        if not self.agents:
            raise RuntimeError("No agents could be loaded")
        
        # Set default agent if not exists
        if "default" not in self.agents and self.agents:
            self.current_agent_name = list(self.agents.keys())[0]
        
        logger.info(f"Loaded {len(self.agents)} agents")
    
    def get_agent(self, agent_name: Optional[str] = None) -> BaseAgent:
        """
        Get an agent by name.
        
        Args:
            agent_name: Name of the agent (uses current if None)
            
        Returns:
            BaseAgent instance
            
        Raises:
            ValueError: If agent not found
        """
        name = agent_name or self.current_agent_name
        
        if name not in self.agents:
            raise ValueError(f"Agent not found: {name}")
        
        return self.agents[name]
    
    def set_current_agent(self, agent_name: str):
        """
        Set the current active agent.
        
        Args:
            agent_name: Name of the agent to activate
            
        Raises:
            ValueError: If agent not found
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent not found: {agent_name}")
        
        self.current_agent_name = agent_name
        logger.info(f"Switched to agent: {agent_name}")
    
    def get_current_agent(self) -> BaseAgent:
        """Get the current active agent."""
        return self.get_agent(self.current_agent_name)
    
    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available agents with their information.
        
        Returns:
            Dictionary of agent names to agent info
        """
        return {
            name: agent.get_info()
            for name, agent in self.agents.items()
        }
    
    def chat(self, message: str, agent_name: Optional[str] = None) -> str:
        """
        Send a message to an agent and get response.
        
        Args:
            message: User message
            agent_name: Optional agent name (uses current if None)
            
        Returns:
            Agent response
        """
        agent = self.get_agent(agent_name)
        return agent.chat(message)
    
    def clear_history(self, agent_name: Optional[str] = None):
        """
        Clear conversation history for an agent.
        
        Args:
            agent_name: Optional agent name (uses current if None)
        """
        agent = self.get_agent(agent_name)
        agent.clear_history()
    
    def clear_all_histories(self):
        """Clear conversation history for all agents."""
        for agent in self.agents.values():
            agent.clear_history()
        logger.info("Cleared all agent histories")
    
    def update_agent_tools(self, use_tools: bool, enable_web_search: bool):
        """
        Update tool configuration for the current agent.
        
        Args:
            use_tools: Whether to enable tools
            enable_web_search: Whether to enable web search
        """
        current_agent = self.get_current_agent()
        current_agent.update_tools(use_tools, enable_web_search)
        logger.info(f"Updated tools for {self.current_agent_name}: use_tools={use_tools}, web_search={enable_web_search}")
    
    def update_agent_tools_individual(
        self,
        enable_calculator: bool,
        enable_rag_search: bool,
        enable_web_search: bool,
        enable_email: bool
    ):
        """
        Update individual tool configurations for the current agent.
        
        Args:
            enable_calculator: Whether to enable calculator tool
            enable_rag_search: Whether to enable RAG search tool
            enable_web_search: Whether to enable web search tool
            enable_email: Whether to enable email tool
        """
        current_agent = self.get_current_agent()
        current_agent.update_tools_individual(
            enable_calculator=enable_calculator,
            enable_rag_search=enable_rag_search,
            enable_web_search=enable_web_search,
            enable_email=enable_email
        )
        logger.info(
            f"Updated individual tools for {self.current_agent_name}: "
            f"calculator={enable_calculator}, rag={enable_rag_search}, "
            f"web={enable_web_search}, email={enable_email}"
        )
    
    def reload_agents(self):
        """Reload all agents from configuration."""
        self.agents.clear()
        self._load_agents()
