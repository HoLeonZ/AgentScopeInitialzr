"""
Health check endpoints.
"""

import os
from fastapi import APIRouter
from initializr_web.models import HealthResponse, DetailedHealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.

    Returns service status and version.
    """
    return HealthResponse(
        status="healthy",
        service="AgentScope Initializr",
        version="0.2.0",
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check() -> DetailedHealthResponse:
    """
    Detailed health check with system metrics.

    Returns CPU, memory, and disk usage along with project statistics.
    """
    try:
        import psutil

        system_metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
        }
    except ImportError:
        # psutil not available, return mock data
        system_metrics = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "disk_usage": 0.0,
        }

    projects_stats = {
        "total_generated": 0,  # TODO: Implement tracking
        "storage_used": 0,
    }

    return DetailedHealthResponse(
        status="healthy",
        service="AgentScope Initializr",
        version="0.2.0",
        system=system_metrics,
        projects=projects_stats,
    )
