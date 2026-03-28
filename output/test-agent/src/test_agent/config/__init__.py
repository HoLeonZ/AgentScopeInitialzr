"""
Configuration module for test-agent.

This module contains all configuration settings and initialization
functions for AgentScope components.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    # Agent Configuration
    AGENT_NAME = "test-agent"
    SYSTEM_PROMPT = """You are a helpful AI assistant named test-agent.
Test agent
You should respond in a friendly and professional manner."""

    # Model Configuration
    MODEL_PROVIDER = "openai"
    ENABLE_STREAMING = true
    ENABLE_THINKING = false
    PARALLEL_TOOL_CALLS = true

    # Memory Configuration
    MEMORY_TYPE = "in-memory"

    # Formatter Configuration
    FORMATTER_TYPE = "chat"


settings = Settings()



def get_model():
    """Get configured model instance."""
    from agentscope.models import OpenAIChatModel

    return OpenAIChatModel(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        stream=settings.ENABLE_STREAMING,
    )



def get_memory():
    """Get configured memory instance."""
    from agentscope.memory import InMemoryMemory

    return InMemoryMemory()



def get_toolkit():
    """Get configured toolkit instance."""
    from agentscope.tools import Toolkit

    toolkit = Toolkit()

    # Register basic tools
    # toolkit.register_tool_function(execute_python_code)
    # toolkit.register_tool_function(execute_shell_command)

    return toolkit



def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatters import ChatFormatter

    return ChatFormatter()

