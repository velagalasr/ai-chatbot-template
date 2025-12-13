"""
Base Agent Class - LangGraph + ReAct Implementation
Uses LangGraph for orchestration and ReAct framework for reasoning and acting.
"""

from typing import List, Dict, Any, Optional, TypedDict, Annotated, Sequence
from dataclasses import dataclass, field
from datetime import datetime
import operator

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage, FunctionMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

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
        
        # Create ReAct agent
        self.agent_executor = self._create_react_agent()
        
        logger.info(f"Initialized LangGraph ReAct agent: {name} with {len(self.tools)} tools")
    
    def _create_react_agent(self) -> Optional[AgentExecutor]:
        """
        Create a ReAct agent using LangChain.
        
        Returns:
            AgentExecutor instance or None if no tools
        """
        if not self.tools:
            logger.info(f"No tools available for {self.name}, using direct LLM")
            return None
        
        # Create ReAct prompt template
        react_prompt = PromptTemplate.from_template(
            """You are {agent_name}: {agent_description}

{system_prompt}

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        )
        
        # Create agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=react_prompt.partial(
                agent_name=self.name,
                agent_description=self.description,
                system_prompt=self.system_prompt
            )
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        return agent_executor
    
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
        Process a user message and return a response using ReAct framework.
        
        Args:
            message: User's message
            use_rag: Override RAG usage for this message (deprecated, use tools instead)
            
        Returns:
            Agent's response
        """
        try:
            # Build conversation context
            history_messages = self._build_messages_for_history()
            
            # If agent has tools, use ReAct agent executor
            if self.agent_executor and self.tools:
                # Add history to prompt context
                context_str = "\n".join([
                    f"{msg.type}: {msg.content}" 
                    for msg in history_messages[-6:]  # Last 3 exchanges
                ])
                
                # Run agent with tools
                result = self.agent_executor.invoke({
                    "input": message,
                    "chat_history": context_str
                })
                
                response_text = result.get("output", "I apologize, but I couldn't generate a response.")
                
                # Store intermediate steps if available
                intermediate_steps = result.get("intermediate_steps", [])
                metadata = {
                    "used_tools": len(intermediate_steps) > 0,
                    "tool_calls": len(intermediate_steps),
                    "tools_used": [step[0].tool for step in intermediate_steps] if intermediate_steps else []
                }
                
            else:
                # No tools, use direct LLM with optional RAG
                should_use_rag = use_rag if use_rag is not None else self.use_rag
                
                # Build messages with RAG context if needed
                messages = history_messages.copy()
                
                if should_use_rag and self.rag_retriever:
                    # Retrieve context
                    docs = self.rag_retriever.get_relevant_documents(message)
                    if docs:
                        context = "\n\n".join([f"[Context {i+1}]\n{doc.page_content}" for i, doc in enumerate(docs)])
                        messages.append(SystemMessage(content=f"Relevant information:\n{context}"))
                
                messages.append(HumanMessage(content=message))
                
                # Get response from LLM
                response = self.llm.invoke(messages)
                response_text = response.content
                
                metadata = {
                    "used_tools": False,
                    "used_rag": should_use_rag and self.rag_retriever is not None
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
