"""
Template registry for AgentScope Initializr.

Manages available project templates and their configurations.
"""

from typing import Dict, List, Optional
from initializr_core.metadata.models import (
    AgentType,
    Dependency,
    ToolConfig,
)


class Template:
    """Represents a project template."""

    def __init__(
        self,
        template_id: str,
        name: str,
        description: str,
        structure_path: str,
        default_dependencies: List[Dependency],
        default_tools: List[ToolConfig],
    ):
        self.template_id = template_id
        self.name = name
        self.description = description
        self.structure_path = structure_path
        self.default_dependencies = default_dependencies
        self.default_tools = default_tools


class TemplateRegistry:
    """
    Registry for available project templates.

    This class manages all available templates and provides
    methods to query and retrieve them.
    """

    def __init__(self):
        """Initialize the template registry."""
        self._templates: Dict[str, Template] = {}
        self._register_default_templates()

    def _register_default_templates(self):
        """Register default templates."""
        # Basic Agent Template (src/ layout)
        self.register(
            Template(
                template_id="basic",
                name="Basic ReAct Agent",
                description="基础 ReAct 智能体，支持对话和工具调用 (src/ layout)",
                structure_path="basic-agent-src",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                ],
                default_tools=[
                    ToolConfig(name="execute_python_code", enabled=True),
                    ToolConfig(name="execute_shell_command", enabled=True),
                ],
            )
        )

        # Multi-Agent Template (src/ layout)
        self.register(
            Template(
                template_id="multi-agent",
                name="Multi-Agent System",
                description="多智能体协作系统，支持智能体间通信和任务分配 (src/ layout)",
                structure_path="multi-agent-src",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                ],
                default_tools=[
                    ToolConfig(name="execute_python_code", enabled=True),
                    ToolConfig(name="execute_shell_command", enabled=True),
                ],
            )
        )

        # Research Agent Template (src/ layout)
        self.register(
            Template(
                template_id="research",
                name="Research Agent",
                description="深度研究智能体，支持网络搜索和信息聚合 (src/ layout)",
                structure_path="research-agent-src",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                    Dependency("httpx"),
                ],
                default_tools=[
                    ToolConfig(name="web_search", enabled=True, config={"provider": "tavily"}),
                    ToolConfig(name="execute_python_code", enabled=True),
                ],
            )
        )

        # Browser Agent Template (src/ layout)
        self.register(
            Template(
                template_id="browser",
                name="Browser Automation Agent",
                description="浏览器自动化智能体，支持网页交互和数据抓取 (src/ layout)",
                structure_path="browser-agent-src",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                    Dependency("playwright"),
                ],
                default_tools=[
                    ToolConfig(name="browser_navigate", enabled=True),
                    ToolConfig(name="browser_click", enabled=True),
                    ToolConfig(name="browser_type", enabled=True),
                    ToolConfig(name="browser_screenshot", enabled=True),
                ],
            )
        )

        # Legacy templates for backward compatibility (lightweight layout)
        self.register(
            Template(
                template_id="basic-legacy",
                name="Basic ReAct Agent (Legacy)",
                description="基础 ReAct 智能体，支持对话和工具调用 (lightweight layout)",
                structure_path="basic-agent",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                ],
                default_tools=[
                    ToolConfig(name="execute_python_code", enabled=True),
                    ToolConfig(name="execute_shell_command", enabled=True),
                ],
            )
        )

        self.register(
            Template(
                template_id="multi-agent-legacy",
                name="Multi-Agent System (Legacy)",
                description="多智能体协作系统，支持智能体间通信和任务分配 (lightweight layout)",
                structure_path="multi-agent",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                ],
                default_tools=[
                    ToolConfig(name="execute_python_code", enabled=True),
                    ToolConfig(name="execute_shell_command", enabled=True),
                ],
            )
        )

        self.register(
            Template(
                template_id="research-legacy",
                name="Research Agent (Legacy)",
                description="深度研究智能体，支持网络搜索和信息聚合 (lightweight layout)",
                structure_path="research-agent",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                    Dependency("httpx"),
                ],
                default_tools=[
                    ToolConfig(name="web_search", enabled=True, config={"provider": "tavily"}),
                    ToolConfig(name="execute_python_code", enabled=True),
                ],
            )
        )

        self.register(
            Template(
                template_id="browser-legacy",
                name="Browser Automation Agent (Legacy)",
                description="浏览器自动化智能体，支持网页交互和数据抓取 (lightweight layout)",
                structure_path="browser-agent",
                default_dependencies=[
                    Dependency("agentscope"),
                    Dependency("python-dotenv"),
                    Dependency("playwright"),
                ],
                default_tools=[
                    ToolConfig(name="browser_navigate", enabled=True),
                    ToolConfig(name="browser_click", enabled=True),
                    ToolConfig(name="browser_type", enabled=True),
                    ToolConfig(name="browser_screenshot", enabled=True),
                ],
            )
        )

    def register(self, template: Template):
        """
        Register a new template.

        Args:
            template: The template to register
        """
        self._templates[template.template_id] = template

    def get(self, agent_type: AgentType) -> Template:
        """
        Get template by agent type.

        Args:
            agent_type: The type of agent

        Returns:
            The matching template

        Raises:
            KeyError: If template not found
        """
        template_id = agent_type.value
        if template_id not in self._templates:
            raise KeyError(f"Template not found: {template_id}")
        return self._templates[template_id]

    def list_templates(self) -> List[Template]:
        """
        List all available templates.

        Returns:
            List of all templates
        """
        return list(self._templates.values())

    def get_template_ids(self) -> List[str]:
        """
        Get all template IDs.

        Returns:
            List of template IDs
        """
        return list(self._templates.keys())
