"""
AgentScope Initializr CLI

Command-line interface for generating AgentScope projects.
"""

import click
import sys
from pathlib import Path
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ModelProvider,
    MemoryType,
    ProjectLayout,
)
from initializr_core.generator.engine import ProjectGenerator


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    AgentScope Initializr CLI

    Quickstart generator for AgentScope projects.
    """
    pass


@cli.command()
@click.option(
    '--name',
    required=True,
    help='Project name'
)
@click.option(
    '--description',
    default='',
    help='Project description'
)
@click.option(
    '--type',
    'agent_type',
    type=click.Choice(['basic', 'multi-agent', 'research', 'browser']),
    default='basic',
    help='Agent type'
)
@click.option(
    '--model',
    'model_provider',
    type=click.Choice(['openai', 'dashscope', 'gemini', 'anthropic', 'ollama']),
    default='openai',
    help='Model provider'
)
@click.option(
    '--memory',
    'memory_type',
    type=click.Choice(['in-memory', 'long-term']),
    default='in-memory',
    help='Memory type'
)
@click.option(
    '--output',
    default='.',
    help='Output directory',
    type=click.Path(exists=True)
)
@click.option(
    '--python-version',
    default='3.10',
    help='Minimum Python version'
)
@click.option(
    '--streaming/--no-streaming',
    default=True,
    help='Enable streaming responses'
)
@click.option(
    '--thinking/--no-thinking',
    default=False,
    help='Enable thinking mode'
)
@click.option(
    '--layout',
    type=click.Choice(['standard', 'lightweight']),
    default='standard',
    help='Project layout: standard (src/) or lightweight (root)'
)
def create(
    name,
    description,
    agent_type,
    model_provider,
    memory_type,
    output,
    python_version,
    streaming,
    thinking,
    layout
):
    """
    Create a new AgentScope project.

    Example:
        agentscope-init create --name my-agent --type basic --model openai
    """
    try:
        # Create metadata
        metadata = AgentScopeMetadata(
            name=name,
            description=description or f"An AgentScope {agent_type} project",
            agent_type=AgentType(agent_type),
            model_provider=ModelProvider(model_provider),
            memory_type=MemoryType(memory_type),
            python_version=python_version,
            enable_streaming=streaming,
            enable_thinking=thinking,
            layout=ProjectLayout(layout),
        )

        # Generate project
        click.echo(f"🚀 Generating AgentScope project: {name}")
        click.echo(f"   Type: {agent_type}")
        click.echo(f"   Model: {model_provider}")
        click.echo()

        generator = ProjectGenerator(output_dir=output)
        project = generator.generate(metadata)

        # Create ZIP file
        project.create_zip()

        click.echo(f"✅ Project generated successfully!")
        click.echo()
        click.echo(f"📁 Location: {project.path}")
        click.echo(f"📦 Archive: {project.zip_path}")
        click.echo()
        click.echo("🚀 Quick start:")
        click.echo(f"   cd {name}")
        click.echo(f"   ./scripts/setup.sh  # or manually: python -m venv venv && source venv/bin/activate")
        click.echo(f"   pip install -r requirements.txt")
        click.echo(f"   cp .env.example .env")
        click.echo(f"   # Edit .env with your API keys")

        if layout == "standard":
            click.echo(f"   python -m {metadata.package_name}.main")
        else:
            click.echo(f"   python main.py")

        click.echo()
        click.echo("📖 Examples:")
        click.echo(f"   python examples/basic_usage.py")
        click.echo(f"   python examples/advanced_multiagent.py")
        click.echo()

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def list_templates():
    """List available project templates."""
    from initializr_core.metadata.templates import TemplateRegistry

    registry = TemplateRegistry()
    templates = registry.list_templates()

    click.echo("Available templates:")
    click.echo()

    for template in templates:
        click.echo(f"  {template.template_id:12} - {template.name}")
        click.echo(f"                {template.description}")
        click.echo()


@cli.command()
def list_models():
    """List available model providers."""
    click.echo("Available model providers:")
    click.echo()

    providers = [
        ("openai", "OpenAI (GPT-4, GPT-3.5)"),
        ("dashscope", "DashScope (Alibaba Cloud - Qwen)"),
        ("gemini", "Google Gemini"),
        ("anthropic", "Anthropic Claude"),
        ("ollama", "Ollama (Local LLMs)"),
    ]

    for provider_id, description in providers:
        click.echo(f"  {provider_id:12} - {description}")
    click.echo()


@cli.command()
@click.option('--name', required=True, help='Project name')
def wizard(name):
    """
    Interactive project creation wizard.

    Guides you through creating an AgentScope project with prompts.
    """
    click.echo(f"🧙 Welcome to AgentScope Initializr Wizard!")
    click.echo(f"Let's create your project: {name}")
    click.echo()

    # Get project description
    description = click.prompt("Project description", default="")

    # Select agent type
    click.echo()
    click.echo("Select agent type:")
    click.echo("  1. basic        - Basic ReAct Agent")
    click.echo("  2. multi-agent  - Multi-Agent System")
    click.echo("  3. research     - Research Agent")
    click.echo("  4. browser      - Browser Automation")

    agent_type_map = {
        "1": "basic",
        "2": "multi-agent",
        "3": "research",
        "4": "browser",
    }
    agent_type_choice = click.prompt(
        "Agent type",
        type=click.Choice(["1", "2", "3", "4"]),
        show_choices=False
    )
    agent_type = agent_type_map[agent_type_choice]

    # Select model provider
    click.echo()
    click.echo("Select model provider:")
    click.echo("  1. openai      - OpenAI (GPT-4)")
    click.echo("  2. dashscope   - DashScope (Qwen)")
    click.echo("  3. gemini      - Google Gemini")
    click.echo("  4. anthropic   - Anthropic Claude")
    click.echo("  5. ollama      - Ollama (Local)")

    model_map = {
        "1": "openai",
        "2": "dashscope",
        "3": "gemini",
        "4": "anthropic",
        "5": "ollama",
    }
    model_choice = click.prompt(
        "Model provider",
        type=click.Choice(["1", "2", "3", "4", "5"]),
        show_choices=False,
        default="1"
    )
    model_provider = model_map[model_choice]

    # Select memory type
    click.echo()
    memory_type = click.prompt(
        "Memory type",
        type=click.Choice(["in-memory", "long-term"]),
        default="in-memory"
    )

    # Enable streaming?
    click.echo()
    streaming = click.confirm("Enable streaming responses?", default=True)

    # Select project layout
    click.echo()
    click.echo("Select project layout:")
    click.echo("  1. standard     - Standard src/ layout (recommended)")
    click.echo("  2. lightweight  - Lightweight root layout")

    layout_map = {
        "1": "standard",
        "2": "lightweight",
    }
    layout_choice = click.prompt(
        "Project layout",
        type=click.Choice(["1", "2"]),
        show_choices=False,
        default="1"
    )
    layout = layout_map[layout_choice]

    # Summary
    click.echo()
    click.echo("📋 Project Summary:")
    click.echo(f"   Name: {name}")
    click.echo(f"   Type: {agent_type}")
    click.echo(f"   Model: {model_provider}")
    click.echo(f"   Memory: {memory_type}")
    click.echo(f"   Layout: {layout}")
    click.echo(f"   Streaming: {streaming}")
    click.echo()

    if not click.confirm("Generate project?"):
        click.echo("Cancelled.")
        return

    # Create metadata
    metadata = AgentScopeMetadata(
        name=name,
        description=description,
        agent_type=AgentType(agent_type),
        model_provider=ModelProvider(model_provider),
        memory_type=MemoryType(memory_type),
        enable_streaming=streaming,
        layout=ProjectLayout(layout),
    )

    # Generate project
    try:
        click.echo()
        click.echo(f"🚀 Generating project...")

        generator = ProjectGenerator()
        project = generator.generate(metadata)
        project.create_zip()

        click.echo(f"✅ Project generated successfully!")
        click.echo()
        click.echo(f"📁 Location: {project.path}")
        click.echo()
        click.echo("🚀 Next steps:")
        click.echo(f"   cd {name}")
        click.echo(f"   ./scripts/setup.sh  # or: python -m venv venv && source venv/bin/activate")
        click.echo(f"   pip install -r requirements.txt")
        click.echo(f"   cp .env.example .env")

        if layout == "standard":
            click.echo(f"   python -m {metadata.package_name}.main")
        else:
            click.echo(f"   python main.py")

        click.echo()
        click.echo("📖 Try the examples:")
        click.echo(f"   python examples/basic_usage.py")
        click.echo(f"   python examples/advanced_multiagent.py")
        click.echo()

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
