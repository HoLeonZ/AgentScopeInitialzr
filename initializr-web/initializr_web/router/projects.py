"""
Project generation and download endpoints.
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from initializr_web.models import ProjectRequest, ProjectResponse
from initializr_web.generator import generate_project, ProjectGenerationError

router = APIRouter(tags=["projects"])

# Output directory for generated projects
output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
output_dir.mkdir(parents=True, exist_ok=True)


@router.post("/api/v1/projects/generate", response_model=ProjectResponse)
async def generate_project_endpoint(
    request: ProjectRequest,
    background_tasks: BackgroundTasks,
) -> ProjectResponse:
    """
    Generate a new AgentScope project.

    Creates a project based on the provided configuration and
    returns a download URL for the generated project bundle.
    """
    try:
        project_id = generate_project(request, output_dir)

        # Schedule cleanup task
        background_tasks.add_task(cleanup_projects)

        return ProjectResponse(
            success=True,
            message="Project generated successfully",
            download_url=f"/api/v1/projects/download/{project_id}",
            project_id=project_id,
        )

    except ProjectGenerationError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/api/v1/projects/download/{project_id}")
async def download_project(project_id: str):
    """
    Download a generated project.

    Returns the project as a ZIP file.
    """
    zip_path = output_dir / f"{project_id}.zip"

    if not zip_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Project not found: {project_id}",
        )

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=f"{project_id}.zip",
    )


def cleanup_projects():
    """Background task to clean up old projects."""
    from initializr_web.generator import cleanup_old_projects
    cleanup_old_projects(output_dir)
