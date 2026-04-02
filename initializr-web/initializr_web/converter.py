"""
Convert ProjectRequest to AgentScopeMetadata.
"""

from initializr_web.models import ProjectRequest
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ModelProvider,
    ToolConfig,
    HookConfig,
    MiddlewareConfig,
    MemoryType,
    FormatterType,
)


def project_request_to_metadata(request: ProjectRequest) -> AgentScopeMetadata:
    """
    Convert ProjectRequest to AgentScopeMetadata.

    Maps the web request format to the existing metadata structure.
    """
    # Convert tools list to ToolConfig objects
    tool_configs = []
    for tool_name in request.tools:
        tool_configs.append(ToolConfig(name=tool_name, enabled=True))

    # Convert hooks list to HookConfig objects
    hook_configs = []
    for hook_type in request.hooks:
        hook_configs.append(HookConfig(hook_type=hook_type, enabled=True))

    # Determine memory type
    memory_type = MemoryType.IN_MEMORY
    if request.long_term_memory and request.long_term_memory != "none":
        memory_type = MemoryType.LONG_TERM

    # Determine formatter
    formatter_type = FormatterType.CHAT
    formatter_name = None
    if request.formatter:
        formatter_name = request.formatter
        if "Chat" in request.formatter:
            formatter_type = FormatterType.CHAT
        elif "MultiAgent" in request.formatter:
            formatter_type = FormatterType.MULTI_AGENT

    # Convert middleware (add defaults based on extensions)
    middleware_configs = []
    if request.enable_rag:
        middleware_configs.append(
            MiddlewareConfig(
                name="rag",
                enabled=True,
                config=request.rag_config or {}
            )
        )
    if request.enable_pipeline:
        middleware_configs.append(
            MiddlewareConfig(
                name="pipeline",
                enabled=True,
                config=request.pipeline_config or {}
            )
        )

    return AgentScopeMetadata(
        # Basic info
        name=request.name,
        description=request.description,
        author=request.author,
        package_name=request.name.replace("-", "_"),
        version="0.1.0",
        python_version=request.python_version,

        # Agent configuration
        agent_type=AgentType(request.agent_type),
        model_provider=ModelProvider(request.model_provider),

        # Tools
        tools=tool_configs,

        # Memory configuration
        memory_type=memory_type,
        short_term_memory=request.short_term_memory,
        long_term_memory=request.long_term_memory,

        # Hooks
        hooks=hook_configs,

        # Middleware
        middleware=middleware_configs,

        # Formatter
        formatter=formatter_type,
        formatter_name=formatter_name,

        # Skills
        enable_skills=request.enable_skills,
        skills=request.skills or [],

        # Knowledge Base
        enable_knowledge=request.enable_knowledge,
        knowledge_config=request.knowledge_config or {},

        # RAG
        enable_rag=request.enable_rag,
        rag_config=request.rag_config or {},

        # Pipeline
        enable_pipeline=request.enable_pipeline,
        pipeline_config=request.pipeline_config or {},

        # Additional settings
        enable_streaming=True,
        enable_thinking=False,
        parallel_tool_calls=True,

        # Testing & Evaluation
        generate_tests=request.generate_tests,
        generate_evaluation=request.generate_evaluation,
        evaluator_type=request.evaluator_type,
        enable_openjudge=request.enable_openjudge,
        openjudge_graders=request.openjudge_graders or [],
        initial_benchmark_tasks=request.initial_benchmark_tasks,
    )
