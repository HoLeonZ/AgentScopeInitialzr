"""
Extension generator for AgentScope Initializr.

Generates code for AgentScope extension points including
Model, Memory, Tool, Hooks, Formatter, Skills, RAG, and Pipeline configurations.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import threading
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
            "from .formatter import get_formatter",
            "from .middleware import middleware_manager, map_to_agent_params",
            "from .lifecycle import ApplicationLifecycle",
        ]

        # Build __all__ list
        all_exports = [
            '"settings"',
            '"get_model"',
            '"get_memory"',
            '"get_toolkit"',
            '"get_formatter"',
            '"middleware_manager"',
            '"map_to_agent_params"',
            '"ApplicationLifecycle"',
        ]

        if metadata.enable_rag:
            imports.append("from .rag import get_rag_retriever")
            all_exports.append('"get_rag_retriever"')

        if metadata.enable_pipeline:
            imports.append("from .pipeline import get_pipeline")
            all_exports.append('"get_pipeline"')

        if metadata.hooks:
            imports.append("from .hooks import HookManager, hook_registry")
            all_exports.append('"HookManager"')
            all_exports.append('"hook_registry"')

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
        cfg = metadata.model_config or {}

        # Extract model config from request, use defaults if not provided
        model_name = cfg.get("model", "qwen-max")
        api_key = cfg.get("api_key", "sk-fake-api-key-placeholder-please-replace")
        base_url = cfg.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        temperature = cfg.get("temperature", 0.7)
        max_tokens = cfg.get("max_tokens", 2000)

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

    # Model Configuration (from .env, with frontend config as defaults)
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "{metadata.model_provider.value}")
    MODEL_NAME = os.getenv("MODEL_NAME") or os.getenv("DASHSCOPE_MODEL") or "{model_name}"
    API_KEY = os.getenv("API_KEY") or os.getenv("DASHSCOPE_API_KEY") or "{api_key}"
    BASE_URL = os.getenv("BASE_URL") or os.getenv("DASHSCOPE_BASE_URL") or "{base_url}"
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "{temperature}"))
    MODEL_MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "{max_tokens}"))
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
        """Generate model configuration code using OpenAIChatModel."""
        return '''
def _normalize_base_url(url: str) -> str:
    """Normalize base URL by removing trailing paths that OpenAI client will add.

    Handles cases where users accidentally include /v1/chat/completions in BASE_URL.
    """
    if not url:
        return url
    # Remove trailing /chat/completions or /v1/chat/completions
    for suffix in ["/chat/completions", "/v1/chat/completions"]:
        if url.rstrip("/").endswith(suffix):
            url = url[: -len(suffix)]
    return url.rstrip("/")


def get_model():
    """Get configured model instance.

    Uses OpenAIChatModel which is compatible with any OpenAI-compatible API
    endpoint (including NPU/PPU servers).
    """
    from agentscope.model import OpenAIChatModel

    return OpenAIChatModel(
        model_name=settings.MODEL_NAME or "",
        api_key=settings.API_KEY or "",
        stream=settings.ENABLE_STREAMING,
        client_kwargs={"base_url": _normalize_base_url(settings.BASE_URL)},
        generate_kwargs={"temperature": settings.MODEL_TEMPERATURE, "max_tokens": settings.MODEL_MAX_TOKENS},
    )
'''

    def _generate_memory_config(self, metadata: AgentScopeMetadata) -> str:
        """Generate memory configuration code with enhanced options."""
        lines = [
            '"""Memory configuration with thread-safe singleton patterns."""',
            '',
            'import os',
            'import threading',
            'from typing import Optional',
            '',
        ]

        # Check if we have specific memory configurations
        has_short_term = metadata.short_term_memory and metadata.short_term_memory != 'in-memory'
        has_long_term = metadata.long_term_memory

        if has_long_term:
            # Long-term memory configuration
            lines.append(f"""
# Long-term memory configuration
LONG_TERM_MEMORY_TYPE = "{metadata.long_term_memory}"
""")

            if metadata.long_term_memory == "mem0":
                mem0_code = '''
def get_long_term_memory():
    """Get long-term memory instance with Mem0."""
    from agentscope.memory import Mem0Memory

    return Mem0Memory(
        api_key=os.getenv("MEM0_API_KEY")'''
                if metadata.rag_config and metadata.rag_config.get('api_url'):
                    mem0_code += ''',
        api_url=os.getenv("MEM0_API_URL")'''
                mem0_code += '''
    )
'''
                lines.append(mem0_code)
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
# Redis connection pool singleton
_redis_long_term_pool: Optional["redis.ConnectionPool"] = None
_redis_long_term_lock = threading.Lock()

def _get_redis_long_term_pool() -> "redis.ConnectionPool":
    """Get or create Redis connection pool for long-term memory (thread-safe singleton)."""
    global _redis_long_term_pool
    if _redis_long_term_pool is None:
        with _redis_long_term_lock:
            if _redis_long_term_pool is None:
                _redis_long_term_pool = redis.ConnectionPool(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", "6379")),
                    db=int(os.getenv("REDIS_DB", "0")),
                    password=os.getenv("REDIS_PASSWORD"),
                    max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
                    decode_responses=True,
                )
    return _redis_long_term_pool

_long_term_memory_instance: Optional["RedisMemory"] = None
_long_term_lock = threading.Lock()

def get_long_term_memory():
    """Get long-term memory instance with Redis (thread-safe singleton)."""
    global _long_term_memory_instance
    if _long_term_memory_instance is None:
        with _long_term_lock:
            if _long_term_memory_instance is None:
                from agentscope.memory import RedisMemory
                _long_term_memory_instance = RedisMemory(
                    connection_pool=_get_redis_long_term_pool(),
                )
    return _long_term_memory_instance
''')
            else:
                # Default fallback
                lines.append('''
def get_long_term_memory():
    """Get long-term memory instance - placeholder."""
    raise NotImplementedError("Long-term memory not configured")
''')

        if has_short_term:
            # Short-term memory configuration
            lines.append(f"""
# Short-term memory configuration
SHORT_TERM_MEMORY_TYPE = "{metadata.short_term_memory}"
""")

            if metadata.short_term_memory == "redis":
                use_redis_url = metadata.rag_config and metadata.rag_config.get('redis_url')

                if use_redis_url:
                    lines.append(f'''
_redis_short_term_pool: Optional["redis.ConnectionPool"] = None
_redis_short_term_lock = threading.Lock()

def _get_redis_short_term_pool() -> "redis.ConnectionPool":
    """Get or create Redis connection pool for short-term memory (thread-safe singleton)."""
    global _redis_short_term_pool
    if _redis_short_term_pool is None:
        with _redis_short_term_lock:
            if _redis_short_term_pool is None:
                _redis_short_term_pool = redis.ConnectionPool.from_url(
                    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
                    max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
                    decode_responses=True,
                )
    return _redis_short_term_pool

_short_term_memory_instance: Optional["RedisMemory"] = None
_short_term_lock = threading.Lock()

def get_short_term_memory():
    """Get short-term memory instance with Redis (thread-safe singleton)."""
    global _short_term_memory_instance
    if _short_term_memory_instance is None:
        with _short_term_lock:
            if _short_term_memory_instance is None:
                from agentscope.memory import RedisMemory
                _short_term_memory_instance = RedisMemory(
                    connection_pool=_get_redis_short_term_pool(),
                )
    return _short_term_memory_instance
''')
                else:
                    lines.append(f'''
_redis_short_term_pool: Optional["redis.ConnectionPool"] = None
_redis_short_term_lock = threading.Lock()

def _get_redis_short_term_pool() -> "redis.ConnectionPool":
    """Get or create Redis connection pool for short-term memory (thread-safe singleton)."""
    global _redis_short_term_pool
    if _redis_short_term_pool is None:
        with _redis_short_term_lock:
            if _redis_short_term_pool is None:
                _redis_short_term_pool = redis.ConnectionPool(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", "6379")),
                    db=int(os.getenv("REDIS_DB", "0")),
                    password=os.getenv("REDIS_PASSWORD"),
                    max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
                    decode_responses=True,
                )
    return _redis_short_term_pool

_short_term_memory_instance: Optional["RedisMemory"] = None
_short_term_lock = threading.Lock()

def get_short_term_memory():
    """Get short-term memory instance with Redis (thread-safe singleton)."""
    global _short_term_memory_instance
    if _short_term_memory_instance is None:
        with _short_term_lock:
            if _short_term_memory_instance is None:
                from agentscope.memory import RedisMemory
                key_prefix = os.getenv("REDIS_KEY_PREFIX", "agent:")
                _short_term_memory_instance = RedisMemory(
                    connection_pool=_get_redis_short_term_pool(),
                    key_prefix=key_prefix,
                )
    return _short_term_memory_instance
''')
            elif metadata.short_term_memory == "oceanbase":
                lines.append(f'''
def get_short_term_memory():
    """Get short-term memory instance with OceanBase."""
    from agentscope.memory import OceanBaseMemory

    return OceanBaseMemory(
        connection_string=os.getenv("OCEANBASE_CONNECTION_STRING"),
        table_name=os.getenv("OCEANBASE_TABLE_NAME", "agent_conversation"),
    )
''')
            else:
                # Default fallback
                lines.append('''
def get_short_term_memory():
    """Get short-term memory instance - placeholder."""
    raise NotImplementedError("Short-term memory not configured")
''')

        # Main get_memory function
        if has_short_term and has_long_term:
            # Combined memory (short-term + long-term)
            lines.append('''
def get_memory():
    """Get configured memory instance with both short and long-term storage."""
    from agentscope.memory import CombinedMemory

    short_term = get_short_term_memory()
    long_term = get_long_term_memory()

    return CombinedMemory(
        short_term=short_term,
        long_term=long_term,
    )
''')
        elif has_short_term:
            # Only short-term memory
            lines.append('''
def get_memory():
    """Get configured memory instance with short-term storage."""
    return get_short_term_memory()
''')
        elif has_long_term:
            # Only long-term memory
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
    from agentscope.tool import Toolkit

    toolkit = Toolkit()
''')

        # Add enabled tools (metadata.tools is a list of ToolConfig objects)
        tool_mappings = {
            "execute_python_code": ("execute_python_code", "from agentscope.tool import execute_python_code"),
            "execute_shell_command": ("execute_shell_command", "from agentscope.tool import execute_shell_command"),
            "web_search": ("web_search_tavily", "from agentscope.tool import web_search_tavily"),
            "browser_navigate": ("browser_navigate", "from agentscope.tool import browser_navigate"),
            "browser_click": ("browser_click", "from agentscope.tool import browser_click"),
            "browser_type": ("browser_type", "from agentscope.tool import browser_type"),
            "browser_screenshot": ("browser_screenshot", "from agentscope.tool import browser_screenshot"),
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
        # Map model providers to their formatter classes
        formatter_map = {
            ModelProvider.DOUBAO: "DashScopeChatFormatter",
            ModelProvider.DEEPSEEK: "OpenAIChatFormatter",
            ModelProvider.DASHSCOPE: "DashScopeChatFormatter",
        }

        # Map for multi-agent formatters
        multi_agent_formatter_map = {
            ModelProvider.DOUBAO: "DashScopeMultiAgentFormatter",
            ModelProvider.DEEPSEEK: "OpenAIMultiAgentFormatter",
            ModelProvider.DASHSCOPE: "DashScopeMultiAgentFormatter",
        }

        if metadata.formatter_name:
            # Use specific formatter by name
            return f'''
def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatter import {metadata.formatter_name}

    return {metadata.formatter_name}()
'''
        elif metadata.formatter == FormatterType.MULTI_AGENT:
            # Multi-agent formatter based on model provider
            formatter_class = multi_agent_formatter_map.get(
                metadata.model_provider,
                "DashScopeMultiAgentFormatter"
            )
            return f'''
def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatter import {formatter_class}

    return {formatter_class}()
'''
        else:
            # Chat formatter based on model provider (default)
            formatter_class = formatter_map.get(
                metadata.model_provider,
                "DashScopeChatFormatter"
            )
            return f'''
def get_formatter():
    """Get configured formatter instance."""
    from agentscope.formatter import {formatter_class}

    return {formatter_class}()
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
        # 优先用 store_type（独立 RAG 时），其次用 type（知识库同步时），默认 qdrant
        store_type = config.get("store_type") or config.get("type") or "qdrant"
        embedding_model = config.get("embedding_model", "openai")
        chunk_size = config.get("chunk_size", 500)
        chunk_overlap = config.get("chunk_overlap", 50)

        lines = [
            '"""RAG configuration with thread-safe singleton patterns."""',
            '',
            'import os',
            'import threading',
            'from typing import Optional',
            '',
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
_qdrant_client_instance: Optional["QdrantClient"] = None
_qdrant_client_lock = threading.Lock()

def _get_qdrant_client() -> "QdrantClient":
    """Get or create Qdrant client (thread-safe singleton with connection pool)."""
    global _qdrant_client_instance
    if _qdrant_client_instance is None:
        with _qdrant_client_lock:
            if _qdrant_client_instance is None:
                _qdrant_client_instance = QdrantClient(
                    url=os.getenv("QDRANT_URL", f"http://{{os.getenv('QDRANT_HOST', 'localhost')}}:{{os.getenv('QDRANT_PORT', '6333')}}"),
                    timeout=int(os.getenv("QDRANT_TIMEOUT", "30")),
                    prefer_grpc=os.getenv("QDRANT_USE_GRPC", "false").lower() == "true",
                )
    return _qdrant_client_instance

_vector_store_instance: Optional["QdrantVectorStore"] = None
_vector_store_lock = threading.Lock()

def get_vector_store() -> "QdrantVectorStore":
    """Get configured Qdrant vector store instance (thread-safe singleton)."""
    global _vector_store_instance
    if _vector_store_instance is None:
        with _vector_store_lock:
            if _vector_store_instance is None:
                from agentscope.rag import QdrantVectorStore
                _vector_store_instance = QdrantVectorStore(
                    client=_get_qdrant_client(),
                    collection_name=os.getenv("QDRANT_COLLECTION", "agent_documents"),
                    embedding_model="{embedding_model}",
                )
    return _vector_store_instance
''')
        elif store_type == "kbase":
            kbase_url = config.get("kbase_url", "")
            lines.append(f'''
import httpx
from urllib.parse import urljoin

_kbase_client_instance: Optional["KBaseRetriever"] = None
_kbase_client_lock = threading.Lock()


class KBaseRetriever:
    """KBase knowledge base retriever using POST."""

    def __init__(
        self,
        base_url: str,
        top_k: int = 10,
        library_id: str = "",
    ):
        self.base_url = base_url.rstrip("/")
        self.search_url = self.base_url
        self.default_top_k = top_k
        self.library_id = library_id

    def retrieve(self, query: str, **kwargs) -> list:
        """Search knowledge base for relevant documents.

        Args:
            query: Search query string
            **kwargs: Additional parameters:
                - top_k: number of results to return
                - library_id: knowledge base library ID

        Returns:
            List of retrieved documents
        """
        top_k = kwargs.get("top_k", self.default_top_k)
        library_id = kwargs.get("library_id", self.library_id)

        payload = {
            "sent": query,
            "library_id": library_id,
            "topk": top_k,
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(self.search_url, json=payload)
            response.raise_for_status()
            result = response.json()
            # 响应结构: rag_prompt (str), rag_source (jsonobject)
            rag_prompt = result.get("rag_prompt", "")
            rag_source = result.get("rag_source", dict())
            return [{"prompt": rag_prompt, "source": rag_source, "score": 1.0}]

    def add_documents(self, documents: list, **kwargs) -> None:
        """Add documents to knowledge base (not supported for KBase)."""
        raise NotImplementedError("KBase does not support manual document addition")


def get_vector_store() -> "KBaseRetriever":
    """Get configured KBase retriever instance (thread-safe singleton)."""
    global _kbase_client_instance
    if _kbase_client_instance is None:
        with _kbase_client_lock:
            if _kbase_client_instance is None:
                _kbase_client_instance = KBaseRetriever(
                    base_url=os.getenv("KBASE_URL", "{kbase_url}"),
                    top_k={chunk_size},
                    library_id=os.getenv("KBASE_LIBRARY_ID", ""),
                )
    return _kbase_client_instance
''')
        else:
            # Default fallback
            lines.append(f'''
def get_vector_store():
    """Get vector store - placeholder for {store_type}."""
    raise NotImplementedError("Vector store type not implemented: {store_type}")
''')

        # Add RAG retriever function
        if store_type == "kbase":
            lines.append('''
def get_rag_retriever():
    """Get configured KBase retriever instance (direct retriever, not vector store)."""
    return get_vector_store()
''')
        else:
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

    def generate_formatter_config_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate formatter.py configuration file."""
        config = self._generate_formatter_config(metadata)

        return f'''"""
Formatter configuration for {metadata.name}.

This module contains the formatter initialization for message formatting.
"""

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
            func_name = hook.name.replace(" ", "_").lower() if hook.name else f"{hook.hook_type}_hook"
            if hook.hook_type == "pre_reply":
                hooks_code.append(f'''
@agent.hook("pre_reply")
async def {func_name}(msg):
    """Hook: {hook.name} - called before agent reply."""
    import logging
    logging.info(f"Pre-reply hook '{hook.name}' called: {{msg}}")
    # Modify msg here if needed
    return msg
''')
            elif hook.hook_type == "post_reply":
                hooks_code.append(f'''
@agent.hook("post_reply")
async def {func_name}(response):
    """Hook: {hook.name} - called after agent reply."""
    import logging
    logging.info(f"Post-reply hook '{hook.name}' called: {{response}}")
    # Modify response here if needed
    return response
''')
            elif hook.hook_type == "pre_observe":
                hooks_code.append(f'''
@agent.hook("pre_observe")
async def {func_name}(observation):
    """Hook: {hook.name} - called before agent observation."""
    import logging
    logging.info(f"Pre-observe hook '{hook.name}' called: {{observation}}")
    # Modify observation here if needed
    return observation
''')
            elif hook.hook_type == "post_observe":
                hooks_code.append(f'''
@agent.hook("post_observe")
async def {func_name}(observation):
    """Hook: {hook.name} - called after agent observation."""
    import logging
    logging.info(f"Post-observe hook '{hook.name}' called: {{observation}}")
    # Process observation here if needed
    return observation
''')

        return "\n".join(hooks_code)

    def generate_hooks_file(self, metadata: AgentScopeMetadata) -> str:
        """
        Generate hooks.py module for managing hook instances.

        Args:
            metadata: Project metadata

        Returns:
            Hooks module code
        """
        if not metadata.hooks:
            return ""

        # Generate hook class definitions based on hook types
        hook_classes = []
        for hook in metadata.hooks:
            if not hook.enabled:
                continue
            func_name = hook.name.replace(" ", "_").replace("-", "_").lower() if hook.name else f"{hook.hook_type}_hook"

            # Generate hook class for each hook type
            if hook.hook_type == "pre_reply":
                hook_classes.append(f'''
class {func_name.title().replace("_", "")}Hook:
    """Hook: {hook.name} - called before agent reply."""

    async def __call__(self, msg):
        """Execute the hook."""
        return msg
''')
            elif hook.hook_type == "post_reply":
                hook_classes.append(f'''
class {func_name.title().replace("_", "")}Hook:
    """Hook: {hook.name} - called after agent reply."""

    async def __call__(self, response):
        """Execute the hook."""
        return response
''')
            elif hook.hook_type == "pre_observe":
                hook_classes.append(f'''
class {func_name.title().replace("_", "")}Hook:
    """Hook: {hook.name} - called before agent observation."""

    async def __call__(self, observation):
        """Execute the hook."""
        return observation
''')
            elif hook.hook_type == "post_observe":
                hook_classes.append(f'''
class {func_name.title().replace("_", "")}Hook:
    """Hook: {hook.name} - called after agent observation."""

    async def __call__(self, observation):
        """Execute the hook."""
        return observation
''')

        # Generate hook instances and registry
        hook_instances = []
        hook_registry_entries = []
        for hook in metadata.hooks:
            if not hook.enabled:
                continue
            func_name = hook.name.replace(" ", "_").replace("-", "_").lower() if hook.name else f"{hook.hook_type}_hook"
            class_name = func_name.title().replace("_", "") + "Hook"
            hook_instances.append(f"{func_name}_instance = {class_name}()")
            hook_registry_entries.append(f'    "{hook.hook_type}:{hook.name}": {func_name}_instance,')

        hook_classes_str = "\n".join(hook_classes)
        hook_instances_str = "\n".join(hook_instances)
        hook_registry_str = "\n".join(hook_registry_entries)

        return f'''"""
Agent Hooks Module

This module manages hook instances and their registration to agents.
Hooks are called at specific points in the agent lifecycle:
- pre_reply: Before agent sends a reply
- post_reply: After agent sends a reply
- pre_observe: Before agent observes environment
- post_observe: After agent observes environment
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# Hook Classes
# =============================================================================

{hook_classes_str}


# =============================================================================
# Hook Instances
# =============================================================================

{hook_instances_str}


# =============================================================================
# Hook Registry
# =============================================================================

class HookRegistry:
    """Registry for managing hook instances."""

    def __init__(self):
        self._hooks: Dict[str, Any] = {{}}
        self._agent_hooks: Dict[str, List[Any]] = {{}}

    def register(self, key: str, hook_instance: Any) -> None:
        """
        Register a hook instance.

        Args:
            key: Unique identifier for the hook (e.g., "pre_reply:logging")
            hook_instance: Hook instance to register
        """
        self._hooks[key] = hook_instance
        logger.debug(f"Registered hook: {{key}}")

    def get(self, key: str) -> Optional[Any]:
        """Get a hook instance by key."""
        return self._hooks.get(key)

    def get_by_type(self, hook_type: str) -> List[Any]:
        """
        Get all hook instances for a specific hook type.

        Args:
            hook_type: Type of hook (e.g., "pre_reply", "post_reply")

        Returns:
            List of hook instances
        """
        return [
            hook for key, hook in self._hooks.items()
            if key.startswith(f"{{hook_type}}:")
        ]

    def attach_to_agent(self, agent: Any, hook_keys: Optional[List[str]] = None) -> None:
        """
        Attach registered hooks to an agent instance.

        Args:
            agent: Agent instance to attach hooks to
            hook_keys: Optional list of specific hook keys to attach.
                      If None, attaches all registered hooks.
        """
        if hook_keys is None:
            hook_keys = list(self._hooks.keys())

        for key in hook_keys:
            hook = self._hooks.get(key)
            if hook:
                # Extract hook type from key
                hook_type = key.split(":")[0] if ":" in key else key
                try:
                    agent.hook(hook_type)(hook)
                    logger.info(f"Attached hook {{key}} to agent")
                except Exception as e:
                    logger.warning(f"Failed to attach hook {{key}}: {{e}}")

    def clear(self) -> None:
        """Clear all registered hooks."""
        self._hooks.clear()
        self._agent_hooks.clear()


# Global hook registry instance
hook_registry = HookRegistry()


# =============================================================================
# Hook Manager
# =============================================================================

class HookManager:
    """
    Manages hook lifecycle and registration.

    This class provides a high-level interface for managing hooks,
    including initialization, attachment to agents, and cleanup.
    """

    def __init__(self):
        self._initialized = False
        self._hook_configs = {{
{hook_registry_str}
        }}

    def initialize(self) -> None:
        """
        Initialize the hook manager and register all hooks.

        This should be called during application initialization.
        """
        if self._initialized:
            return

        # Register all hook instances
        for key, hook_instance in self._hook_configs.items():
            hook_registry.register(key, hook_instance)

        self._initialized = True
        logger.info(f"HookManager initialized with {{len(self._hook_configs)}} hooks")

    def shutdown(self) -> None:
        """
        Shutdown the hook manager and cleanup hooks.

        This should be called during application shutdown.
        """
        if not self._initialized:
            return

        hook_registry.clear()
        self._initialized = False
        logger.info("HookManager shutdown complete")

    def attach_to_agent(self, agent: Any, hook_types: Optional[List[str]] = None) -> None:
        """
        Attach hooks to an agent.

        Args:
            agent: Agent instance to attach hooks to
            hook_types: Optional list of hook types to attach
        """
        if not self._initialized:
            logger.warning("HookManager not initialized. Call initialize() first.")
            return

        if hook_types is None:
            # Attach all hooks
            hook_registry.attach_to_agent(agent)
        else:
            # Attach only specified hook types
            keys = [
                key for key in self._hook_configs.keys()
                if any(key.startswith(f"{{ht}}:") for ht in hook_types)
            ]
            hook_registry.attach_to_agent(agent, keys)

    def get_hook(self, name: str) -> Optional[Any]:
        """
        Get a specific hook by name.

        Args:
            name: Hook name (e.g., "logging" for "pre_reply:logging")

        Returns:
            Hook instance or None
        """
        for key, hook in self._hook_configs.items():
            if name in key:
                return hook
        return None


# Global hook manager instance
HookManager = HookManager()
'''
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

    def generate_ragas_evaluation_code(self, metadata: AgentScopeMetadata) -> str:
        """Generate RAGAS evaluation module code."""
        if not metadata.enable_ragas_evaluation:
            return ""

        config = metadata
        metrics_imports = []
        metrics_instances = []

        if "faithfulness" in config.evaluation_metrics:
            metrics_imports.append("faithfulness")
            metrics_instances.append("faithfulness")
        if "answer_relevancy" in config.evaluation_metrics:
            metrics_imports.append("answer_relevancy")
            metrics_instances.append("answer_relevancy")
        if "context_precision" in config.evaluation_metrics:
            metrics_imports.append("context_precision")
            metrics_instances.append("context_precision")
        if "context_recall" in config.evaluation_metrics:
            metrics_imports.append("context_recall")
            metrics_instances.append("context_recall")

        metrics_import_str = ", ".join(metrics_imports)
        metrics_list_str = ", ".join(f"    {m}" for m in metrics_instances)

        code = f'''"""
RAGAS Evaluation Module for {metadata.name}.

This module provides RAGAS-based evaluation for RAG systems.
Place your evaluation data CSV file in this directory.
"""
import os
import pandas as pd
from datetime import datetime
from ragas import evaluate
from ragas.metrics import {metrics_import_str}
from datasets import Dataset


def load_evaluation_data(csv_filename: str = "{config.evaluation_csv_filename}") -> Dataset:
    """
    Load evaluation data from CSV file.

    Args:
        csv_filename: Name of the CSV file in the evaluation directory

    Returns:
        Dataset ready for evaluation
    """
    eval_dir = os.path.dirname(__file__)
    csv_path = os.path.join(eval_dir, csv_filename)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Evaluation data file not found: {{csv_path}}\\n"
            f"Please place your CSV file with columns: question, answer, context, reference"
        )

    df = pd.read_csv(csv_path)
    required_columns = ['question', 'answer', 'context', 'reference']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {{missing}}")

    return Dataset.from_pandas(df)


def run_evaluation(csv_filename: str = "{config.evaluation_csv_filename}") -> dict:
    """
    Run RAGAS evaluation on the dataset.

    Args:
        csv_filename: Name of the CSV file

    Returns:
        Evaluation result object
    """
    print(f"Loading evaluation data from: {{csv_filename}}")
    dataset = load_evaluation_data(csv_filename)

    metrics = [
{metrics_list_str},
    ]

    print(f"Running evaluation with metrics: {{[m.name for m in metrics]}}")
    result = evaluate(dataset, metrics=metrics)

    return result


def generate_html_report(result, metadata, output_path: str = "evaluation_report.html"):
    """
    Generate HTML report from evaluation results.

    Args:
        result: RAGAS evaluation result
        metadata: AgentScope metadata
        output_path: Path to save the HTML report
    """
    scores = result.scores
    result_df = result.to_pandas()

    metrics_html = ""
    if isinstance(scores, dict):
        for metric_name, score_value in scores.items():
            score_fmt = f"{score_value:.4f}"
            metrics_html += f"""
        <div class="metric-card">
            <div class="metric-value">{score_fmt}</div>
            <div class="metric-name">{metric_name}</div>
        </div>"""

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAGAS Evaluation Report - {metadata.name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f5f7fa; padding: 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; margin-bottom: 10px; }}
        .subtitle {{ color: #7f8c8d; margin-bottom: 30px; }}
        .card {{ background: white; border-radius: 12px; padding: 30px;
                margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                         gap: 20px; margin: 20px 0; }}
        .metric-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 25px; border-radius: 10px; color: white; text-align: center; }}
        .metric-value {{ font-size: 36px; font-weight: bold; margin-bottom: 8px; }}
        .metric-name {{ font-size: 14px; opacity: 0.9; text-transform: uppercase; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ebeef5; padding: 12px; text-align: left; }}
        th {{ background: #f5f7fa; font-weight: 600; color: #2c3e50; }}
        tr:hover {{ background: #fafafa; }}
        .footer {{ text-align: center; color: #95a5a6; margin-top: 30px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>RAGAS Evaluation Report</h1>
        <p class="subtitle">Project: {metadata.name} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="card">
            <h2>Overall Scores</h2>
            <div class="metrics-grid">
                {metrics_html or '<p>No metrics available</p>'}
            </div>
        </div>

        <div class="card">
            <h2>Detailed Results</h2>
            {result_df.to_html(index=False, classes='detail-table', escape=False) if hasattr(result_df, 'to_html') else '<p>No detailed data available</p>'}
        </div>

        <div class="footer">
            Generated by AgentScope Initializr - RAGAS Evaluation Module
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Report generated: {{output_path}}")


if __name__ == "__main__":
    print("=" * 60)
    print("RAGAS Evaluation for {metadata.name}")
    print("=" * 60)
    print()
    print(f"CSV File: {config.evaluation_csv_filename}")
    print(f"Metrics: {', '.join(config.evaluation_metrics)}")
    print()

    result = run_evaluation()
    generate_html_report(result, metadata)

    print()
    print("=" * 60)
    print("Evaluation complete! Open evaluation_report.html to view results.")
    print("=" * 60)
'''

        return code

    def generate_ragas_requirements(self, metadata: AgentScopeMetadata) -> str:
        """Generate requirements.txt for RAGAS evaluation."""
        if not metadata.enable_ragas_evaluation:
            return ""

        return """# RAGAS Evaluation Dependencies
ragas>=0.1.0
langchain>=0.1.0
langchain-openai>=0.0.5
pandas>=2.0.0
datasets>=2.14.0
"""

    def generate_ragas_readme(self, metadata: AgentScopeMetadata) -> str:
        """Generate README for evaluation directory."""
        if not metadata.enable_ragas_evaluation:
            return ""

        return f"""# RAGAS Evaluation Module

This directory contains the RAGAS-based evaluation module for **{metadata.name}**.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your evaluation data:**
   Create a CSV file named `{metadata.evaluation_csv_filename}` with the following columns:
   - `question`: The question being asked
   - `answer`: The generated answer from your RAG system
   - `context`: The retrieved context used to generate the answer
   - `reference`: The reference/ground truth answer

   Example CSV:
   ```csv
   question,answer,context,reference
   "What is AgentScope?","AgentScope is...","AgentScope is a...","AgentScope is a multi-agent platform..."
   ```

3. **Run evaluation:**
   ```bash
   python ragas_evaluator.py
   ```

4. **View results:**
   Open `evaluation_report.html` in your browser.

## Metrics

The evaluation uses the following RAGAS metrics:
- **Faithfulness**: Measures how faithful the answer is to the context
- **Answer Relevancy**: Measures how relevant the answer is to the question
- **Context Precision**: Measures how precise the retrieved context is
- **Context Recall**: Measures how well the context captures the reference

## Configuration

You can customize the evaluation by modifying `ragas_evaluator.py`:
- Change the CSV filename
- Add or remove metrics
- Customize the HTML report template

## Output

The evaluation generates:
- `evaluation_report.html`: Interactive HTML report with visualizations
- Console output with metric scores
"""

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


    def generate_middleware_manager_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate middleware manager for auto-injection."""
        return f'''"""
Middleware manager for {metadata.name}.

This module provides automatic middleware injection and lifecycle management.
"""

from typing import Dict, Any, Optional, List
# Import from specific modules to avoid circular imports
from {metadata.package_name}.config.model import get_model
from {metadata.package_name}.config.formatter import get_formatter
from {metadata.package_name}.config.memory import get_memory
from {metadata.package_name}.config.toolkit import get_toolkit


class MiddlewareManager:
    """Framework-level middleware manager for automatic injection."""

    def __init__(self):
        self._middlewares: Dict[str, Dict[str, Any]] = {{}}
        self._initialized = False

    def register(self, name: str, factory: callable, config: Dict[str, Any] = None):
        """
        Register a middleware factory function.

        Args:
            name: Middleware name
            factory: Factory function that creates the middleware instance
            config: Optional configuration dict
        """
        self._middlewares[name] = {{
            'factory': factory,
            'config': config or {{}},
            'instance': None
        }}

    def initialize_all(self):
        """Initialize all registered middlewares."""
        if self._initialized:
            return

        for name, middleware in self._middlewares.items():
            try:
                middleware['instance'] = middleware['factory'](**middleware['config'])
            except Exception as e:
                raise RuntimeError(f"Failed to initialize middleware '{{name}}': {{e}}")

        self._initialized = True

    def get(self, name: str) -> Any:
        """
        Get middleware instance.

        Args:
            name: Middleware name

        Returns:
            Middleware instance

        Raises:
            RuntimeError: If middlewares not initialized
            KeyError: If middleware not found
        """
        if not self._initialized:
            raise RuntimeError(
                "Middlewares not initialized. "
                "Call initialize_all() after agentscope.init()"
            )
        return self._middlewares[name]['instance']

    def has(self, name: str) -> bool:
        """Check if middleware is registered."""
        return name in self._middlewares

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._middlewares.get(key, {{}}).get('config', {{}}).get(key, default)

    def shutdown_all(self):
        """Cleanup all middleware resources."""
        for middleware in self._middlewares.values():
            instance = middleware['instance']
            if instance and hasattr(instance, 'close'):
                try:
                    instance.close()
                except Exception as e:
                    print(f"Warning: Error closing middleware: {{e}}")
        self._initialized = False


# Global middleware manager instance
middleware_manager = MiddlewareManager()


def register_core_middlewares():
    """Register core middlewares (model, formatter, memory, toolkit)."""
    # Register core components
    middleware_manager.register('model', lambda: get_model(), {{}})
    middleware_manager.register('formatter', lambda: get_formatter(), {{}})
    middleware_manager.register('memory', lambda: get_memory(), {{}})
    middleware_manager.register('toolkit', lambda: get_toolkit(), {{}})


def map_to_agent_params() -> Dict[str, Any]:
    """
    Map middlewares to ReActAgent parameters.

    Returns:
        Dictionary of agent parameters
    """
    params = {{
        'model': middleware_manager.get('model'),
        'formatter': middleware_manager.get('formatter'),
    }}

    # Optional middlewares
    optional_middlewares = ['toolkit', 'memory']

    for middleware_name in optional_middlewares:
        if middleware_manager.has(middleware_name):
            params[middleware_name] = middleware_manager.get(middleware_name)

    # Add optional RAG middleware if registered
    if middleware_manager.has('knowledge'):
        params['knowledge'] = middleware_manager.get('knowledge')

    # Add optional pipeline middleware if registered
    if middleware_manager.has('plan_notebook'):
        params['plan_notebook'] = middleware_manager.get('plan_notebook')

    # Add configuration parameters
    params.update({{
        'enable_meta_tool': middleware_manager.get_config('enable_meta_tool', False),
        'parallel_tool_calls': middleware_manager.get_config('parallel_tool_calls', False),
        'max_iters': middleware_manager.get_config('max_iters', 10),
    }})

    return params
'''

    def generate_lifecycle_manager_file(self, metadata: AgentScopeMetadata) -> str:
        """Generate application lifecycle manager with instance-based state."""
        pkg_name = metadata.package_name
        proj_name = metadata.name

        # Build imports
        imports = [
            f'''"""
Application lifecycle manager for {proj_name}.

This module provides framework-level initialization and shutdown
integrated with AgentScope lifecycle.
"""''',
            '''
import os
import logging
from typing import Optional, Dict, Any

import agentscope
from ''' + pkg_name + '''.config.middleware import (
    middleware_manager,
    register_core_middlewares,
    map_to_agent_params,
)''',
        ]

        if metadata.enable_rag:
            imports.append(f'''
from {pkg_name}.config.rag import get_rag_retriever''')

        if metadata.enable_pipeline:
            imports.append(f'''
from {pkg_name}.config.pipeline import get_pipeline''')

        if metadata.hooks:
            imports.append(f'''
from {pkg_name}.config.hooks import HookManager, hook_registry''')

        # Build class definition
        class_def = '''
logger = logging.getLogger(__name__)


class ApplicationLifecycle:
    """
    Application lifecycle manager integrated with AgentScope.

    This class manages the application lifecycle including:
    - AgentScope initialization
    - Middleware registration and initialization
    - Hook instantiation and registration
    - Resource cleanup on shutdown

    Uses instance-based state to avoid class-level state issues.
    """

    def __init__(self):
        """Initialize lifecycle manager with instance-based state."""
        self._initialized = False
        self._agentscope_initialized = False

    def initialize(self) -> None:
        """
        Initialize application with AgentScope and all middlewares.

        This should be called before creating any agents.
        """
        if self._initialized:
            logger.debug("ApplicationLifecycle already initialized")
            return

        logger.info("Initializing ApplicationLifecycle...")

        # 1. Initialize AgentScope (if not already initialized)
        if not self._agentscope_initialized:
            # Ensure logs directory exists
            os.makedirs("logs", exist_ok=True)
            agentscope.init(
                project="''' + proj_name + '''",
                name="''' + proj_name + '''_instance",
                logging_path="logs/agentscope.log",
                logging_level=os.getenv("LOG_LEVEL", "INFO"),
            )
            self._agentscope_initialized = True

        # 2. Register core middlewares
        register_core_middlewares()

        # 3. Register optional middlewares'''

        if metadata.enable_rag:
            class_def += '''
        # Register RAG as knowledge middleware
        middleware_manager.register(
            'knowledge',
            lambda: get_rag_retriever(),
            {}
        )'''

        if metadata.enable_pipeline:
            class_def += '''
        # Register pipeline as plan notebook middleware
        middleware_manager.register(
            'plan_notebook',
            lambda: get_pipeline(),
            {}
        )'''

        class_def += '''

        # 4. Initialize all middlewares
        middleware_manager.initialize_all()'''

        if metadata.hooks:
            class_def += '''

        # 5. Initialize hook manager
        HookManager.initialize()
        logger.info("Initialized " + str(len(HookManager._hook_configs)) + " hooks")'''

        class_def += '''

        self._initialized = True
        logger.info("ApplicationLifecycle initialization complete")

    def shutdown(self) -> None:
        """
        Shutdown application and cleanup resources.

        This should be called when exiting the application.
        """
        if not self._initialized:
            logger.debug("ApplicationLifecycle not initialized, skipping shutdown")
            return

        logger.info("Shutting down ApplicationLifecycle...")'''

        if metadata.hooks:
            class_def += '''
        # 1. Shutdown hooks
        HookManager.shutdown()'''

        class_def += '''

        # 2. Shutdown middlewares
        middleware_manager.shutdown_all()

        self._initialized = False
        logger.info("ApplicationLifecycle shutdown complete")

    def get_agent_params(self) -> Dict[str, Any]:
        """
        Get agent parameters with all middlewares auto-injected.

        Returns:
            Dictionary of agent parameters

        Raises:
            RuntimeError: If lifecycle not initialized
        """
        if not self._initialized:
            raise RuntimeError(
                "Application not initialized. Call ApplicationLifecycle.initialize() first."
            )

        return map_to_agent_params()

    def attach_hooks_to_agent(self, agent: Any, hook_types: Optional[list] = None) -> None:
        """
        Attach configured hooks to an agent instance.

        This should be called after creating an agent to register
        all configured hooks.

        Args:
            agent: Agent instance to attach hooks to
            hook_types: Optional list of specific hook types to attach
                       (e.g., ["pre_reply", "post_reply"])
                       If None, all hooks are attached.
        """
        if not self._initialized:
            raise RuntimeError(
                "Application not initialized. Call ApplicationLifecycle.initialize() first."
            )'''

        if metadata.hooks:
            class_def += '''
        HookManager.attach_to_agent(agent, hook_types)
        logger.info("Attached hooks to agent " + str(agent.name))'''
        else:
            class_def += '''
        logger.debug("No hooks configured, skipping hook attachment")'''

        class_def += '''

    @property
    def is_initialized(self) -> bool:
        """Check if lifecycle manager is initialized."""
        return self._initialized


# Global lifecycle manager instance
_app_lifecycle: Optional["ApplicationLifecycle"] = None

# Save reference to the original class before reassignment
_ApplicationLifecycleBase = ApplicationLifecycle


def get_lifecycle() -> "ApplicationLifecycle":
    """
    Get the global ApplicationLifecycle instance.

    Returns:
        The global ApplicationLifecycle instance
    """
    global _app_lifecycle
    if _app_lifecycle is None:
        _app_lifecycle = _ApplicationLifecycleBase()
    return _app_lifecycle


# Backwards compatibility: singleton-style class methods
class _ApplicationLifecycleCompat:
    """
    Backwards compatibility wrapper for ApplicationLifecycle.

    Provides class-method interface while using instance-based lifecycle.
    """

    @classmethod
    def initialize(cls) -> None:
        """Initialize the application lifecycle."""
        get_lifecycle().initialize()

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown the application lifecycle."""
        get_lifecycle().shutdown()

    @classmethod
    def get_agent_params(cls) -> Dict[str, Any]:
        """Get agent parameters."""
        return get_lifecycle().get_agent_params()

    @classmethod
    def attach_hooks_to_agent(cls, agent: Any, hook_types: Optional[list] = None) -> None:
        """Attach hooks to an agent."""
        get_lifecycle().attach_hooks_to_agent(agent, hook_types)

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if initialized."""
        return get_lifecycle().is_initialized


# Use compatibility class for backwards compatibility
ApplicationLifecycle = _ApplicationLifecycleCompat
'''
        return '\n'.join(imports) + class_def
