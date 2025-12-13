"""
Base Agent Class - LangGraph + ReAct Implementation
Uses LangGraph for orchestration and ReAct framework for reasoning and acting.
"""

from typing import List, Dict, Any, Optional, TypedDict, Annotated, Sequence
from dataclasses import dataclass, field
from datetime import datetime
import operator

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate

from ..llm import get_llm
from ..utils import get_logger
from .tools import get_available_tools

logger = get_logger(__name__)


@dataclass
class Message:
    """Represents a chat message."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentState(TypedDict):
    """State for the agent graph."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    intermediate_steps: List[tuple]


class BaseAgent:
    """Base class for all chatbot agents using LangGraph + ReAct."""
    
    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        rag_retriever: Optional[Any] = None
    ):
        """
        Initialize the agent with LangGraph and ReAct framework.
        
        Args:
            name: Agent name
            config: Agent configuration dictionary
            rag_retriever: Optional RAG retriever instance
        """
        self.name = name
        self.config = config
        self.rag_retriever = rag_retriever
        
        # Extract configuration
        self.description = config.get('description', '')
        self.system_prompt = config.get('system_prompt', '')
        self.use_rag = config.get('use_rag', False)
        self.max_history = config.get('max_history', 10)
        self.use_tools = config.get('use_tools', True)
        
        # Initialize LLM
        self.llm = get_llm(agent_config=config)
        
        # Initialize tools
        self.tools = []
        if self.use_tools:
            # Get email config from agent config or None
            email_config = config.get('email_config')
            
            self.tools = get_available_tools(
                rag_retriever=self.rag_retriever if self.use_rag else None,
                include_web_search=config.get('enable_web_search', False),
                email_config=email_config
            )
        
        # Initialize conversation history
        self.conversation_history: List[Message] = []
        
        # Bind tools to LLM if available
        if self.tools:
            try:
                self.llm_with_tools = self.llm.bind_tools(self.tools)
                logger.info(f"Bound {len(self.tools)} tools to LLM for {name}")
            except Exception as e:
                logger.warning(f"Could not bind tools to LLM: {e}. Tools will not be available.")
                self.llm_with_tools = self.llm
        else:
            self.llm_with_tools = self.llm
        
        logger.info(f"Initialized agent: {name} with {len(self.tools)} tools")
    
    def _build_messages_for_history(self) -> List[BaseMessage]:
        """
        Build message history for context.
        
        Returns:
            List of BaseMessage objects
        """
        messages = []
        
        # Add system message
        messages.append(SystemMessage(content=self.system_prompt))
        
        # Add conversation history (limit to max_history)
        history_to_include = self.conversation_history[-(self.max_history * 2):]
        for msg in history_to_include:
            if msg.role == 'user':
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                messages.append(AIMessage(content=msg.content))
        
        return messages
    
    def chat(
        self,
        message: str,
        use_rag: Optional[bool] = None
    ) -> str:
        """
        Process a user message and return a response.
        
        Args:
            message: User's message
            use_rag: Override RAG usage for this message (deprecated, use tools instead)
            
        Returns:
            Agent's response
        """
        try:
            # Build conversation context
            history_messages = self._build_messages_for_history()
            
            # Add current user message
            history_messages.append(HumanMessage(content=message))
            
            # Use LLM (with tools if available)
            response = self.llm_with_tools.invoke(history_messages)
            
            # Handle tool calls if present
            tool_calls_made = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # LLM wants to use tools - add the AI response first
                history_messages.append(response)
                
                # Execute each tool call
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get('name', '')
                    tool_args = tool_call.get('args', {})
                    tool_call_id = tool_call.get('id', '')
                    
                    # Find and execute the tool
                    tool_result = None
                    for tool in self.tools:
                        if tool.name == tool_name:
                            try:
                                # Execute tool with arguments
                                if isinstance(tool_args, dict) and len(tool_args) == 1:
                                    # Single argument, pass directly
                                    arg_value = list(tool_args.values())[0]
                                    tool_result = tool.func(arg_value)
                                else:
                                    # Multiple or no arguments
                                    tool_result = tool.func(**tool_args) if tool_args else tool.func()
                                
                                tool_calls_made.append(f"{tool_name}: {tool_result}")
                                logger.info(f"Executed tool {tool_name} with result: {tool_result[:100] if tool_result else 'None'}")
                            except Exception as e:
                                tool_result = f"Error executing {tool_name}: {str(e)}"
                                logger.error(f"Tool execution error: {e}")
                            break
                    
                    # If tool wasn't found, provide error message
                    if tool_result is None:
                        tool_result = f"Tool {tool_name} not found"
                    
                    # Add tool result with proper tool_call_id
                    history_messages.append(
                        ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_call_id
                        )
                    )
                
                # Get final response after tool execution
                if tool_calls_made:
                    response = self.llm_with_tools.invoke(history_messages)
            
            # Extract response text
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # If response is still empty, provide default
            if not response_text or response_text.strip() == "":
                response_text = "I apologize, but I couldn't generate a response. Please try rephrasing your question."
            
            metadata = {
                "used_tools": len(tool_calls_made) > 0,
                "tools_executed": tool_calls_made
            }
            
            # Store in conversation history
            self.conversation_history.append(Message(role="user", content=message))
            self.conversation_history.append(
                Message(
                    role="assistant",
                    content=response_text,
                    metadata=metadata
                )
            )
            
            logger.info(f"Generated response for: {message[:50]}... (tools: {metadata.get('used_tools', False)})")
            return response_text
        
        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info(f"Cleared conversation history for agent: {self.name}")
    
    def update_tools(self, use_tools: bool, enable_web_search: bool):
        """
        Update agent tools dynamically.
        
        Args:
            use_tools: Whether to enable tools
            enable_web_search: Whether to enable web search
        """
        from .tools import get_available_tools
        
        self.use_tools = use_tools
        self.config['use_tools'] = use_tools
        self.config['enable_web_search'] = enable_web_search
        
        # Reload tools
        self.tools = []
        if use_tools:
            email_config = self.config.get('email_config')
            self.tools = get_available_tools(
                rag_retriever=self.rag_retriever if self.use_rag else None,
                include_web_search=enable_web_search,
                email_config=email_config
            )
        
        # Rebind tools to LLM
        if self.tools:
            try:
                self.llm_with_tools = self.llm.bind_tools(self.tools)
                logger.info(f"Rebound {len(self.tools)} tools to LLM for {self.name}")
            except Exception as e:
                logger.warning(f"Could not bind tools to LLM: {e}")
                self.llm_with_tools = self.llm
        else:
            self.llm_with_tools = self.llm
        
        logger.info(f"Updated tools for {self.name}: {len(self.tools)} tools active")
    
    def update_tools_individual(
        self,
        enable_calculator: bool,
        enable_rag_search: bool,
        enable_web_search: bool,
        enable_email: bool
    ):
        """
        Update individual tool configurations dynamically.
        
        Args:
            enable_calculator: Whether to enable calculator tool
            enable_rag_search: Whether to enable RAG search tool
            enable_web_search: Whether to enable web search tool
            enable_email: Whether to enable email tool
        """
        from .tools import get_individual_tools
        
        # Update config
        self.config['enable_calculator'] = enable_calculator
        self.config['enable_rag_search'] = enable_rag_search
        self.config['enable_web_search'] = enable_web_search
        self.config['enable_email'] = enable_email
        
        # Determine if any tools are enabled
        any_tools_enabled = enable_calculator or enable_rag_search or enable_web_search or enable_email
        self.use_tools = any_tools_enabled
        self.config['use_tools'] = any_tools_enabled
        
        # Reload tools with individual selections
        self.tools = []
        if any_tools_enabled:
            email_config = self.config.get('email_config')
            self.tools = get_individual_tools(
                rag_retriever=self.rag_retriever if self.use_rag else None,
                enable_calculator=enable_calculator,
                enable_rag_search=enable_rag_search,
                enable_web_search=enable_web_search,
                enable_email=enable_email,
                email_config=email_config
            )
        
        # Rebind tools to LLM
        if self.tools:
            try:
                self.llm_with_tools = self.llm.bind_tools(self.tools)
                logger.info(f"Rebound {len(self.tools)} tools to LLM for {self.name}")
            except Exception as e:
                logger.warning(f"Could not bind tools to LLM: {e}")
                self.llm_with_tools = self.llm
        else:
            self.llm_with_tools = self.llm
        
        logger.info(
            f"Updated individual tools for {self.name}: {len(self.tools)} tools active "
            f"(calc={enable_calculator}, rag={enable_rag_search}, web={enable_web_search}, email={enable_email})"
        )
    
    def get_history(self) -> List[Message]:
        """Get conversation history."""
        return self.conversation_history.copy()
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": self.name,
            "description": self.description,
            "framework": "LangGraph + ReAct",
            "use_tools": len(self.tools) > 0,
            "tools": [tool.name for tool in self.tools],
            "use_rag": self.use_rag,
            "max_history": self.max_history,
            "message_count": len(self.conversation_history)
        }
