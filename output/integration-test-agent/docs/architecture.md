# integration-test-agent Architecture

## Project Structure

```
integration-test-agent/
├── src/
│   └── integration_test_agent/          # Main package
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
2. **Development**: Modify code in `src/integration_test_agent/`
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
