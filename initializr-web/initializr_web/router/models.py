"""
Model providers listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import ModelsResponse
from initializr_core.metadata.models import ModelProvider

router = APIRouter(tags=["models"])


@router.get("/api/v1/models", response_model=ModelsResponse)
async def list_models() -> ModelsResponse:
    """
    List available model providers.

    Returns provider IDs and display names.
    """
    return ModelsResponse(
        providers=[
            {
                "id": provider.value,
                "name": provider.value.replace("_", " ").title(),
            }
            for provider in ModelProvider
        ]
    )
