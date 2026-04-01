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

    def generate_config_init(self, metadata: AgentScopeMetadata) -> str:
        """
        Generate config/__init__.py with Settings class and imports.

        Args:
            metadata: Project metadata

        Returns:
            Configuration __init__ module code
        """
        # Build import statements based on enabled features
        imports = [
            "from .settings import settings",
            "from .model import get_model",
            "from .memory import get_memory",
            "from .toolkit import get_toolkit",
        ]

        # Build __all__ list
        all_exports = [
            '"settings"',
            '"get_model"',
            '"get_memory"',
            '"get_toolkit"',
        ]

        if metadata.enable_rag:
            imports.append("from .rag import get_rag_retriever")
            all_exports.append('"get_rag_retriever"')

        if metadata.enable_pipeline:
            imports.append("from .pipeline import get_pipeline")
            all_exports.append('"get_pipeline"')

        imports_str = "\n".join(imports)
        all_exports_str = ",\n    ".join(all_exports)

        return f'''"""
Configuration module for {metadata.name}.

This module contains all configuration settings and initialization
functions for AgentScope components.
"""

{imports_str}


__all__ = [
    {all_exports_str},
]
'''

    def generate_settings_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate settings.py file with Settings class."""
        return f'''"""
Application settings for {metadata.name}.

This module loads all configuration from environment variables.
Settings are accessed via the `settings` object.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Agent Configuration (from .env)
    AGENT_NAME = os.getenv("AGENT_NAME", "{metadata.name}")
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", """You are a helpful AI assistant named {metadata.name}.
{metadata.description}
You should respond in a friendly and professional.""")

    # Model Configuration (from .env)
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "{metadata.model_provider.value}")
    ENABLE_STREAMING = os.getenv("ENABLE_STREAMING", "true").lower() == "true"
    ENABLE_THINKING = os.getenv("ENABLE_THINKING", "false").lower() == "true"
    PARALLEL_TOOL_CALLS = os.getenv("PARALLEL_TOOL_CALLS", "true").lower() == "true"

    # Memory Configuration (from .env)
    MEMORY_TYPE = os.getenv("MEMORY_TYPE", "{metadata.memory_type.value}")
    LONG_TERM_MEMORY = os.getenv("LONG_TERM_MEMORY", {f'"{metadata.long_term_memory}"' if metadata.long_term_memory else 'None'})

    # RAG Configuration (from .env)
    ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"

    # Pipeline Configuration (from .env)
    ENABLE_PIPELINE = os.getenv("ENABLE_PIPELINE", "false").lower() == "true"

    # Logging Configuration (from .env)
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
    LOG_FILE_MAX_BYTES = int(os.getenv("LOG_FILE_MAX_BYTES", "10485760"))  # 10 MB
    LOG_FILE_BACKUP_COUNT = int(os.getenv("LOG_FILE_BACKUP_COUNT", "5"))  # 5 backups
    LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "30"))  # 30 days


# Create global settings instance
settings = Settings()
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

        # Determine memory configuration based on memory_type
        if metadata.memory_type == MemoryType.LONG_TERM and metadata.long_term_memory:
            # Long-term memory configuration
            lines.append(f"""
# Long-term memory configuration
LONG_TERM_MEMORY_TYPE = "{metadata.long_term_memory}"
""")

            if metadata.long_term_memory == "mem0":
                lines.append(f'''
def get_long_term_memory():
    """Get long-term memory instance with Mem0."""
    from agentscope.memory import Mem0Memory

    return Mem0Memory(
        api_key=os.getenv("MEM0_API_KEY"),
    )
''')
            elif metadata.long_term_memory == "zep":
                lines.append(f'''
def get_long_term_memory():
    """Get long-term memory instance with Zep."""
    from agentscope.memory import ZepMemory

    return ZepMemory(
        api_key=os.getenv("ZEP_API_KEY"),
        endpoint=os.getenv("ZEP_ENDPOINT"),
        session_id=os.getenv("ZEP_SESSION_ID", "default"),
    )
''')
            elif metadata.long_term_memory == "oceanbase":
                lines.append(f'''
def get_long_term_memory():
    """Get long-term memory instance with OceanBase."""
    from agentscope.memory import OceanBaseMemory

    return OceanBaseMemory(
        connection_string=os.getenv("OCEANBASE_CONNECTION_STRING"),
        table_name=os.getenv("OCEANBASE_TABLE_NAME", "agent_memory"),
    )
''')
            elif metadata.long_term_memory == "redis":
                lines.append(f'''
def get_long_term_memory():
    """Get long-term memory instance with Redis."""
    from agentscope.memory import RedisMemory

    return RedisMemory(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
        password=os.getenv("REDIS_PASSWORD", None),
    )
''')
            else:
                # Default fallback
                lines.append('''
def get_long_term_memory():
    """Get long-term memory instance - placeholder."""
    raise NotImplementedError("Long-term memory not configured")
''')

            # Main get_memory function for long-term
            lines.append('''
def get_memory():
    """Get configured memory instance with long-term storage."""
    return get_long_term_memory()
''')

        else:
            # In-memory configuration (default)
            lines.append('''
# In-memory configuration
MEMORY_TYPE = "in-memory"

def get_memory():
    """Get configured in-memory instance."""
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
            "execute_python_code": ("execute_python_code", "from agentscope.tools import execute_python_code"),
            "execute_shell_command": ("execute_shell_command", "from agentscope.tools import execute_shell_command"),
            "web_search": ("web_search_tavily", "from agentscope.tools import web_search_tavily"),
            "browser_navigate": ("browser_navigate", "from agentscope.tools import browser_navigate"),
            "browser_click": ("browser_click", "from agentscope.tools import browser_click"),
            "browser_type": ("browser_type", "from agentscope.tools import browser_type"),
            "browser_screenshot": ("browser_screenshot", "from agentscope.tools import browser_screenshot"),
        }

        # Import statements for tools
        imports_added = set()
        for tool_config in metadata.tools:
            tool_name = tool_config.name
            if tool_name in tool_mappings:
                func_name, import_stmt = tool_mappings[tool_name]
                if import_stmt not in imports_added:
                    lines.append(f'    {import_stmt}')
                    imports_added.add(import_stmt)

        # Register tools
        if metadata.tools:
            lines.append('')
            for tool_config in metadata.tools:
                tool_name = tool_config.name
                if tool_name in tool_mappings:
                    func_name, _ = tool_mappings[tool_name]
                    lines.append(f'    toolkit.register({func_name})')
                    lines.append(f'    # {tool_name} enabled')

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
        """Generate RAG configuration code with client instantiation."""
        if not metadata.enable_rag:
            return '''
# RAG not enabled
'''

        config = metadata.rag_config or {}
        store_type = config.get("store_type", "qdrant")
        embedding_model = config.get("embedding_model", "openai")
        chunk_size = config.get("chunk_size", 500)
        chunk_overlap = config.get("chunk_overlap", 50)

        lines = [
            f'''# RAG Configuration
RAG_STORE_TYPE = "{store_type}"
RAG_EMBEDDING_MODEL = "{embedding_model}"
RAG_CHUNK_SIZE = {chunk_size}
RAG_CHUNK_OVERLAP = {chunk_overlap}
'''
        ]

        # Generate client instantiation code based on store type
        if store_type == "qdrant":
            lines.append(f'''
def get_vector_store():
    """Get configured Qdrant vector store instance."""
    from agentscope.rag import QdrantVectorStore
    from qdrant_client import QdrantClient

    client = QdrantClient(
        url=os.getenv("QDRANT_URL", f"http://{{os.getenv('QDRANT_HOST', 'localhost')}}:{{os.getenv('QDRANT_PORT', '6333')}}"),
    )

    return QdrantVectorStore(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION", "agent_documents"),
        embedding_model="{embedding_model}",
    )
''')
        elif store_type == "kbase":
            lines.append(f'''
def get_vector_store():
    """Get configured KBase vector store instance."""
    from agentscope.rag import KBaseVectorStore

    return KBaseVectorStore(
        retrieval_url=os.getenv("KBASE_RETRIEVAL_URL"),
        embedding_model="{embedding_model}",
    )
''')
        else:
            # Default fallback
            lines.append(f'''
def get_vector_store():
    """Get vector store - placeholder for {store_type}."""
    raise NotImplementedError("Vector store type not implemented: {store_type}")
''')

        # Add RAG retriever function
        lines.append(f'''
def get_rag_retriever():
    """Get configured RAG retriever instance."""
    from agentscope.rag import RAGRetriever

    vector_store = get_vector_store()

    return RAGRetriever(
        vector_store=vector_store,
        chunk_size={chunk_size},
        chunk_overlap={chunk_overlap},
    )
''')

        return "\n".join(lines)

    def _generate_pipeline_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate pipeline configuration code with client instantiation."""
        if not metadata.enable_pipeline:
            return '''
# Pipeline not enabled
'''

        config = metadata.pipeline_config or {}
        pipeline_type = config.get("type", "sequential")
        num_stages = config.get("num_stages", 3)
        error_handling = config.get("error_handling", "stop")

        lines = [
            f'''# Pipeline Configuration
PIPELINE_TYPE = "{pipeline_type}"
PIPELINE_NUM_STAGES = {num_stages}
PIPELINE_ERROR_HANDLING = "{error_handling}"
'''
        ]

        # Generate pipeline instantiation based on type
        if pipeline_type == "sequential":
            lines.append(f'''
def get_pipeline():
    """Get configured sequential pipeline instance."""
    from agentscope.pipeline import SequentialPipeline

    return SequentialPipeline(
        num_stages={num_stages},
        error_handling="{error_handling}",
    )
''')
        elif pipeline_type == "parallel":
            lines.append(f'''
def get_pipeline():
    """Get configured parallel pipeline instance."""
    from agentscope.pipeline import ParallelPipeline

    return ParallelPipeline(
        num_stages={num_stages},
        error_handling="{error_handling}",
        max_concurrency=int(os.getenv("PIPELINE_MAX_CONCURRENCY", "3")),
    )
''')
        elif pipeline_type == "conditional":
            lines.append(f'''
def get_pipeline():
    """Get configured conditional pipeline instance."""
    from agentscope.pipeline import ConditionalPipeline

    return ConditionalPipeline(
        num_stages={num_stages},
        error_handling="{error_handling}",
    )
''')
        else:
            # Default fallback
            lines.append(f'''
def get_pipeline():
    """Get pipeline - placeholder for {pipeline_type}."""
    raise NotImplementedError("Pipeline type not implemented: {pipeline_type}")
''')

        return "\n".join(lines)

    def generate_model_config_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate model.py configuration file."""
        config = self._generate_model_config(metadata)

        return f'''"""
Model configuration for {metadata.name}.

This module contains the model client initialization.
"""

import os
from .settings import settings

{config}
'''

    def generate_memory_config_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate memory.py configuration file."""
        config = self._generate_memory_config(metadata)

        return f'''"""
Memory configuration for {metadata.name}.

This module contains the memory client initialization.
"""

import os
from .settings import settings

{config}
'''

    def generate_rag_config_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate rag.py configuration file."""
        config = self._generate_rag_config(metadata)

        return f'''"""
RAG configuration for {metadata.name}.

This module contains the RAG and vector store client initialization.
"""

import os
from .settings import settings

{config}
'''

    def generate_pipeline_config_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate pipeline.py configuration file."""
        config = self._generate_pipeline_config(metadata)

        return f'''"""
Pipeline configuration for {metadata.name}.

This module contains the pipeline client initialization.
"""

import os
from .settings import settings

{config}
'''

    def generate_toolkit_config_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate toolkit.py configuration file."""
        config = self._generate_toolkit_config(metadata)

        return f'''"""
Toolkit configuration for {metadata.name}.

This module contains the toolkit initialization.
"""

import os
from .settings import settings

{config}
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


    def generate_skills_files(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate skill implementation files based on metadata.

        Each skill is organized in its own folder following the AgentScope
        standard skill structure with a SKILL.md file.
        """
        from pathlib import Path

        skills_dir = pkg_dir / "skills"
        skills_dir.mkdir(exist_ok=True)

        # If skills are enabled, generate individual skill directories
        if metadata.enable_skills and metadata.skills:
            for skill in metadata.skills:
                skill_name = skill.lower().replace('-', '_')
                skill_dir = skills_dir / skill_name
                skill_dir.mkdir(exist_ok=True)

                # Generate SKILL.md with YAML frontmatter
                skill_md_content = f'''---
name: {skill}
description: A skill for {skill.lower()} operations
license: MIT
version: 1.0.0
---

# {skill.capitalize()} Skill

## Overview

This skill provides {skill.lower()} capabilities for the agent.

## Capabilities

- Execute basic {skill.lower()} operations
- Handle {skill.lower()} related requests
- Process {skill.lower()} inputs and provide results

## Usage

When the agent needs to perform {skill.lower()} operations, this skill will be invoked.

## Implementation

The skill is implemented in the `scripts/` directory with the following functions:

- `{skill_name}_execute`: Basic {skill.lower()} operation
- `{skill_name}_advanced`: Advanced {skill.lower()} operation with additional options

## Examples

### Basic Usage

```
Input: "Perform {skill.lower()} on X"
Output: Result of {skill.lower()} operation
```

### Advanced Usage

```
Input: "Perform advanced {skill.lower()} with options Y"
Output: Advanced {skill.lower()} result with options Y applied
```

## Notes

- This is a skeleton implementation
- Modify the implementation in `scripts/` to add actual functionality
- Update this SKILL.md to reflect the actual capabilities
'''
                (skill_dir / "SKILL.md").write_text(skill_md_content)

                # Create scripts directory for implementation
                scripts_dir = skill_dir / "scripts"
                scripts_dir.mkdir(exist_ok=True)

                # Generate skill implementation
                skill_impl_content = f'''"""
{skill.capitalize()} skill implementation.

This module provides the {skill} capability for the agent.
"""

from typing import Any, Dict, Optional
from agentscope.skills import skill


@skill("{skill}")
def {skill_name}_execute(input_text: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Execute {skill} operation.

    Args:
        input_text: Input text or command for {skill} operation
        context: Additional context for the operation

    Returns:
        Result of the {skill} operation
    """
    # TODO: Implement {skill} logic here
    # This is a skeleton implementation

    if context is None:
        context = {{}}

    # Placeholder implementation
    result = f"{{skill}} operation executed with input: {{input_text}}"

    return result


@skill("{skill}_advanced")
def {skill_name}_advanced(input_text: str, options: Optional[Dict[str, Any]] = None) -> str:
    """
    Execute advanced {skill} operation.

    Args:
        input_text: Input text or command for {skill} operation
        options: Additional options for the operation

    Returns:
        Result of the advanced {skill} operation
    """
    # TODO: Implement advanced {skill} logic here

    if options is None:
        options = {{}}

    # Placeholder implementation
    result = f"Advanced {{skill}} operation executed with options: {{options}}"

    return result
'''
                (scripts_dir / "__init__.py").write_text(skill_impl_content)

                # Create __init__.py for the skill directory
                (skill_dir / "__init__.py").write_text(f'''"""
{skill.capitalize()} skill package.
"""
''')

        # Always generate a base skills module for common utilities
        base_skills_dir = skills_dir / "base_skills"
        base_skills_dir.mkdir(exist_ok=True)

        base_skill_md = '''---
name: base_skills
description: Common utility skills for conversations, analysis, and summarization
license: MIT
version: 1.0.0
---

# Base Skills

## Overview

This skill provides common utility skills that can be used across different agents.

## Capabilities

- **Conversational Response**: Generate conversational responses
- **Analysis**: Analyze input text (length, word count, etc.)
- **Summarization**: Summarize text content

## Usage

These are general-purpose skills available to all agents by default.

## Implementation

The skills are implemented in `scripts/__init__.py`.
'''
        (base_skills_dir / "SKILL.md").write_text(base_skill_md)

        base_scripts_dir = base_skills_dir / "scripts"
        base_scripts_dir.mkdir(exist_ok=True)

        base_skills_content = '''"""
Base skills for the agent.

This module provides common skills that can be used across different agents.
"""

from typing import Any, Dict, Optional
from agentscope.skills import skill


@skill("conversation")
def conversational_response(input_text: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a conversational response.

    Args:
        input_text: User input text
        context: Conversation context and history

    Returns:
        Conversational response
    """
    if context is None:
        context = {}

    # Extract conversation history if available
    history = context.get("history", [])

    # Basic conversational logic
    response = f"Received: {input_text}"

    return response


@skill("analysis")
def analyze_input(input_text: str, analysis_type: str = "general") -> Dict[str, Any]:
    """
    Analyze input text.

    Args:
        input_text: Text to analyze
        analysis_type: Type of analysis (general, sentiment, entities, etc.)

    Returns:
        Analysis results
    """
    result = {
        "input": input_text,
        "analysis_type": analysis_type,
        "length": len(input_text),
        "word_count": len(input_text.split()),
    }

    # TODO: Add more sophisticated analysis based on analysis_type

    return result


@skill("summarization")
def summarize_text(input_text: str, max_length: int = 100) -> str:
    """
    Summarize input text.

    Args:
        input_text: Text to summarize
        max_length: Maximum length of summary

    Returns:
        Summarized text
    """
    # Basic summarization - take first max_length characters
    if len(input_text) <= max_length:
        return input_text

    summary = input_text[:max_length] + "..."

    return summary
'''
        (base_scripts_dir / "__init__.py").write_text(base_skills_content)
        (base_skills_dir / "__init__.py").write_text('''"""
Base skills package.
"""
''')

        # Generate skills __init__.py to export skills
        skills_init_path = skills_dir / "__init__.py"
        skills_init_content = f'''"""
Agent skills module.

This package contains various skill implementations for {metadata.package_name}.
"""
'''
        skills_init_content += '''
from .base_skills.scripts import (
    conversational_response,
    analyze_input,
    summarize_text,
)

__all__ = [
    "conversational_response",
    "analyze_input",
    "summarize_text",
]
'''

        # Add imports for custom skills
        if metadata.enable_skills and metadata.skills:
            for skill in metadata.skills:
                skill_module = skill.lower().replace('-', '_')
                skills_init_content += f'''

from .{skill_module}.scripts import {skill_module}_execute
'''

                # Add to __all__
                skills_init_content = skills_init_content.replace(
                    ']',
            f'    "{skill_module}_execute",\n]'
                )

        skills_init_path.write_text(skills_init_content)
