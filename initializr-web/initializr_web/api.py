"""
FastAPI application initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AgentScope Initializr Web Service",
        "version": "0.2.0",
        "docs": "/docs",
    }
