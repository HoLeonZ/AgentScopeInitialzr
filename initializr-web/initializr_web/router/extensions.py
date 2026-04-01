"""
Extension point options listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import ExtensionsResponse

router = APIRouter(tags=["extensions"])


@router.get("/api/v1/extensions", response_model=ExtensionsResponse)
async def list_extensions() -> ExtensionsResponse:
    """
    List available extension point options.

    Returns memory types, tools, formatters, evaluators, and OpenJudge graders.
    """
    return ExtensionsResponse(
        memory={
            "short_term": ["oceanbase", "redis"],  # Only OceanBase and Redis for short-term
            "long_term": ["mem0", "oceanbase"],  # Only Mem0 and OceanBase for long-term
        },
        tools={
            "execute_python_code": "Execute Python code safely",
            "execute_shell_command": "Execute shell commands",
            "web_search": "Web search using Tavily API",
            "browser_navigate": "Browser navigation",
            "browser_click": "Browser click interaction",
            "browser_type": "Browser text input",
            "browser_screenshot": "Browser screenshot capture",
        },
        formatters=["DashScopeChatFormatter", "OpenAIChatFormatter"],
        evaluators=["general", "ray"],
        openjudge_graders=[
            "RelevanceGrader",
            "CorrectnessGrader",
            "HallucinationGrader",
            "SafetyGrader",
            "CodeQualityGrader",
        ],
    )
