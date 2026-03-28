"""
Integration tests for the web service.
"""

import pytest
import tempfile
import zipfile
from pathlib import Path
from fastapi.testclient import TestClient
from initializr_web.api import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_full_project_generation_flow(client):
    """Test complete flow: health -> templates -> generate -> download"""
    # 1. Check health
    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "healthy"

    # 2. Get templates
    templates_response = client.get("/api/v1/templates")
    assert templates_response.status_code == 200
    templates = templates_response.json()["templates"]
    assert len(templates) > 0

    # 3. Get models
    models_response = client.get("/api/v1/models")
    assert models_response.status_code == 200
    providers = models_response.json()["providers"]
    assert len(providers) > 0

    # 4. Get extensions
    extensions_response = client.get("/api/v1/extensions")
    assert extensions_response.status_code == 200
    extensions = extensions_response.json()
    assert "memory" in extensions
    assert "tools" in extensions

    # 5. Generate project
    request_data = {
        "name": "integration-test-agent",
        "description": "Integration test agent",
        "layout": "standard",
        "agent_type": "basic",
        "model_provider": "openai",
        "enable_tools": True,
        "tools": ["execute_python_code"],
    }

    gen_response = client.post("/api/v1/projects/generate", json=request_data)
    assert gen_response.status_code == 200
    gen_data = gen_response.json()
    assert gen_data["success"] is True
    assert "project_id" in gen_data
    assert "download_url" in gen_data

    project_id = gen_data["project_id"]

    # 6. Download project
    download_response = client.get(f"/api/v1/projects/download/{project_id}")
    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/zip"

    # 7. Verify zip contents
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(download_response.content)
        tmp_path = Path(tmp.name)

    with zipfile.ZipFile(tmp_path, 'r') as zf:
        files = zf.namelist()
        # Should contain project structure
        assert any("integration_test_agent" in f for f in files)

    tmp_path.unlink()


def test_error_handling_invalid_project(client):
    """Test error handling for invalid project configuration."""
    request_data = {
        "name": "",  # Invalid: empty name
        "layout": "invalid",  # Invalid: wrong layout
    }

    response = client.post("/api/v1/projects/generate", json=request_data)
    assert response.status_code == 422  # Validation error
