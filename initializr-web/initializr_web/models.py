"""
Pydantic models for API request/response validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    """Request model for project generation."""

    # Basic settings
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: str = Field(default="", max_length=500, description="Project description")
    author: str = Field(default="", max_length=100, description="Author name")

    # Project structure
    agent_type: str = Field(default="basic", description="Agent type")
    python_version: str = Field(
        default="3.14",
        pattern=r"^3\.14$",
        description="Python version (only 3.14 supported)"
    )

    # Model configuration
    model_provider: str = Field(default="dashscope", description="Model provider")
    model_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Model configuration parameters"
    )

    # Extension points
    enable_memory: bool = Field(default=False, description="Enable memory")
    short_term_memory: Optional[str] = Field(default=None, description="Short-term memory type")
    long_term_memory: Optional[str] = Field(default=None, description="Long-term memory type")

    enable_tools: bool = Field(default=False, description="Enable tools")
    tools: List[str] = Field(default_factory=list, description="Enabled tools")

    enable_skills: bool = Field(default=False, description="Enable skills")
    skills: List[str] = Field(default_factory=list, description="Enabled skills")

    enable_hooks: bool = Field(default=False, description="Enable hooks")
    hooks: List[str] = Field(default_factory=list, description="Enabled hooks")

    enable_formatter: bool = Field(default=False, description="Enable formatter")
    formatter: Optional[str] = Field(default=None, description="Formatter type")

    enable_rag: bool = Field(default=False, description="Enable RAG")
    rag_config: Optional[Dict[str, Any]] = Field(default=None, description="RAG configuration")

    enable_pipeline: bool = Field(default=False, description="Enable pipeline")
    pipeline_config: Optional[Dict[str, Any]] = Field(default=None, description="Pipeline configuration")

    # Testing & evaluation
    generate_tests: bool = Field(default=False, description="Generate test module")
    generate_evaluation: bool = Field(default=False, description="Generate evaluation module")
    evaluator_type: str = Field(default="general", description="Evaluator type")
    enable_openjudge: bool = Field(default=False, description="Enable OpenJudge integration")
    openjudge_graders: List[str] = Field(default_factory=list, description="OpenJudge graders")
    initial_benchmark_tasks: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Number of initial benchmark tasks"
    )

    model_config = {"json_schema_extra": {"examples": [{
        "name": "my-agent",
        "description": "My custom agent",
        "agent_type": "multi-agent",
        "model_provider": "dashscope",
        "model_config": {"model": "qwen-max", "temperature": 0.7},
        "enable_memory": False,
        "short_term_memory": None,
        "long_term_memory": None,
    }]}}


class ProjectResponse(BaseModel):
    """Response model for project generation."""

    success: bool = Field(..., description="Whether generation succeeded")
    message: str = Field(..., description="Response message")
    download_url: Optional[str] = Field(None, description="Download URL")
    project_id: Optional[str] = Field(None, description="Project ID")


class TemplateInfo(BaseModel):
    """Information about a template."""

    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")


class TemplatesResponse(BaseModel):
    """Response model for templates listing."""

    templates: List[TemplateInfo] = Field(..., description="Available templates")


class ModelProviderInfo(BaseModel):
    """Information about a model provider."""

    id: str = Field(..., description="Provider ID")
    name: str = Field(..., description="Provider name")


class ModelsResponse(BaseModel):
    """Response model for models listing."""

    providers: List[ModelProviderInfo] = Field(..., description="Available providers")


class ExtensionsResponse(BaseModel):
    """Response model for extensions listing."""

    memory: Dict[str, List[str]] = Field(..., description="Memory options")
    tools: Dict[str, str] = Field(..., description="Tools descriptions")
    formatters: List[str] = Field(..., description="Available formatters")
    evaluators: List[str] = Field(..., description="Available evaluators")
    openjudge_graders: List[str] = Field(..., description="Available OpenJudge graders")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response with system metrics."""

    system: Dict[str, float] = Field(..., description="System metrics")
    projects: Dict[str, Any] = Field(..., description="Project statistics")


# Skill Management Models

class SkillUploadResponse(BaseModel):
    """Response model for skill upload."""

    success: bool = Field(..., description="Whether upload succeeded")
    message: str = Field(..., description="Response message")
    skill: Optional[Dict[str, Any]] = Field(None, description="Skill metadata")


class SkillListResponse(BaseModel):
    """Response model for skills listing."""

    skills: List[Dict[str, Any]] = Field(..., description="List of skills")
    total: int = Field(..., description="Total number of skills")


class SkillDetailResponse(BaseModel):
    """Response model for skill details."""

    skill: Dict[str, Any] = Field(..., description="Skill metadata")


class SkillDeleteResponse(BaseModel):
    """Response model for skill deletion."""

    success: bool = Field(..., description="Whether deletion succeeded")
    message: str = Field(..., description="Response message")
