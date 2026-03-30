# API Reference Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.agentscope-initializr.dev
```

## Authentication

Currently, the API does not require authentication. Future versions will support API keys and OAuth2.

## Content Type

All requests must use `Content-Type: application/json`.

## Response Format

All responses follow this structure:

```json
{
  "data": { ... },
  "success": true,
  "message": "Optional message"
}
```

Error responses:

```json
{
  "detail": "Error description",
  "success": false
}
```

---

## Endpoints

### 1. Health Check

#### GET /health

Basic health check endpoint for load balancers and monitoring systems.

**Request:**
```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "0.2.0"
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/health
```

---

#### GET /health/detailed

Detailed health check with system information.

**Request:**
```http
GET /health/detailed
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "0.2.0",
  "timestamp": "2026-03-27T10:30:00Z",
  "uptime_seconds": 3600,
  "system": {
    "python_version": "3.11.0",
    "platform": "Linux-5.15.0-x86_64"
  }
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/health/detailed
```

---

### 2. Templates

#### GET /api/v1/templates

Retrieve list of available project templates.

**Request:**
```http
GET /api/v1/templates
```

**Response (200 OK):**
```json
{
  "templates": [
    {
      "id": "basic",
      "name": "Basic ReAct Agent",
      "description": "Single agent with tool support and in-memory conversation history",
      "icon": "robot",
      "tags": ["beginner", "single-agent"],
      "suitable_for": ["Simple task automation", "Basic chatbots", "Tool integration"]
    },
    {
      "id": "multi-agent",
      "name": "Multi-Agent System",
      "description": "Multiple collaborating agents with message hub and pipelines",
      "icon": "users",
      "tags": ["advanced", "orchestration"],
      "suitable_for": ["Complex task decomposition", "Parallel processing", "Role-based agents"]
    },
    {
      "id": "research",
      "name": "Research Agent",
      "description": "Web search capabilities with information aggregation",
      "icon": "search",
      "tags": ["research", "web-scraping"],
      "suitable_for": ["Literature review", "Data collection", "Market research"]
    },
    {
      "id": "browser",
      "name": "Browser Automation Agent",
      "description": "Playwright integration for web interaction and scraping",
      "icon": "globe",
      "tags": ["automation", "browser"],
      "suitable_for": ["Web testing", "Form automation", "Data extraction"]
    }
  ]
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/templates
```

---

### 3. Model Providers

#### GET /api/v1/models

Retrieve list of supported model providers.

**Request:**
```http
GET /api/v1/models
```

**Response (200 OK):**
```json
{
  "providers": [
    {
      "id": "openai",
      "name": "OpenAI",
      "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
      "description": "OpenAI's GPT models",
      "requires_api_key": true,
      "config_schema": {
        "model": {
          "type": "string",
          "enum": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
          "default": "gpt-4"
        },
        "temperature": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 2.0,
          "default": 0.7
        },
        "max_tokens": {
          "type": "integer",
          "minimum": 1,
          "default": 2000
        }
      }
    },
    {
      "id": "dashscope",
      "name": "DashScope (Alibaba Cloud)",
      "models": ["qwen-turbo", "qwen-plus", "qwen-max"],
      "description": "Alibaba Cloud's Qwen models",
      "requires_api_key": true,
      "config_schema": {
        "model": {
          "type": "string",
          "enum": ["qwen-turbo", "qwen-plus", "qwen-max"],
          "default": "qwen-turbo"
        }
      }
    },
    {
      "id": "gemini",
      "name": "Google Gemini",
      "models": ["gemini-pro", "gemini-ultra"],
      "description": "Google's Gemini models",
      "requires_api_key": true
    },
    {
      "id": "anthropic",
      "name": "Anthropic Claude",
      "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
      "description": "Anthropic's Claude models",
      "requires_api_key": true
    },
    {
      "id": "ollama",
      "name": "Ollama (Local LLMs)",
      "models": ["llama2", "mistral", "codellama"],
      "description": "Run local LLMs via Ollama",
      "requires_api_key": false,
      "config_schema": {
        "base_url": {
          "type": "string",
          "default": "http://localhost:11434"
        }
      }
    }
  ]
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/models
```

---

### 4. Extensions

#### GET /api/v1/extensions

Retrieve available extension points and their options.

**Request:**
```http
GET /api/v1/extensions
```

**Response (200 OK):**
```json
{
  "memory": {
    "short_term": [
      {
        "id": "in-memory",
        "name": "In-Memory",
        "description": "Store conversation history in process memory"
      }
    ],
    "long_term": [
      {
        "id": "mem0",
        "name": "Mem0",
        "description": "Persistent long-term memory with Mem0",
        "requires_config": true
      }
    ]
  },
  "tools": [
    {
      "id": "execute_python_code",
      "name": "Execute Python Code",
      "description": "Execute Python code in a sandboxed environment",
      "category": "execution"
    },
    {
      "id": "web_search",
      "name": "Web Search",
      "description": "Search the web for information",
      "category": "search"
    },
    {
      "id": "shell_command",
      "name": "Shell Command",
      "description": "Execute shell commands",
      "category": "system"
    }
  ],
  "formatters": [
    {
      "id": "chat",
      "name": "Chat Formatter",
      "description": "Format messages for chat applications"
    },
    {
      "id": "multi-agent",
      "name": "Multi-Agent Formatter",
      "description": "Format messages for multi-agent systems"
    }
  ]
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/extensions
```

---

### 5. Project Generation

#### POST /api/v1/projects/generate

Generate a new AgentScope project based on configuration.

**Request:**
```http
POST /api/v1/projects/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "my-agent",
  "description": "My custom agent",
  "author": "Your Name",
  "layout": "standard",
  "agent_type": "basic",
  "model_provider": "openai",
  "model_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "enable_memory": true,
  "short_term_memory": "in-memory",
  "long_term_memory": null,
  "enable_tools": true,
  "tools": ["execute_python_code", "web_search"],
  "python_version": "3.11",
  "generate_tests": true
}
```

**Field Descriptions:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | - | Project name (1-100 chars, alphanumeric + hyphens) |
| `description` | string | No | "" | Project description |
| `author` | string | No | "" | Author name |
| `layout` | string | No | "standard" | Project layout ("standard" or "lightweight") |
| `agent_type` | string | No | "basic" | Agent template ID |
| `model_provider` | string | No | "openai" | Model provider ID |
| `model_config` | object | No | {} | Model-specific configuration |
| `enable_memory` | boolean | No | true | Enable memory extension |
| `short_term_memory` | string | No | "in-memory" | Short-term memory type |
| `long_term_memory` | string | No | null | Long-term memory type |
| `enable_tools` | boolean | No | true | Enable tool extension |
| `tools` | array | No | [] | List of tool IDs to include |
| `python_version` | string | No | "3.11" | Minimum Python version |
| `generate_tests` | boolean | No | true | Include test files |

**Response (200 OK):**
```json
{
  "success": true,
  "project_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "download_url": "/api/v1/projects/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Project generated successfully",
  "project": {
    "name": "my-agent",
    "type": "basic",
    "files_generated": 12
  }
}
```

**Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Failed to generate project: Template rendering error"
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/projects/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-agent",
    "agent_type": "basic",
    "model_provider": "openai"
  }'
```

---

### 6. Project Download

#### GET /api/v1/projects/download/{project_id}

Download a generated project as a ZIP file.

**Request:**
```http
GET /api/v1/projects/download/{project_id}
```

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string (UUID) | Yes | Unique project identifier from generation response |

**Response (200 OK):**
```
Content-Type: application/zip
Content-Disposition: attachment; filename="my-agent.zip"

<BINARY ZIP DATA>
```

**Response (404 Not Found):**
```json
{
  "detail": "Project not found or has expired"
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/projects/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  --output my-agent.zip
```

**PowerShell Example:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890" `
  -OutFile "my-agent.zip"
```

---

## Error Codes

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 200 | - | Success |
| 400 | BadRequest | Invalid request format |
| 404 | NotFound | Resource not found |
| 422 | ValidationError | Request validation failed |
| 500 | InternalServerError | Server error during processing |

---

## Rate Limiting

Currently, there are no rate limits. Future versions will implement:

- Anonymous: 10 requests/minute
- Authenticated: 100 requests/minute

Rate limit headers will be included:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## CORS Policy

**Development:**
```
Allow-Origins: http://localhost:5173, http://localhost:8080
Allow-Methods: GET, POST, OPTIONS
Allow-Headers: Content-Type, Authorization
```

**Production:**
```
Allow-Origins: https://agentscope-initializr.dev
Allow-Methods: GET, POST, OPTIONS
Allow-Headers: Content-Type, Authorization
```

---

## SDK Examples

### Python

```python
import requests

API_BASE = "http://localhost:8000"

# Generate project
response = requests.post(
    f"{API_BASE}/api/v1/projects/generate",
    json={
        "name": "my-agent",
        "agent_type": "basic",
        "model_provider": "openai"
    }
)

if response.status_code == 200:
    data = response.json()
    project_id = data["project_id"]

    # Download project
    download_response = requests.get(
        f"{API_BASE}{data['download_url']}"
    )

    with open("my-agent.zip", "wb") as f:
        f.write(download_response.content)
```

### JavaScript (Axios)

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// Generate project
const response = await axios.post(`${API_BASE}/api/v1/projects/generate`, {
  name: 'my-agent',
  agent_type: 'basic',
  model_provider: 'openai'
});

const { project_id, download_url } = response.data;

// Download project
const downloadResponse = await axios.get(`${API_BASE}${download_url}`, {
  responseType: 'blob'
});

// Save file (browser)
const url = window.URL.createObjectURL(new Blob([downloadResponse.data]));
const link = document.createElement('a');
link.href = url;
link.setAttribute('download', 'my-agent.zip');
document.body.appendChild(link);
link.click();
```

### TypeScript

```typescript
import axios from 'axios';

interface ProjectRequest {
  name: string;
  agent_type?: string;
  model_provider?: string;
  // ... other fields
}

interface GenerateResponse {
  success: boolean;
  project_id: string;
  download_url: string;
}

const API_BASE = 'http://localhost:8000';

async function generateProject(config: ProjectRequest): Promise<void> {
  const { data } = await axios.post<GenerateResponse>(
    `${API_BASE}/api/v1/projects/generate`,
    config
  );

  const response = await axios.get(
    `${API_BASE}${data.download_url}`,
    { responseType: 'blob' }
  );

  // Handle blob...
}
```

---

## Changelog

### Version 1.0 (2026-03-27)
- Initial API release
- Health check endpoints
- Template, model, and extension listing
- Project generation and download
- Pydantic validation

---

**Document Version**: 1.0
**Last Updated**: 2026-03-27
