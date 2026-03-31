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

        # Create subdirectories
        (pkg_dir / "agents").mkdir(exist_ok=True)
        (pkg_dir / "tools").mkdir(exist_ok=True)
        (pkg_dir / "prompts").mkdir(exist_ok=True)
        (pkg_dir / "config").mkdir(exist_ok=True)

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

        # Generate .gitignore
        gitignore = self._generate_gitignore()
        (project_path / ".gitignore").write_text(gitignore)

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

        # Generate tools files
        self._generate_tools(pkg_dir, metadata)

        # Generate prompts files
        self._generate_prompts(pkg_dir, metadata)

        # Generate config files
        self._generate_config(pkg_dir, metadata)

        # Generate examples
        self._generate_examples(project_path, metadata)

        # Generate scripts
        self._generate_scripts(project_path, metadata)

        # Generate docs
        self._generate_docs(project_path, metadata)

        # Generate main.py
        main_content = self._generate_main(metadata)
        main_path.write_text(main_content)

    def _generate_readme(self, metadata: AgentScopeMetadata, project_path: Path):
        """Generate README.md."""
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
python main.py
```

## Project Structure

```
{metadata.name}/
├── {metadata.package_name}/          # Package directory
│   ├── agents/              # Agent implementations
│   ├── tools/               # Custom tools
│   └── config/              # Configuration
├── tests/                   # Tests
├── main.py                  # Entry point
└── requirements.txt         # Dependencies
```

## AgentScope Configuration

- **Agent Type**: {metadata.agent_type.value}
- **Model Provider**: {metadata.model_provider.value}
- **Memory Type**: {metadata.memory_type.value}
- **Python Version**: {metadata.python_version}

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
requires-python = ">={metadata.python_version}"
dependencies = [
    "agentscope>=0.1.0",
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py310']

[tool.isort]
profile = "black"
line_length = 100
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
        return f'''"""
Main entry point for {metadata.name}.

This module initializes and runs the AgentScope agent.
"""

import asyncio
import os
from dotenv import load_dotenv

from {metadata.package_name}.config import settings, get_model, get_memory, get_toolkit
from agentscope.agent import ReActAgent

# Load environment variables
load_dotenv()


async def main():
    """Main entry point."""
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

    # Start interaction
    print(f"🤖 {metadata.name} is ready! Type 'exit' to quit.")
    print(f"   Agent Type: {metadata.agent_type.value}")
    print(f"   Model Provider: {metadata.model_provider.value}")
    print()

    while True:
        try:
            user_input = input("\\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            response = await agent(user_input)
            print(f"\\n{metadata.name}: {{response}}")

        except KeyboardInterrupt:
            print("\\nGoodbye!")
            break
        except Exception as e:
            print(f"\\nError: {{e}}")


if __name__ == "__main__":
    asyncio.run(main())
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
        (pkg_dir / "tools" / "__init__.py").write_text('"""Tool implementations."""\n')
        (pkg_dir / "prompts" / "__init__.py").write_text('"""Prompt templates."""\n')

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
        """Generate tool implementation files."""
        tools_content = '''"""
Custom tools for the agent.
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


@tool("get_current_time")
def get_current_time() -> str:
    """
    Get the current time.

    Returns:
        Current time as string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
'''
        (pkg_dir / "tools" / "custom_tools.py").write_text(tools_content)

    def _generate_prompts(self, pkg_dir: Path, metadata: AgentScopeMetadata):
        """Generate prompt template files."""
        prompts_content = f'''"""
System prompts for {metadata.name}.
"""

DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant powered by AgentScope.
You have access to various tools to help answer questions and complete tasks.
Think step-by-step and explain your reasoning.
"""

REACT_AGENT_PROMPT = """
You are a ReAct agent. Use the following format:

Thought: you should always think about what to do
Action: the action to take
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Available tools:
- calculate: Calculate mathematical expressions
- get_current_time: Get the current time
"""

MULTI_AGENT_COORDINATOR_PROMPT = """
You are a coordinator agent managing multiple specialized agents.
Your role is to:
1. Understand the user's request
2. Break down complex tasks into subtasks
3. Delegate subtasks to appropriate specialized agents
4. Synthesize results from multiple agents
5. Provide a cohesive final response
"""

RESEARCH_AGENT_PROMPT = """
You are a research agent specialized in finding and synthesizing information.
Your capabilities include:
- Searching for current information
- Analyzing multiple sources
- Synthesizing findings into coherent reports
- Citing sources appropriately
"""
'''
        (pkg_dir / "prompts" / "system_prompts.py").write_text(prompts_content)

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
        setup_script = '''#!/bin/bash
# Setup script for AgentScope project

echo "🚀 Setting up AgentScope project..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys"
fi

echo "✅ Setup complete! Activate your environment with: source venv/bin/activate"
'''
        (project_path / "scripts" / "setup.sh").write_text(setup_script)

        deploy_script = '''#!/bin/bash
# Deploy script for AgentScope project

echo "🚀 Deploying AgentScope project..."

# Run tests
echo "Running tests..."
pytest tests/ -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Aborting deployment."
    exit 1
fi

echo "✅ Deployment ready!"
'''
        (project_path / "scripts" / "deploy.sh").write_text(deploy_script)

    def _generate_docs(self, project_path: Path, metadata: AgentScopeMetadata):
        """Generate documentation files."""
        architecture_content = f'''# {metadata.name} Architecture

## Project Structure

```
{metadata.name}/
├── src/
│   └── {metadata.package_name}/          # Main package
│       ├── agents/              # Agent implementations
│       ├── tools/               # Custom tools
│       ├── prompts/             # Prompt templates
│       ├── config/              # Configuration
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
- **ReActAgent**: Basic reasoning-acting agent
- **Multi-Agent**: Specialized agents for different tasks

### Tool Layer
- **Calculator**: Mathematical calculations
- **Time**: Current time and date utilities

### Configuration Layer
- **Settings**: Application settings management
- **Models**: Model provider configuration
- **Memory**: Short and long-term memory management

### Extension Points
- **Hooks**: Agent lifecycle hooks
- **Middleware**: Request/response processing
- **Formatters**: Message formatting

## Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Extensibility**: Easy to add new agents, tools, and features
3. **Testability**: Comprehensive test coverage
4. **Documentation**: Clear documentation and examples

## Development Workflow

1. **Setup**: Run `./scripts/setup.sh`
2. **Development**: Modify code in `src/{metadata.package_name}/`
3. **Testing**: Run `pytest tests/`
4. **Examples**: Check `examples/` for usage patterns
5. **Deployment**: Run `./scripts/deploy.sh`

## Contributing

When adding new features:
1. Add agent in `agents/` directory
2. Add tools in `tools/` directory
3. Update prompts in `prompts/` directory
4. Add tests in `tests/` directory
5. Provide examples in `examples/` directory
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