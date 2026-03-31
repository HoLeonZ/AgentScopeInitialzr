"""
API routers package.
"""

from initializr_web.router.health import router as health_router
from initializr_web.router.templates import router as templates_router
from initializr_web.router.models import router as models_router
from initializr_web.router.extensions import router as extensions_router
from initializr_web.router.projects import router as projects_router
from initializr_web.router.skills import router as skills_router

__all__ = [
    "health_router",
    "templates_router",
    "models_router",
    "extensions_router",
    "projects_router",
    "skills_router",
]
