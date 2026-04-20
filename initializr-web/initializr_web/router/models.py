"""
Model providers listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import ModelsResponse, ModelProviderInfo, ModelInfo
from initializr_core.metadata.models import ModelProvider

router = APIRouter(tags=["models"])

# Default NPU/PPU models configuration
DEFAULT_NPU_MODELS = [
    # LLM models
    ModelInfo(id="deepseek-qwen-32b-NPU", name="deepseek-qwen-32b-NPU", url="http://203.3.112.178:10080/v1/chat/completions"),
    ModelInfo(id="Qwen3-32B-NPU", name="Qwen3-32B-NPU", url="http://203.3.112.179:10864/v1/chat/completions"),
    ModelInfo(id="Qwen2.5-72B-NPU", name="Qwen2.5-72B-NPU", url="http://203.3.112.179:10081/v1/chat/completions"),
    ModelInfo(id="Qwen3-235B-A22B-PPU", name="Qwen3-235B-A22B-PPU", url="http://203.1.244.82:9001/v1/chat/completions"),
    ModelInfo(id="Qwen3-32B-PPU", name="Qwen3-32B-PPU", url="http://203.1.244.82:9002/v1/chat/completions"),
    ModelInfo(id="Qwen2.5-72B-PPU", name="Qwen2.5-72B-PPU", url="http://203.1.244.82:9003/v1/chat/completions"),
    # Embedding models
    ModelInfo(id="bge-large-zh-v1.5", name="bge-large-zh-v1.5", url="http://203.1.244.82:9005/v1/embeddings", is_embedding=True),
]


@router.get("/api/v1/models", response_model=ModelsResponse)
async def list_models() -> ModelsResponse:
    """
    List available model providers and models.

    Returns provider IDs, display names, and available models.
    """
    return ModelsResponse(
        providers=[
            ModelProviderInfo(
                id=provider.value,
                name=provider.value.replace("_", " ").title(),
                models=DEFAULT_NPU_MODELS if provider == ModelProvider.NPU else [],
            )
            for provider in ModelProvider
        ]
    )
