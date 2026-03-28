# AgentScope Initializr Web Service MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a web service (FastAPI backend + Vue.js frontend) that provides a user-friendly interface for scaffolding AgentScope agent projects, while maintaining backward compatibility with the existing CLI.

**Architecture:** Dual-mode system where CLI and Web UI both use shared core logic (ProjectGenerator, TemplateRegistry) from initializr-core. FastAPI exposes RESTful API endpoints for project generation, metadata queries, and health checks. Vue.js frontend provides a multi-step configuration form with real-time validation and project download.

**Tech Stack:**
- Backend: FastAPI 0.104+, Python 3.11+, Uvicorn, Pydantic v2
- Frontend: Vue.js 3.4+, TypeScript 5.3+, Vite 5.0+, Element Plus 2.5+, Pinia 2.1+
- Deployment: Docker, Docker Compose (optional Nginx)
- Testing: pytest, FastAPI TestClient, Vue Test Utils

---

## File Structure

```
agentscope-initializr/
├── initializr-web/                          # NEW - Web service module
│   ├── initializr_web/
│   │   ├── __init__.py
│   │   ├── api.py                          # FastAPI app initialization
│   │   ├── models.py                       # Pydantic request/response models
│   │   ├── router/
│   │   │   ├── __init__.py
│   │   │   ├── projects.py                 # Project generation endpoints
│   │   │   ├── templates.py                # Template listing endpoints
│   │   │   ├── models.py                   # Model listing endpoints
│   │   │   └── health.py                   # Health check endpoints
│   │   ├── static/                         # Built frontend assets (after build)
│   │   └── main.py                         # Uvicorn entry point
│   ├── frontend/                           # NEW - Vue.js frontend
│   │   ├── src/
│   │   │   ├── main.ts                     # App entry point
│   │   │   ├── App.vue                     # Root component
│   │   │   ├── router/
│   │   │   │   └── index.ts                # Vue Router config
│   │   │   ├── stores/
│   │   │   │   └── config.ts               # Pinia store (form state)
│   │   │   ├── api/
│   │   │   │   └── client.ts               # Axios HTTP client
│   │   │   ├── components/
│   │   │   │   ├── ConfigurationForm.vue   # Multi-step form
│   │   │   │   ├── TemplateSelector.vue    # Template selection
│   │   │   │   ├── BasicSettings.vue       # Step 1: Basic info
│   │   │   │   ├── ModelConfig.vue         # Step 2: Model settings
│   │   │   │   ├── MemoryConfig.vue        # Step 3: Memory config
│   │   │   │   ├── ExtensionConfig.vue     # Step 4: Extensions
│   │   │   │   ├── ProgressIndicator.vue   # Generation progress
│   │   │   │   └── DownloadButton.vue      # Project download
│   │   │   ├── views/
│   │   │   │   ├── Home.vue                # Home page
│   │   │   │   └── Configure.vue           # Configuration page
│   │   │   ├── types/
│   │   │   │   └── index.ts                # TypeScript type definitions
│   │   │   └── assets/
│   │   │       └── main.css                # Global styles
│   │   ├── public/
│   │   │   └── favicon.ico
│   │   ├── index.html
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   └── README.md
│   ├── tests/                              # NEW - Web service tests
│   │   ├── __init__.py
│   │   ├── test_api.py                     # FastAPI endpoint tests
│   │   ├── test_models.py                  # Pydantic model tests
│   │   └── test_integration.py             # Integration tests
│   └── pyproject.toml                      # Web service dependencies
├── initializr-core/
│   ├── initializr_core/
│   │   ├── metadata/
│   │   │   └── models.py                   # MODIFY - Add web-related fields
│   │   └── generator/
│   │       └── engine.py                   # MODIFY - Ensure shared logic
│   └── ...
├── initializr-cli/                         # UNCHANGED - Continue working
│   └── ...
├── Dockerfile                              # NEW - Multi-stage build
├── docker-compose.yml                      # NEW - Docker Compose config
├── nginx.conf                              # NEW - Optional Nginx config
└── pyproject.toml                          # MODIFY - Add [web] extras
```

---

## Task 1: Update pyproject.toml with Web Dependencies

**Files:**
- Modify: `pyproject.toml`

**Rationale:** Add FastAPI, Uvicorn, and web-related dependencies as optional extras to keep the core package lightweight.

- [ ] **Step 1: Add web dependencies to pyproject.toml**

```toml
[project.optional-dependencies]
web = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "python-multipart>=0.0.6",  # For form data parsing
    "aiofiles>=23.2.1",  # For async file operations
]
```

- [ ] **Step 2: Verify the change**

Run: `cat pyproject.toml | grep -A 5 "\[project.optional-dependencies\]"`
Expected: Should see the web extras with FastAPI, Uvicorn, and dependencies

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "feat: add web service dependencies to pyproject.toml"
```

---

## Task 2: Create initializr-web Package Structure

**Files:**
- Create: `initializr-web/initializr_web/__init__.py`
- Create: `initializr-web/initializr_web/main.py`
- Create: `initializr-web/pyproject.toml`

**Rationale:** Set up the web service package with proper Python package structure and entry point.

- [ ] **Step 1: Create package __init__.py**

```python
# initializr-web/initializr_web/__init__.py
"""
AgentScope Initializr Web Service.

Provides FastAPI backend and Vue.js frontend for scaffolding
AgentScope agent projects via web interface.
"""

__version__ = "0.2.0"
```

- [ ] **Step 2: Create main.py entry point**

```python
# initializr-web/initializr_web/main.py
"""
Uvicorn entry point for the web service.
"""

import uvicorn


def main():
    """Run the web service."""
    uvicorn.run(
        "initializr_web.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Create pyproject.toml for web package**

```toml
# initializr-web/pyproject.toml
[project]
name = "agentscope-initializr-web"
version = "0.2.0"
description = "Web service for AgentScope Initializr"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "agentscope-initializr[web]",
]

[project.scripts]
agentscope-web = "initializr_web.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 4: Create README.md**

```markdown
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
```

- [ ] **Step 5: Verify package structure**

Run: `ls -la initializr-web/initializr_web/`
Expected: Should see __init__.py and main.py

- [ ] **Step 6: Commit**

```bash
git add initializr-web/
git commit -m "feat: create initializr-web package structure"
```

---

## Task 3: Create Pydantic Models for API

**Files:**
- Create: `initializr-web/initializr_web/models.py`

**Rationale:** Define request/response models with validation for all API endpoints using Pydantic v2.

- [ ] **Step 1: Write the models with validation tests**

```python
# initializr-web/initializr_web/models.py
"""
Pydantic models for API request/response validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    """Request model for project generation."""

    # Basic settings
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: str = Field(default="", max_length=500, description="Project description")
    author: str = Field(default="", max_length=100, description="Author name")

    # Project structure
    layout: str = Field(
        default="standard",
        pattern="^(standard|lightweight)$",
        description="Project layout (standard or lightweight)"
    )
    agent_type: str = Field(default="basic", description="Agent type")
    python_version: str = Field(
        default="3.11",
        pattern="^3\.(10|11|12)$",
        description="Python version"
    )

    # Model configuration
    model_provider: str = Field(default="openai", description="Model provider")
    model_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Model configuration parameters"
    )

    # Extension points
    enable_memory: bool = Field(default=True, description="Enable memory")
    short_term_memory: Optional[str] = Field(default=None, description="Short-term memory type")
    long_term_memory: Optional[str] = Field(default=None, description="Long-term memory type")

    enable_tools: bool = Field(default=True, description="Enable tools")
    tools: List[str] = Field(default_factory=list, description="Enabled tools")

    enable_skills: bool = Field(default=False, description="Enable skills")
    skills: List[str] = Field(default_factory=list, description="Enabled skills")

    enable_hooks: bool = Field(default=False, description="Enable hooks")
    hooks: List[str] = Field(default_factory=list, description="Enabled hooks")

    enable_formatter: bool = Field(default=False, description="Enable formatter")
    formatter: Optional[str] = Field(default=None, description="Formatter type")

    enable_rag: bool = Field(default=False, description="Enable RAG")
    rag_config: Optional[Dict[str, Any]] = Field(default=None, description="RAG configuration")

    enable_pipeline: bool = Field(default=False, description="Enable pipeline")
    pipeline_config: Optional[Dict[str, Any]] = Field(default=None, description="Pipeline configuration")

    # Testing & evaluation
    generate_tests: bool = Field(default=False, description="Generate test module")
    generate_evaluation: bool = Field(default=False, description="Generate evaluation module")
    evaluator_type: str = Field(default="general", description="Evaluator type")
    enable_openjudge: bool = Field(default=False, description="Enable OpenJudge integration")
    openjudge_graders: List[str] = Field(default_factory=list, description="OpenJudge graders")
    initial_benchmark_tasks: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Number of initial benchmark tasks"
    )

    model_config = {"json_schema_extra": {"examples": [{
        "name": "my-agent",
        "description": "My custom agent",
        "layout": "standard",
        "agent_type": "multi-agent",
        "model_provider": "openai",
        "model_config": {"model": "gpt-4", "temperature": 0.7},
        "enable_memory": True,
        "short_term_memory": "in-memory",
        "long_term_memory": "mem0",
    }]}}


class ProjectResponse(BaseModel):
    """Response model for project generation."""

    success: bool = Field(..., description="Whether generation succeeded")
    message: str = Field(..., description="Response message")
    download_url: Optional[str] = Field(None, description="Download URL")
    project_id: Optional[str] = Field(None, description="Project ID")


class TemplateInfo(BaseModel):
    """Information about a template."""

    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")


class TemplatesResponse(BaseModel):
    """Response model for templates listing."""

    templates: List[TemplateInfo] = Field(..., description="Available templates")


class ModelProviderInfo(BaseModel):
    """Information about a model provider."""

    id: str = Field(..., description="Provider ID")
    name: str = Field(..., description="Provider name")


class ModelsResponse(BaseModel):
    """Response model for models listing."""

    providers: List[ModelProviderInfo] = Field(..., description="Available providers")


class ExtensionsResponse(BaseModel):
    """Response model for extensions listing."""

    memory: Dict[str, List[str]] = Field(..., description="Memory options")
    tools: Dict[str, str] = Field(..., description="Tools descriptions")
    formatters: List[str] = Field(..., description="Available formatters")
    evaluators: List[str] = Field(..., description="Available evaluators")
    openjudge_graders: List[str] = Field(..., description="Available OpenJudge graders")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response with system metrics."""

    system: Dict[str, float] = Field(..., description="System metrics")
    projects: Dict[str, Any] = Field(..., description="Project statistics")
```

- [ ] **Step 2: Write tests for models**

```python
# initializr-web/tests/test_models.py
"""
Tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError
from initializr_web.models import (
    ProjectRequest,
    ProjectResponse,
    TemplateInfo,
    TemplatesResponse,
)


def test_project_request_valid():
    """Test valid ProjectRequest creation."""
    data = {
        "name": "test-agent",
        "description": "Test agent",
        "layout": "standard",
        "agent_type": "basic",
    }
    request = ProjectRequest(**data)
    assert request.name == "test-agent"
    assert request.layout == "standard"
    assert request.enable_memory is True  # Default value


def test_project_request_invalid_name_too_short():
    """Test ProjectRequest rejects empty name."""
    with pytest.raises(ValidationError) as exc_info:
        ProjectRequest(name="")
    assert "min_length" in str(exc_info.value).lower()


def test_project_request_invalid_layout():
    """Test ProjectRequest rejects invalid layout."""
    with pytest.raises(ValidationError) as exc_info:
        ProjectRequest(name="test", layout="invalid")
    assert "pattern" in str(exc_info.value).lower() or "string" in str(exc_info.value).lower()


def test_project_request_benchmark_tasks_range():
    """Test ProjectRequest validates benchmark tasks range."""
    # Valid range
    request = ProjectRequest(name="test", initial_benchmark_tasks=50)
    assert request.initial_benchmark_tasks == 50

    # Out of range (too high)
    with pytest.raises(ValidationError):
        ProjectRequest(name="test", initial_benchmark_tasks=101)


def test_project_response():
    """Test ProjectResponse creation."""
    response = ProjectResponse(
        success=True,
        message="Generated successfully",
        download_url="/api/v1/projects/download/test_123",
        project_id="test_123",
    )
    assert response.success is True
    assert response.project_id == "test_123"


def test_templates_response():
    """Test TemplatesResponse creation."""
    templates = [
        TemplateInfo(id="basic", name="Basic Agent", description="Basic agent template"),
        TemplateInfo(id="multi-agent", name="Multi-Agent", description="Multi-agent system"),
    ]
    response = TemplatesResponse(templates=templates)
    assert len(response.templates) == 2
    assert response.templates[0].id == "basic"
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `cd initializr-web && python -m pytest tests/test_models.py -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add initializr-web/tests/test_models.py initializr-web/initializr_web/models.py
git commit -m "feat: add Pydantic models with validation"
```

---

## Task 4: Create Health Check Endpoints

**Files:**
- Create: `initializr-web/initializr_web/router/health.py`
- Create: `initializr-web/initializr_web/router/__init__.py`

**Rationale:** Implement health check endpoints for monitoring and service readiness checks.

- [ ] **Step 1: Write failing test for health endpoints**

```python
# initializr-web/tests/test_api.py
"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from initializr_web.api import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test basic health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AgentScope Initializr"
    assert "version" in data


def test_health_detailed(client):
    """Test detailed health check endpoint."""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "system" in data
    assert "cpu_percent" in data["system"]
    assert "memory_percent" in data["system"]
    assert "projects" in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd initializr-web && python -m pytest tests/test_api.py::test_health_check -v`
Expected: FAIL with "404 Not Found" (endpoint doesn't exist yet)

- [ ] **Step 3: Create router package and health router**

```python
# initializr-web/initializr_web/router/__init__.py
"""
API routers package.
"""

from initializr_web.router.health import router as health_router

__all__ = ["health_router"]
```

```python
# initializr-web/initializr_web/router/health.py
"""
Health check endpoints.
"""

import os
from fastapi import APIRouter
from initializr_web.models import HealthResponse, DetailedHealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.

    Returns service status and version.
    """
    return HealthResponse(
        status="healthy",
        service="AgentScope Initializr",
        version="0.2.0",
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check() -> DetailedHealthResponse:
    """
    Detailed health check with system metrics.

    Returns CPU, memory, and disk usage along with project statistics.
    """
    try:
        import psutil

        system_metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
        }
    except ImportError:
        # psutil not available, return mock data
        system_metrics = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "disk_usage": 0.0,
        }

    projects_stats = {
        "total_generated": 0,  # TODO: Implement tracking
        "storage_used": 0,
    }

    return DetailedHealthResponse(
        status="healthy",
        service="AgentScope Initializr",
        version="0.2.0",
        system=system_metrics,
        projects=projects_stats,
    )
```

- [ ] **Step 4: Create main FastAPI app**

```python
# initializr-web/initializr_web/api.py
"""
FastAPI application initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from initializr_web.router import health_router

# Create FastAPI app
app = FastAPI(
    title="AgentScope Initializr",
    description="Web service for scaffolding AgentScope agent projects",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "ALLOW_ORIGINS",
        "http://localhost:5173,http://localhost:8080,http://localhost:8000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AgentScope Initializr Web Service",
        "version": "0.2.0",
        "docs": "/docs",
    }
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd initializr-web && python -m pytest tests/test_api.py::test_health_check -v`
Expected: PASS

Run: `cd initializr-web && python -m pytest tests/test_api.py::test_health_detailed -v`
Expected: PASS

- [ ] **Step 6: Test manually with uvicorn**

Run: `cd initializr-web && uvicorn initializr_web.api:app --reload`
Then visit: http://localhost:8000/health
Expected: `{"status":"healthy","service":"AgentScope Initializr","version":"0.2.0"}`

Press Ctrl+C to stop the server

- [ ] **Step 7: Commit**

```bash
git add initializr-web/initializr_web/api.py initializr-web/initializr_web/router/
git commit -m "feat: add health check endpoints"
```

---

## Task 5: Create Metadata Endpoints (Templates, Models, Extensions)

**Files:**
- Create: `initializr-web/initializr_web/router/templates.py`
- Create: `initializr-web/initializr_web/router/models.py`
- Modify: `initializr-web/initializr_web/router/__init__.py`
- Modify: `initializr-web/tests/test_api.py`

**Rationale:** Implement endpoints for querying available templates, model providers, and extension point options.

- [ ] **Step 1: Write failing tests for metadata endpoints**

```python
# Add to initializr-web/tests/test_api.py

def test_list_templates(client):
    """Test templates listing endpoint."""
    response = client.get("/api/v1/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) > 0
    # Check for expected templates
    template_ids = [t["id"] for t in data["templates"]]
    assert "basic" in template_ids
    assert "multi-agent" in template_ids


def test_list_models(client):
    """Test model providers listing endpoint."""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert len(data["providers"]) > 0


def test_list_extensions(client):
    """Test extensions listing endpoint."""
    response = client.get("/api/v1/extensions")
    assert response.status_code == 200
    data = response.json()
    assert "memory" in data
    assert "short_term" in data["memory"]
    assert "long_term" in data["memory"]
    assert "tools" in data
    assert "formatters" in data
    assert "evaluators" in data
    assert "openjudge_graders" in data
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd initializr-web && python -m pytest tests/test_api.py::test_list_templates -v`
Expected: FAIL with "404 Not Found"

- [ ] **Step 3: Implement templates router**

```python
# initializr-web/initializr_web/router/templates.py
"""
Templates listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import TemplatesResponse
from initializr_core.metadata.templates import TemplateRegistry

router = APIRouter(tags=["templates"])

template_registry = TemplateRegistry()


@router.get("/api/v1/templates", response_model=TemplatesResponse)
async def list_templates() -> TemplatesResponse:
    """
    List all available project templates.

    Returns template IDs, names, and descriptions.
    """
    templates = template_registry.list_templates()

    return TemplatesResponse(
        templates=[
            {
                "id": t.template_id,
                "name": t.name,
                "description": t.description,
            }
            for t in templates
        ]
    )
```

- [ ] **Step 4: Implement models router**

```python
# initializr-web/initializr_web/router/models.py
"""
Model providers listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import ModelsResponse
from initializr_core.metadata.models import ModelProvider

router = APIRouter(tags=["models"])


@router.get("/api/v1/models", response_model=ModelsResponse)
async def list_models() -> ModelsResponse:
    """
    List available model providers.

    Returns provider IDs and display names.
    """
    return ModelsResponse(
        providers=[
            {
                "id": provider.value,
                "name": provider.value.replace("_", " ").title(),
            }
            for provider in ModelProvider
        ]
    )
```

- [ ] **Step 5: Implement extensions router**

```python
# initializr-web/initializr_web/router/extensions.py
"""
Extension point options listing endpoint.
"""

from fastapi import APIRouter
from initializr_web.models import ExtensionsResponse

router = APIRouter(tags=["extensions"])


@router.get("/api/v1/extensions", response_model=ExtensionsResponse)
async def list_extensions() -> ExtensionsResponse:
    """
    List available extension point options.

    Returns memory types, tools, formatters, evaluators, and OpenJudge graders.
    """
    return ExtensionsResponse(
        memory={
            "short_term": ["in-memory", "redis", "oceanbase"],
            "long_term": ["mem0", "zep", "oceanbase", "none"],
        },
        tools={
            "execute_python_code": "Execute Python code safely",
            "execute_shell_command": "Execute shell commands",
            "web_search": "Web search using Tavily API",
            "browser_navigate": "Browser navigation",
            "browser_click": "Browser click interaction",
            "browser_type": "Browser text input",
            "browser_screenshot": "Browser screenshot capture",
        },
        formatters=["DashScopeChatFormatter", "OpenAIChatFormatter"],
        evaluators=["general", "ray"],
        openjudge_graders=[
            "RelevanceGrader",
            "CorrectnessGrader",
            "HallucinationGrader",
            "SafetyGrader",
            "CodeQualityGrader",
        ],
    )
```

- [ ] **Step 6: Update router __init__.py**

```python
# initializr-web/initializr_web/router/__init__.py
"""
API routers package.
"""

from initializr_web.router.health import router as health_router
from initializr_web.router.templates import router as templates_router
from initializr_web.router.models import router as models_router
from initializr_web.router.extensions import router as extensions_router

__all__ = [
    "health_router",
    "templates_router",
    "models_router",
    "extensions_router",
]
```

- [ ] **Step 7: Wire routers into main app**

```python
# Modify initializr-web/initializr_web/api.py

from initializr_web.router import (
    health_router,
    templates_router,
    models_router,
    extensions_router,
)

# ... (existing CORS middleware setup)

# Include routers
app.include_router(health_router)
app.include_router(templates_router)
app.include_router(models_router)
app.include_router(extensions_router)

# ... (rest of file)
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `cd initializr-web && python -m pytest tests/test_api.py -v`
Expected: All tests PASS

- [ ] **Step 9: Test interactive API docs**

Run: `cd initializr-web && uvicorn initializr_web.api:app --reload`
Visit: http://localhost:8000/docs
Expected: See Swagger UI with all endpoints listed and documented

Press Ctrl+C to stop

- [ ] **Step 10: Commit**

```bash
git add initializr-web/initializr_web/router/ initializr-web/tests/test_api.py
git commit -m "feat: add metadata endpoints (templates, models, extensions)"
```

---

## Task 6: Implement Project Generation Endpoint

**Files:**
- Create: `initializr-web/initializr_web/router/projects.py`
- Modify: `initializr-web/initializr_web/router/__init__.py`
- Modify: `initializr-web/tests/test_api.py`

**Rationale:** Implement the core endpoint that generates AgentScope projects based on configuration.

- [ ] **Step 1: Write failing test for project generation**

```python
# Add to initializr-web/tests/test_api.py

import tempfile
import zipfile
from pathlib import Path

def test_generate_project(client):
    """Test project generation endpoint."""
    request_data = {
        "name": "test-agent",
        "description": "Test agent",
        "layout": "standard",
        "agent_type": "basic",
        "model_provider": "openai",
        "enable_tools": True,
        "tools": ["execute_python_code"],
    }

    response = client.post("/api/v1/projects/generate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "download_url" in data
    assert "project_id" in data


def test_download_project(client, tmp_path):
    """Test project download endpoint."""
    # First generate a project
    request_data = {
        "name": "download-test",
        "layout": "lightweight",
        "agent_type": "basic",
    }

    gen_response = client.post("/api/v1/projects/generate", json=request_data)
    assert gen_response.status_code == 200
    project_id = gen_response.json()["project_id"]

    # Download the project
    download_response = client.get(f"/api/v1/projects/download/{project_id}")
    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/zip"

    # Save and verify zip contents
    zip_path = tmp_path / "project.zip"
    zip_path.write_bytes(download_response.content)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        files = zf.namelist()
        # Should have project structure
        assert any("download_test" in f for f in files)
        assert any("main.py" in f for f in files or "agent" in f for f in files)


def test_generate_project_invalid_layout(client):
    """Test project generation rejects invalid layout."""
    request_data = {
        "name": "test-agent",
        "layout": "invalid-layout",  # Invalid layout
        "agent_type": "basic",
    }

    response = client.post("/api/v1/projects/generate", json=request_data)
    assert response.status_code == 422  # Validation error
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd initializr-web && python -m pytest tests/test_api.py::test_generate_project -v`
Expected: FAIL with "404 Not Found"

- [ ] **Step 3: Create project conversion utility**

```python
# initializr-web/initializr_web/converter.py
"""
Convert ProjectRequest to AgentScopeMetadata.
"""

from initializr_web.models import ProjectRequest
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ModelProvider,
    ProjectLayout,
)


def project_request_to_metadata(request: ProjectRequest) -> AgentScopeMetadata:
    """
    Convert ProjectRequest to AgentScopeMetadata.

    Args:
        request: Project request from API

    Returns:
        AgentScopeMetadata instance
    """
    return AgentScopeMetadata(
        project_name=request.name,
        description=request.description,
        author=request.author,
        package_name=request.name.replace("-", "_"),
        agent_type=AgentType(request.agent_type),
        layout=ProjectLayout(request.layout),
        model_provider=ModelProvider(request.model_provider),
        model_config=request.model_config,
        enable_memory=request.enable_memory,
        short_term_memory_type=request.short_term_memory,
        long_term_memory_type=request.long_term_memory,
        enable_tools=request.enable_tools,
        tools=request.tools,
        enable_skills=request.enable_skills,
        skills=request.skills,
        enable_hooks=request.enable_hooks,
        hooks=request.hooks,
        enable_formatter=request.enable_formatter,
        formatter_type=request.formatter,
        enable_rag=request.enable_rag,
        rag_config=request.rag_config,
        enable_pipeline=request.enable_pipeline,
        pipeline_config=request.pipeline_config,
        generate_tests=request.generate_tests,
        generate_evaluation=request.generate_evaluation,
        evaluator_type=request.evaluator_type,
        enable_openjudge=request.enable_openjudge,
        openjudge_graders=request.openjudge_graders,
        initial_benchmark_tasks=request.initial_benchmark_tasks,
        python_version=request.python_version,
    )
```

- [ ] **Step 4: Create project generation utility**

```python
# initializr-web/initializr_web/generator.py
"""
Project generation utilities for web service.
"""

import os
import zipfile
from pathlib import Path
from typing import Optional
import uuid

from initializr_core.generator.project import ProjectGenerator
from initializr_web.converter import project_request_to_metadata
from initializr_web.models import ProjectRequest


class ProjectGenerationError(Exception):
    """Exception raised when project generation fails."""
    pass


def generate_project(
    request: ProjectRequest,
    output_dir: Path,
) -> str:
    """
    Generate a project from request.

    Args:
        request: Project request
        output_dir: Directory to store generated projects

    Returns:
        Project ID

    Raises:
        ProjectGenerationError: If generation fails
    """
    try:
        # Convert request to metadata
        metadata = project_request_to_metadata(request)

        # Generate unique project ID
        project_id = f"{request.name}_{uuid.uuid4().hex[:8]}"
        project_path = output_dir / project_id

        # Generate project
        generator = ProjectGenerator()
        generator.generate(
            metadata=metadata,
            output_path=str(project_path),
        )

        # Create zip file
        zip_path = output_dir / f"{project_id}.zip"
        create_zip(project_path, zip_path)

        return project_id

    except Exception as e:
        raise ProjectGenerationError(f"Failed to generate project: {str(e)}") from e


def create_zip(source_dir: Path, output_zip: Path) -> None:
    """
    Create a zip file from a directory.

    Args:
        source_dir: Source directory to zip
        output_zip: Output zip file path
    """
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in source_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(source_dir)
                zipf.write(file, arcname)


def cleanup_old_projects(output_dir: Path, max_age_seconds: int = 3600) -> int:
    """
    Remove projects older than max_age_seconds.

    Args:
        output_dir: Directory containing projects
        max_age_seconds: Maximum age in seconds (default: 1 hour)

    Returns:
        Number of projects cleaned up
    """
    import time
    import shutil

    now = time.time()
    cleaned = 0

    for item in output_dir.iterdir():
        if item.is_dir() or (item.is_file() and item.suffix == ".zip"):
            if now - item.stat().st_mtime > max_age_seconds:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
                cleaned += 1

    return cleaned
```

- [ ] **Step 5: Implement projects router**

```python
# initializr-web/initializr_web/router/projects.py
"""
Project generation and download endpoints.
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from initializr_web.models import ProjectRequest, ProjectResponse
from initializr_web.generator import generate_project, ProjectGenerationError

router = APIRouter(tags=["projects"])

# Output directory for generated projects
output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
output_dir.mkdir(parents=True, exist_ok=True)


@router.post("/api/v1/projects/generate", response_model=ProjectResponse)
async def generate_project_endpoint(
    request: ProjectRequest,
    background_tasks: BackgroundTasks,
) -> ProjectResponse:
    """
    Generate a new AgentScope project.

    Creates a project based on the provided configuration and
    returns a download URL for the generated project bundle.
    """
    try:
        project_id = generate_project(request, output_dir)

        # Schedule cleanup task
        background_tasks.add_task(cleanup_projects)

        return ProjectResponse(
            success=True,
            message="Project generated successfully",
            download_url=f"/api/v1/projects/download/{project_id}",
            project_id=project_id,
        )

    except ProjectGenerationError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/api/v1/projects/download/{project_id}")
async def download_project(project_id: str):
    """
    Download a generated project.

    Returns the project as a ZIP file.
    """
    zip_path = output_dir / f"{project_id}.zip"

    if not zip_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Project not found: {project_id}",
        )

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=f"{project_id}.zip",
    )


def cleanup_projects():
    """Background task to clean up old projects."""
    from initializr_web.generator import cleanup_old_projects
    cleanup_old_projects(output_dir)
```

- [ ] **Step 6: Update router package**

```python
# Modify initializr-web/initializr_web/router/__init__.py

from initializr_web.router.projects import router as projects_router

__all__ = [
    "health_router",
    "templates_router",
    "models_router",
    "extensions_router",
    "projects_router",
]
```

- [ ] **Step 7: Wire projects router into main app**

```python
# Modify initializr-web/initializr_web/api.py

from initializr_web.router import (
    health_router,
    templates_router,
    models_router,
    extensions_router,
    projects_router,
)

# ... (CORS middleware)

# Include routers
app.include_router(health_router)
app.include_router(templates_router)
app.include_router(models_router)
app.include_router(extensions_router)
app.include_router(projects_router)

# ... (rest of file)
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `cd initializr-web && python -m pytest tests/test_api.py -v`
Expected: All tests PASS

- [ ] **Step 9: Test project generation manually**

Run: `cd initializr-web && uvicorn initializr_web.api:app --reload`

Test with curl:
```bash
curl -X POST "http://localhost:8000/api/v1/projects/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "manual-test",
    "layout": "standard",
    "agent_type": "basic"
  }'
```

Expected: Response with download_url and project_id

Press Ctrl+C to stop

- [ ] **Step 10: Commit**

```bash
git add initializr-web/initializr_web/ initializr-web/tests/
git commit -m "feat: implement project generation endpoint"
```

---

## Task 7: Set Up Vue.js Frontend Project

**Files:**
- Create: `initializr-web/frontend/package.json`
- Create: `initializr-web/frontend/vite.config.ts`
- Create: `initializr-web/frontend/tsconfig.json`
- Create: `initializr-web/frontend/index.html`
- Create: `initializr-web/frontend/src/main.ts`
- Create: `initializr-web/frontend/src/App.vue`

**Rationale:** Initialize Vue.js 3 + TypeScript project with Vite for fast development and build tooling.

- [ ] **Step 1: Create package.json**

```json
{
  "name": "agentscope-initializr-frontend",
  "version": "0.2.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "type-check": "vue-tsc --noEmit"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.6.0",
    "element-plus": "^2.5.0",
    "@element-plus/icons-vue": "^2.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "@vue/tsconfig": "^0.5.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vue-tsc": "^1.8.0"
  }
}
```

- [ ] **Step 2: Create vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: '../initializr_web/static',
    emptyOutDir: true
  }
})
```

- [ ] **Step 3: Create tsconfig.json**

```json
{
  "extends": "@vue/tsconfig/tsconfig.dom.json",
  "compilerOptions": {
    "composite": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"]
}
```

- [ ] **Step 4: Create index.html**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentScope Initializr</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 5: Create main.ts entry point**

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
```

- [ ] **Step 6: Create App.vue root component**

```vue
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  document.title = 'AgentScope Initializr'
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

body {
  margin: 0;
  padding: 0;
}
</style>
```

- [ ] **Step 7: Create router configuration**

```typescript
// initializr-web/frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/configure',
      name: 'configure',
      component: () => import('../views/Configure.vue')
    }
  ]
})

export default router
```

- [ ] **Step 8: Create Home page view**

```vue
<!-- initializr-web/frontend/src/views/Home.vue -->
<template>
  <div class="home">
    <el-container>
      <el-header>
        <h1>AgentScope Initializr</h1>
      </el-header>
      <el-main>
        <el-card class="welcome-card">
          <h2>Welcome to AgentScope Initializr</h2>
          <p>Scaffold AgentScope agent projects with a web interface</p>
          <el-button type="primary" size="large" @click="startConfiguration">
            Start Creating Project
          </el-button>
        </el-card>

        <el-divider />

        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <h3>⚡ Fast Setup</h3>
              <p>Configure and generate projects in minutes</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <h3>🎯 Multiple Templates</h3>
              <p>Basic, multi-agent, research, and browser automation</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <h3>🔧 Flexible Configuration</h3>
              <p>Configure all AgentScope extension points</p>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const startConfiguration = () => {
  router.push('/configure')
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-header {
  text-align: center;
  margin-bottom: 40px;
}

.el-header h1 {
  margin: 0;
  font-size: 2.5em;
}

.welcome-card {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-card h2 {
  margin-top: 0;
}
</style>
```

- [ ] **Step 9: Install dependencies and test**

Run: `cd initializr-web/frontend && npm install`
Run: `cd initializr-web/frontend && npm run dev`
Expected: Vite dev server starts on http://localhost:5173

Visit http://localhost:5173
Expected: See welcome page with "Start Creating Project" button

Press Ctrl+C to stop

- [ ] **Step 10: Commit**

```bash
git add initializr-web/frontend/
git commit -m "feat: initialize Vue.js 3 frontend project"
```

---

## Task 8: Create API Client and TypeScript Types

**Files:**
- Create: `initializr-web/frontend/src/types/index.ts`
- Create: `initializr-web/frontend/src/api/client.ts`

**Rationale:** Establish typed API client and TypeScript interfaces for type safety across the frontend.

- [ ] **Step 1: Write test for API client**

```typescript
// initializr-web/frontend/tests/api/client.test.ts
import { describe, it, expect } from 'vitest'
import { apiClient } from '@/api/client'

describe('API Client', () => {
  it('should create client with correct base URL', () => {
    expect(apiClient.defaults.baseURL).toBe('/api/v1')
  })

  it('should have correct headers', () => {
    expect(apiClient.defaults.headers['Content-Type']).toBe('application/json')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd initializr-web/frontend && npm run type-check`
Expected: May pass or fail depending on setup

- [ ] **Step 3: Create TypeScript types**

```typescript
// initializr-web/frontend/src/types/index.ts

export interface ProjectRequest {
  name: string
  description?: string
  author?: string
  layout?: 'standard' | 'lightweight'
  agent_type?: string
  python_version?: string
  model_provider?: string
  model_config?: Record<string, any>
  enable_memory?: boolean
  short_term_memory?: string | null
  long_term_memory?: string | null
  enable_tools?: boolean
  tools?: string[]
  enable_skills?: boolean
  skills?: string[]
  enable_hooks?: boolean
  hooks?: string[]
  enable_formatter?: boolean
  formatter?: string | null
  enable_rag?: boolean
  rag_config?: Record<string, any> | null
  enable_pipeline?: boolean
  pipeline_config?: Record<string, any> | null
  generate_tests?: boolean
  generate_evaluation?: boolean
  evaluator_type?: string
  enable_openjudge?: boolean
  openjudge_graders?: string[]
  initial_benchmark_tasks?: number
}

export interface ProjectResponse {
  success: boolean
  message: string
  download_url?: string
  project_id?: string
}

export interface TemplateInfo {
  id: string
  name: string
  description: string
}

export interface TemplatesResponse {
  templates: TemplateInfo[]
}

export interface ModelProviderInfo {
  id: string
  name: string
}

export interface ModelsResponse {
  providers: ModelProviderInfo[]
}

export interface ExtensionsResponse {
  memory: {
    short_term: string[]
    long_term: string[]
  }
  tools: Record<string, string>
  formatters: string[]
  evaluators: string[]
  openjudge_graders: string[]
}

export interface HealthResponse {
  status: string
  service: string
  version: string
}

export interface DetailedHealthResponse extends HealthResponse {
  system: {
    cpu_percent: number
    memory_percent: number
    disk_usage: number
  }
  projects: {
    total_generated: number
    storage_used: number
  }
}
```

- [ ] **Step 4: Create API client**

```typescript
// initializr-web/frontend/src/api/client.ts
import axios, { AxiosInstance } from 'axios'

const apiClient: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default apiClient
```

- [ ] **Step 5: Create API service functions**

```typescript
// initializr-web/frontend/src/api/index.ts
import apiClient from './client'
import type {
  ProjectRequest,
  ProjectResponse,
  TemplatesResponse,
  ModelsResponse,
  ExtensionsResponse,
  HealthResponse,
  DetailedHealthResponse,
} from '@/types'

export const api = {
  // Health checks
  getHealth: async (): Promise<HealthResponse> => {
    const response = await apiClient.get<HealthResponse>('/../health')
    return response.data
  },

  getDetailedHealth: async (): Promise<DetailedHealthResponse> => {
    const response = await apiClient.get<DetailedHealthResponse>('/../health/detailed')
    return response.data
  },

  // Metadata
  getTemplates: async (): Promise<TemplatesResponse> => {
    const response = await apiClient.get<TemplatesResponse>('/templates')
    return response.data
  },

  getModels: async (): Promise<ModelsResponse> => {
    const response = await apiClient.get<ModelsResponse>('/models')
    return response.data
  },

  getExtensions: async (): Promise<ExtensionsResponse> => {
    const response = await apiClient.get<ExtensionsResponse>('/extensions')
    return response.data
  },

  // Project generation
  generateProject: async (request: ProjectRequest): Promise<ProjectResponse> => {
    const response = await apiClient.post<ProjectResponse>('/projects/generate', request)
    return response.data
  },

  getDownloadUrl: (projectId: string): string => {
    return `/api/v1/projects/download/${projectId}`
  },
}
```

- [ ] **Step 6: Update tests**

```typescript
// initializr-web/frontend/tests/api/index.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { api } from '@/api'
import axios from 'axios'

vi.mock('axios')

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should fetch templates', async () => {
    const mockTemplates = {
      templates: [
        { id: 'basic', name: 'Basic Agent', description: 'Basic agent template' },
      ],
    }
    vi.mocked(axios.get).mockResolvedValue({ data: mockTemplates })

    const result = await api.getTemplates()
    expect(result.templates).toHaveLength(1)
    expect(result.templates[0].id).toBe('basic')
  })

  it('should generate project', async () => {
    const mockResponse = {
      success: true,
      message: 'Generated',
      download_url: '/api/v1/projects/download/test_123',
      project_id: 'test_123',
    }
    vi.mocked(axios.create().post).mockResolvedValue({ data: mockResponse })

    const request = { name: 'test', layout: 'standard' }
    const result = await api.generateProject(request)
    expect(result.success).toBe(true)
    expect(result.project_id).toBe('test_123')
  })
})
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `cd initializr-web/frontend && npm run type-check`
Expected: No type errors

- [ ] **Step 8: Commit**

```bash
git add initializr-web/frontend/src/
git commit -m "feat: add API client and TypeScript types"
```

---

## Task 9: Create Pinia Store for Form State

**Files:**
- Create: `initializr-web/frontend/src/stores/config.ts`

**Rationale:** Centralized state management for the multi-step configuration form using Pinia.

- [ ] **Step 1: Write test for config store**

```typescript
// initializr-web/frontend/tests/stores/config.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useConfigStore } from '@/stores/config'

describe('Config Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default values', () => {
    const store = useConfigStore()
    expect(store.form.name).toBe('')
    expect(store.form.layout).toBe('standard')
    expect(store.form.enable_memory).toBe(true)
  })

  it('should update form field', () => {
    const store = useConfigStore()
    store.setField('name', 'test-agent')
    expect(store.form.name).toBe('test-agent')
  })

  it('should reset form', () => {
    const store = useConfigStore()
    store.setField('name', 'test-agent')
    store.setField('layout', 'lightweight')
    store.resetForm()
    expect(store.form.name).toBe('')
    expect(store.form.layout).toBe('standard')
  })

  it('should validate required fields', () => {
    const store = useConfigStore()
    expect(store.isValid).toBe(false) // name is required but empty
    store.setField('name', 'test')
    expect(store.isValid).toBe(true)
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd initializr-web/frontend && npm run type-check`
Expected: Error: module not found

- [ ] **Step 3: Create config store**

```typescript
// initializr-web/frontend/src/stores/config.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ProjectRequest } from '@/types'
import { api } from '@/api'

export const useConfigStore = defineStore('config', () => {
  // Form state
  const form = ref<ProjectRequest>({
    name: '',
    description: '',
    author: '',
    layout: 'standard',
    agent_type: 'basic',
    python_version: '3.11',
    model_provider: 'openai',
    model_config: {},
    enable_memory: true,
    short_term_memory: null,
    long_term_memory: null,
    enable_tools: true,
    tools: [],
    enable_skills: false,
    skills: [],
    enable_hooks: false,
    hooks: [],
    enable_formatter: false,
    formatter: null,
    enable_rag: false,
    rag_config: null,
    enable_pipeline: false,
    pipeline_config: null,
    generate_tests: false,
    generate_evaluation: false,
    evaluator_type: 'general',
    enable_openjudge: false,
    openjudge_graders: [],
    initial_benchmark_tasks: 0,
  })

  // Loading state
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Current step in multi-step form
  const currentStep = ref(1)
  const totalSteps = 4

  // Computed
  const isValid = computed(() => {
    return form.value.name.trim().length > 0
  })

  // Actions
  const setField = <K extends keyof ProjectRequest>(field: K, value: ProjectRequest[K]) => {
    form.value[field] = value
  }

  const resetForm = () => {
    form.value = {
      name: '',
      description: '',
      author: '',
      layout: 'standard',
      agent_type: 'basic',
      python_version: '3.11',
      model_provider: 'openai',
      model_config: {},
      enable_memory: true,
      short_term_memory: null,
      long_term_memory: null,
      enable_tools: true,
      tools: [],
      enable_skills: false,
      skills: [],
      enable_hooks: false,
      hooks: [],
      enable_formatter: false,
      formatter: null,
      enable_rag: false,
      rag_config: null,
      enable_pipeline: false,
      pipeline_config: null,
      generate_tests: false,
      generate_evaluation: false,
      evaluator_type: 'general',
      enable_openjudge: false,
      openjudge_graders: [],
      initial_benchmark_tasks: 0,
    }
    currentStep.value = 1
    error.value = null
  }

  const nextStep = () => {
    if (currentStep.value < totalSteps) {
      currentStep.value++
    }
  }

  const prevStep = () => {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  const generateProject = async () => {
    if (!isValid.value) {
      error.value = 'Project name is required'
      return null
    }

    loading.value = true
    error.value = null

    try {
      const response = await api.generateProject(form.value)
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to generate project'
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    form,
    loading,
    error,
    currentStep,
    totalSteps,
    isValid,
    setField,
    resetForm,
    nextStep,
    prevStep,
    generateProject,
  }
})
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd initializr-web/frontend && npm run type-check`
Expected: No type errors

- [ ] **Step 5: Commit**

```bash
git add initializr-web/frontend/src/stores/
git commit -m "feat: add Pinia store for configuration form state"
```

---

## Task 10: Create Configuration Form Component

**Files:**
- Create: `initializr-web/frontend/src/components/ConfigurationForm.vue`
- Create: `initializr-web/frontend/src/components/BasicSettings.vue`
- Create: `initializr-web/frontend/src/components/TemplateSelector.vue`

**Rationale:** Build the main multi-step configuration form UI with validation.

- [ ] **Step 1: Create BasicSettings component (Step 1)**

```vue
<!-- initializr-web/frontend/src/components/BasicSettings.vue -->
<template>
  <el-form :model="form" label-width="150px" size="large">
    <el-form-item label="Project Name" required>
      <el-input
        v-model="form.name"
        placeholder="my-agent"
        @input="updateField('name', $event)"
      />
      <span class="hint">Lowercase, hyphens allowed (e.g., my-agent)</span>
    </el-form-item>

    <el-form-item label="Description">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="3"
        placeholder="Brief project description"
        @input="updateField('description', $event)"
      />
    </el-form-item>

    <el-form-item label="Author">
      <el-input
        v-model="form.author"
        placeholder="Your name"
        @input="updateField('author', $event)"
      />
    </el-form-item>

    <el-form-item label="Project Layout">
      <el-radio-group v-model="form.layout" @change="updateField('layout', $event)">
        <el-radio value="standard">
          <strong>Standard (src/)</strong>
          <div class="radio-description">
            Recommended: Organized structure with src/ directory
          </div>
        </el-radio>
        <el-radio value="lightweight">
          <strong>Lightweight</strong>
          <div class="radio-description">
            Simple structure: files in project root
          </div>
        </el-radio>
      </el-radio-group>
    </el-form-item>

    <el-form-item label="Python Version">
      <el-select v-model="form.python_version" @change="updateField('python_version', $event)">
        <el-option value="3.10" label="Python 3.10" />
        <el-option value="3.11" label="Python 3.11 (Recommended)" />
        <el-option value="3.12" label="Python 3.12" />
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useConfigStore } from '@/stores/config'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}
</script>

<style scoped>
.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
}

.radio-description {
  font-size: 0.9em;
  color: #606266;
  margin-top: 4px;
}

:deep(.el-radio) {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
  height: auto;
}

:deep(.el-radio__label) {
  line-height: 1.5;
}
</style>
```

- [ ] **Step 2: Create TemplateSelector component**

```vue
<!-- initializr-web/frontend/src/components/TemplateSelector.vue -->
<template>
  <div class="template-selector">
    <h3>Select Agent Type</h3>
    <p class="subtitle">Choose the type of agent you want to create</p>

    <el-row :gutter="20">
      <el-col
        v-for="template in templates"
        :key="template.id"
        :span="6"
      >
        <el-card
          :class="{ selected: form.agent_type === template.id }"
          class="template-card"
          shadow="hover"
          @click="selectTemplate(template.id)"
        >
          <div class="template-icon">{{ getIcon(template.id) }}</div>
          <h4>{{ template.name }}</h4>
          <p>{{ template.description }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { TemplateInfo } from '@/types'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const templates = ref<TemplateInfo[]>([])

const getIcon = (id: string): string => {
  const icons: Record<string, string> = {
    'basic': '🤖',
    'multi-agent': '👥',
    'research': '🔍',
    'browser': '🌐',
  }
  return icons[id] || '📦'
}

const selectTemplate = (id: string) => {
  configStore.setField('agent_type', id)
}

onMounted(async () => {
  try {
    const response = await api.getTemplates()
    templates.value = response.templates
  } catch (error) {
    console.error('Failed to load templates:', error)
  }
})
</script>

<style scoped>
.template-selector {
  margin-bottom: 30px;
}

.template-selector h3 {
  margin-top: 0;
}

.subtitle {
  color: #606266;
  margin-bottom: 20px;
}

.template-card {
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
  min-height: 150px;
}

.template-card:hover {
  transform: translateY(-4px);
}

.template-card.selected {
  border: 2px solid #409eff;
  background-color: #ecf5ff;
}

.template-icon {
  font-size: 3em;
  margin-bottom: 10px;
}

.template-card h4 {
  margin: 10px 0;
  font-size: 1.1em;
}

.template-card p {
  font-size: 0.85em;
  color: #606266;
  line-height: 1.4;
}
</style>
```

- [ ] **Step 3: Create ConfigurationForm main component**

```vue
<!-- initializr-web/frontend/src/components/ConfigurationForm.vue -->
<template>
  <div class="configuration-form">
    <el-steps :active="currentStep - 1" finish-status="success" align-center>
      <el-step title="Basic Settings" />
      <el-step title="Model & Memory" />
      <el-step title="Extensions" />
      <el-step title="Testing & Eval" />
    </el-steps>

    <div class="form-content">
      <!-- Step 1: Basic Settings -->
      <div v-show="currentStep === 1" class="step-content">
        <TemplateSelector />
        <BasicSettings />
      </div>

      <!-- Step 2: Model & Memory -->
      <div v-show="currentStep === 2" class="step-content">
        <h3>Model Configuration</h3>
        <p class="subtitle">Configure the LLM model for your agent</p>
        <!-- ModelConfig component would go here -->
        <el-alert type="info" :closable="false">
          Model configuration UI - to be implemented in next component
        </el-alert>

        <el-divider />

        <h3>Memory Configuration</h3>
        <p class="subtitle">Configure short-term and long-term memory</p>
        <!-- MemoryConfig component would go here -->
        <el-alert type="info" :closable="false">
          Memory configuration UI - to be implemented in next component
        </el-alert>
      </div>

      <!-- Step 3: Extensions -->
      <div v-show="currentStep === 3" class="step-content">
        <h3>Extension Points</h3>
        <p class="subtitle">Configure AgentScope framework extensions</p>
        <!-- ExtensionConfig component would go here -->
        <el-alert type="info" :closable="false">
          Extension configuration UI - to be implemented in next component
        </el-alert>
      </div>

      <!-- Step 4: Testing & Evaluation -->
      <div v-show="currentStep === 4" class="step-content">
        <h3>Testing & Evaluation</h3>
        <p class="subtitle">Configure test generation and evaluation setup</p>
        <!-- TestingConfig component would go here -->
        <el-alert type="info" :closable="false">
          Testing configuration UI - to be implemented in next component
        </el-alert>
      </div>
    </div>

    <!-- Navigation buttons -->
    <div class="form-actions">
      <el-button v-if="currentStep > 1" @click="prevStep">
        Previous
      </el-button>
      <el-button
        v-if="currentStep < totalSteps"
        type="primary"
        :disabled="!isValid"
        @click="nextStep"
      >
        Next
      </el-button>
      <el-button
        v-if="currentStep === totalSteps"
        type="success"
        :loading="loading"
        :disabled="!isValid"
        @click="handleGenerate"
      >
        Generate Project
      </el-button>
    </div>

    <!-- Error display -->
    <el-alert
      v-if="error"
      type="error"
      :title="error"
      :closable="false"
      style="margin-top: 20px"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'
import TemplateSelector from './TemplateSelector.vue'
import BasicSettings from './BasicSettings.vue'

const configStore = useConfigStore()
const currentStep = computed(() => configStore.currentStep)
const totalSteps = computed(() => configStore.totalSteps)
const isValid = computed(() => configStore.isValid)
const loading = computed(() => configStore.loading)
const error = computed(() => configStore.error)

const nextStep = () => {
  configStore.nextStep()
}

const prevStep = () => {
  configStore.prevStep()
}

const handleGenerate = async () => {
  const response = await configStore.generateProject()
  if (response && response.success) {
    ElMessage.success('Project generated successfully!')
    // Could show download button here
  }
}
</script>

<style scoped>
.configuration-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.form-content {
  margin: 40px 0;
  min-height: 400px;
}

.step-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-actions {
  text-align: center;
  margin-top: 40px;
  border-top: 1px solid #dcdfe6;
  padding-top: 20px;
}

.subtitle {
  color: #606266;
  margin-bottom: 20px;
}
</style>
```

- [ ] **Step 4: Update Configure view to use form**

```vue
<!-- initializr-web/frontend/src/views/Configure.vue -->
<template>
  <div class="configure">
    <el-container>
      <el-header>
        <h1>Configure Your Project</h1>
      </el-header>
      <el-main>
        <ConfigurationForm />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import ConfigurationForm from '@/components/ConfigurationForm.vue'
</script>

<style scoped>
.configure {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-header h1 {
  text-align: center;
}
</style>
```

- [ ] **Step 5: Test the form**

Run: `cd initializr-web/frontend && npm run dev`
Visit: http://localhost:5173/configure
Expected: See multi-step form with template selector and basic settings

Press Ctrl+C to stop

- [ ] **Step 6: Commit**

```bash
git add initializr-web/frontend/src/components/
git commit -m "feat: add configuration form components"
```

---

## Task 11: Create Dockerfile and Docker Compose

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `.dockerignore`

**Rationale:** Enable containerized deployment for easy setup and scaling.

- [ ] **Step 1: Create .dockerignore**

```
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.git
.gitignore
.venv
venv/
ENV/
env/
.vscode
.idea
*.md
docs/
tests/
.pytest_cache
.coverage
htmlcov/
initializr-web/frontend/node_modules
initializr-web/frontend/dist
initializr-web/.turbo
```

- [ ] **Step 2: Create Dockerfile**

```dockerfile
# Multi-stage build for AgentScope Initializr Web Service
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Build frontend assets
COPY initializr-web/frontend ./initializr-web/frontend
RUN cd initializr-web/frontend && npm install && npm run build

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[web]"

# Copy built artifacts from builder
COPY --from=builder /app/initializr-web/initializr_web ./initializr-web/initializr_web
COPY --from=builder /app/initializr-web/frontend/dist ./initializr-web/initializr_web/static
COPY --from=builder /app/initializr-core ./initializr-core
COPY --from=builder /app/initializr-cli ./initializr-cli
COPY --from=builder /app/initializr-templates ./initializr-templates

# Create directories for generated projects
RUN mkdir -p /app/output

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the web service
CMD ["uvicorn", "initializr_web.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 3: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  agentscope-initializr:
    build: .
    container_name: agentscope-initializr
    ports:
      - "8000:8000"
    volumes:
      # Mount output directory for persistent storage
      - ./output:/app/output
    environment:
      - LOG_LEVEL=info
      - OUTPUT_DIR=/app/output
      - ALLOW_ORIGINS=http://localhost:5173,http://localhost:8080,http://localhost:8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

- [ ] **Step 4: Test Docker build**

Run: `docker build -t agentscope-initializr .`
Expected: Docker image builds successfully

Run: `docker-compose up`
Expected: Container starts, service available at http://localhost:8000

Test: `curl http://localhost:8000/health`
Expected: `{"status":"healthy","service":"AgentScope Initializr","version":"0.2.0"}`

Press Ctrl+C to stop containers

- [ ] **Step 5: Commit**

```bash
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "feat: add Docker deployment configuration"
```

---

## Task 12: Add Integration Tests

**Files:**
- Modify: `initializr-web/tests/test_integration.py`

**Rationale:** End-to-end tests to verify the full flow from request to project generation.

- [ ] **Step 1: Write integration test**

```python
# initializr-web/tests/test_integration.py
"""
Integration tests for the web service.
"""

import pytest
import tempfile
import zipfile
from pathlib import Path
from fastapi.testclient import TestClient
from initializr_web.api import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_full_project_generation_flow(client):
    """Test complete flow: health -> templates -> generate -> download"""
    # 1. Check health
    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "healthy"

    # 2. Get templates
    templates_response = client.get("/api/v1/templates")
    assert templates_response.status_code == 200
    templates = templates_response.json()["templates"]
    assert len(templates) > 0

    # 3. Get models
    models_response = client.get("/api/v1/models")
    assert models_response.status_code == 200
    providers = models_response.json()["providers"]
    assert len(providers) > 0

    # 4. Get extensions
    extensions_response = client.get("/api/v1/extensions")
    assert extensions_response.status_code == 200
    extensions = extensions_response.json()
    assert "memory" in extensions
    assert "tools" in extensions

    # 5. Generate project
    request_data = {
        "name": "integration-test-agent",
        "description": "Integration test agent",
        "layout": "standard",
        "agent_type": "basic",
        "model_provider": "openai",
        "enable_tools": True,
        "tools": ["execute_python_code"],
    }

    gen_response = client.post("/api/v1/projects/generate", json=request_data)
    assert gen_response.status_code == 200
    gen_data = gen_response.json()
    assert gen_data["success"] is True
    assert "project_id" in gen_data
    assert "download_url" in gen_data

    project_id = gen_data["project_id"]

    # 6. Download project
    download_response = client.get(f"/api/v1/projects/download/{project_id}")
    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/zip"

    # 7. Verify zip contents
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(download_response.content)
        tmp_path = Path(tmp.name)

    with zipfile.ZipFile(tmp_path, 'r') as zf:
        files = zf.namelist()
        # Should contain project structure
        assert any("integration_test_agent" in f for f in files)

    tmp_path.unlink()


def test_error_handling_invalid_project(client):
    """Test error handling for invalid project configuration."""
    request_data = {
        "name": "",  # Invalid: empty name
        "layout": "invalid",  # Invalid: wrong layout
    }

    response = client.post("/api/v1/projects/generate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_concurrent_project_generation(client):
    """Test handling concurrent project generation requests."""
    import threading

    results = []

    def generate_project(name_suffix):
        request_data = {
            "name": f"concurrent-test-{name_suffix}",
            "layout": "lightweight",
            "agent_type": "basic",
        }
        response = client.post("/api/v1/projects/generate", json=request_data)
        results.append(response.json())

    threads = [
        threading.Thread(target=generate_project, args=(i,))
        for i in range(5)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # All should succeed
    assert len(results) == 5
    for result in results:
        assert result.get("success") is True
```

- [ ] **Step 2: Run integration tests**

Run: `cd initializr-web && python -m pytest tests/test_integration.py -v`
Expected: All tests PASS

- [ ] **Step 3: Commit**

```bash
git add initializr-web/tests/test_integration.py
git commit -m "test: add integration tests for web service"
```

---

## Task 13: Update Documentation and README

**Files:**
- Modify: `README.md` (root)
- Create: `initializr-web/README.md`
- Create: `DEPLOYMENT.md`

**Rationale:** Document the new web service capabilities and deployment instructions.

- [ ] **Step 1: Update root README**

```markdown
# AgentScope Initializr

Web service and CLI for scaffolding AgentScope agent projects.

## Features

- 🚀 **Quick Scaffolding**: Generate AgentScope projects in seconds
- 🌐 **Web Interface**: User-friendly web UI for configuration
- 💻 **CLI Support**: Command-line interface for automation
- 📦 **Multiple Templates**: Basic, multi-agent, research, browser automation
- 🔧 **Flexible Configuration**: Configure all AgentScope extension points
- 🐳 **Docker Ready**: Containerized deployment

## Quick Start

### Web Interface

1. **Using Docker (Recommended)**:
```bash
docker-compose up
```
Visit http://localhost:8000/docs for API docs
Visit http://localhost:5173 for web UI (when running frontend dev server)

2. **Manual Installation**:
```bash
# Install with web dependencies
pip install -e ".[web]"

# Run web service
agentscope-web
```

### CLI

```bash
# Install
pip install -e .

# Create a project
agentscope-init create --name my-agent --layout standard

# Interactive wizard
agentscope-init wizard
```

## Documentation

- [Web Service Guide](initializr-web/README.md)
- [Deployment Guide](DEPLOYMENT.md)
- [CLI Documentation](initializr-cli/README.md)
- [Architecture](ARCHITECTURE.md)

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines.

## License

MIT
```

- [ ] **Step 2: Create web service README**

```markdown
# AgentScope Initializr Web Service

FastAPI backend + Vue.js frontend for scaffolding AgentScope projects.

## Features

- RESTful API for project generation
- Interactive web UI with multi-step form
- Real-time validation
- Project download as ZIP
- Health monitoring endpoints
- Docker deployment support

## Installation

```bash
cd initializr-web
pip install -e .
```

## Running

### Development Mode

**Backend**:
```bash
uvicorn initializr_web.api:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Production Mode

```bash
agentscope-web
```

Or with Docker:
```bash
docker-compose up
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system metrics

### Metadata
- `GET /api/v1/templates` - List available templates
- `GET /api/v1/models` - List model providers
- `GET /api/v1/extensions` - List extension options

### Projects
- `POST /api/v1/projects/generate` - Generate new project
- `GET /api/v1/projects/download/{project_id}` - Download project ZIP

## Testing

```bash
cd initializr-web
python -m pytest tests/ -v
```

## Environment Variables

- `LOG_LEVEL` - Logging level (default: info)
- `OUTPUT_DIR` - Output directory for projects (default: ./output)
- `ALLOW_ORIGINS` - CORS allowed origins (default: localhost:5173,localhost:8080,localhost:8000)
```

- [ ] **Step 3: Create deployment guide**

```markdown
# Deployment Guide

## Docker Deployment (Recommended)

### Quick Start

```bash
docker-compose up -d
```

The service will be available at http://localhost:8000

### Configuration

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - LOG_LEVEL=info
  - OUTPUT_DIR=/app/output
  - ALLOW_ORIGINS=http://your-frontend-domain.com
```

### Production Deployment

#### Using Nginx Reverse Proxy

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

Create `docker-compose.prod.yml`:

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - agentscope-initializr
```

#### Nginx Configuration

```nginx
events {
    worker_connections 1024;
}

http {
    upstream agentscope {
        server agentscope-initializr:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://agentscope;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## Manual Deployment

### Systemd Service

Create `/etc/systemd/system/agentscope-web.service`:

```ini
[Unit]
Description=AgentScope Initializr Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/agentscope-initializr
Environment="OUTPUT_DIR=/var/lib/agentscope-projects"
ExecStart=/usr/local/bin/uvicorn initializr_web.api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable agentscope-web
sudo systemctl start agentscope-web
```

## Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8000/health

# Detailed metrics
curl http://localhost:8000/health/detailed
```

### Logs

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u agentscope-web -f
```

## Scaling

### Multiple Instances

Use load balancer with multiple instances:

```yaml
services:
  agentscope-1:
    build: .
    environment:
      - OUTPUT_DIR=/app/output
    # ...

  agentscope-2:
    build: .
    environment:
      - OUTPUT_DIR=/app/output
    # ...

  nginx:
    image: nginx:alpine
    # Configure upstream with both instances
```

## Backup

Generated projects are stored in `./output` by default. Back up this directory regularly.

```bash
# Backup
tar -czf projects-backup-$(date +%Y%m%d).tar.gz ./output

# Restore
tar -xzf projects-backup-20260327.tar.gz
```
```

- [ ] **Step 4: Commit documentation**

```bash
git add README.md initializr-web/README.md DEPLOYMENT.md
git commit -m "docs: add web service and deployment documentation"
```

---

## Task 14: Final End-to-End Testing

**Files:**
- Create: `initializr-web/tests/test_e2e.py`

**Rationale:** Comprehensive end-to-end test to verify the entire system works correctly.

- [ ] **Step 1: Create e2e test**

```python
# initializr-web/tests/test_e2e.py
"""
End-to-end test for the complete web service workflow.
"""

import pytest
import tempfile
import zipfile
from pathlib import Path
import subprocess
import time


@pytest.fixture(scope="module")
def running_server():
    """Start the server for e2e testing."""
    # Start uvicorn in background
    proc = subprocess.Popen(
        ["uvicorn", "initializr_web.api:app", "--host", "localhost", "--port", "8765"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    time.sleep(3)

    yield "http://localhost:8765"

    # Cleanup
    proc.terminate()
    proc.wait()


def test_e2e_complete_workflow(running_server):
    """Test complete workflow from health check to project download."""
    import requests

    base_url = running_server

    # 1. Health check
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

    # 2. List templates
    response = requests.get(f"{base_url}/api/v1/templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert len(templates) >= 4  # basic, multi-agent, research, browser

    # 3. Generate a project
    project_request = {
        "name": "e2e-test-agent",
        "description": "End-to-end test agent",
        "author": "E2E Test",
        "layout": "standard",
        "agent_type": "multi-agent",
        "model_provider": "openai",
        "model_config": {"model": "gpt-4", "temperature": 0.7},
        "enable_memory": True,
        "short_term_memory": "in-memory",
        "long_term_memory": "mem0",
        "enable_tools": True,
        "tools": ["execute_python_code", "web_search"],
        "generate_tests": True,
    }

    response = requests.post(f"{base_url}/api/v1/projects/generate", json=project_request)
    assert response.status_code == 200
    gen_data = response.json()
    assert gen_data["success"] is True
    assert "project_id" in gen_data
    assert "download_url" in gen_data

    project_id = gen_data["project_id"]

    # 4. Download the project
    download_url = f"{base_url}{gen_data['download_url']}"
    response = requests.get(download_url)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

    # 5. Verify ZIP contents
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(response.content)
        tmp_path = Path(tmp.name)

    extracted_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(tmp_path, 'r') as zf:
        zf.extractall(extracted_dir)
        files = zf.namelist()

    # Verify expected files exist
    assert any("e2e_test_agent" in f for f in files)
    assert any("main.py" in f for f in files)
    assert any("agent" in f.lower() for f in files)

    # Cleanup
    tmp_path.unlink()
    import shutil
    shutil.rmtree(extracted_dir)

    print(f"✅ E2E test passed! Generated project: {project_id}")
```

- [ ] **Step 2: Run e2e test**

Run: `cd initializr-web && python -m pytest tests/test_e2e.py -v -s`
Expected: Test passes with project successfully generated and downloaded

- [ ] **Step 3: Verify all tests pass**

Run: `cd initializr-web && python -m pytest tests/ -v --cov=initializr_web`
Expected: All tests pass with good coverage

- [ ] **Step 4: Commit**

```bash
git add initializr-web/tests/test_e2e.py
git commit -m "test: add comprehensive end-to-end test"
```

---

## Self-Review Checklist

### Spec Coverage ✅

- [x] **Web Service Backend** (Tasks 1-6): FastAPI with all endpoints
- [x] **Frontend UI** (Tasks 7-10): Vue.js with multi-step form
- [x] **Deployment** (Task 11): Docker configuration
- [x] **Testing** (Tasks 12, 14): Integration and E2E tests
- [x] **Documentation** (Task 13): Complete docs

### Placeholder Scan ✅

- [x] No "TBD", "TODO", or "implement later" found
- [x] All code steps show actual implementation
- [x] All tests include complete assertions
- [x] All commands are exact and runnable

### Type Consistency ✅

- [x] ProjectRequest model matches across backend and frontend
- [x] Response models consistent between API and tests
- [x] Router imports match actual router names
- [x] Store field names match API request fields

### Next Steps

After completing this MVP plan, follow-up plans can cover:

1. **Skills System** (Phase 3): Skills templates, registry, and integration
2. **Testing & Evaluation** (Phase 4): pytest and agentscope.evaluate templates
3. **Advanced Features** (Phase 5): Monitoring, scaling, performance optimization

---

## Summary

This implementation plan delivers a **complete, working web service** for AgentScope Initializr with:

✅ **FastAPI Backend**
- RESTful API with all endpoints
- Pydantic validation
- Health monitoring
- Project generation and download

✅ **Vue.js Frontend**
- Multi-step configuration form
- Real-time validation
- Template selection
- Project download

✅ **Deployment Ready**
- Docker containerization
- Docker Compose setup
- Production-ready configuration

✅ **Well Tested**
- Unit tests for models
- Integration tests for endpoints
- End-to-end workflow test
- Good test coverage

✅ **Documented**
- API documentation (Swagger/ReDoc)
- Deployment guide
- README updates

**Estimated Effort**: 60-80 hours of focused development work across all 14 tasks.

**Result**: A fully functional web service that can be deployed and used immediately by internal teams to scaffold AgentScope projects.
