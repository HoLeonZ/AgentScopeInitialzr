"""
Project generator engine for AgentScope Initializr.

Generates AgentScope projects based on metadata and templates.
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template

from initializr_core.metadata.models import AgentScopeMetadata
from initializr_core.metadata.templates import TemplateRegistry
from initializr_core.validator.validator import MetadataValidator
from initializr_core.generator.extensions import ExtensionGenerator


class GeneratedProject:
    """Represents a generated project."""

    def __init__(self, path: Path, metadata: AgentScopeMetadata):
        self.path = path
        self.metadata = metadata
        self.zip_path = path.parent / f"{metadata.name}.zip"

    def create_zip(self) -> str:
        """
        Create a ZIP file of the project.

        Returns:
            Path to the ZIP file
        """
        with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in self.path.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(self.path)
                    zipf.write(file, arcname)
        return str(self.zip_path)


class ProjectGenerator:
    """
    Project generator engine.

    This class handles the generation of AgentScope projects
    based on metadata and templates.
    """

    def __init__(self, output_dir: str = "/tmp/agentscope-initializr"):
        """
        Initialize the generator.

        Args:
            output_dir: Directory to store generated projects
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.template_registry = TemplateRegistry()
        self.extension_generator = ExtensionGenerator()
        self.validator = MetadataValidator()

    def generate(self, metadata: AgentScopeMetadata) -> GeneratedProject:
        """
        Generate a project based on metadata.

        Args:
            metadata: Project metadata

        Returns:
            GeneratedProject instance

        Raises:
            ValidationError: If metadata is invalid
        """
        # Step 1: Validate metadata
        self.validator.validate(metadata)

        # Step 2: Get template
        template = self.template_registry.get(metadata.agent_type)

        # Step 3: Create project directory
        project_path = self.output_dir / metadata.name
        if project_path.exists():
            shutil.rmtree(project_path)
        project_path.mkdir(parents=True)

        # Step 4: Generate project structure
        self._generate_project_structure(metadata, project_path)

        # Step 5: Generate configuration files
        self._generate_config_files(metadata, project_path)

        # Step 6: Generate source code
        self._generate_source_code(metadata, project_path, template)

        # Step 7: Generate README
        self._generate_readme(metadata, project_path)

        return GeneratedProject(project_path, metadata)

    def _generate_project_structure(
        self,
        metadata: AgentScopeMetadata,
        project_path: Path
    ):
        """Generate basic project directory structure."""
        # Standard src/ layout: src/project_name/
        src_dir = project_path / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        pkg_dir = src_dir / metadata.package_name
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories - following industry best practices
        (pkg_dir / "agents").mkdir(exist_ok=True)
        (pkg_dir / "skills").mkdir(exist_ok=True)
        (pkg_dir / "tools").mkdir(exist_ok=True)
        (pkg_dir / "prompts").mkdir(exist_ok=True)
        (pkg_dir / "config").mkdir(exist_ok=True)
        (pkg_dir / "utils").mkdir(exist_ok=True)

        # Create tests directory
        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create examples directory
        examples_dir = project_path / "examples"
        examples_dir.mkdir(exist_ok=True)

        # Create scripts directory
        scripts_dir = project_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        # Create docs directory
        docs_dir = project_path / "docs"
        docs_dir.mkdir(exist_ok=True)

    def _generate_config_files(
        self,
        metadata: AgentScopeMetadata,
        project_path: Path
    ):
        """Generate configuration files."""
        # Generate .env.example
        env_example = self._generate_env_example(metadata)
        (project_path / ".env.example").write_text(env_example)

        # Generate requirements.txt
        requirements = self._generate_requirements(metadata)
        (project_path / "requirements.txt").write_text(requirements)

        # Generate pyproject.toml
        pyproject = self._generate_pyproject(metadata)
        (project_path / "pyproject.toml").write_text(pyproject)

    def _generate_source_code(
        self,
        metadata: AgentScopeMetadata,
        project_path: Path,
        template
    ):
        """Generate source code files."""
        # Standard src/ layout: src/project_name/
        pkg_dir = project_path / "src" / metadata.package_name
        main_path = pkg_dir / "main.py"

        # Generate __init__.py files
        self._generate_init_files(pkg_dir, metadata)

        # Generate agents files
        self._generate_agents(pkg_dir, metadata)

        # Generate skills files
        self._generate_skills(pkg_dir, metadata)

        # Generate tools files
        self._generate_tools(pkg_dir, metadata)

        # Generate prompts files
        self._generate_prompts(pkg_dir, metadata)

        # Generate config files
        self._generate_config(pkg_dir, metadata)

        # Generate utils files
        self._generate_utils(pkg_dir, metadata)

        # Generate examples
        self._generate_examples(project_path, metadata)

        # Generate scripts
        self._generate_scripts(project_path, metadata)

        # Generate docs
        self._generate_docs(project_path, metadata)

        # Generate tests and evaluation
        self._generate_tests_and_evaluation(project_path, metadata)

        # Generate main.py
        main_content = self._generate_main(metadata)
        main_path.write_text(main_content)

    def _get_display_agent_type(self, agent_type_value: str) -> str:
        """Get display name for agent type."""
        display_names = {
            "basic": "Basic Agent",
            "multi-agent": "Multi-Agent System",
            "research": "Research Agent",
            "browser": "Browser Agent",
        }
        return display_names.get(agent_type_value, agent_type_value)

    def _generate_readme(self, metadata: AgentScopeMetadata, project_path: Path):
        """Generate README.md."""
        agent_type_display = self._get_display_agent_type(metadata.agent_type.value)

        readme = f"""# {metadata.name}

{metadata.description}

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure your API keys:

```bash
cp .env.example .env
```

## Usage

```bash
python -m {metadata.package_name}.main
```

## Project Structure

```
{metadata.name}/
├── src/
│   └── {metadata.package_name}/          # Package directory
│       ├── agents/              # Agent implementations
│       ├── skills/              # Agent skill modules
│       ├── tools/               # Custom tools
│       ├── prompts/             # Prompt templates
│       ├── config/              # Configuration
│       ├── utils/               # Utility functions
│       └── main.py              # Entry point
├── tests/                       # Tests
├── examples/                    # Usage examples
├── scripts/                     # Utility scripts
├── docs/                        # Documentation
├── pyproject.toml              # Project config
├── requirements.txt             # Dependencies
└── .env.example                # Environment template
```

## AgentScope Configuration

- **Agent Type**: {agent_type_display}
- **Model Provider**: {metadata.model_provider.value}
- **Memory Type**: {metadata.memory_type.value}
- **Python Version**: {metadata.python_version}

## Features

This project includes:
- Pre-configured AgentScope agents
- Modular skill system for extensibility
- Integrated tools for common tasks
- Comprehensive testing framework
- Example usage and documentation

## License

MIT
"""
        (project_path / "README.md").write_text(readme)

    def _generate_env_example(self, metadata: AgentScopeMetadata) -> str:
        """Generate .env.example content."""
        lines = ["# Agent Configuration"]

        if metadata.model_provider.value == "openai":
            lines.append("OPENAI_API_KEY=your-api-key-here")
            lines.append("OPENAI_MODEL=gpt-4")
        elif metadata.model_provider.value == "dashscope":
            lines.append("DASHSCOPE_API_KEY=your-api-key-here")
            lines.append("DASHSCOPE_MODEL=qwen-max")
        elif metadata.model_provider.value == "anthropic":
            lines.append("ANTHROPIC_API_KEY=your-api-key-here")
            lines.append("ANTHROPIC_MODEL=claude-3-5-sonnet-20241022")
        elif metadata.model_provider.value == "gemini":
            lines.append("GEMINI_API_KEY=your-api-key-here")
            lines.append("GEMINI_MODEL=gemini-pro")

        if metadata.memory_type.value == "long-term":
            lines.append("")
            lines.append("# Long-term Memory Configuration")
            lines.append("MEMORY_BACKEND=mem0")
            lines.append("MEMORY_API_KEY=your-memory-api-key")

        if metadata.agent_type.value == "research":
            lines.append("")
            lines.append("# Search API Configuration")
            lines.append("TAVILY_API_KEY=your-tavily-api-key")

        # Add logging configuration
        lines.append("")
        lines.append("# Logging Configuration")
        lines.append("LOG_LEVEL=INFO")
        lines.append("LOG_TO_FILE=true")
        lines.append("LOG_TO_CONSOLE=true")
        lines.append("# Max log file size in bytes (default: 10485760 = 10 MB)")
        lines.append("LOG_FILE_MAX_BYTES=10485760")
        lines.append("# Number of backup files to keep (default: 5)")
        lines.append("LOG_FILE_BACKUP_COUNT=5")
        lines.append("# Number of days to keep log files (default: 30)")
        lines.append("LOG_RETENTION_DAYS=30")

        return "\n".join(lines)

    def _generate_gitignore(self) -> str:
        """Generate .gitignore content."""
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env

# AgentScope specific
.state/
*.log

# OS
.DS_Store
Thumbs.db
"""

    def _generate_requirements(self, metadata: AgentScopeMetadata) -> str:
        """Generate requirements.txt content."""
        deps = [
            "agentscope>=0.1.0",
            "python-dotenv>=1.0.0",
        ]

        # Add model-specific dependencies
        if metadata.model_provider.value == "openai":
            deps.append("openai>=1.0.0")
        elif metadata.model_provider.value == "anthropic":
            deps.append("anthropic>=0.18.0")
        elif metadata.model_provider.value == "dashscope":
            deps.append("dashscope>=1.0.0")

        # Add memory-specific dependencies
        if metadata.memory_type.value == "long-term":
            deps.append("mem0ai>=0.1.0")

        # Add agent-type specific dependencies
        if metadata.agent_type.value == "research":
            deps.append("httpx>=0.27.0")
        elif metadata.agent_type.value == "browser":
            deps.append("playwright>=1.40.0")

        return "\n".join(deps)

    def _generate_pyproject(self, metadata: AgentScopeMetadata) -> str:
        """Generate pyproject.toml content."""
        return f"""[project]
name = "{metadata.name}"
version = "{metadata.version}"
description = "{metadata.description}"
authors = [
    {{name = "{metadata.author}", email = "{metadata.email}"}},
]
readme = "README.md"
requires-python = ">={metadata.python_version}"
dependencies = [
    "agentscope>=0.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
]

[project.scripts]
{metadata.package_name} = "{metadata.package_name}.main:run_cli"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 100
target-version = ['py310']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
skip_gitignore = true

[tool.mypy]
python_version = "{metadata.python_version}"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
"""

    def _generate_package_init(self, metadata: AgentScopeMetadata) -> str:
        """Generate package __init__.py."""
        return f'''"""
{metadata.name}

{metadata.description}
"""

__version__ = "{metadata.version}"
'''

    def _generate_main(self, metadata: AgentScopeMetadata) -> str:
        """Generate main.py entry point."""
        agent_type_display = self._get_display_agent_type(metadata.agent_type.value)
        skills_import = ""
        skills_usage = ""

        if metadata.enable_skills and metadata.skills:
            skills_import = f"""
from {metadata.package_name}.skills import (
    conversational_response,
    analyze_input,
    summarize_text,
)
"""
            skills_usage = """
    # Skills are available through the agent's toolkit
    # Custom skills can be called directly:
    # result = await conversational_response(input_text)
"""

        return f'''"""
Main entry point for {metadata.name}.

This module initializes and runs the AgentScope agent.
"""

import asyncio
import logging
import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from {metadata.package_name}.config import settings, get_model, get_memory, get_toolkit
from {metadata.package_name}.utils.logging import setup_logging, cleanup_old_logs
from agentscope.agent import ReActAgent
{skills_import}

# Load environment variables
load_dotenv()

# Setup unified logging with file rotation and retention
logger = setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    log_to_file=settings.LOG_TO_FILE,
    log_to_console=settings.LOG_TO_CONSOLE,
    max_bytes=settings.LOG_FILE_MAX_BYTES,
    backup_count=settings.LOG_FILE_BACKUP_COUNT,
    retention_days=settings.LOG_RETENTION_DAYS,
)


async def main():
    """Main entry point."""
    try:
        # Log startup
        logger.info(f"Starting {metadata.name}...")
        logger.info(f"Agent Type: {agent_type_display}")
        logger.info(f"Model Provider: {metadata.model_provider.value}")
        logger.info(f"Log Level: {os.getenv('LOG_LEVEL', 'INFO')}")
        logger.info(f"Log Retention: {{settings.LOG_RETENTION_DAYS}} days")

        # Clean up old logs
        cleanup_old_logs(retention_days=settings.LOG_RETENTION_DAYS)

        # Initialize configuration
        model = get_model()
        memory = get_memory()
        toolkit = get_toolkit()

        # Create agent
        agent = ReActAgent(
            name="{metadata.name}",
            sys_prompt=settings.SYSTEM_PROMPT,
            model=model,
            toolkit=toolkit,
            memory=memory,
        )

        logger.info("Agent initialized successfully")
{skills_usage}
        # Start interaction
        print(f"🤖 {metadata.name} is ready!")
        print(f"   Type: {agent_type_display}")
        print(f"   Model: {metadata.model_provider.value}")
        print(f"   Started at: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        print(f"   Type 'exit' or 'quit' to stop, 'help' for commands")
        print()

        while True:
            try:
                user_input = input("\\n💬 You: ")

                # Handle commands
                if user_input.lower() in ['exit', 'quit']:
                    print("\\n👋 Goodbye!")
                    logger.info("Agent shutdown by user")
                    break

                if user_input.lower() == 'help':
                    print("\\n📖 Available commands:")
                    print("  - help: Show this help message")
                    print("  - exit/quit: Exit the agent")
                    print("  - stats: Show agent statistics")
                    print("  - logs: Show log configuration")
                    print("  - Any other text will be sent to the agent")
                    continue

                if user_input.lower() == 'stats':
                    print("\\n📊 Agent Statistics:")
                    print(f"  Name: {metadata.name}")
                    print(f"  Type: {agent_type_display}")
                    print(f"  Model: {metadata.model_provider.value}")
                    print(f"  Memory: {metadata.memory_type.value}")
                    print(f"  Log Level: {{logging.getLevelName(logger.level)}}")
                    print(f"  Log Retention: {{settings.LOG_RETENTION_DAYS}} days")
                    continue

                if user_input.lower() == 'logs':
                    print("\\n📝 Log Configuration:")
                    print(f"  Log Directory: logs/")
                    print(f"  Log Level: {{logging.getLevelName(logger.level)}}")
                    print(f"  File Logging: {{'Enabled' if settings.LOG_TO_FILE else 'Disabled'}}")
                    print(f"  Console Logging: {{'Enabled' if settings.LOG_TO_CONSOLE else 'Disabled'}}")
                    print(f"  Max File Size: {{settings.LOG_FILE_MAX_BYTES / 1024 / 1024:.1f}} MB")
                    print(f"  Backup Count: {{settings.LOG_FILE_BACKUP_COUNT}}")
                    print(f"  Retention Days: {{settings.LOG_RETENTION_DAYS}}")
                    continue

                if not user_input.strip():
                    continue

                # Process input
                logger.info(f"User input: {{user_input[:50]}}...")
                response = await agent(user_input)
                print(f"\\n🤖 {metadata.name}:")
                print(f"{{response}}")
                logger.info("Response generated")

            except KeyboardInterrupt:
                print("\\n\\n👋 Interrupted. Goodbye!")
                logger.info("Agent shutdown by interrupt")
                break
            except Exception as e:
                error_msg = f"Error processing request: {{str(e)}}"
                print(f"\\n❌ {{error_msg}}")
                logger.error(error_msg, exc_info=True)

    except Exception as e:
        logger.error(f"Fatal error: {{str(e)}}", exc_info=True)
        print(f"\\n❌ Fatal error: {{str(e)}}")
        sys.exit(1)


def run_cli():
    """Entry point for CLI."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n\\n👋 Interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {{str(e)}}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
'''

    def _generate_init_files(
        self,
        pkg_dir: Path,
        metadata: AgentScopeMetadata
    ):
        """Generate __init__.py files for all modules."""
        # Main package __init__.py
        init_content = self._generate_package_init(metadata)
        (pkg_dir / "__init__.py").write_text(init_content)

        # Submodule __init__.py files
        (pkg_dir / "agents" / "__init__.py").write_text('"""Agent implementations."""\n')
        (pkg_dir / "skills" / "__init__.py").write_text('"""Agent skill modules."""\n')
        (pkg_dir / "tools" / "__init__.py").write_text('"""Tool implementations."""\n')
        (pkg_dir / "prompts" / "__init__.py").write_text('"""Prompt templates."""\n')
        (pkg_dir / "utils" / "__init__.py").write_text('"""Utility functions."""\n')

    def _generate_agents(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate agent implementation files."""
        if metadata.agent_type.value == "basic":
            agent_content = f'''"""
Base ReAct agent implementation.
"""

from agentscope.agent import ReActAgent
from {metadata.package_name}.config import get_model, get_memory, get_toolkit


def create_react_agent(name: str = "{metadata.name}") -> ReActAgent:
    """
    Create a ReAct agent instance.

    Args:
        name: Agent name

    Returns:
        Configured ReActAgent instance
    """
    model = get_model()
    memory = get_memory()
    toolkit = get_toolkit()

    return ReActAgent(
        name=name,
        sys_prompt="You are a helpful assistant with access to various tools.",
        model=model,
        toolkit=toolkit,
        memory=memory,
    )
'''
            (pkg_dir / "agents" / "react_agent.py").write_text(agent_content)

    def _generate_tools(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate tool implementation files - one tool per folder."""
        tools_dir = pkg_dir / "tools"
        tools_dir.mkdir(exist_ok=True)

        # Generate calculator tool
        calculator_dir = tools_dir / "calculator"
        calculator_dir.mkdir(exist_ok=True)
        (calculator_dir / "__init__.py").write_text('''"""
Calculator tool for mathematical expressions.
"""
from .calculator import calculator
''')
        (calculator_dir / "calculator.py").write_text('''"""
Calculator tool implementation.
"""

from agentscope.tools import tool


@tool("calculate")
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
''')

        # Generate time tool
        time_dir = tools_dir / "get_current_time"
        time_dir.mkdir(exist_ok=True)
        (time_dir / "__init__.py").write_text('''"""
Get current time tool.
"""
from .get_current_time import get_current_time
''')
        (time_dir / "get_current_time.py").write_text('''"""
Get current time tool implementation.
"""

from agentscope.tools import tool


@tool("get_current_time")
def get_current_time() -> str:
    """
    Get the current time.

    Returns:
        Current time as string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
''')

        # Generate tools __init__.py
        (tools_dir / "__init__.py").write_text('''"""
Custom tools for the agent.
"""
from .calculator import calculator
from .get_current_time import get_current_time

__all__ = ["calculator", "get_current_time"]
''')

    def _generate_skills(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate skill implementation files."""
        # Generate skills using extension generator
        self.extension_generator.generate_skills_files(pkg_dir, metadata)

    def _generate_utils(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate utility function files."""
        # Generate logging module
        logging_content = f'''"""
Unified logging module for {metadata.name}.

This module provides centralized logging configuration with file rotation,
retention policies, and structured logging support.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional
from datetime import datetime


class LoggerConfig:
    """Logger configuration."""

    # Log directory
    LOG_DIR = Path("logs")

    # Log format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Log file settings
    LOG_FILE_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_FILE_BACKUP_COUNT = 5  # Keep 5 backup files

    # Log retention settings (in days)
    LOG_RETENTION_DAYS = 30  # Keep logs for 30 days

    # Console log colors
    COLORS = {{
        'DEBUG': '\\033[36m',     # Cyan
        'INFO': '\\033[32m',      # Green
        'WARNING': '\\033[33m',   # Yellow
        'ERROR': '\\033[31m',     # Red
        'CRITICAL': '\\033[35m',  # Magenta
        'RESET': '\\033[0m',      # Reset
    }}


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""

    def __init__(self, fmt: str, datefmt: str, use_colors: bool = True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        if self.use_colors:
            levelname = record.levelname
            if levelname in LoggerConfig.COLORS:
                record.levelname = f"{{LoggerConfig.COLORS[levelname]}}{{levelname}}{{LoggerConfig.COLORS['RESET']}}"

        formatted = super().format(record)
        return formatted


def setup_logging(
    name: str = "{metadata.package_name}",
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True,
    max_bytes: int = LoggerConfig.LOG_FILE_MAX_BYTES,
    backup_count: int = LoggerConfig.LOG_FILE_BACKUP_COUNT,
    retention_days: int = LoggerConfig.LOG_RETENTION_DAYS,
) -> logging.Logger:
    """
    Setup unified logging with file rotation and retention.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Enable file logging
        log_to_console: Enable console logging
        max_bytes: Maximum log file size before rotation (bytes)
        backup_count: Number of backup files to keep
        retention_days: Number of days to keep log files

    Returns:
        Configured logger instance

    Example:
        >>> # Basic usage
        >>> logger = setup_logging()
        >>>
        >>> # Custom configuration
        >>> logger = setup_logging(
        ...     level="DEBUG",
        ...     max_bytes=20*1024*1024,  # 20 MB
        ...     backup_count=10,
        ...     retention_days=60
        ... )
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()  # Clear existing handlers

    # Create formatters
    file_formatter = logging.Formatter(
        fmt=LoggerConfig.LOG_FORMAT,
        datefmt=LoggerConfig.DATE_FORMAT
    )

    console_formatter = ColoredFormatter(
        fmt=LoggerConfig.LOG_FORMAT,
        datefmt=LoggerConfig.DATE_FORMAT,
        use_colors=True
    )

    # File handler with rotation
    if log_to_file:
        # Ensure log directory exists
        LoggerConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Use rotating file handler (size-based)
        log_file = LoggerConfig.LOG_DIR / f"{{name}}.log"
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Also add time-based rotation for daily cleanup
        timed_handler = TimedRotatingFileHandler(
            filename=LoggerConfig.LOG_DIR / f"{{name}}_daily.log",
            when='midnight',
            interval=1,
            backupCount=retention_days,
            encoding='utf-8'
        )
        timed_handler.setLevel(logging.DEBUG)
        timed_handler.setFormatter(file_formatter)
        timed_handler.suffix = "%Y-%m-%d"
        logger.addHandler(timed_handler)

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get an existing logger or create a new one.

    Args:
        name: Logger name (defaults to package name)

    Returns:
        Logger instance
    """
    if name is None:
        name = "{metadata.package_name}"
    return logging.getLogger(name)


def cleanup_old_logs(retention_days: int = LoggerConfig.LOG_RETENTION_DAYS):
    """
    Clean up log files older than retention_days.

    Args:
        retention_days: Number of days to keep logs
    """
    if not LoggerConfig.LOG_DIR.exists():
        return

    import os
    import time

    current_time = time.time()
    cutoff_time = current_time - (retention_days * 24 * 60 * 60)

    for log_file in LoggerConfig.LOG_DIR.glob("*.log*"):
        try:
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                get_logger().info(f"Deleted old log file: {{log_file}}")
        except Exception as e:
            get_logger().warning(f"Failed to delete {{log_file}}: {{e}}")


class LoggerContext:
    """Context manager for temporary logging configuration."""

    def __init__(self, logger: logging.Logger, level: str):
        self.logger = logger
        self.level = level
        self.old_level = None

    def __enter__(self):
        self.old_level = self.logger.level
        self.logger.setLevel(getattr(logging, self.level.upper()))
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.old_level)
        return False


# Example usage:
if __name__ == "__main__":
    # Setup logging
    logger = setup_logging(
        level="DEBUG",
        max_bytes=1024*1024,  # 1 MB for testing
        backup_count=3,
        retention_days=7
    )

    # Test logging
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Using context manager for temporary level change
    with LoggerContext(logger, "DEBUG"):
        logger.debug("Debug message in context")

    # Cleanup old logs
    cleanup_old_logs(retention_days=7)
'''
        (pkg_dir / "utils" / "logging.py").write_text(logging_content)

        # Generate helpers module
        helpers_content = f'''"""
Utility helper functions for {metadata.name}.

This module provides common utility functions used throughout the application.
"""

from typing import Any, Dict, Optional
from datetime import datetime

from .logging import get_logger


logger = get_logger(__name__)


def format_response(response: Any, format_type: str = "text") -> str:
    """
    Format agent response for display.

    Args:
        response: Agent response object
        format_type: Format type (text, json, markdown)

    Returns:
        Formatted response string
    """
    if format_type == "json":
        import json
        return json.dumps(response, indent=2, ensure_ascii=False)
    elif format_type == "markdown":
        return f"```\\n{{str(response)}}\\n```"
    else:
        return str(response)


def parse_tool_result(result: Any) -> Dict[str, Any]:
    """
    Parse tool execution result.

    Args:
        result: Result from tool execution

    Returns:
        Parsed result dictionary
    """
    if isinstance(result, dict):
        return result
    elif isinstance(result, str):
        return {{"result": result}}
    else:
        return {{
            "result": str(result),
            "type": type(result).__name__
        }}


def validate_input(input_text: str, max_length: int = 10000) -> bool:
    """
    Validate user input.

    Args:
        input_text: Input text to validate
        max_length: Maximum allowed length

    Returns:
        True if valid, False otherwise
    """
    if not input_text or not input_text.strip():
        logger.warning("Empty input received")
        return False
    if len(input_text) > max_length:
        logger.warning(f"Input too long: {{len(input_text)}} > {{max_length}}")
        return False
    return True


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        ISO formatted timestamp
    """
    return datetime.utcnow().isoformat() + "Z"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_execute(func, *args, default=None, log_error: bool = True, **kwargs):
    """
    Safely execute a function and return default value on exception.

    Args:
        func: Function to execute
        *args: Positional arguments for the function
        default: Default value to return on exception
        log_error: Whether to log errors
        **kwargs: Keyword arguments for the function

    Returns:
        Function result or default value
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_error:
            logger.error(f"Error executing {{func.__name__}}: {{e}}", exc_info=True)
        return default


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{{seconds*1000:.0f}}ms"
    elif seconds < 60:
        return f"{{seconds:.1f}}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{{minutes:.1f}}m"
    else:
        hours = seconds / 3600
        return f"{{hours:.1f}}h"


def format_bytes(size_bytes: int) -> str:
    """
    Format bytes to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{{size_bytes:.1f}}{{unit}}"
        size_bytes /= 1024.0
    return f"{{size_bytes:.1f}}PB"
'''
        (pkg_dir / "utils" / "helpers.py").write_text(helpers_content)

    def _generate_prompts(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate prompt template files as Markdown."""
        prompts_dir = pkg_dir / "prompts"
        prompts_dir.mkdir(exist_ok=True)

        # Generate default system prompt
        default_prompt = f'''# Default System Prompt

**Agent Name**: {metadata.name}
**Description**: {metadata.description}

## Instructions

You are a helpful AI assistant powered by AgentScope.
You have access to various tools to help answer questions and complete tasks.
Think step-by-step and explain your reasoning.

## Available Tools

- `calculate`: Calculate mathematical expressions
- `get_current_time`: Get the current time

## Response Guidelines

1. Be clear and concise
2. Show your reasoning when appropriate
3. Use tools when needed
4. Ask for clarification if the request is ambiguous
'''
        (prompts_dir / "default_system_prompt.md").write_text(default_prompt)

        # Generate ReAct agent prompt
        react_prompt = '''# ReAct Agent System Prompt

## Role

You are a ReAct (Reasoning + Acting) agent that combines reasoning and acting to solve problems.

## Workflow

Follow this pattern for each task:

1. **Thought**: Think about what to do next
2. **Action**: Choose and execute an action
3. **Observation**: Observe the result of the action
4. **Repeat** until you have enough information
5. **Final Answer**: Provide the final answer

## Format

```
Thought: [your reasoning about what to do]
Action: [the action to take, e.g., use a tool]
Observation: [the result you observe]
... (repeat as needed)
Thought: I now know the final answer
Final Answer: [your final response]
```

## Available Tools

- `calculate`: Calculate mathematical expressions
- `get_current_time`: Get the current time

## Guidelines

- Break down complex tasks into steps
- Use tools when appropriate
- Verify your findings
- Provide clear, accurate answers
'''
        (prompts_dir / "react_agent_prompt.md").write_text(react_prompt)

        # Generate multi-agent coordinator prompt
        coordinator_prompt = '''# Multi-Agent Coordinator System Prompt

## Role

You are a coordinator agent managing multiple specialized agents in a collaborative system.

## Responsibilities

1. **Understand** the user's request thoroughly
2. **Break down** complex tasks into subtasks
3. **Delegate** subtasks to appropriate specialized agents
4. **Synthesize** results from multiple agents
5. **Provide** a cohesive final response

## Coordination Strategy

- Identify which agents are needed for each task
- Sequence tasks appropriately when dependencies exist
- Aggregate and reconcile results from multiple agents
- Handle conflicts or discrepancies in agent outputs
- Ensure the final response addresses all aspects of the user's request

## Best Practices

- Be explicit about delegation
- Provide context when delegating tasks
- Combine insights from multiple sources
- Maintain coherence across agent outputs
'''
        (prompts_dir / "multi_agent_coordinator_prompt.md").write_text(coordinator_prompt)

        # Generate research agent prompt
        research_prompt = '''# Research Agent System Prompt

## Role

You are a research agent specialized in finding, analyzing, and synthesizing information from multiple sources.

## Capabilities

- **Search** for current and relevant information
- **Analyze** multiple sources critically
- **Synthesize** findings into coherent reports
- **Cite** sources appropriately

## Research Process

1. **Clarify** the research question
2. **Identify** key search terms and concepts
3. **Search** for relevant information
4. **Evaluate** source credibility and relevance
5. **Synthesize** findings into insights
6. **Cite** all sources used

## Source Evaluation

Consider:
- Author credibility and expertise
- Publication quality and reputation
- Currency and timeliness
- Supporting evidence and data
- Potential biases or conflicts

## Output Format

- Clear executive summary
- Key findings organized by theme
- Proper citations for all sources
- Limitations and areas for further research
'''
        (prompts_dir / "research_agent_prompt.md").write_text(research_prompt)

        # Generate browser agent prompt
        browser_prompt = '''# Browser Agent System Prompt

## Role

You are a browser agent capable of interacting with web pages through automation.

## Capabilities

- **Navigate** to web pages
- **Click** on interactive elements
- **Type** into form fields
- **Screenshot** page states
- **Extract** information from pages

## Browser Automation Commands

- `browser_navigate(url)`: Navigate to a URL
- `browser_click(selector)`: Click an element
- `browser_type(selector, text)`: Type text into an input
- `browser_screenshot()`: Capture page screenshot

## Best Practices

- Wait for page loads before acting
- Handle dynamic content gracefully
- Take screenshots for verification
- Handle errors and timeouts
- Respect website terms of service
'''
        (prompts_dir / "browser_agent_prompt.md").write_text(browser_prompt)

        # Generate prompts __init__.py for loading markdown files
        init_content = '''"""
System prompts for the agent.

This module provides functions to load prompt templates from markdown files.
"""

from pathlib import Path
from typing import Optional


PROMPTS_DIR = Path(__file__).parent


def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt template from a markdown file.

    Args:
        prompt_name: Name of the prompt file (without .md extension)

    Returns:
        Prompt content as string
    """
    prompt_file = PROMPTS_DIR / f"{prompt_name}.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")


def get_default_system_prompt() -> str:
    """Get the default system prompt."""
    return load_prompt("default_system_prompt")


def get_react_agent_prompt() -> str:
    """Get the ReAct agent prompt."""
    return load_prompt("react_agent_prompt")


def get_multi_agent_coordinator_prompt() -> str:
    """Get the multi-agent coordinator prompt."""
    return load_prompt("multi_agent_coordinator_prompt")


def get_research_agent_prompt() -> str:
    """Get the research agent prompt."""
    return load_prompt("research_agent_prompt")


def get_browser_agent_prompt() -> str:
    """Get the browser agent prompt."""
    return load_prompt("browser_agent_prompt")
'''
        (prompts_dir / "__init__.py").write_text(init_content)

    def _generate_config(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate configuration files."""
        config_content = self.extension_generator.generate_config(metadata)
        (pkg_dir / "config" / "__init__.py").write_text(config_content)

        # Generate YAML config
        yaml_config = f'''# AgentScope Configuration
# Generated for {metadata.name}

agents:
  - name: {metadata.name}
    type: {metadata.agent_type.value}
    model_provider: {metadata.model_provider.value}
    model: {self._get_default_model(metadata.model_provider.value)}
    memory_type: {metadata.memory_type.value}
    system_prompt: "You are a helpful assistant."

models:
  {metadata.model_provider.value}:
    api_key_env: "{self._get_api_key_env(metadata.model_provider.value)}"
    model: {self._get_default_model(metadata.model_provider.value)}

tools:
  - name: calculate
    enabled: true
  - name: get_current_time
    enabled: true
'''
        (pkg_dir / "config" / "agents.yaml").write_text(yaml_config)

    def _generate_examples(self, project_path: Path, metadata: AgentScopeMetadata):
        """Generate example usage files."""
        basic_example = f'''"""
Basic usage example for {metadata.name}.

This example demonstrates how to use the agent to answer questions.
"""

import asyncio
from {metadata.package_name}.agents.react_agent import create_react_agent


async def main():
    """Run basic agent example."""
    # Create agent
    agent = create_react_agent()

    # Example questions
    questions = [
        "What is 25 * 34?",
        "What time is it now?",
        "Can you help me with a math problem?",
    ]

    for question in questions:
        print(f"\\nUser: {{question}}")
        response = await agent(question)
        print(f"Agent: {{response}}")


if __name__ == "__main__":
    asyncio.run(main())
'''
        (project_path / "examples" / "basic_usage.py").write_text(basic_example)

        advanced_example = f'''"""
Advanced multi-agent example for {metadata.name}.

This example demonstrates multi-agent collaboration.
"""

import asyncio
from agentscope.agent import ReActAgent
from {metadata.package_name}.config import get_model, get_memory, get_toolkit


async def main():
    """Run advanced multi-agent example."""
    # Create specialized agents
    researcher = ReActAgent(
        name="Researcher",
        sys_prompt="You are a research specialist. Find and analyze information.",
        model=get_model(),
        memory=get_memory(),
        toolkit=get_toolkit(),
    )

    analyst = ReActAgent(
        name="Analyst",
        sys_prompt="You are an analyst. Synthesize information and provide insights.",
        model=get_model(),
        memory=get_memory(),
        toolkit=get_toolkit(),
    )

    # Example workflow
    query = "What are the latest developments in AI?"

    print(f"\\nQuery: {{query}}")
    print(f"\\n--- Researcher Agent ---")
    research_result = await researcher(query)
    print(f"Research result: {{research_result}}")

    print(f"\\n--- Analyst Agent ---")
    analysis = await analyst(f"Analyze this research: {{research_result}}")
    print(f"Analysis: {{analysis}}")


if __name__ == "__main__":
    asyncio.run(main())
'''
        (project_path / "examples" / "advanced_multiagent.py").write_text(advanced_example)

    def _generate_scripts(self, project_path: Path, metadata: AgentScopeMetadata):
        """Generate utility scripts."""
        setup_script = f'''#!/bin/bash
# Setup script for {metadata.name} project

set -e

echo "🚀 Setting up {metadata.name} project..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{{print $2}}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📥 Installing dependencies..."
pip install -e .

# Install development dependencies (optional)
echo "📥 Installing development dependencies..."
pip install -e ".[dev]" || echo "⚠️  Warning: Dev dependencies not installed"

# Create .env file from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env file - Please update it with your API keys"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Configure your API keys in .env file"
echo "  3. Run the agent: {metadata.package_name}"
echo "  4. Or run with: python -m {metadata.package_name}.main"
echo "  5. Run tests: pytest tests/"
echo ""
'''
        (project_path / "scripts" / "setup.sh").write_text(setup_script)

        # Make setup script executable
        import stat
        setup_path = project_path / "scripts" / "setup.sh"
        setup_path.chmod(setup_path.stat().st_mode | stat.S_IEXEC)

        deploy_script = '''#!/bin/bash
# Deploy script for AgentScope project

set -e

echo "🚀 Deploying AgentScope project..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Run code quality checks
echo "🔍 Running code quality checks..."

# Format with black (if installed)
if command -v black &> /dev/null; then
    echo "🎨 Formatting code with black..."
    black src/ tests/ --check
fi

# Sort imports with isort (if installed)
if command -v isort &> /dev/null; then
    echo "📦 Sorting imports with isort..."
    isort src/ tests/ --check-only
fi

# Type checking with mypy (if installed)
if command -v mypy &> /dev/null; then
    echo "🔎 Type checking with mypy..."
    mypy src/
fi

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Aborting deployment."
    exit 1
fi

echo ""
echo "✅ Deployment ready!"
echo "📦 To build the package: python -m build"
echo "📤 To publish: twine upload dist/*"
'''
        (project_path / "scripts" / "deploy.sh").write_text(deploy_script)

        # Make deploy script executable
        deploy_path = project_path / "scripts" / "deploy.sh"
        deploy_path.chmod(deploy_path.stat().st_mode | stat.S_IEXEC)

        # Add run script for convenience
        run_script = f'''#!/bin/bash
# Run script for {metadata.name}

set -e

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Run the agent
echo "🚀 Starting {metadata.name}..."
python -m {metadata.package_name}.main "$@"
'''
        (project_path / "scripts" / "run.sh").write_text(run_script)

        # Make run script executable
        run_path = project_path / "scripts" / "run.sh"
        run_path.chmod(run_path.stat().st_mode | stat.S_IEXEC)

    def _generate_docs(self, project_path: Path, metadata: AgentScopeMetadata):
        """Generate documentation files."""
        agent_type_display = self._get_display_agent_type(metadata.agent_type.value)

        architecture_content = f'''# {metadata.name} Architecture

## Project Structure

```
{metadata.name}/
├── src/
│   └── {metadata.package_name}/          # Main package
│       ├── agents/              # Agent implementations
│       ├── skills/              # Agent skill modules
│       ├── tools/               # Custom tools
│       ├── prompts/             # Prompt templates
│       ├── config/              # Configuration
│       ├── utils/               # Utility functions
│       └── main.py              # Entry point
├── tests/                       # Tests
├── examples/                    # Usage examples
├── scripts/                     # Utility scripts
├── docs/                        # Documentation
├── pyproject.toml              # Project config
├── requirements.txt             # Dependencies
└── .env.example                # Environment template
```

## Architecture Overview

### Agent Layer
- **Agent Type**: {agent_type_display}
- **Pattern**: ReAct (Reasoning + Acting) paradigm
- **Capabilities**: Task execution with tool usage

### Skill Layer
- **Modular Skills**: Reusable skill modules
- **Skill Composition**: Combine multiple skills
- **Extensibility**: Easy to add custom skills

### Tool Layer
- **Built-in Tools**: Calculator, time utilities
- **Custom Tools**: Extend with domain-specific tools
- **Tool Registry**: Dynamic tool registration

### Configuration Layer
- **Settings**: Application settings management
- **Models**: Model provider configuration (OpenAI, Anthropic, etc.)
- **Memory**: Short and long-term memory management
- **Formatters**: Message formatting for different providers

### Extension Points
- **Hooks**: Agent lifecycle hooks (pre/post reply, pre/post observe)
- **Middleware**: Request/response processing pipeline
- **Formatters**: Custom message formatters
- **Skills**: Modular skill system
- **RAG**: Retrieval-Augmented Generation support
- **Pipeline**: Multi-agent pipeline orchestration

## Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Extensibility**: Easy to add new agents, tools, and skills
3. **Testability**: Comprehensive test coverage
4. **Documentation**: Clear documentation and examples
5. **Industry Best Practices**: Following Python packaging standards

## Development Workflow

1. **Setup**: Run `./scripts/setup.sh`
2. **Development**: Modify code in `src/{metadata.package_name}/`
3. **Testing**: Run `pytest tests/`
4. **Examples**: Check `examples/` for usage patterns
5. **Deployment**: Run `./scripts/deploy.sh`

## Contributing

When adding new features:
1. Add agent implementations in `agents/` directory
2. Add skill modules in `skills/` directory
3. Add tools in `tools/` directory
4. Update prompts in `prompts/` directory
5. Add utility functions in `utils/` directory
6. Add tests in `tests/` directory
7. Provide examples in `examples/` directory

## Directory Details

### `agents/`
Contains agent implementations and factory functions.

### `skills/`
Contains modular skill implementations that can be composed into agents.

### `tools/`
Contains custom tool functions that agents can use.

### `prompts/`
Contains prompt templates and system prompts.

### `config/`
Contains configuration modules for models, memory, and tools.

### `utils/`
Contains utility functions for logging, formatting, validation, etc.
'''
        (project_path / "docs" / "architecture.md").write_text(architecture_content)

    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider."""
        models = {
            "openai": "gpt-4",
            "dashscope": "qwen-max",
            "anthropic": "claude-3-5-sonnet-20241022",
            "gemini": "gemini-pro",
            "ollama": "llama2",
        }
        return models.get(provider, "gpt-4")

    def _get_api_key_env(self, provider: str) -> str:
        """Get API key environment variable name for provider."""
        keys = {
            "openai": "OPENAI_API_KEY",
            "dashscope": "DASHSCOPE_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "ollama": "OLLAMA_HOST",
        }
        return keys.get(provider, "API_KEY")

    def _generate_tests_and_evaluation(
        self,
        project_path: Path,
        metadata: AgentScopeMetadata
    ):
        """Generate test and evaluation modules."""
        tests_dir = project_path / "tests"

        # Generate test module
        if metadata.generate_tests:
            test_code = self.extension_generator.generate_tests_code(metadata)
            (tests_dir / f"test_{metadata.package_name}.py").write_text(test_code)

        # Generate evaluation module
        if metadata.generate_evaluation:
            eval_code = self.extension_generator.generate_evaluation_code(metadata)
            (tests_dir / f"test_evaluation.py").write_text(eval_code)

        # Generate pytest configuration
        pytest_content = f"""[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
"""
        (project_path / "pytest.ini").write_text(pytest_content)

        # Generate benchmark tasks if specified
        if metadata.initial_benchmark_tasks > 0:
            self._generate_benchmark_tests(tests_dir, metadata)

    def _generate_benchmark_tests(
        self,
        tests_dir: Path,
        metadata: AgentScopeMetadata
    ):
        """Generate benchmark test tasks."""
        benchmark_content = f'''"""
Benchmark tests for {metadata.name}.

This module contains benchmark tasks for performance evaluation.
"""

import pytest
from {metadata.package_name}.agents import create_react_agent


class TestBenchmarks:
    """Benchmark test cases."""

    @pytest.mark.asyncio
    async def test_benchmark_task_1(self):
        """Benchmark task 1: Basic conversation."""
        agent = create_react_agent()
        response = await agent("Hello, who are you?")
        assert response is not None

    @pytest.mark.asyncio
    async def test_benchmark_task_2(self):
        """Benchmark task 2: Tool usage."""
        agent = create_react_agent()
        response = await agent("What is 25 * 34?")
        assert response is not None

    @pytest.mark.asyncio
    async def test_benchmark_task_3(self):
        """Benchmark task 3: Complex query."""
        agent = create_react_agent()
        response = await agent("Can you help me solve a math problem?")
        assert response is not None
'''
        (tests_dir / "test_benchmarks.py").write_text(benchmark_content)