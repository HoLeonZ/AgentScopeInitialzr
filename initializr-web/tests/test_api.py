"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from initializr_web.api import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test basic health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AgentScope Initializr"
    assert "version" in data


def test_health_detailed(client):
    """Test detailed health check endpoint."""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "system" in data
    assert "cpu_percent" in data["system"]
    assert "memory_percent" in data["system"]
    assert "projects" in data


def test_list_templates(client):
    """Test templates listing endpoint."""
    response = client.get("/api/v1/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) > 0
    # Check for expected templates
    template_ids = [t["id"] for t in data["templates"]]
    assert "basic" in template_ids
    assert "multi-agent" in template_ids


def test_list_models(client):
    """Test model providers listing endpoint."""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert len(data["providers"]) > 0


def test_list_extensions(client):
    """Test extensions listing endpoint."""
    response = client.get("/api/v1/extensions")
    assert response.status_code == 200
    data = response.json()
    assert "memory" in data
    assert "short_term" in data["memory"]
    assert "long_term" in data["memory"]
    assert "tools" in data
    assert "formatters" in data
    assert "evaluators" in data
    assert "openjudge_graders" in data


def test_generate_project(client):
    """Test project generation endpoint."""
    request_data = {
        "name": "test-agent",
        "description": "Test agent",
        "layout": "standard",
        "agent_type": "basic",
        "model_provider": "openai",
        "enable_tools": True,
        "tools": ["execute_python_code"],
    }

    response = client.post("/api/v1/projects/generate", json=request_data)
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "download_url" in data
    assert "project_id" in data


def test_generate_project_invalid_layout(client):
    """Test project generation rejects invalid layout."""
    request_data = {
        "name": "test-agent",
        "layout": "invalid-layout",  # Invalid layout
        "agent_type": "basic",
    }

    response = client.post("/api/v1/projects/generate", json=request_data)
    assert response.status_code == 422  # Validation error

