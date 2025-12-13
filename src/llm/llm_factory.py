"""
LLM Provider Factory
Creates LLM instances based on configuration.
"""

from typing import Any, Dict, Optional
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_community.chat_models import ChatAnthropic, ChatCohere
from langchain_community.llms import HuggingFaceHub

from ..utils import get_config, get_logger

logger = get_logger(__name__)


class LLMFactory:
    """Factory class for creating LLM instances."""
    
    @staticmethod
    def create_llm(
        agent_config: Optional[Dict[str, Any]] = None,
        override_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Create an LLM instance based on configuration.
        
        Args:
            agent_config: Agent-specific configuration (may contain llm_override)
            override_params: Additional parameters to override
            
        Returns:
            LLM instance
        """
        config = get_config()
        llm_config = config.get_llm_config().copy()
        
        # Apply agent-specific overrides
        if agent_config and agent_config.get('llm_override'):
            llm_config.update(agent_config['llm_override'])
        
        # Apply additional overrides
        if override_params:
            llm_config.update(override_params)
        
        provider = llm_config.get('provider', 'openai')
        
        logger.info(f"Creating LLM instance for provider: {provider}")
        
        if provider == 'openai':
            return LLMFactory._create_openai(llm_config, config)
        elif provider == 'azure_openai':
            return LLMFactory._create_azure_openai(llm_config, config)
        elif provider == 'anthropic':
            return LLMFactory._create_anthropic(llm_config, config)
        elif provider == 'cohere':
            return LLMFactory._create_cohere(llm_config, config)
        elif provider == 'huggingface':
            return LLMFactory._create_huggingface(llm_config, config)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    @staticmethod
    def _create_openai(llm_config: Dict[str, Any], config: Any) -> ChatOpenAI:
        """Create OpenAI LLM instance."""
        api_key = config.get_api_key(llm_config.get('api_key_env', 'OPENAI_API_KEY'))
        
        return ChatOpenAI(
            model=llm_config.get('model', 'gpt-4'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 2000),
            top_p=llm_config.get('top_p', 1.0),
            frequency_penalty=llm_config.get('frequency_penalty', 0.0),
            presence_penalty=llm_config.get('presence_penalty', 0.0),
            openai_api_key=api_key
        )
    
    @staticmethod
    def _create_azure_openai(llm_config: Dict[str, Any], config: Any) -> AzureChatOpenAI:
        """Create Azure OpenAI LLM instance."""
        api_key = config.get_api_key(llm_config.get('api_key_env', 'AZURE_OPENAI_API_KEY'))
        azure_config = llm_config.get('azure', {})
        
        return AzureChatOpenAI(
            deployment_name=azure_config.get('deployment_name'),
            azure_endpoint=azure_config.get('endpoint'),
            api_version=azure_config.get('api_version', '2024-02-15-preview'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 2000),
            openai_api_key=api_key
        )
    
    @staticmethod
    def _create_anthropic(llm_config: Dict[str, Any], config: Any) -> ChatAnthropic:
        """Create Anthropic (Claude) LLM instance."""
        api_key = config.get_api_key(llm_config.get('api_key_env', 'ANTHROPIC_API_KEY'))
        
        return ChatAnthropic(
            model=llm_config.get('model', 'claude-3-sonnet-20240229'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 2000),
            anthropic_api_key=api_key
        )
    
    @staticmethod
    def _create_cohere(llm_config: Dict[str, Any], config: Any) -> ChatCohere:
        """Create Cohere LLM instance."""
        api_key = config.get_api_key(llm_config.get('api_key_env', 'COHERE_API_KEY'))
        
        return ChatCohere(
            model=llm_config.get('model', 'command'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 2000),
            cohere_api_key=api_key
        )
    
    @staticmethod
    def _create_huggingface(llm_config: Dict[str, Any], config: Any) -> HuggingFaceHub:
        """Create HuggingFace LLM instance."""
        api_key = config.get_api_key(llm_config.get('api_key_env', 'HUGGINGFACE_API_KEY'))
        hf_config = llm_config.get('huggingface', {})
        
        return HuggingFaceHub(
            repo_id=hf_config.get('model_id', 'meta-llama/Llama-2-7b-chat-hf'),
            model_kwargs={
                'temperature': llm_config.get('temperature', 0.7),
                'max_new_tokens': llm_config.get('max_tokens', 2000),
            },
            huggingfacehub_api_token=api_key
        )


def get_llm(
    agent_config: Optional[Dict[str, Any]] = None,
    override_params: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Convenience function to create an LLM instance.
    
    Args:
        agent_config: Agent-specific configuration
        override_params: Additional parameters to override
        
    Returns:
        LLM instance
    """
    return LLMFactory.create_llm(agent_config, override_params)
