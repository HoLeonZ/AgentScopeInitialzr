"""
Extension generator for AgentScope Initializr.

Generates code for AgentScope extension points including
Model, Memory, Tool, Hooks, Formatter, Skills, RAG, and Pipeline configurations.
"""

from typing import Dict, Any, List
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
    SHORT_TERM_MEMORY = {f'"{metadata.short_term_memory}"' if metadata.short_term_memory else 'None'}
    LONG_TERM_MEMORY = {f'"{metadata.long_term_memory}"' if metadata.long_term_memory else 'None'}

    # Formatter Configuration
    FORMATTER_TYPE = "{metadata.formatter.value}"
    FORMATTER_NAME = {f'"{metadata.formatter_name}"' if metadata.formatter_name else 'None'}

    # Skills Configuration
    ENABLE_SKILLS = {str(metadata.enable_skills).lower()}
    SKILLS = {metadata.skills}

    # RAG Configuration
    ENABLE_RAG = {str(metadata.enable_rag).lower()}

    # Pipeline Configuration
    ENABLE_PIPELINE = {str(metadata.enable_pipeline).lower()}


settings = Settings()


{self._generate_model_config(metadata)}

{self._generate_memory_config(metadata)}

{self._generate_toolkit_config(metadata)}

{self._generate_formatter_config(metadata)}

{self._generate_skills_config(metadata)}

{self._generate_rag_config(metadata)}

{self._generate_pipeline_config(metadata)}
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
        """Generate memory configuration code with enhanced options."""
        lines = []

        # Short-term memory
        if metadata.short_term_memory:
            lines.append(f"""
# Short-term memory configuration
SHORT_TERM_MEMORY_TYPE = "{metadata.short_term_memory}"
""")

            if metadata.short_term_memory == "in-memory":
                lines.append('''
def get_short_term_memory():
    """Get short-term memory instance."""
    from agentscope.memory import InMemoryMemory
    return InMemoryMemory()
''')
            elif metadata.short_term_memory == "redis":
                lines.append('''
def get_short_term_memory():
    """Get short-term memory instance with Redis."""
    from agentscope.memory import RedisMemory
    return RedisMemory(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
    )
''')
            elif metadata.short_term_memory == "oceanbase":
                lines.append('''
def get_short_term_memory():
    """Get short-term memory instance with OceanBase."""
    from agentscope.memory import OceanBaseMemory
    return OceanBaseMemory(
        connection_string=os.getenv("OCEANBASE_CONNECTION_STRING"),
    )
''')

        # Long-term memory
        if metadata.long_term_memory and metadata.long_term_memory != "none":
            lines.append(f"""
# Long-term memory configuration
LONG_TERM_MEMORY_TYPE = "{metadata.long_term_memory}"
""")

            if metadata.long_term_memory == "mem0":
                lines.append('''
def get_long_term_memory():
    """Get long-term memory instance with Mem0."""
    from agentscope.memory import Mem0LongTermMemory
    return Mem0LongTermMemory(
        api_key=os.getenv("MEMORY_API_KEY"),
    )
''')
            elif metadata.long_term_memory == "zep":
                lines.append('''
def get_long_term_memory():
    """Get long-term memory instance with Zep."""
    from agentscope.memory import ZepLongTermMemory
    return ZepLongTermMemory(
        api_key=os.getenv("ZEP_API_KEY"),
        endpoint=os.getenv("ZEP_ENDPOINT"),
    )
''')
            elif metadata.long_term_memory == "oceanbase":
                lines.append('''
def get_long_term_memory():
    """Get long-term memory instance with OceanBase."""
    from agentscope.memory import OceanBaseLongTermMemory
    return OceanBaseLongTermMemory(
        connection_string=os.getenv("OCEANBASE_CONNECTION_STRING"),
    )
''')

        # Main get_memory function
        if metadata.long_term_memory and metadata.long_term_memory != "none":
            lines.append('''
def get_memory():
    """Get configured memory instance with both short and long-term memory."""
    from agentscope.memory import CombinedMemory

    short_term = get_short_term_memory()
    long_term = get_long_term_memory()

    return CombinedMemory(
        short_term=short_term,
        long_term=long_term,
    )
''')
        else:
            lines.append('''
def get_memory():
    """Get configured memory instance."""
    from agentscope.memory import InMemoryMemory
    return InMemoryMemory()
''')

        return "\n".join(lines)

    def _generate_toolkit_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate toolkit configuration code with enabled tools."""
        lines = []
        lines.append('''
def get_toolkit():
    """Get configured toolkit instance."""
    from agentscope.tools import Toolkit

    toolkit = Toolkit()
''')

        # Add enabled tools (metadata.tools is a list of ToolConfig objects)
        tool_mappings = {
            "execute_python_code": "execute_python_code",
            "execute_shell_command": "execute_shell_command",
            "web_search": "web_search_tavily",
            "browser_navigate": "browser_navigate",
            "browser_click": "browser_click",
            "browser_type": "browser_type",
            "browser_screenshot": "browser_screenshot",
        }

        for tool_config in metadata.tools:
            tool_name = tool_config.name  # Get tool name from ToolConfig
            if tool_name in tool_mappings:
                func_name = tool_mappings[tool_name]
                lines.append(f'    # toolkit.register({func_name})')

        lines.append('''
    return toolkit
''')

        return "\n".join(lines)

    def _generate_formatter_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate formatter configuration code."""
        if metadata.formatter_name:
            # Use specific formatter by name
            return f'''
def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatters import {metadata.formatter_name}

    return {metadata.formatter_name}()
'''
        elif metadata.formatter == FormatterType.CHAT:
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

    def _generate_skills_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate skills configuration code."""
        if not metadata.enable_skills or not metadata.skills:
            return '''
# Skills not enabled
def get_skills():
    """Get skills list - placeholder."""
    return []
'''

        lines = ['''
def get_skills():
    """Get configured skills list."""
    skills = []
''']

        for skill in metadata.skills:
            lines.append(f'    # skills.append({skill})')
            lines.append(f'    # TODO: Implement {skill} skill')

        lines.append('''
    return skills
''')

        return "\n".join(lines)

    def _generate_rag_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate RAG configuration code."""
        if not metadata.enable_rag:
            return '''
# RAG not enabled
'''

        config = metadata.rag_config or {}
        store_type = config.get("store_type", "chroma")
        embedding_model = config.get("embedding_model", "openai:text-embedding-ada-002")
        chunk_size = config.get("chunk_size", 500)
        chunk_overlap = config.get("chunk_overlap", 50)

        return f'''
# RAG Configuration
RAG_STORE_TYPE = "{store_type}"
RAG_EMBEDDING_MODEL = "{embedding_model}"
RAG_CHUNK_SIZE = {chunk_size}
RAG_CHUNK_OVERLAP = {chunk_overlap}

def get_rag_retriever():
    """Get configured RAG retriever instance."""
    from agentscope.rag import RAGRetriever

    return RAGRetriever(
        store_type="{store_type}",
        embedding_model="{embedding_model}",
        chunk_size={chunk_size},
        chunk_overlap={chunk_overlap},
    )
'''

    def _generate_pipeline_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate pipeline configuration code."""
        if not metadata.enable_pipeline:
            return '''
# Pipeline not enabled
'''

        config = metadata.pipeline_config or {}
        pipeline_type = config.get("type", "sequential")
        num_stages = config.get("num_stages", 3)
        error_handling = config.get("error_handling", "stop")

        return f'''
# Pipeline Configuration
PIPELINE_TYPE = "{pipeline_type}"
PIPELINE_NUM_STAGES = {num_stages}
PIPELINE_ERROR_HANDLING = "{error_handling}"

def get_pipeline():
    """Get configured pipeline instance."""
    from agentscope.pipeline import Pipeline

    pipeline = Pipeline(
        type="{pipeline_type}",
        num_stages={num_stages},
        error_handling="{error_handling}",
    )

    return pipeline
'''

    def generate_hooks_code(self, metadata: AgentScopeMetadata) -> str:
        """Generate hooks implementation code."""
        if not metadata.hooks:
            return ""

        hooks_code = ['''
# Agent Hooks
# These hooks are called at specific points in the agent lifecycle
''']

        for hook in metadata.hooks:
            if hook.hook_type == "pre_reply":
                hooks_code.append('''
@agent.hook("pre_reply")
async def pre_reply_hook(msg):
    """Hook called before agent reply."""
    import logging
    logging.info(f"Pre-reply hook called: {msg}")
    # Modify msg here if needed
    return msg
''')
            elif hook.hook_type == "post_reply":
                hooks_code.append('''
@agent.hook("post_reply")
async def post_reply_hook(response):
    """Hook called after agent reply."""
    import logging
    logging.info(f"Post-reply hook called: {response}")
    # Modify response here if needed
    return response
''')
            elif hook.hook_type == "pre_observe":
                hooks_code.append('''
@agent.hook("pre_observe")
async def pre_observe_hook(observation):
    """Hook called before agent observation."""
    import logging
    logging.info(f"Pre-observe hook called: {observation}")
    # Modify observation here if needed
    return observation
''')
            elif hook.hook_type == "post_observe":
                hooks_code.append('''
@agent.hook("post_observe")
async def post_observe_hook(observation):
    """Hook called after agent observation."""
    import logging
    logging.info(f"Post-observe hook called: {observation}")
    # Process observation here if needed
    return observation
''')

        return "\n".join(hooks_code)

    def generate_tests_code(self, metadata: AgentScopeMetadata) -> str:
        """Generate test module code."""
        if not metadata.generate_tests:
            return ""

        return f'''"""
Test module for {metadata.name}.

This module contains unit and integration tests.
"""

import pytest
from {metadata.package_name}.config import get_model, get_memory, get_toolkit


class TestModel:
    """Test model configuration."""

    def test_get_model(self):
        """Test model initialization."""
        model = get_model()
        assert model is not None

    def test_model_streaming(self):
        """Test model streaming capability."""
        model = get_model()
        # Add streaming test here
        pass


class TestMemory:
    """Test memory configuration."""

    def test_get_memory(self):
        """Test memory initialization."""
        memory = get_memory()
        assert memory is not None

    def test_memory_storage(self):
        """Test memory storage and retrieval."""
        memory = get_memory()
        # Add memory test here
        pass


class TestToolkit:
    """Test toolkit configuration."""

    def test_get_toolkit(self):
        """Test toolkit initialization."""
        toolkit = get_toolkit()
        assert toolkit is not None


class TestAgent:
    """Test agent functionality."""

    @pytest.mark.asyncio
    async def test_agent_response(self):
        """Test agent basic response."""
        # Add agent test here
        pass
'''

    def generate_evaluation_code(self, metadata: AgentScopeMetadata) -> str:
        """Generate evaluation module code."""
        if not metadata.generate_evaluation:
            return ""

        evaluator_type = metadata.evaluator_type or "general"

        code = f'''"""
Evaluation module for {metadata.name}.

This module contains evaluation functions and benchmarks.
"""

import pytest
from {metadata.package_name}.agents import create_react_agent


class TestEvaluation:
    """Test evaluation framework."""

    @pytest.mark.asyncio
    async def test_basic_evaluation(self):
        """Test basic evaluation."""
        agent = create_react_agent()
        # Add evaluation test here
        pass
'''

        if metadata.enable_openjudge and metadata.openjudge_graders:
            code += f'''

# OpenJudge Integration
OPENJUDGE_GRADERS = {metadata.openjudge_graders}

class TestOpenJudge:
    """Test OpenJudge integration."""

    @pytest.mark.asyncio
    async def test_relevance_grader(self):
        """Test RelevanceGrader."""
        # Add grader test here
        pass

    @pytest.mark.asyncio
    async def test_correctness_grader(self):
        """Test CorrectnessGrader."""
        # Add grader test here
        pass
'''

        if metadata.initial_benchmark_tasks > 0:
            code += f'''

# Benchmark Tasks
BENCHMARK_TASKS_COUNT = {metadata.initial_benchmark_tasks}

class TestBenchmarks:
    """Test benchmark tasks."""

    @pytest.mark.asyncio
    async def test_benchmark_suite(self):
        """Test benchmark suite."""
        # Add benchmark tests here
        pass
'''

        return code

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
