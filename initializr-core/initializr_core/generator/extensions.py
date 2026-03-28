"""
Extension generator for AgentScope Initializr.

Generates code for AgentScope extension points including
Model, Memory, Tool, Hooks, and Formatter configurations.
"""

from typing import Dict, Any
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    ModelProvider,
    MemoryType,
    FormatterType,
)


class ExtensionGenerator:
    """
    Generator for AgentScope extension points.

    This class generates configuration code for various
    AgentScope extension points.
    """

    def generate_config(self, metadata: AgentScopeMetadata) -> str:
        """
        Generate complete configuration module.

        Args:
            metadata: Project metadata

        Returns:
            Configuration module code
        """
        return f'''"""
Configuration module for {metadata.name}.

This module contains all configuration settings and initialization
functions for AgentScope components.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    # Agent Configuration
    AGENT_NAME = "{metadata.name}"
    SYSTEM_PROMPT = """You are a helpful AI assistant named {metadata.name}.
{metadata.description}
You should respond in a friendly and professional manner."""

    # Model Configuration
    MODEL_PROVIDER = "{metadata.model_provider.value}"
    ENABLE_STREAMING = {str(metadata.enable_streaming).lower()}
    ENABLE_THINKING = {str(metadata.enable_thinking).lower()}
    PARALLEL_TOOL_CALLS = {str(metadata.parallel_tool_calls).lower()}

    # Memory Configuration
    MEMORY_TYPE = "{metadata.memory_type.value}"

    # Formatter Configuration
    FORMATTER_TYPE = "{metadata.formatter.value}"


settings = Settings()


{self._generate_model_config(metadata)}

{self._generate_memory_config(metadata)}

{self._generate_toolkit_config(metadata)}

{self._generate_formatter_config(metadata)}
'''

    def _generate_model_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate model configuration code."""
        provider = metadata.model_provider

        if provider == ModelProvider.OPENAI:
            return '''
def get_model():
    """Get configured model instance."""
    from agentscope.models import OpenAIChatModel

    return OpenAIChatModel(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        stream=settings.ENABLE_STREAMING,
    )
'''
        elif provider == ModelProvider.DASHSCOPE:
            return '''
def get_model():
    """Get configured model instance."""
    from agentscope.models import DashScopeChatModel

    return DashScopeChatModel(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model_name=os.getenv("DASHSCOPE_MODEL", "qwen-max"),
        stream=settings.ENABLE_STREAMING,
    )
'''
        elif provider == ModelProvider.ANTHROPIC:
            return '''
def get_model():
    """Get configured model instance."""
    from agentscope.models import AnthropicChatModel

    return AnthropicChatModel(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model_name=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        stream=settings.ENABLE_STREAMING,
    )
'''
        elif provider == ModelProvider.GEMINI:
            return '''
def get_model():
    """Get configured model instance."""
    from agentscope.models import GeminiChatModel

    return GeminiChatModel(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name=os.getenv("GEMINI_MODEL", "gemini-pro"),
        stream=settings.ENABLE_STREAMING,
    )
'''
        elif provider == ModelProvider.OLLAMA:
            return '''
def get_model():
    """Get configured model instance."""
    from agentscope.models import OllamaChatModel

    return OllamaChatModel(
        model_name=os.getenv("OLLAMA_MODEL", "llama2"),
        stream=settings.ENABLE_STREAMING,
    )
'''
        else:
            return '''
def get_model():
    """Get configured model instance - placeholder."""
    raise NotImplementedError("Model provider not configured")
'''

    def _generate_memory_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate memory configuration code."""
        if metadata.memory_type == MemoryType.IN_MEMORY:
            return '''
def get_memory():
    """Get configured memory instance."""
    from agentscope.memory import InMemoryMemory

    return InMemoryMemory()
'''
        elif metadata.memory_type == MemoryType.LONG_TERM:
            return '''
def get_memory():
    """Get configured memory instance."""
    from agentscope.memory import Mem0LongTermMemory

    return Mem0LongTermMemory(
        api_key=os.getenv("MEMORY_API_KEY"),
    )
'''
        else:
            return '''
def get_memory():
    """Get configured memory instance - placeholder."""
    from agentscope.memory import InMemoryMemory

    return InMemoryMemory()
'''

    def _generate_toolkit_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate toolkit configuration code."""
        return '''
def get_toolkit():
    """Get configured toolkit instance."""
    from agentscope.tools import Toolkit

    toolkit = Toolkit()

    # Register basic tools
    # toolkit.register_tool_function(execute_python_code)
    # toolkit.register_tool_function(execute_shell_command)

    return toolkit
'''

    def _generate_formatter_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate formatter configuration code."""
        if metadata.formatter == FormatterType.CHAT:
            return '''
def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatters import ChatFormatter

    return ChatFormatter()
'''
        elif metadata.formatter == FormatterType.MULTI_AGENT:
            return '''
def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatters import MultiAgentFormatter

    return MultiAgentFormatter()
'''
        else:
            return '''
def get_formatter():
    """Get configured formatter instance - placeholder."""
    from agentscope.formatters import ChatFormatter

    return ChatFormatter()
'''

    def generate_hooks_code(self, metadata: AgentScopeMetadata) -> str:
        """Generate hooks implementation code."""
        if not metadata.hooks:
            return ""

        hooks_code = ["# Agent Hooks"]
        hooks_code.append("")

        for hook in metadata.hooks:
            if hook.hook_type == "pre_reply":
                hooks_code.append("""
@agent.hook("pre_reply")
async def pre_reply_hook(msg):
    '''Hook called before agent reply.'''
    import logging
    logging.info(f"Pre-reply hook: {msg}")
""")
            elif hook.hook_type == "post_reply":
                hooks_code.append("""
@agent.hook("post_reply")
async def post_reply_hook(response):
    '''Hook called after agent reply.'''
    import logging
    logging.info(f"Post-reply hook: {response}")
""")

        return "\n".join(hooks_code)

    def generate_state_management_code(self, metadata: AgentScopeMetadata) -> str:
        """Generate state management code."""
        return '''
# State Management
# AgentScope agents support automatic state persistence

# To save agent state:
# state = agent.state_dict()

# To load agent state:
# agent.load_state_dict(state)

# This is useful for:
# - Resuming long-running tasks
# - Debugging agent behavior
# - Checkpoint and recovery
'''
