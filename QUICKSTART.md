# AgentScope Initializr - Quick Start Guide

## Installation

```bash
pip install agentscope-initializr
```

## Create Your First Agent

### Option 1: Quick Command

```bash
agentscope-init create --name my-first-agent
```

### Option 2: Interactive Wizard

```bash
agentscope-init wizard --name my-first-agent
```

### Option 3: Custom Configuration

```bash
agentscope-init create \
  --name research-bot \
  --description "Agent that researches topics online" \
  --type research \
  --model openai \
  --memory long-term \
  --streaming
```

## Next Steps

1. **Navigate to your project:**
   ```bash
   cd my-first-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

5. **Run your agent:**
   ```bash
   python main.py
   ```

## Available Templates

| Template | Description | Use Case |
|----------|-------------|----------|
| `basic` | Basic ReAct Agent | Simple conversational agents |
| `multi-agent` | Multi-Agent System | Team of collaborating agents |
| `research` | Research Agent | Information gathering and analysis |
| `browser` | Browser Automation | Web interaction and scraping |

## Available Models

| Provider | Models |
|----------|--------|
| `openai` | GPT-4, GPT-3.5 |
| `dashscope` | Qwen (Alibaba Cloud) |
| `gemini` | Google Gemini |
| `anthropic` | Claude |
| `ollama` | Local LLMs |

## Example: Creating a Research Agent

```bash
agentscope-init create \
  --name research-assistant \
  --type research \
  --model openai \
  --memory long-term

cd research-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure your API keys in .env
echo "OPENAI_API_KEY=sk-xxx" > .env
echo "TAVILY_API_KEY=tvly-xxx" >> .env

# Run the agent
python main.py
```

## Getting Help

```bash
# List all commands
agentscope-init --help

# Get help for a specific command
agentscope-init create --help

# List available templates
agentscope-init list-templates

# List available models
agentscope-init list-models
```

## Troubleshooting

### Issue: Module not found

**Solution:** Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: API key errors

**Solution:** Check your `.env` file:
```bash
cat .env  # Verify your API keys are set
```

### Issue: Python version too old

**Solution:** Use Python 3.10 or newer:
```bash
python --version  # Should be >= 3.10
```

## Next Steps

- 📖 Read the [full documentation](README.md)
- 🤖 Learn about [AgentScope](https://doc.agentscope.io/)
- 💬 Join the [community](https://github.com/agentscope-ai/initializr/discussions)
