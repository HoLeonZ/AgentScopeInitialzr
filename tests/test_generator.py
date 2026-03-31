"""Tests for project generator."""

import pytest
import tempfile
from pathlib import Path
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ToolConfig,
)
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
        pkg_dir = project.path / "src" / "test_agent"
        assert pkg_dir.exists()

        # Check main.py location (src layout)
        assert (pkg_dir / "main.py").exists()

        # Check standard files
        assert (project.path / "requirements.txt").exists()
        assert (project.path / ".env.example").exists()
        assert (project.path / "README.md").exists()
        assert (project.path / "pyproject.toml").exists()

        # Check that .gitignore is NOT generated
        assert not (project.path / ".gitignore").exists()


def test_project_structure_with_skills_and_tools():
    """Test that skills and tools directories are always created."""
    metadata = AgentScopeMetadata(
        name="structure-test",
        description="Test directory structure",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        pkg_dir = project.path / "src" / "structure_test"

        # Check all required directories exist
        assert (pkg_dir / "agents").exists()
        assert (pkg_dir / "agents" / "__init__.py").exists()

        # Skills directory should always exist
        assert (pkg_dir / "skills").exists()
        assert (pkg_dir / "skills" / "__init__.py").exists()
        assert (pkg_dir / "skills" / "base_skills.py").exists()

        # Tools directory should always exist
        assert (pkg_dir / "tools").exists()
        assert (pkg_dir / "tools" / "__init__.py").exists()
        assert (pkg_dir / "tools" / "custom_tools.py").exists()

        # Utils directory should always exist
        assert (pkg_dir / "utils").exists()
        assert (pkg_dir / "utils" / "__init__.py").exists()
        assert (pkg_dir / "utils" / "helpers.py").exists()

        # Prompts and config
        assert (pkg_dir / "prompts").exists()
        assert (pkg_dir / "config").exists()


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
        pkg_dir = project.path / "src" / "multi_agent_test"
        assert pkg_dir.exists()


def test_agent_type_display_names():
    """Test that agent type display names are correct."""
    metadata = AgentScopeMetadata(
        name="display-test",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        # Read README and check display name
        readme_path = project.path / "README.md"
        readme_content = readme_path.read_text()

        # Should show "Basic Agent" not "basic"
        assert "Basic Agent" in readme_content
        assert "basic react agent" not in readme_content.lower()


def test_tools_are_registered():
    """Test that enabled tools are actually registered in code."""
    metadata = AgentScopeMetadata(
        name="tools-test",
        agent_type=AgentType.BASIC,
        tools=[
            ToolConfig(name="execute_python_code"),
            ToolConfig(name="web_search"),
        ],
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        # Check generated config
        config_path = project.path / "src" / "tools_test" / "config" / "__init__.py"
        config_content = config_path.read_text()

        # Tools should be imported
        assert "from agentscope.tools import execute_python_code" in config_content
        assert "from agentscope.tools import web_search_tavily" in config_content

        # Tools should be registered (not commented out)
        assert "toolkit.register(execute_python_code)" in config_content
        assert "toolkit.register(web_search_tavily)" in config_content


def test_skills_files_generation():
    """Test that skills files are generated when enabled."""
    metadata = AgentScopeMetadata(
        name="skills-test",
        agent_type=AgentType.BASIC,
        enable_skills=True,
        skills=["coding", "writing"],
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        skills_dir = project.path / "src" / "skills_test" / "skills"

        # Check base skills exist
        assert (skills_dir / "base_skills.py").exists()

        # Check custom skill files exist
        assert (skills_dir / "coding_skill.py").exists()
        assert (skills_dir / "writing_skill.py").exists()

        # Check skills __init__.py exports skills
        skills_init = (skills_dir / "__init__.py").read_text()
        assert "conversational_response" in skills_init
        assert "coding_execute" in skills_init
        assert "writing_execute" in skills_init


def test_project_zip_creation():
    """Test creating a ZIP file of the project."""
    metadata = AgentScopeMetadata(name="zip-test")

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)
        zip_path = project.create_zip()

        assert Path(zip_path).exists()
        assert zip_path.endswith(".zip")


def test_scripts_are_executable():
    """Test that generated scripts have executable permissions."""
    metadata = AgentScopeMetadata(
        name="scripts-test",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        scripts_dir = project.path / "scripts"

        # Check script files exist
        assert (scripts_dir / "setup.sh").exists()
        assert (scripts_dir / "deploy.sh").exists()
        assert (scripts_dir / "run.sh").exists()

        # Check scripts have executable permission
        import stat
        setup_mode = (scripts_dir / "setup.sh").stat().st_mode
        assert setup_mode & stat.S_IEXEC

        deploy_mode = (scripts_dir / "deploy.sh").stat().st_mode
        assert deploy_mode & stat.S_IEXEC

        run_mode = (scripts_dir / "run.sh").stat().st_mode
        assert run_mode & stat.S_IEXEC


def test_pyproject_has_entry_point():
    """Test that pyproject.toml has CLI entry point configured."""
    metadata = AgentScopeMetadata(
        name="entry-test",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        pyproject_path = project.path / "pyproject.toml"
        pyproject_content = pyproject_path.read_text()

        # Check for entry point (package name uses underscores)
        assert '[project.scripts]' in pyproject_content
        assert 'entry_test = "entry_test.main:run_cli"' in pyproject_content


def test_main_py_has_logging_and_commands():
    """Test that main.py includes logging and CLI commands."""
    metadata = AgentScopeMetadata(
        name="main-test",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        main_path = project.path / "src" / "main_test" / "main.py"
        main_content = main_path.read_text()

        # Check for logging
        assert "import logging" in main_content
        assert "setup_logging" in main_content
        assert "cleanup_old_logs" in main_content

        # Check for commands (using single quotes)
        assert "def run_cli" in main_content
        assert "'help'" in main_content or '"help"' in main_content
        assert "'stats'" in main_content or '"stats"' in main_content
        assert "'logs'" in main_content or '"logs"' in main_content

        # Check for error handling
        assert "except KeyboardInterrupt" in main_content
        assert "logger.error" in main_content


def test_unified_logging_module():
    """Test that unified logging module is generated."""
    metadata = AgentScopeMetadata(
        name="logging-test",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        # Check logging module exists
        logging_path = project.path / "src" / "logging_test" / "utils" / "logging.py"
        assert logging_path.exists()

        logging_content = logging_path.read_text()

        # Check for key logging features
        assert "class LoggerConfig" in logging_content
        assert "def setup_logging" in logging_content
        assert "RotatingFileHandler" in logging_content
        assert "TimedRotatingFileHandler" in logging_content
        assert "def cleanup_old_logs" in logging_content
        assert "class ColoredFormatter" in logging_content

        # Check for configuration options
        assert "LOG_FILE_MAX_BYTES" in logging_content
        assert "LOG_FILE_BACKUP_COUNT" in logging_content
        assert "LOG_RETENTION_DAYS" in logging_content


def test_env_example_has_logging_config():
    """Test that .env.example includes logging configuration."""
    metadata = AgentScopeMetadata(
        name="env-test",
        agent_type=AgentType.BASIC,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        generator = ProjectGenerator(output_dir=tmpdir)
        project = generator.generate(metadata)

        env_path = project.path / ".env.example"
        env_content = env_path.read_text()

        # Check for logging configuration
        assert "LOG_LEVEL" in env_content
        assert "LOG_TO_FILE" in env_content
        assert "LOG_TO_CONSOLE" in env_content
        assert "LOG_FILE_MAX_BYTES" in env_content
        assert "LOG_FILE_BACKUP_COUNT" in env_content
        assert "LOG_RETENTION_DAYS" in env_content

