"""
End-to-end test for the complete web service workflow.
"""

import pytest
import tempfile
import zipfile
from pathlib import Path
import subprocess
import time


@pytest.fixture(scope="module")
def running_server():
    """Start the server for e2e testing."""
    # Start uvicorn in background
    proc = subprocess.Popen(
        ["uvicorn", "initializr_web.api:app", "--host", "localhost", "--port", "8766"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    time.sleep(3)

    yield "http://localhost:8766"

    # Cleanup
    proc.terminate()
    proc.wait()


def test_e2e_complete_workflow(running_server):
    """Test complete workflow from health check to project download."""
    import requests

    base_url = running_server

    # 1. Health check
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

    # 2. List templates
    response = requests.get(f"{base_url}/api/v1/templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert len(templates) >= 4  # basic, multi-agent, research, browser

    # 3. List models
    response = requests.get(f"{base_url}/api/v1/models")
    assert response.status_code == 200
    providers = response.json()["providers"]
    assert len(providers) > 0

    # 4. List extensions
    response = requests.get(f"{base_url}/api/v1/extensions")
    assert response.status_code == 200
    extensions = response.json()
    assert "memory" in extensions
    assert "tools" in extensions

    # 5. Generate a project
    project_request = {
        "name": "e2e-test-agent",
        "description": "End-to-end test agent",
        "author": "E2E Test",
        "layout": "standard",
        "agent_type": "multi-agent",
        "model_provider": "openai",
        "model_config": {"model": "gpt-4", "temperature": 0.7},
        "enable_memory": True,
        "short_term_memory": "in-memory",
        "long_term_memory": "mem0",
        "enable_tools": True,
        "tools": ["execute_python_code", "web_search"],
        "generate_tests": True,
    }

    response = requests.post(f"{base_url}/api/v1/projects/generate", json=project_request)
    assert response.status_code == 200
    gen_data = response.json()
    assert gen_data["success"] is True
    assert "project_id" in gen_data
    assert "download_url" in gen_data

    project_id = gen_data["project_id"]

    # 6. Download the project
    download_url = f"{base_url}{gen_data['download_url']}"
    response = requests.get(download_url)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

    # 7. Verify ZIP contents
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(response.content)
        tmp_path = Path(tmp.name)

    extracted_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(tmp_path, 'r') as zf:
        zf.extractall(extracted_dir)
        files = zf.namelist()

    # Verify expected files exist
    assert any("e2e_test_agent" in f for f in files)
    assert any("main.py" in f for f in files)
    assert any("agent" in f.lower() for f in files)

    # Cleanup
    tmp_path.unlink()
    import shutil
    shutil.rmtree(extracted_dir)

    print(f"✅ E2E test passed! Generated project: {project_id}")
