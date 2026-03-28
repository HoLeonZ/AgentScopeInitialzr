# AgentScope Initializr Web Service

Web interface for scaffolding AgentScope agent projects.

## Installation

```bash
pip install -e .
```

## Running

```bash
agentscope-web
```

Or with uvicorn directly:

```bash
uvicorn initializr_web.api:app --reload
```

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.
