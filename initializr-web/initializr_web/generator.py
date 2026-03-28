"""
Project generation utilities for web service.
"""

import os
import zipfile
from pathlib import Path
from typing import Optional
import uuid

from initializr_core.generator.engine import ProjectGenerator
from initializr_web.converter import project_request_to_metadata
from initializr_web.models import ProjectRequest


class ProjectGenerationError(Exception):
    """Exception raised when project generation fails."""
    pass


def generate_project(
    request: ProjectRequest,
    output_dir: Path,
) -> str:
    """
    Generate a project from request.

    Args:
        request: Project request
        output_dir: Directory to store generated projects

    Returns:
        Project ID

    Raises:
        ProjectGenerationError: If generation fails
    """
    try:
        # Convert request to metadata
        metadata = project_request_to_metadata(request)

        # Generate unique project ID
        project_id = f"{request.name}_{uuid.uuid4().hex[:8]}"

        # Generate project using ProjectGenerator
        generator = ProjectGenerator(output_dir=str(output_dir))
        generated = generator.generate(metadata)

        # Create zip file
        zip_path = output_dir / f"{project_id}.zip"
        generated.create_zip()

        # Rename zip to use project_id
        if generated.zip_path != zip_path:
            generated.zip_path.rename(zip_path)

        return project_id

    except Exception as e:
        raise ProjectGenerationError(f"Failed to generate project: {str(e)}") from e


def create_zip(source_dir: Path, output_zip: Path) -> None:
    """
    Create a zip file from a directory.

    Args:
        source_dir: Source directory to zip
        output_zip: Output zip file path
    """
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in source_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(source_dir)
                zipf.write(file, arcname)


def cleanup_old_projects(output_dir: Path, max_age_seconds: int = 3600) -> int:
    """
    Remove projects older than max_age_seconds.

    Args:
        output_dir: Directory containing projects
        max_age_seconds: Maximum age in seconds (default: 1 hour)

    Returns:
        Number of projects cleaned up
    """
    import time
    import shutil

    now = time.time()
    cleaned = 0

    for item in output_dir.iterdir():
        if item.is_dir() or (item.is_file() and item.suffix == ".zip"):
            if now - item.stat().st_mtime > max_age_seconds:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
                cleaned += 1

    return cleaned
