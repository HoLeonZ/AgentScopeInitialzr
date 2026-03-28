"""
Metadata models for AgentScope Initializr.

Defines the data structures for project configuration and metadata.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class AgentType(Enum):
    """Agent type enumeration."""
    BASIC = "basic"
    MULTI_AGENT = "multi-agent"
    RESEARCH = "research"
    BROWSER = "browser"


class ModelProvider(Enum):
    """Model provider enumeration."""
    OPENAI = "openai"
    DASHSCOPE = "dashscope"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class MemoryType(Enum):
    """Memory type enumeration."""
    IN_MEMORY = "in-memory"
    LONG_TERM = "long-term"


class FormatterType(Enum):
    """Formatter type enumeration."""
    CHAT = "chat"
    MULTI_AGENT = "multi-agent"


class ProjectLayout(Enum):
    """Project layout enumeration."""
    STANDARD = "standard"  # src/project_name/ layout (recommended)
    LIGHTWEIGHT = "lightweight"  # project_name/ layout


@dataclass
class Dependency:
    """Represents a project dependency."""
    name: str
    version: Optional[str] = None
    optional: bool = False

    def __str__(self) -> str:
        if self.version:
            return f"{self.name}=={self.version}"
        return self.name


@dataclass
class ToolConfig:
    """Configuration for a tool."""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HookConfig:
    """Configuration for an agent hook."""
    hook_type: str  # pre_reply, post_reply, pre_observe, post_observe
    enabled: bool = True
    implementation: Optional[str] = None


@dataclass
class MiddlewareConfig:
    """Configuration for middleware."""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentScopeMetadata:
    """
    AgentScope project metadata.

    This class contains all the information needed to generate
    an AgentScope project with specific configurations.
    """
    # Project basic info
    name: str
    description: str = ""
    package_name: str = ""
    version: str = "0.1.0"
    python_version: str = "3.10"

    # Project layout
    layout: ProjectLayout = ProjectLayout.STANDARD

    # Agent configuration
    agent_type: AgentType = AgentType.BASIC
    model_provider: ModelProvider = ModelProvider.OPENAI

    # Dependencies and tools
    dependencies: List[Dependency] = field(default_factory=list)
    tools: List[ToolConfig] = field(default_factory=list)

    # Memory configuration
    memory_type: MemoryType = MemoryType.IN_MEMORY

    # AgentScope extension points
    hooks: List[HookConfig] = field(default_factory=list)
    middleware: List[MiddlewareConfig] = field(default_factory=list)
    formatter: FormatterType = FormatterType.CHAT

    # Additional settings
    enable_streaming: bool = True
    enable_thinking: bool = False
    parallel_tool_calls: bool = True

    # Author information
    author: str = ""
    email: str = ""

    def __post_init__(self):
        """Validate and normalize metadata after initialization."""
        if not self.package_name:
            # Convert project name to package name
            self.package_name = self.name.lower().replace("-", "_").replace(" ", "_")

        # Ensure dependencies is a list
        if not isinstance(self.dependencies, list):
            self.dependencies = list(self.dependencies)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "package_name": self.package_name,
            "version": self.version,
            "python_version": self.python_version,
            "layout": self.layout.value,
            "agent_type": self.agent_type.value,
            "model_provider": self.model_provider.value,
            "memory_type": self.memory_type.value,
            "formatter": self.formatter.value,
            "enable_streaming": self.enable_streaming,
            "enable_thinking": self.enable_thinking,
            "parallel_tool_calls": self.parallel_tool_calls,
            "author": self.author,
            "email": self.email,
        }
