"""
Tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError
from initializr_web.models import (
    ProjectRequest,
    ProjectResponse,
    TemplateInfo,
    TemplatesResponse,
)


def test_project_request_valid():
    """Test valid ProjectRequest creation."""
    data = {
        "name": "test-agent",
        "description": "Test agent",
        "layout": "standard",
        "agent_type": "basic",
    }
    request = ProjectRequest(**data)
    assert request.name == "test-agent"
    assert request.layout == "standard"
    assert request.enable_memory is True  # Default value


def test_project_request_invalid_name_too_short():
    """Test ProjectRequest rejects empty name."""
    with pytest.raises(ValidationError) as exc_info:
        ProjectRequest(name="")
    assert "string_too_short" in str(exc_info.value).lower() or "min_length" in str(exc_info.value).lower()


def test_project_request_invalid_layout():
    """Test ProjectRequest rejects invalid layout."""
    with pytest.raises(ValidationError) as exc_info:
        ProjectRequest(name="test", layout="invalid")
    assert "pattern" in str(exc_info.value).lower() or "string" in str(exc_info.value).lower()


def test_project_request_benchmark_tasks_range():
    """Test ProjectRequest validates benchmark tasks range."""
    # Valid range
    request = ProjectRequest(name="test", initial_benchmark_tasks=50)
    assert request.initial_benchmark_tasks == 50

    # Out of range (too high)
    with pytest.raises(ValidationError):
        ProjectRequest(name="test", initial_benchmark_tasks=101)


def test_project_response():
    """Test ProjectResponse creation."""
    response = ProjectResponse(
        success=True,
        message="Generated successfully",
        download_url="/api/v1/projects/download/test_123",
        project_id="test_123",
    )
    assert response.success is True
    assert response.project_id == "test_123"


def test_templates_response():
    """Test TemplatesResponse creation."""
    templates = [
        TemplateInfo(id="basic", name="Basic Agent", description="Basic agent template"),
        TemplateInfo(id="multi-agent", name="Multi-Agent", description="Multi-agent system"),
    ]
    response = TemplatesResponse(templates=templates)
    assert len(response.templates) == 2
    assert response.templates[0].id == "basic"
