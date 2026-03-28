"""Tests for project generator."""

import pytest
import tempfile
from pathlib import Path
from initializr_core.metadata.models import AgentScopeMetadata, AgentType
from initializr_core.generator.engine import ProjectGenerator


def test_generate_basic_project():
    """Test generating a basic project."""
    metadata = AgentScopeMetadata(
        name="test-agent",
        description="Test agent for generation",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        # Check project was created
        assert project.path.exists()
        assert (project.path / "test_agent").exists()
        assert (project.path / "main.py").exists()
        assert (project.path / "requirements.txt").exists()
        assert (project.path / ".env.example").exists()
        assert (project.path / "README.md").exists()


def test_generate_multi_agent_project():
    """Test generating a multi-agent project."""
    metadata = AgentScopeMetadata(
        name="multi-agent-test",
        agent_type=AgentType.MULTI_AGENT,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        # Check project structure
        assert project.path.exists()
        assert (project.path / "multi_agent_test").exists()


def test_project_zip_creation():
    """Test creating a ZIP file of the project."""
    metadata = AgentScopeMetadata(name="zip-test")

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)
        zip_path = project.create_zip()

        assert Path(zip_path).exists()
        assert zip_path.endswith(".zip")
