# AgentScope Initializr

A project scaffolding generator for [AgentScope](https://doc.agentscope.io/) applications, inspired by [Spring Boot Initializr](https://start.spring.io/).

## Features

- 🚀 **Quick Start** - Generate production-ready AgentScope projects in seconds
- 🎯 **Multiple Templates** - Pre-configured templates for common agent patterns
- 🔌 **Extension Integration** - Deep integration with AgentScope extension points
- 🛠️ **CLI & Web** - Use via command-line or web interface
- 📦 **Standardized Structure** - Follows AgentScope best practices

## Installation

```bash
# Install CLI only
pip install agentscope-initializr

# Install with web service support
pip install -e ".[web]"
```

## Quick Start

### Web Interface (Recommended)

1. **Using Docker (Recommended)**:
```bash
docker-compose up
```
Visit http://localhost:8000/docs for API docs

2. **Manual Installation**:
```bash
# Install with web dependencies
pip install -e ".[web]"

# Run web service
agentscope-web
```

Then visit http://localhost:8000 for the API or http://localhost:8000/docs for interactive documentation.

### Using CLI

Create a basic ReAct agent project:

```bash
agentscope-init create --name my-agent --type basic --model openai
```

Interactive wizard mode:

```bash
agentscope-init wizard --name my-agent
```

### Available Templates

1. **basic** - Basic ReAct Agent
   - Single agent with tool support
   - In-memory conversation history

2. **multi-agent** - Multi-Agent System
   - Multiple collaborating agents
   - Message hub and pipelines

3. **research** - Research Agent
   - Web search capabilities
   - Information aggregation

4. **browser** - Browser Automation Agent
   - Playwright integration
   - Web interaction and scraping

### Available Model Providers

- `openai` - OpenAI (GPT-4, GPT-3.5)
- `dashscope` - DashScope (Alibaba Cloud - Qwen)
- `gemini` - Google Gemini
- `anthropic` - Anthropic Claude
- `ollama` - Ollama (Local LLMs)

## Usage Examples

### Create a Basic Agent

```bash
agentscope-init create \
  --name my-assistant \
  --type basic \
  --model openai \
  --memory in-memory \
  --streaming
```

### Create a Research Agent

```bash
agentscope-init create \
  --name research-bot \
  --type research \
  --model openai \
  --memory long-term
```

### Create a Multi-Agent System

```bash
agentscope-init create \
  --name agent-team \
  --type multi-agent \
  --model dashscope
```

## After Generation

1. Navigate to your project:
   ```bash
   cd my-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run your agent:
   ```bash
   python main.py
   ```

## CLI Commands

### `create` - Create a new project

```bash
agentscope-init create [OPTIONS]
```

Options:
- `--name` - Project name (required)
- `--description` - Project description
- `--type` - Agent type (basic, multi-agent, research, browser)
- `--model` - Model provider (openai, dashscope, gemini, anthropic, ollama)
- `--memory` - Memory type (in-memory, long-term)
- `--output` - Output directory (default: current directory)
- `--python-version` - Minimum Python version (default: 3.10)
- `--streaming/--no-streaming` - Enable streaming (default: enabled)
- `--thinking/--no-thinking` - Enable thinking mode (default: disabled)

### `wizard` - Interactive project creation

```bash
agentscope-init wizard --name my-agent
```

Guides you through project creation with prompts.

### `list-templates` - List available templates

```bash
agentscope-init list-templates
```

### `list-models` - List available model providers

```bash
agentscope-init list-models
```

## Project Structure

Generated projects follow this structure:

```
my-agent/
├── my_agent/              # Package directory
│   ├── __init__.py
│   ├── agents/           # Agent implementations
│   ├── tools/            # Custom tools
│   └── config/           # Configuration
│       └── __init__.py
├── tests/                # Tests
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── pyproject.toml       # Project configuration
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## AgentScope Extension Points

AgentScope Initializr integrates with AgentScope's extension points:

### Model Layer
- Configured model provider (OpenAI, DashScope, etc.)
- Streaming support
- Usage tracking

### Memory Layer
- In-memory: `InMemoryMemory`
- Long-term: `Mem0LongTermMemory`

### Tool Layer
- Basic tools (Python execution, shell commands)
- MCP client integration
- Tool grouping

### Formatter
- Chat: `ChatFormatter`
- Multi-Agent: `MultiAgentFormatter`

### State Management
- Automatic state persistence
- Checkpoint and recovery

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/agentscope-ai/initializr.git
cd initializr

# Install with all dependencies
pip install -e ".[dev,web]"

# Run tests
pytest

# Format code
black .
isort .
```

### Web Development

**Backend (FastAPI)**:
```bash
cd initializr-web
uvicorn initializr_web.api:app --reload
```

**Frontend (Vue.js)**:
```bash
cd initializr-web/frontend
npm install
npm run dev
```

### Docker Development

```bash
# Build and run with Docker Compose
docker-compose up

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Adding Custom Templates

Custom templates can be added to `initializr-templates/`. Each template should include:

1. Template structure files
2. Metadata in `template.yaml`
3. Jinja2 templates for code generation

See existing templates for examples.

## Architecture

```
agentscope-initializr/
├── initializr-core/      # Core generation engine
│   ├── metadata/        # Metadata management
│   ├── generator/       # Project generator
│   └── validator/       # Configuration validator
├── initializr-cli/       # Command-line interface
├── initializr-web/       # Web interface
│   ├── initializr_web/  # FastAPI backend
│   ├── frontend/        # Vue.js 3 frontend
│   └── tests/           # Web service tests
└── initializr-templates/ # Project templates
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Inspired by [Spring Boot Initializr](https://github.com/spring-io/initializr)
- Built on top of [AgentScope](https://doc.agentscope.io/)
- Part of the AgentScope ecosystem

## Links

- [AgentScope Documentation](https://doc.agentscope.io/)
- [AgentScope GitHub](https://github.com/modelscope/agentscope)
- [AgentScope Paper](https://arxiv.org/html/2508.16279v1)
- [Web Service Guide](initializr-web/README.md)

## Support

- 📖 Documentation: https://doc.agentscope.io/
- 🐛 Issues: https://github.com/agentscope-ai/initializr/issues
- 💬 Discussions: https://github.com/agentscope-ai/initializr/discussions
