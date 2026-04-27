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
    DOUBAO = "doubao"
    DEEPSEEK = "deepseek"
    DASHSCOPE = "dashscope"
    NPU = "npu"


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
    STANDARD = "standard"
    LIGHTWEIGHT = "lightweight"


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
    name: str  # User-defined name for the hook
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
    python_version: str = "3.14"

    # Agent configuration
    agent_type: AgentType = AgentType.BASIC
    model_provider: ModelProvider = ModelProvider.DASHSCOPE

    # Dependencies and tools
    dependencies: List[Dependency] = field(default_factory=list)
    tools: List[ToolConfig] = field(default_factory=list)

    # Memory configuration
    memory_type: MemoryType = MemoryType.IN_MEMORY
    short_term_memory: Optional[str] = None
    long_term_memory: Optional[str] = None

    # AgentScope extension points
    hooks: List[HookConfig] = field(default_factory=list)
    middleware: List[MiddlewareConfig] = field(default_factory=list)
    formatter: FormatterType = FormatterType.CHAT
    formatter_name: Optional[str] = None

    # Skills configuration
    enable_skills: bool = False
    skills: List[str] = field(default_factory=list)

    # Knowledge base configuration
    enable_knowledge: bool = False
    knowledge_config: Dict[str, Any] = field(default_factory=dict)

    # RAG configuration
    enable_rag: bool = False
    rag_config: Dict[str, Any] = field(default_factory=dict)

    # Pipeline configuration
    enable_pipeline: bool = False
    pipeline_config: Dict[str, Any] = field(default_factory=dict)

    # Additional settings
    enable_streaming: bool = True
    enable_thinking: bool = False
    parallel_tool_calls: bool = True
    model_config: Dict[str, Any] = field(default_factory=dict)  # model, api_key, base_url, temperature, max_tokens

    # Author information
    author: str = ""
    email: str = ""

    # Testing & Evaluation
    generate_tests: bool = False
    generate_evaluation: bool = False
    evaluator_type: str = "general"
    enable_openjudge: bool = False
    openjudge_graders: List[str] = field(default_factory=list)
    initial_benchmark_tasks: int = 0

    # RAGAS Evaluation
    enable_ragas_evaluation: bool = False
    evaluation_csv_filename: str = "evaluation_data.csv"
    evaluation_metrics: List[str] = field(default_factory=lambda: [
        "faithfulness", "answer_relevancy", "context_precision", "context_recall"
    ])

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
            "agent_type": self.agent_type.value,
            "model_provider": self.model_provider.value,
            "memory_type": self.memory_type.value,
            "short_term_memory": self.short_term_memory,
            "long_term_memory": self.long_term_memory,
            "formatter": self.formatter.value,
            "formatter_name": self.formatter_name,
            "enable_skills": self.enable_skills,
            "skills": self.skills,
            "enable_knowledge": self.enable_knowledge,
            "knowledge_config": self.knowledge_config,
            "enable_rag": self.enable_rag,
            "rag_config": self.rag_config,
            "enable_pipeline": self.enable_pipeline,
            "pipeline_config": self.pipeline_config,
            "enable_streaming": self.enable_streaming,
            "enable_thinking": self.enable_thinking,
            "parallel_tool_calls": self.parallel_tool_calls,
            "author": self.author,
            "email": self.email,
            "generate_tests": self.generate_tests,
            "generate_evaluation": self.generate_evaluation,
            "evaluator_type": self.evaluator_type,
            "enable_openjudge": self.enable_openjudge,
            "openjudge_graders": self.openjudge_graders,
            "initial_benchmark_tasks": self.initial_benchmark_tasks,
        }
