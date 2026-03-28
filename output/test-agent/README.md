# test-agent

Test agent

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

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
test-agent/
├── test_agent/          # Package directory
│   ├── agents/              # Agent implementations
│   ├── tools/               # Custom tools
│   └── config/              # Configuration
├── tests/                   # Tests
├── main.py                  # Entry point
└── requirements.txt         # Dependencies
```

## AgentScope Configuration

- **Agent Type**: basic
- **Model Provider**: openai
- **Memory Type**: in-memory
- **Python Version**: 3.11

## License

MIT
