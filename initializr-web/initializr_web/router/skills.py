"""
Skills router for skill management API.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
import tempfile
import os

from initializr_web.skill_manager import SkillManager
from initializr_web.models import (
    SkillUploadResponse,
    SkillListResponse,
    SkillDetailResponse,
    SkillDeleteResponse,
)

# Create router
router = APIRouter(prefix="/api/skills", tags=["skills"])

# Initialize skill manager
skill_manager = SkillManager()


@router.post("/upload", response_model=SkillUploadResponse)
async def upload_skill(
    file: UploadFile = File(..., description="Skill package ZIP file")
):
    """
    Upload a skill package.

    The ZIP file should contain a skill following the AgentScope standard structure:
    - Must contain a SKILL.md file with YAML frontmatter
    - Can optionally include scripts/, resources/, examples/ directories

    Tags:
        Skills: Management
    """
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed")

    # Save uploaded file to temp location
    temp_fd, temp_path = tempfile.mkstemp(suffix='.zip')
    try:
        with os.fdopen(temp_fd, 'wb') as temp_file:
            content = await file.read()
            temp_file.write(content)

        # Upload skill
        success, message, metadata = skill_manager.upload_skill(temp_path)

        if success:
            return SkillUploadResponse(
                success=True,
                message=message,
                skill=metadata.to_dict() if metadata else None
            )
        else:
            raise HTTPException(status_code=400, detail=message)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@router.get("/", response_model=SkillListResponse)
async def list_skills(
    search: Optional[str] = Query(None, description="Search query for name, description, or tags"),
    tag: Optional[str] = Query(None, description="Filter by tag")
):
    """
    List all available skills.

    Can optionally search or filter by tag.

    Tags:
        Skills: Management
    """
    try:
        if search:
            skills = skill_manager.search_skills(search)
        elif tag:
            skills = [
                skill for skill in skill_manager.list_skills()
                if tag in skill.tags
            ]
        else:
            skills = skill_manager.list_skills()

        return SkillListResponse(
            skills=[skill.to_dict() for skill in skills],
            total=len(skills)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing skills: {str(e)}")


@router.get("/{skill_id}", response_model=SkillDetailResponse)
async def get_skill(skill_id: str):
    """
    Get details of a specific skill.

    Tags:
        Skills: Management
    """
    skill = skill_manager.get_skill(skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return SkillDetailResponse(skill=skill.to_dict())


@router.delete("/{skill_id}", response_model=SkillDeleteResponse)
async def delete_skill(skill_id: str):
    """
    Delete a skill package.

    Tags:
        Skills: Management
    """
    success, message = skill_manager.delete_skill(skill_id)

    if not success:
        raise HTTPException(status_code=404, detail=message)

    return SkillDeleteResponse(
        success=True,
        message=message
    )


@router.get("/tags/list")
async def list_tags():
    """
    List all available tags across all skills.

    Tags:
        Skills: Management
    """
    try:
        skills = skill_manager.list_skills()
        all_tags = set()

        for skill in skills:
            all_tags.update(skill.tags)

        return {"tags": sorted(list(all_tags))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tags: {str(e)}")
