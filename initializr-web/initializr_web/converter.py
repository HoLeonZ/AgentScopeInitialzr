"""
Convert ProjectRequest to AgentScopeMetadata.
"""

from initializr_web.models import ProjectRequest
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ModelProvider,
    ProjectLayout,
    ToolConfig,
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

    return AgentScopeMetadata(
        name=request.name,
        description=request.description,
        author=request.author,
        package_name=request.name.replace("-", "_"),
        layout=ProjectLayout(request.layout),
        agent_type=AgentType(request.agent_type),
        model_provider=ModelProvider(request.model_provider),
        tools=tool_configs,
        python_version=request.python_version,
    )
