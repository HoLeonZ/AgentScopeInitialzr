# AgentScope Initializr - Project Structure

## Directory Structure

```
agentscope-initializr/
├── initializr-core/              # Core generation engine
│   └── initializr_core/
│       ├── __init__.py
│       ├── metadata/             # Metadata management
│       │   ├── __init__.py
│       │   ├── models.py         # Data models (AgentScopeMetadata, AgentType, etc.)
│       │   └── templates.py      # Template registry
│       ├── generator/            # Project generator
│       │   ├── __init__.py
│       │   ├── engine.py         # Main ProjectGenerator class
│       │   └── extensions.py     # Extension point generators
│       └── validator/            # Configuration validation
│           ├── __init__.py
│           └── validator.py      # MetadataValidator
│
├── initializr-cli/               # Command-line interface
│   └── initializr_cli/
│       ├── __init__.py
│       └── main.py               # Click-based CLI commands
│
├── initializr-templates/         # Project templates
│   ├── basic-agent/
│   │   └── main.py.jinja2        # Basic ReAct agent template
│   ├── multi-agent/
│   │   └── main.py.jinja2        # Multi-agent system template
│   ├── research-agent/
│   │   └── main.py.jinja2        # Research agent template
│   └── browser-agent/
│       └── main.py.jinja2        # Browser automation template
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_metadata.py          # Metadata model tests
│   ├── test_validator.py         # Validator tests
│   └── test_generator.py         # Generator tests
│
├── pyproject.toml                # Project configuration
├── requirements.txt              # Dependencies
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── ARCHITECTURE.md               # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## Component Overview

### 1. Core Module (`initializr-core`)

**Purpose:** Provides the core functionality for project generation.

**Key Classes:**
- `AgentScopeMetadata` - Data model for project configuration
- `TemplateRegistry` - Manages available project templates
- `ProjectGenerator` - Main engine that generates projects
- `ExtensionGenerator` - Generates AgentScope extension point code
- `MetadataValidator` - Validates project configuration

**Workflow:**
1. User provides metadata via CLI or API
2. MetadataValidator validates the configuration
3. TemplateRegistry selects appropriate template
4. ProjectGenerator creates project structure
5. ExtensionGenerator adds AgentScope-specific code

### 2. CLI Module (`initializr-cli`)

**Purpose:** Provides command-line interface for project creation.

**Commands:**
- `create` - Create a project with specified options
- `wizard` - Interactive project creation
- `list-templates` - List available templates
- `list-models` - List available model providers

**Usage Example:**
```bash
agentscope-init create --name my-agent --type basic --model openai
```

### 3. Templates (`initializr-templates`)

**Purpose:** Jinja2 templates for different agent types.

**Template Types:**
1. **basic-agent** - Single ReAct agent with tools
2. **multi-agent** - Multiple collaborating agents
3. **research-agent** - Agent with search capabilities
4. **browser-agent** - Agent with browser automation

**Template Variables:**
- `{{ name }}` - Project name
- `{{ description }}` - Project description
- `{{ package_name }}` - Python package name
- `{{ agent_type }}` - Agent type enum
- `{{ model_provider }}` - Model provider enum

### 4. Tests (`tests/`)

**Purpose:** Ensure code quality and correctness.

**Test Categories:**
- Unit tests for metadata models
- Validation tests
- Generator integration tests

**Running Tests:**
```bash
pytest tests/
```

## Data Flow

```
User Input (CLI/API)
    ↓
AgentScopeMetadata
    ↓
MetadataValidator
    ↓
TemplateRegistry
    ↓
ProjectGenerator
    ↓
ExtensionGenerator
    ↓
GeneratedProject
    ↓
ZIP File / Directory
```

## Extension Points Integration

The generator integrates with AgentScope's extension points:

1. **Model Layer** - Generates model configuration for selected provider
2. **Memory Layer** - Configures InMemoryMemory or Mem0LongTermMemory
3. **Tool Layer** - Sets up Toolkit with selected tools
4. **Formatter** - Chooses ChatFormatter or MultiAgentFormatter
5. **Hooks** - Adds agent lifecycle hooks if configured
6. **State Management** - Includes state persistence code

## Generated Project Structure

When a user creates a project, the following structure is generated:

```
my-agent/
├── my_agent/              # Python package
│   ├── __init__.py
│   ├── agents/           # Agent implementations
│   ├── tools/            # Custom tools
│   └── config/           # Configuration
│       └── __init__.py   # Generated config code
├── tests/                # Tests
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── pyproject.toml       # Project config
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Configuration Modules

The generated `config/__init__.py` includes:

1. **Settings Class** - Application settings
2. **get_model()** - Returns configured model instance
3. **get_memory()** - Returns configured memory instance
4. **get_toolkit()** - Returns configured toolkit
5. **get_formatter()** - Returns configured formatter

## Dependencies

### Core Dependencies
- `agentscope>=0.1.0` - AgentScope framework
- `click>=8.1.0` - CLI framework
- `jinja2>=3.1.0` - Template engine
- `python-dotenv>=1.0.0` - Environment variable management

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=23.0.0` - Code formatter
- `isort>=5.12.0` - Import sorter
- `mypy>=1.0.0` - Type checker

## Future Enhancements

### Planned Features
1. **Web UI** - FastAPI + Vue.js interface
2. **Custom Templates** - User-defined template support
3. **Template Gallery** - Community-contributed templates
4. **Advanced Extensions** - More AgentScope extension points
5. **CI/CD Integration** - GitHub Actions for testing
6. **Documentation Site** - Full documentation with examples

### Web UI Architecture (Planned)
```
initializr-web/
├── api/
│   └── main.py              # FastAPI backend
├── src/
│   ├── App.vue             # Main Vue component
│   ├── views/
│   │   └── ProjectGenerator.vue
│   └── components/
│       ├── AgentTypeSelector.vue
│       ├── ModelProviderSelector.vue
│       └── ExtensionConfig.vue
└── package.json
```

## Contributing

When contributing to AgentScope Initializr:

1. **Core Changes** - Modify `initializr-core/`
2. **CLI Changes** - Modify `initializr-cli/`
3. **New Templates** - Add to `initializr-templates/`
4. **Tests** - Add corresponding tests in `tests/`

## License

MIT License - see LICENSE file for details.
