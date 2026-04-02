"""
FastAPI application initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from initializr_web.router import (
    health_router,
    templates_router,
    models_router,
    extensions_router,
    projects_router,
    skills_router,
)

# Create FastAPI app
app = FastAPI(
    title="AgentScope Initializr",
    description="Web service for scaffolding AgentScope agent projects",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "ALLOW_ORIGINS",
        "http://localhost:5173,http://localhost:8080,http://localhost:8000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(templates_router)
app.include_router(models_router)
app.include_router(extensions_router)
app.include_router(projects_router)
app.include_router(skills_router)

# Get static directory path
STATIC_DIR = Path(__file__).parent / "static"

# Mount assets directory for JS, CSS, etc.
app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse(STATIC_DIR / "index.html")


# Catch-all route for SPA (Single Page Application)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Serve the SPA for all routes that don't match API endpoints.
    This enables client-side routing.
    """
    # Check if it's an API route (skip for API routes)
    if full_path.startswith(("api/", "docs", "redoc", "openapi.json")):
        return None
    
    # For all other routes, serve the SPA
    return FileResponse(STATIC_DIR / "index.html")
