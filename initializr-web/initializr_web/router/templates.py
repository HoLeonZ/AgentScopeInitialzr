"""
Templates listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import TemplatesResponse
from initializr_core.metadata.templates import TemplateRegistry

router = APIRouter(tags=["templates"])

template_registry = TemplateRegistry()


@router.get("/api/v1/templates", response_model=TemplatesResponse)
async def list_templates() -> TemplatesResponse:
    """
    List all available project templates.

    Returns template IDs, names, and descriptions.
    """
    templates = template_registry.list_templates()

    return TemplatesResponse(
        templates=[
            {
                "id": t.template_id,
                "name": t.name,
                "description": t.description,
            }
            for t in templates
        ]
    )
