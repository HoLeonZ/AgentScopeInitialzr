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

        # Generate pip-sources.ini
        pip_sources = self._generate_pip_sources()
        (project_path / "pip-sources.ini").write_text(pip_sources)

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

        # Generate main.py (simplified, following single responsibility principle)
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

### Private PyPI Source Configuration

If you use a private PyPI server, edit `pip-sources.ini` first, then run the setup script:

```bash
# 1. Edit pip-sources.ini - fill in your private PyPI URLs
vim pip-sources.ini

# 2. Generate pip.conf from pip-sources.ini
./scripts/setup-pip-source.sh              # Global pip (~/.config/pip/pip.conf)
./scripts/setup-pip-source.sh --venv       # venv pip (venv/pip.conf)

# 3. Re-run install with private index
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
├── scripts/                     # Utility scripts (setup.sh, setup-pip-source.sh, etc.)
├── docs/                        # Documentation
├── requirements.txt             # Dependencies
├── pip-sources.ini              # Private PyPI source configuration
└── .env.example                 # Environment template
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
        lines = []

        # Agent Configuration
        lines.append("# ==============================================")
        lines.append("# Agent Configuration")
        lines.append("# ==============================================")
        lines.append(f"AGENT_NAME={metadata.name}")
        lines.append(f'SYSTEM_PROMPT="You are a helpful AI assistant named {metadata.name}."')
        lines.append("")

        # Model Configuration
        lines.append("# ==============================================")
        lines.append("# Model Configuration")
        lines.append("# ==============================================")
        cfg = metadata.model_config or {}
        lines.append(f"MODEL_NAME={cfg.get('model', '')}")
        lines.append(f"API_KEY={cfg.get('api_key', '')}")
        lines.append(f"BASE_URL={cfg.get('base_url', '')}")
        lines.append(f"MODEL_TEMPERATURE={cfg.get('temperature', 0.7)}")
        lines.append(f"MODEL_MAX_TOKENS={cfg.get('max_tokens', 2000)}")
        lines.append("ENABLE_STREAMING=true")
        lines.append("ENABLE_THINKING=false")
        lines.append("PARALLEL_TOOL_CALLS=true")
        lines.append("")

        # Memory Configuration
        lines.append("# ==============================================")
        lines.append("# Memory Configuration")
        lines.append("# ==============================================")
        lines.append(f"MEMORY_TYPE={metadata.memory_type.value}")
        if metadata.long_term_memory:
            lines.append(f"LONG_TERM_MEMORY={metadata.long_term_memory}")

        # Memory backend configuration
        # Short-term memory configuration
        if metadata.short_term_memory and metadata.short_term_memory != 'in-memory':
            if metadata.short_term_memory == 'redis':
                lines.append("# Short-term Memory: Redis Configuration")
                # Check if using URL or manual configuration
                if metadata.rag_config and metadata.rag_config.get('redis_url'):
                    lines.append(f"REDIS_URL={metadata.rag_config.get('redis_url')}")
                else:
                    lines.append("REDIS_HOST=localhost")
                    lines.append("REDIS_PORT=6379")
                    lines.append("REDIS_DB=0")
                    lines.append("# REDIS_PASSWORD=your-redis-password  # Optional")
            elif metadata.short_term_memory == 'oceanbase':
                lines.append("# Short-term Memory: OceanBase Configuration")
                lines.append("OCEANBASE_CONNECTION_STRING=postgresql://user:password@localhost:2881/tenant")
                lines.append("OCEANBASE_TABLE_NAME=agent_conversation")
            lines.append("")

        # Long-term memory configuration
        if metadata.long_term_memory:
            if metadata.long_term_memory == "mem0":
                lines.append("# Long-term Memory: Mem0 Configuration")
                lines.append("MEM0_API_KEY=your-mem0-api-key")
                # Check if mem0 URL is provided in rag_config
                if metadata.rag_config and metadata.rag_config.get('api_url'):
                    lines.append(f"MEM0_API_URL={metadata.rag_config['api_url']}")
                else:
                    lines.append("# MEM0_API_URL=https://api.mem0.ai  # Optional, uncomment if using custom endpoint")
            elif metadata.long_term_memory == "oceanbase":
                lines.append("# Long-term Memory: OceanBase Configuration")
                lines.append("OCEANBASE_CONNECTION_STRING=postgresql://user:password@localhost:2881/tenant")
                lines.append("OCEANBASE_TABLE_NAME=agent_memory")
            elif metadata.long_term_memory == "redis":
                lines.append("# Long-term Memory: Redis Configuration")
                lines.append("REDIS_HOST=localhost")
                lines.append("REDIS_PORT=6379")
                lines.append("REDIS_DB=0")
                lines.append("# REDIS_PASSWORD=your-redis-password  # Optional")
        lines.append("")

        # RAG Configuration
        if metadata.enable_rag:
            lines.append("# ==============================================")
            lines.append("# RAG Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_RAG=true")

            rag_config = metadata.rag_config or {}
            store_type = rag_config.get("store_type", "qdrant")

            if store_type == "qdrant":
                lines.append("# Qdrant vector database configuration")
                lines.append("RAG_STORE_TYPE=qdrant")
                lines.append("QDRANT_HOST=localhost")
                lines.append("QDRANT_PORT=6333")
                lines.append("QDRANT_COLLECTION=agent_documents")
                lines.append("# Or use full URL: QDRANT_URL=http://localhost:6333")
            elif store_type == "kbase":
                lines.append("# KBase knowledge base configuration")
                lines.append("RAG_STORE_TYPE=kbase")
                lines.append("KBASE_RETRIEVAL_URL=https://kbase.example.com/api/retrieve")
            lines.append("")

        # Pipeline Configuration
        if metadata.enable_pipeline:
            lines.append("# ==============================================")
            lines.append("# Pipeline Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_PIPELINE=true")
            lines.append("PIPELINE_MAX_CONCURRENCY=3")
            lines.append("")

        # Research agent search API
        if metadata.agent_type.value == "research":
            lines.append("# ==============================================")
            lines.append("# Search API Configuration")
            lines.append("# ==============================================")
            lines.append("TAVILY_API_KEY=your-tavily-api-key")
            lines.append("")

        # Knowledge Base Configuration
        if metadata.enable_knowledge:
            lines.append("# ==============================================")
            lines.append("# Knowledge Base Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_KNOWLEDGE=true")

            knowledge_config = metadata.knowledge_config or {}
            kb_type = knowledge_config.get("type", "qdrant")

            if kb_type == "qdrant":
                lines.append("# Qdrant Knowledge Base Configuration")
                lines.append("KNOWLEDGE_STORE_TYPE=qdrant")
                lines.append(f"QDRANT_HOST={knowledge_config.get('qdrant_host', 'localhost')}")
                lines.append(f"QDRANT_PORT={knowledge_config.get('qdrant_port', 6333)}")
                lines.append(f"QDRANT_COLLECTION={knowledge_config.get('collection_name', 'agent_knowledge')}")
                lines.append(f"EMBEDDING_MODEL={knowledge_config.get('embedding_model', 'text-embedding-ada-002')}")
                lines.append(f"EMBEDDING_DIMENSION={knowledge_config.get('dimension', 1536)}")
                lines.append(f"RETRIEVAL_TOP_K={knowledge_config.get('top_k', 5)}")
                lines.append(f"SIMILARITY_THRESHOLD={knowledge_config.get('similarity_threshold', 0.7)}")
            elif kb_type == "kbase":
                lines.append("# KBase Knowledge Base Configuration")
                lines.append("KNOWLEDGE_STORE_TYPE=kbase")
                lines.append(f"KBASE_URL={knowledge_config.get('kbase_url', 'https://kbase.example.com')}")
                lines.append(f"RETRIEVAL_TOP_K={knowledge_config.get('top_k', 5)}")
                lines.append(f"SIMILARITY_THRESHOLD={knowledge_config.get('similarity_threshold', 0.7)}")
            lines.append("")

        # Skills Configuration
        if metadata.enable_skills and metadata.skills:
            lines.append("# ==============================================")
            lines.append("# Skills Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_SKILLS=true")
            lines.append(f"ENABLED_SKILLS={','.join(metadata.skills)}")
            lines.append("")

        # Hooks Configuration
        if metadata.hooks:
            lines.append("# ==============================================")
            lines.append("# Hooks Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_HOOKS=true")
            enabled_hooks = [h.hook_type for h in metadata.hooks if h.enabled]
            if enabled_hooks:
                lines.append(f"ENABLED_HOOKS={','.join(enabled_hooks)}")
            lines.append("")

        # Formatter Configuration
        if metadata.formatter_name:
            lines.append("# ==============================================")
            lines.append("# Formatter Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_FORMATTER=true")
            lines.append(f"FORMATTER_TYPE={metadata.formatter_name}")
            lines.append("")

        # Testing & Evaluation Configuration
        if metadata.generate_tests or metadata.generate_evaluation:
            lines.append("# ==============================================")
            lines.append("# Testing & Evaluation Configuration")
            lines.append("# ==============================================")
            if metadata.generate_tests:
                lines.append("GENERATE_TESTS=true")
                lines.append("TEST_FRAMEWORK=pytest")
                lines.append("TEST_COVERAGE=true")
            if metadata.generate_evaluation:
                lines.append("ENABLE_EVALUATION=true")
                lines.append(f"EVALUATOR_TYPE={metadata.evaluator_type}")
            lines.append("")

        # OpenJudge Configuration
        if metadata.enable_openjudge:
            lines.append("# ==============================================")
            lines.append("# OpenJudge Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_OPENJUDGE=true")
            if metadata.openjudge_graders:
                lines.append(f"OPENJUDGE_GRADERS={','.join(metadata.openjudge_graders)}")
            lines.append("")

        # Benchmark Configuration
        if metadata.initial_benchmark_tasks > 0:
            lines.append("# ==============================================")
            lines.append("# Benchmark Configuration")
            lines.append("# ==============================================")
            lines.append(f"INITIAL_BENCHMARK_TASKS={metadata.initial_benchmark_tasks}")
            lines.append("BENCHMARK_SUITE=custom")
            lines.append("")

        # RAGAS Evaluation Configuration
        if metadata.enable_ragas_evaluation:
            lines.append("# ==============================================")
            lines.append("# RAGAS Evaluation Configuration")
            lines.append("# ==============================================")
            lines.append("ENABLE_RAGAS_EVALUATION=true")
            lines.append(f"EVALUATION_CSV_FILENAME={metadata.evaluation_csv_filename}")
            lines.append(f"EVALUATION_METRICS={','.join(metadata.evaluation_metrics)}")
            lines.append("")

        # Logging Configuration
        lines.append("# ==============================================")
        lines.append("# Logging Configuration")
        lines.append("# ==============================================")
        lines.append("# Log directory path (relative or absolute)")
        lines.append("LOG_DIR=logs")
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
        """Generate requirements.txt content with all runtime dependencies."""
        deps = [
            "# Core dependencies",
            "agentscope>=0.1.0",
            "python-dotenv>=1.0.0",
            "",
            "# Model provider dependencies",
        ]

        # Add model-specific dependencies
        if metadata.model_provider.value == "openai":
            deps.append("openai>=1.0.0")
        elif metadata.model_provider.value == "anthropic":
            deps.append("anthropic>=0.18.0")
        elif metadata.model_provider.value == "dashscope":
            deps.append("dashscope>=1.0.0")
        elif metadata.model_provider.value == "gemini":
            deps.append("google-generativeai>=0.3.0")

        deps.append("")
        deps.append("# Feature-specific dependencies")

        # Add memory-specific dependencies
        if metadata.memory_type.value == "long-term":
            deps.append("mem0ai>=0.1.0")

        # Add agent-type specific dependencies
        if metadata.agent_type.value == "research":
            deps.append("httpx>=0.27.0")
        elif metadata.agent_type.value == "browser":
            deps.append("playwright>=1.40.0")

        # Add knowledge base dependencies
        if metadata.enable_knowledge:
            deps.append("qdrant-client>=1.7.0")

        return "\n".join(deps)

    def _generate_pip_sources(self) -> str:
        """Generate pip-sources.ini configuration file."""
        return '''# =============================================================================
# pip source (private package index) configuration
# =============================================================================
#
# Edit this file to configure your private PyPI server(s).
# Then run: ./scripts/setup-pip-source.sh
#
# This file is the source of truth - do NOT edit pip.conf directly,
# as it will be overwritten by setup-pip-source.sh.
#
# =============================================================================

[source]
# Primary package index (your private PyPI server)
index_url = http://203.3.234.97:8082/repository/pypi/simple

[fallback]
# Fallback / secondary index
extra_index_url = http://mypypi.ai.test.com:4000/simple

[trusted]
# Comma-separated list of trusted hosts
trusted_host = 203.3.234.97,mypypi.ai.test.com
'''

    def _generate_package_init(self, metadata: AgentScopeMetadata) -> str:
        """Generate package __init__.py."""
        return f'''"""
{metadata.name}

{metadata.description}
"""

__version__ = "{metadata.version}"
'''

    def _generate_main(self, metadata: AgentScopeMetadata) -> str:
        """Generate main.py entry point - simplified following Single Responsibility Principle."""
        template = '''"""
Main entry point for {name}.

This module follows Single Responsibility Principle:
- Loads logging configuration
- Creates the agent
- Provides basic agent interaction example
"""

import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from {package_name}.config import settings
from {package_name}.config.lifecycle import ApplicationLifecycle
from {package_name}.agents.react_agent import create_react_agent

# Load environment variables
load_dotenv()

# Setup unified logging with file rotation and retention
logger = setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    log_dir=settings.LOG_DIR,
    log_to_file=settings.LOG_TO_FILE,
    log_to_console=settings.LOG_TO_CONSOLE,
    max_bytes=settings.LOG_FILE_MAX_BYTES,
    backup_count=settings.LOG_FILE_BACKUP_COUNT,
    retention_days=settings.LOG_RETENTION_DAYS,
)


async def main():
    """Main entry point - demonstrates basic agent usage."""
    try:
        # Step 1: Initialize logging
        logger.info("Starting {name}...")
        logger.info("Log Level: " + os.getenv("LOG_LEVEL", "INFO"))

        # Step 2: Clean up old logs
        cleanup_old_logs(
            retention_days=settings.LOG_RETENTION_DAYS,
            log_dir=settings.LOG_DIR
        )

        # Step 3: Initialize application lifecycle (includes agentscope.init() and middleware injection)
        ApplicationLifecycle.initialize()
        logger.info("Application lifecycle initialized")

        # Step 4: Create agent
        agent = create_react_agent(
            name="{name}",
            sys_prompt=settings.SYSTEM_PROMPT
        )
        logger.info("Agent created successfully")

        # Step 5: Example usage
        print("🤖 Agent '{name}' is ready!\\n")

        # Simple example
        response = await agent("Hello! Please introduce yourself.")
        print("Agent:", response)
        logger.info("Example interaction completed")

    except Exception as e:
        logger.error("Fatal error: " + str(e), exc_info=True)
        print("\\n❌ Fatal error:", str(e))
        sys.exit(1)
    finally:
        # Cleanup application lifecycle
        try:
            ApplicationLifecycle.shutdown()
            logger.info("Application shutdown completed")
        except Exception as e:
            logger.error("Error during shutdown: " + str(e), exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n\\n👋 Interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error("Unexpected error: " + str(e), exc_info=True)
        sys.exit(1)
'''
        return template.format(
            name=metadata.name,
            package_name=metadata.package_name
        )

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
        (pkg_dir / "utils" / "__init__.py").write_text('''"""Utility functions."""

from . import helpers
from . import log

__all__ = ["helpers", "log"]
''')

    def _generate_agents(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate agent implementation files."""
        if metadata.agent_type.value == "basic":
            # Build imports based on whether hooks are enabled
            pkg_name = metadata.package_name
            hook_import = ""
            hook_attachment = ""
            if metadata.hooks:
                hook_import = f'''
from {pkg_name}.config.lifecycle import ApplicationLifecycle'''
                hook_attachment = '''
    # Attach hooks to the agent
    ApplicationLifecycle.attach_hooks_to_agent(agent)'''

            # Create agent content
            agent_content = '''"""
Base ReAct agent implementation.
"""

from typing import Optional
from agentscope.agent import ReActAgent
from ''' + pkg_name + '''.config import get_model, get_memory, get_toolkit, get_formatter
from ''' + pkg_name + '''.config.middleware import middleware_manager''' + hook_import + '''


def create_react_agent(
    name: str = "''' + pkg_name + '''",
    sys_prompt: Optional[str] = None,
) -> ReActAgent:
    """
    Create a ReAct agent instance.

    Args:
        name: Agent name
        sys_prompt: System prompt (uses default if not provided)

    Returns:
        Configured ReActAgent instance
    """
    # Get core middlewares
    model = get_model()
    formatter = get_formatter()

    # Get optional middlewares
    memory = get_memory() if middleware_manager.has('memory') else None
    toolkit = get_toolkit() if middleware_manager.has('toolkit') else None

    # Get configuration parameters
    enable_meta_tool = middleware_manager.get_config('enable_meta_tool', False)
    parallel_tool_calls = middleware_manager.get_config('parallel_tool_calls', False)
    max_iters = middleware_manager.get_config('max_iters', 10)

    # Use provided prompt or default
    prompt = sys_prompt or "You are a helpful assistant with access to various tools."

    agent = ReActAgent(
        name=name,
        sys_prompt=prompt,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        memory=memory,
        enable_meta_tool=enable_meta_tool,
        parallel_tool_calls=parallel_tool_calls,
        max_iters=max_iters,
    )
''' + hook_attachment + '''

    return agent
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
        # Create log directory under utils
        log_dir = pkg_dir / "utils" / "log"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Generate logging module in utils/log/
        logging_content = f'''"""
Unified logging module for {metadata.name}.

This module provides centralized logging configuration with file rotation,
retention policies, and structured logging support.
"""

import logging
import os
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional
from datetime import datetime


class LoggerConfig:
    """Logger configuration."""

    # Log directory (can be overridden via environment variable)
    LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))

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
    log_dir: Optional[Path] = None,
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
        log_dir: Log directory path (defaults to LOG_DIR env var or "logs")
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

    # Determine log directory
    if log_dir is None:
        log_dir = LoggerConfig.LOG_DIR
    else:
        log_dir = Path(log_dir)

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
        log_dir.mkdir(parents=True, exist_ok=True)

        # Use rotating file handler (size-based)
        log_file = log_dir / f"{{name}}.log"
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
            filename=log_dir / f"{{name}}_daily.log",
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


def cleanup_old_logs(
    retention_days: int = LoggerConfig.LOG_RETENTION_DAYS,
    log_dir: Optional[Path] = None
):
    """
    Clean up log files older than retention_days.

    Args:
        retention_days: Number of days to keep logs
        log_dir: Log directory path (defaults to LOG_DIR env var or "logs")
    """
    if log_dir is None:
        log_dir = LoggerConfig.LOG_DIR
    else:
        log_dir = Path(log_dir)

    if not log_dir.exists():
        return

    import os
    import time

    current_time = time.time()
    cutoff_time = current_time - (retention_days * 24 * 60 * 60)

    for log_file in log_dir.glob("*.log*"):
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
        (log_dir / "logging.py").write_text(logging_content)

        # Generate log module __init__.py
        log_init_content = '''"""
Log management utilities.

This package contains all logging-related functionality.
"""

from .logging import (
    setup_logging,
    get_logger,
    cleanup_old_logs,
    LoggerContext,
    LoggerConfig,
)

__all__ = [
    "setup_logging",
    "get_logger",
    "cleanup_old_logs",
    "LoggerContext",
    "LoggerConfig",
]
'''
        (log_dir / "__init__.py").write_text(log_init_content)

        # Generate helpers module
        helpers_content = f'''"""
Utility helper functions for {metadata.name}.

This module provides common utility functions used throughout the application.
"""

from typing import Any, Dict, Optional
from datetime import datetime

from .log.logging import get_logger


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
        """Generate configuration files with separate modules for each middleware."""
        # Generate settings.py first
        settings_content = self.extension_generator.generate_settings_file(metadata)
        (pkg_dir / "config" / "settings.py").write_text(settings_content)

        # Generate main __init__.py with Settings class only
        init_content = self.extension_generator.generate_config_init(metadata)
        (pkg_dir / "config" / "__init__.py").write_text(init_content)

        # Generate separate config files for each component
        # Model configuration
        model_content = self.extension_generator.generate_model_config_file(metadata)
        (pkg_dir / "config" / "model.py").write_text(model_content)

        # Formatter configuration (required for ReActAgent)
        formatter_content = self.extension_generator.generate_formatter_config_file(metadata)
        (pkg_dir / "config" / "formatter.py").write_text(formatter_content)

        # Memory configuration
        memory_content = self.extension_generator.generate_memory_config_file(metadata)
        (pkg_dir / "config" / "memory.py").write_text(memory_content)

        # Toolkit configuration
        toolkit_content = self.extension_generator.generate_toolkit_config_file(metadata)
        (pkg_dir / "config" / "toolkit.py").write_text(toolkit_content)

        # Middleware manager (for auto-injection)
        middleware_content = self.extension_generator.generate_middleware_manager_file(metadata)
        (pkg_dir / "config" / "middleware.py").write_text(middleware_content)

        # Application lifecycle manager
        lifecycle_content = self.extension_generator.generate_lifecycle_manager_file(metadata)
        (pkg_dir / "config" / "lifecycle.py").write_text(lifecycle_content)

        # Hooks configuration (if enabled)
        if metadata.hooks:
            hooks_content = self.extension_generator.generate_hooks_file(metadata)
            (pkg_dir / "config" / "hooks.py").write_text(hooks_content)

        # RAG configuration (if enabled)
        if metadata.enable_rag:
            rag_content = self.extension_generator.generate_rag_config_file(metadata)
            (pkg_dir / "config" / "rag.py").write_text(rag_content)

        # Pipeline configuration (if enabled)
        if metadata.enable_pipeline:
            pipeline_content = self.extension_generator.generate_pipeline_config_file(metadata)
            (pkg_dir / "config" / "pipeline.py").write_text(pipeline_content)

    def _generate_examples(self, project_path: Path, metadata: AgentScopeMetadata):
        """Generate example usage files."""
        basic_template = '''"""
Basic usage example for {name}.

This example demonstrates how to use the agent to answer questions.
"""

import asyncio
from {package_name}.agents.react_agent import create_react_agent


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
        print("\\nUser:", question)
        response = await agent(question)
        print("Agent:", response)


if __name__ == "__main__":
    asyncio.run(main())
'''
        basic_example = basic_template.format(
            name=metadata.name,
            package_name=metadata.package_name
        )
        (project_path / "examples" / "basic_usage.py").write_text(basic_example)

        advanced_template = '''"""
Advanced multi-agent example for {name}.

This example demonstrates multi-agent collaboration.
"""

import asyncio
from agentscope.agent import ReActAgent
from {package_name}.config import get_model, get_memory, get_toolkit, get_formatter


async def main():
    """Run advanced multi-agent example."""
    # Create specialized agents
    researcher = ReActAgent(
        name="Researcher",
        sys_prompt="You are a research specialist. Find and analyze information.",
        model=get_model(),
        formatter=get_formatter(),
        memory=get_memory(),
        toolkit=get_toolkit(),
    )

    analyst = ReActAgent(
        name="Analyst",
        sys_prompt="You are an analyst. Synthesize information and provide insights.",
        model=get_model(),
        formatter=get_formatter(),
        memory=get_memory(),
        toolkit=get_toolkit(),
    )

    # Example workflow
    query = "What are the latest developments in AI?"

    print("\\nQuery:", query)
    print("\\n--- Researcher Agent ---")
    research_result = await researcher(query)
    print("Research result:", research_result)

    print("\\n--- Analyst Agent ---")
    analysis = await analyst("Analyze this research: " + str(research_result))
    print("Analysis:", analysis)


if __name__ == "__main__":
    asyncio.run(main())
'''
        advanced_example = advanced_template.format(
            name=metadata.name,
            package_name=metadata.package_name
        )
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

# Configure pip source (private package index) - optional
echo ""
echo "🔧 Pip source configuration (optional):"
echo "   If you use a private PyPI server:"
echo "   1. Edit pip-sources.ini to fill in your private PyPI URLs"
echo "   2. Run: ./scripts/setup-pip-source.sh"
echo "   3. Then re-run: pip install -r requirements.txt"

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

        # Generate pip source configuration script
        pip_source_script = '''#!/bin/bash
# Generate pip.conf from pip-sources.ini
#
# Usage:
#   ./scripts/setup-pip-source.sh              # Configure global pip (default)
#   ./scripts/setup-pip-source.sh --venv      # Configure venv pip (venv/pip.conf)
#
# The actual source of truth is pip-sources.ini - edit that file to change
# your private PyPI settings, then re-run this script to regenerate pip.conf.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INI_FILE="$PROJECT_DIR/pip-sources.ini"

# Resolve output pip.conf location
MODE="global"
for arg in "$@"; do
    case $arg in
        --venv) MODE="venv" ;;
        --help|-h)
            echo "Usage: $0 [--venv]"
            echo "  (no flag)  Configure global pip (${HOME}/.config/pip/pip.conf)"
            echo "  --venv     Configure venv pip (venv/pip.conf)"
            exit 0
            ;;
    esac
done

if [ "$MODE" = "venv" ]; then
    if [ ! -d "$PROJECT_DIR/venv" ]; then
        echo "❌ Error: venv not found at $PROJECT_DIR/venv"
        exit 1
    fi
    PIP_CONF="$PROJECT_DIR/venv/pip.conf"
else
    # Cross-platform global pip config dir
    if [ -n "$XDG_CONFIG_HOME" ]; then
        PIP_DIR="$XDG_CONFIG_HOME/pip"
    elif [ "$(uname)" = "Darwin" ]; then
        PIP_DIR="$HOME/Library/Application Support/pip"
    else
        PIP_DIR="$HOME/.config/pip"
    fi
    PIP_CONF="$PIP_DIR/pip.conf"
fi

# Parse pip-sources.ini
INDEX_URL=$(sed -n 's/^index_url *= *//p' "$INI_FILE" | tr -d ' "'  )
EXTRA_INDEX_URL=$(sed -n 's/^extra_index_url *= *//p' "$INI_FILE" | tr -d ' "')
TRUSTED_HOST=$(sed -n 's/^trusted_host *= *//p' "$INI_FILE" | tr -d ' "')

if [ -z "$INDEX_URL" ]; then
    echo "⚠️  index_url is empty in pip-sources.ini - skipping pip configuration."
    echo "   Edit pip-sources.ini and re-run this script to configure."
    exit 0
fi

# Auto-detect trusted host from index_url if not set
if [ -z "$TRUSTED_HOST" ]; then
    HOST_WITH_AUTH=$(echo "$INDEX_URL" | sed -E 's|^https?://||' | cut -d'/' -f1)
    TRUSTED_HOST=$(echo "$HOST_WITH_AUTH" | cut -d'@' -f2)
fi

# Ensure trusted hosts include any hosts from extra_index_url too
if [ -n "$EXTRA_INDEX_URL" ]; then
    EXTRA_HOST=$(echo "$EXTRA_INDEX_URL" | sed -E 's|^https?://||' | cut -d'/' -f1 | cut -d'@' -f2)
    # Deduplicate
    if [ -n "$EXTRA_HOST" ] && [ "$EXTRA_HOST" != "$TRUSTED_HOST" ]; then
        TRUSTED_HOST="$TRUSTED_HOST,$EXTRA_HOST"
    fi
fi

mkdir -p "$(dirname "$PIP_CONF")"

{
    echo "[global]"
    echo "index-url = $INDEX_URL"
    [ -n "$EXTRA_INDEX_URL" ] && echo "extra-index-url = $EXTRA_INDEX_URL"
    echo "trusted-host = $TRUSTED_HOST"
} > "$PIP_CONF"

echo "✅ pip.conf written to: $PIP_CONF"
cat "$PIP_CONF"
'''
        (project_path / "scripts" / "setup-pip-source.sh").write_text(pip_source_script)

        import stat
        pip_source_path = project_path / "scripts" / "setup-pip-source.sh"
        pip_source_path.chmod(pip_source_path.stat().st_mode | stat.S_IEXEC)

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
├── scripts/                     # Utility scripts (setup.sh, setup-pip-source.sh, etc.)
├── docs/                        # Documentation
├── requirements.txt             # Dependencies
└── .env.example                 # Environment template
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

        # Generate RAGAS evaluation module
        if metadata.enable_ragas_evaluation:
            self._generate_ragas_evaluation(project_path, metadata)

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

    def _generate_ragas_evaluation(
        self,
        project_path: Path,
        metadata: AgentScopeMetadata
    ):
        """Generate RAGAS evaluation module."""
        eval_dir = project_path / "evaluation"
        eval_dir.mkdir(exist_ok=True)

        # Generate __init__.py
        init_content = '''"""RAGAS Evaluation Module."""
__all__ = ["ragas_evaluator"]
'''
        (eval_dir / "__init__.py").write_text(init_content)

        # Generate evaluator script
        eval_code = self.extension_generator.generate_ragas_evaluation_code(metadata)
        (eval_dir / "ragas_evaluator.py").write_text(eval_code)

        # Generate requirements.txt
        requirements_content = self.extension_generator.generate_ragas_requirements(metadata)
        (eval_dir / "requirements.txt").write_text(requirements_content)

        # Generate README
        readme_content = self.extension_generator.generate_ragas_readme(metadata)
        (eval_dir / "README.md").write_text(readme_content)