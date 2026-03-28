# AgentScope Initializr - Web Service & Skills System Design

**Date**: 2026-03-27
**Version**: 0.2.0
**Status**: Design Phase

## Executive Summary

Upgrade AgentScope Initializr from CLI-only tool to dual-mode system (CLI + Web Service) with comprehensive Skills system, testing/evaluation modules, and full AgentScope extension point configuration support.

## Table of Contents

1. [Goals and Requirements](#goals-and-requirements)
2. [Architecture Overview](#architecture-overview)
3. [Web Service Design](#web-service-design)
4. [Skills System](#skills-system)
5. [Testing & Evaluation](#testing--evaluation)
6. [Extension Points Configuration](#extension-points-configuration)
7. [Deployment & Operations](#deployment--operations)
8. [API Reference](#api-reference)
9. [Implementation Phases](#implementation-phases)

---

## Goals and Requirements

### Primary Objectives

1. **Web Service Deployment**: Deploy as web service with configuration page for internal team collaboration
2. **No Authentication Required**: Internal team use without authentication/permissions
3. **Skills System**: Add skills folder following AutoGen/CrewAI's skills concept
4. **Testing & Evaluation**: Integrate comprehensive testing and evaluation using AgentScope's built-in packages
5. **Memory Architecture**: Support both short-term and long-term memory configurations
6. **Extension Points**: Configure all AgentScope framework extension points (Model, Memory, Skills, Formatter, Hooks, Pipeline, RAG)

### Key Constraints

- Must use AgentScope's built-in `agentscope.evaluate` package (not custom evaluators)
- Must maintain backward compatibility with existing CLI
- All extension points must be optional with sensible defaults
- Skills follow AutoGen/CrewAI pattern: atomic ability units

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface Layer                        │
├───────────────────────────┬─────────────────────────────────────┤
│   CLI Interface (Click)   │   Web Interface (Vue.js 3)          │
│   - Existing commands     │   - Multi-step configuration form   │
│   - Wizard mode           │   - Real-time validation            │
│   - All features          │   - Project download                │
└───────────────┬───────────┴─────────────────┬───────────────────┘
                │                             │
                └─────────────┬───────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      API Layer                                   │
├─────────────────────────────┬───────────────────────────────────┤
│   CLI Handler               │   FastAPI REST API                │
│   (initializr-cli/)         │   (initializr-web/)               │
└───────────────┬─────────────┴─────────────────┬─────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    Core Logic Layer                             │
├─────────────────────────────────────────────────────────────────┤
│   ProjectGenerator          │   TemplateRegistry                │
│   - Generates projects      │   - Manages templates             │
│   - Renders templates       │   - Template metadata             │
│   - Applies configuration   │                                   │
├─────────────────────────────────────────────────────────────────┤
│   ExtensionGenerator        │   SkillsRegistry (NEW)            │
│   - Model/Memory/Tools      │   - Discovers skills              │
│   - Formatter/Hooks         │   - Skill metadata                │
│   - Pipeline/RAG            │   - Auto-import to agents         │
├─────────────────────────────────────────────────────────────────┤
│   AgentScopeMetadata        │   Data Models                     │
│   - Configuration dataclass │   - Enums, dataclasses            │
└─────────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    Template Layer                               │
├─────────────────────────────────────────────────────────────────┤
│   Jinja2 Templates           │   Skills Templates (NEW)         │
│   - basic-agent-src         │   - skills/{skill_name}/         │
│   - multi-agent-src         │   - skill.py, README.md, tests   │
│   - research-agent-src      │                                   │
│   - browser-agent-src       │   Testing Templates (NEW)        │
│                             │   - tests/conftest.py            │
│   Evaluation Templates (NEW)│   - tests/unit/                  │
│   - evaluation/run_eval.py  │   - tests/integration/           │
│   - benchmarks/             │                                   │
│   - metrics/                │                                   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    Generated Output                             │
├─────────────────────────────────────────────────────────────────┤
│   Standard Layout (src/)      │   Lightweight Layout             │
│   src/{package_name}/        │   {package_name}/                │
│   ├── agents/                │   ├── agents/                    │
│   ├── tools/                 │   ├── tools/                     │
│   ├── skills/ (NEW)          │   ├── config/                    │
│   ├── prompts/               │   ├── main.py                    │
│   ├── config/                │                                   │
│   ├── main.py                │                                   │
│   ├── tests/ (NEW)           │                                   │
│   └── evaluation/ (NEW)      │                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

**CLI Mode Flow:**
```
User → Click Command → ProjectGenerator → Template Rendering → Generated Project
                  ↓
            AgentScopeMetadata
```

**Web Mode Flow:**
```
User → Vue.js UI → API Request → FastAPI → ProjectGenerator → Template Rendering → Generated Project
                                          ↓
                                    AgentScopeMetadata
                                          ↓
                                      Response + Download URL
```

---

## Web Service Design

### Technology Stack

**Backend:**
- FastAPI 0.104+ (high-performance async framework)
- Python 3.11+
- Uvicorn (ASGI server)
- Pydantic v2 (data validation)

**Frontend:**
- Vue.js 3.4+ (Composition API)
- TypeScript 5.3+
- Vite 5.0+ (build tool)
- Element Plus 2.5+ (UI components)
- Pinia 2.1+ (state management)

**Deployment:**
- Docker (containerization)
- Docker Compose (orchestration)
- Nginx (reverse proxy, optional)

### FastAPI Backend Structure

```
initializr-web/
├── initializr_web/
│   ├── __init__.py
│   ├── api.py              # FastAPI application
│   ├── models.py           # Pydantic models
│   ├── router/
│   │   ├── __init__.py
│   │   ├── projects.py     # Project endpoints
│   │   ├── templates.py    # Template endpoints
│   │   └── metadata.py     # Metadata endpoints
│   └── static/             # Built frontend assets
└── pyproject.toml
```

### Key API Endpoints

**Project Generation:**
```python
POST /api/v1/projects/generate
Request: ProjectRequest (JSON)
Response: ProjectResponse {
  success: bool,
  message: str,
  download_url: str,
  project_id: str
}

GET /api/v1/projects/download/{project_id}
Response: ZIP file (application/zip)
```

**Metadata:**
```python
GET /api/v1/templates
Response: { templates: [...] }

GET /api/v1/models
Response: { providers: [...] }

GET /api/v1/extensions
Response: {
  memory: { short_term: [...], long_term: [...] },
  tools: { ... },
  formatters: [...],
  evaluators: [...],
  openjudge_graders: [...]
}
```

**Health:**
```python
GET /health
Response: { status: "healthy", ... }

GET /health/detailed
Response: {
  status: "healthy",
  system: { cpu_percent, memory_percent, disk_usage },
  projects: { total_generated, storage_used }
}
```

### Request/Response Models

```python
class ProjectRequest(BaseModel):
    # Basic settings
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    author: str = Field(default="", max_length=100)

    # Project structure
    layout: str = Field(default="standard", pattern="^(standard|lightweight)$")
    agent_type: str = Field(default="basic")
    python_version: str = Field(default="3.11", pattern="^3\.(10|11|12)$")

    # Model configuration
    model_provider: str = Field(default="openai")
    model_config: dict = Field(default_factory=dict)

    # Extension points (detailed in Extension Points section)
    enable_memory: bool = True
    short_term_memory: Optional[str] = None
    long_term_memory: Optional[str] = None

    enable_tools: bool = True
    tools: list[str] = Field(default_factory=list)

    enable_skills: bool = False
    skills: list[str] = Field(default_factory=list)

    enable_hooks: bool = False
    hooks: list[str] = Field(default_factory=list)

    enable_formatter: bool = False
    formatter: Optional[str] = None

    enable_rag: bool = False
    rag_config: Optional[dict] = None

    enable_pipeline: bool = False
    pipeline_config: Optional[dict] = None

    # Testing & evaluation
    generate_tests: bool = False
    generate_evaluation: bool = False
    evaluator_type: str = Field(default="general")
    enable_openjudge: bool = False
    openjudge_graders: list[str] = Field(default_factory=list)
    initial_benchmark_tasks: int = Field(default=0, ge=0, le=100)
```

### Vue.js Frontend Structure

```
initializr-web/src/
├── main.ts                    # Application entry
├── App.vue                    # Root component
├── router/
│   └── index.ts               # Vue Router configuration
├── stores/
│   └── config.ts              # Pinia store (form state)
├── components/
│   ├── ConfigurationForm.vue  # Multi-step form
│   ├── TemplateSelector.vue   # Template selection
│   ├── ExtensionConfig.vue    # Extension point config
│   ├── ProgressIndicator.vue  # Generation progress
│   └── DownloadButton.vue     # Download handler
├── views/
│   ├── Home.vue               # Home page
│   └── Configure.vue          # Configuration page
├── api/
│   └── client.ts              # Axios client
└── types/
    └── index.ts               # TypeScript types
```

### Web UI Flow

1. **Landing Page**: User selects agent type (basic/multi-agent/research/browser)
2. **Configuration Form** (Multi-step):
   - Step 1: Basic settings (name, description, author)
   - Step 2: Project layout (standard/lightweight)
   - Step 3: Model configuration
   - Step 4: Memory configuration (short-term + long-term)
   - Step 5: Tools & Skills selection
   - Step 6: Advanced extensions (Formatter, Hooks, RAG, Pipeline)
   - Step 7: Testing & Evaluation options
3. **Generation**: Show progress indicator
4. **Download**: Button to download generated project ZIP

---

## Skills System

### Skills Concept

**Definition**: Skills are high-level business abilities organized as atomic units, wrapping low-level tools.

**Tools vs Skills:**
- **Tools** = Low-level atomic functions decorated with `@tool`
- **Skills** = High-level classes that wrap tools into business capabilities

**Reference**: AutoGen/CrewAI skills pattern

### Generated Skills Structure

```
src/{project_name}/skills/
├── __init__.py                 # Skills discovery & exports
├── file_io/
│   ├── __init__.py
│   ├── skill.py                # FileIOSkill class
│   ├── README.md               # Skill documentation
│   ├── tools.py                # Skill-specific tools
│   └── tests.py                # Skill tests
├── web_api/
│   ├── __init__.py
│   ├── skill.py                # WebAPISkill class
│   ├── README.md
│   ├── tools.py
│   └── tests.py
└── data_analysis/
    ├── __init__.py
    ├── skill.py                # DataAnalysisSkill class
    ├── README.md
    ├── tools.py
    └── tests.py
```

### Skill Class Template

**Template: `skills/{skill_name}/skill.py.jinja2`**

```python
"""
{{ skill_description }} skill.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from agentscope.tools import tool

class {{ skill_class_name }}:
    """
    {{ skill_description }} skill.

    Wraps low-level tools into high-level business capability.
    """

    skill_name = "{{ skill_name }}"
    skill_category = "{{ skill_category }}"
    version = "1.0.0"
    description = "{{ skill_description }}"
    dependencies = [
        # List external dependencies here
        # e.g., "pandas>=1.0.0"
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the skill.

        Args:
            config: Skill configuration
        """
        self.config = config or {}
        self._initialize()

    def _initialize(self):
        """Initialize skill-specific resources."""
        # Initialize resources (connections, clients, etc.)
        pass

    async def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a skill operation.

        Args:
            operation: Operation name
            **kwargs: Operation arguments

        Returns:
            Operation result
        """
        if operation not in self.operations:
            raise ValueError(f"Unknown operation: {operation}")

        return await self.operations[operation](**kwargs)

    @property
    def operations(self) -> Dict[str, callable]:
        """Get available operations."""
        return {
            "operation1": self._operation1,
            "operation2": self._operation2,
        }

    async def _operation1(self, param1: str, param2: int) -> Dict[str, Any]:
        """
        Execute operation 1.

        Args:
            param1: First parameter
            param2: Second parameter

        Returns:
            Operation result
        """
        try:
            # Implement operation logic
            result = {
                "success": True,
                "data": "operation result",
            }
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    async def _operation2(self, **kwargs) -> Dict[str, Any]:
        """Execute operation 2."""
        # Implementation
        pass
```

### Skill README Template

**Template: `skills/{skill_name}/README.md.jinja2`**

```markdown
# {{ skill_class_name }} {{ skill_name }}

{{ skill_description }}

## Version
1.0.0

## Category
{{ skill_category }}

## Dependencies
{% if dependencies %}
{% for dep in dependencies %}
- {{ dep }}
{% endfor %}
{% else %}
None
{% endif %}

## Operations

### operation1
**Description**: Operation 1 description

**Parameters**:
- `param1` (str): Parameter 1 description
- `param2` (int): Parameter 2 description

**Returns**: Operation result dictionary

**Example**:
```python
skill = {{ skill_class_name }}()
result = await skill.execute("operation1", param1="value", param2=123)
```

### operation2
**Description**: Operation 2 description

**Parameters**: (TBD)

**Returns**: (TBD)

## Usage Example

```python
from {{ package_name }}.skills.{{ skill_name }} import {{ skill_class_name }}

# Initialize skill
skill = {{ skill_class_name }}(config={"option": "value"})

# Execute operation
result = await skill.execute("operation1", param1="test", param2=456)

if result["success"]:
    print(f"Success: {result['data']}")
else:
    print(f"Error: {result['error']}")
```

## Testing

Run skill tests:
```bash
pytest src/{{ package_name }}/skills/{{ skill_name }}/tests.py
```
```

### Skills Registry

**Template: `skills/__init__.py.jinja2`**

```python
"""
Skills module for {{ project_name }}.

Provides high-level business capabilities built on low-level tools.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type, List

from {{ package_name }}.skills.base import BaseSkill


def discover_skills() -> Dict[str, Type[BaseSkill]]:
    """
    Discover all skills in the skills directory.

    Returns:
        Dictionary mapping skill names to skill classes
    """
    skills = {}

    skills_dir = Path(__file__).parent
    for skill_module in pkgutil.iter_modules([str(skills_dir)]):
        if skill_module.name.startswith("_"):
            continue

        try:
            module = importlib.import_module(
                f"{{ package_name }}.skills.{skill_module.name}"
            )

            # Look for skill class (convention: skill.py or {name}_skill.py)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseSkill)
                    and attr is not BaseSkill
                ):
                    skills[attr.skill_name] = attr
                    break
        except ImportError:
            continue

    return skills


def get_skill(skill_name: str) -> Type[BaseSkill]:
    """
    Get a skill by name.

    Args:
        skill_name: Name of the skill

    Returns:
        Skill class

    Raises:
        ValueError: If skill not found
    """
    skills = discover_skills()
    if skill_name not in skills:
        raise ValueError(f"Skill not found: {skill_name}")
    return skills[skill_name]


def list_skills() -> List[str]:
    """
    List all available skills.

    Returns:
        List of skill names
    """
    return list(discover_skills().keys())


# Auto-import selected skills
{% for skill in skills %}
from {{ package_name }}.skills.{{ skill.name }} import {{ skill.class_name }}
{% endfor %}

__all__ = [
    "discover_skills",
    "get_skill",
    "list_skills",
    {% for skill in skills %}
    "{{ skill.class_name }}",
    {% endfor %}
]
```

### Skills Integration with Agents

**Template: `config/__init__.py.jinja2` (Skill Integration)**

```python
"""
Configuration module with skills integration.
"""

from {{ package_name }}.skills import discover_skills


def get_skillkit(agent_config: dict):
    """
    Get skillkit with configured skills.

    Args:
        agent_config: Agent configuration

    Returns:
        Skillkit or None
    """
    if not agent_config.get("enable_skills", False):
        return None

    from agentscope.tools import SkillKit

    skillkit = SkillKit()

    skills_to_load = agent_config.get("skills", [])
    skills_registry = discover_skills()

    for skill_name in skills_to_load:
        if skill_name in skills_registry:
            skill_class = skills_registry[skill_name]
            skill_instance = skill_class(config=agent_config.get("skill_configs", {}).get(skill_name, {}))

            # Add skill operations to toolkit
            for op_name, op_func in skill_instance.operations.items():
                skillkit.add(op_func)

    return skillkit
```

---

## Testing & Evaluation

### Testing Module

**Framework**: pytest

**Generated Structure**:
```
tests/
├── conftest.py                 # pytest fixtures
├── unit/
│   ├── test_agents.py          # Agent unit tests
│   ├── test_skills.py          # Skills unit tests
│   └── test_tools.py           # Tools unit tests
└── integration/
    └── test_agent_flow.py      # Integration tests
```

**Template: `tests/conftest.py.jinja2`**

```python
"""
pytest fixtures for {{ project_name }}.
"""

import pytest
import os
from pathlib import Path


@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return {
        "model": {
            "type": "test",
            "name": "test-model",
        },
        "memory": {
            "type": "in-memory",
        },
    }


@pytest.fixture
def test_model(test_config):
    """Test Model fixture."""
    from {{ package_name }}.config import get_model
    return get_model(config=test_config)


@pytest.fixture
def test_memory(test_config):
    """Test Memory fixture."""
    from {{ package_name }}.config import get_memory
    return get_memory(config=test_config)


@pytest.fixture
def test_toolkit():
    """Test Toolkit fixture."""
    from {{ package_name }}.config import get_toolkit
    return get_toolkit()


@pytest.fixture
def test_agent(test_model, test_memory, test_toolkit):
    """Test Agent fixture."""
    from {{ package_name }}.agents import create_{{ agent_type }}_agent
    return create_{{ agent_type }}_agent(
        model=test_model,
        memory=test_memory,
        toolkit=test_toolkit,
    )


@pytest.fixture
def sample_data_dir():
    """Sample data directory fixture."""
    return Path(__file__).parent / "data"
```

### Evaluation Module (Using AgentScope Native Framework)

**Key Principle**: Must use AgentScope's built-in `agentscope.evaluate` package

**Framework Components**:
- `BenchmarkBase`: Base class for custom benchmarks
- `Task`: Individual evaluation units
- `MetricBase`: Base class for custom metrics
- `GeneralEvaluator`: Sequential evaluator
- `RayEvaluator`: Parallel/distributed evaluator
- `FileEvaluatorStorage`: Persistent result storage

**Generated Structure**:
```
evaluation/
├── __init__.py                 # Evaluation module exports
├── run_evaluation.py           # Main evaluation entry point
├── config/
│   ├── __init__.py
│   └── evaluation_config.yaml  # Benchmark configuration
├── benchmarks/
│   ├── __init__.py
│   ├── base_benchmark.py       # Base benchmark class
│   └── custom_benchmark.py     # Custom benchmark implementation
├── metrics/
│   ├── __init__.py
│   └── custom_metrics.py       # Custom MetricBase implementations
└── reports/
    └── .gitkeep                # Evaluation report outputs
```

**Template: `evaluation/run_evaluation.py.jinja2`**

```python
"""
Evaluation entry point for {{ project_name }}.

Uses AgentScope's built-in evaluation framework.
"""

import asyncio
import os
import yaml
from pathlib import Path
from typing import Callable

from agentscope.evaluate import (
    GeneralEvaluator,
    RayEvaluator,
    FileEvaluatorStorage,
)

from {{ package_name }}.evaluation.benchmarks.custom_benchmark import CustomBenchmark
from {{ package_name }}.agents import create_{{ agent_type }}_agent


def load_config(config_path: str = "evaluation/config/evaluation_config.yaml") -> dict:
    """Load evaluation configuration."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


async def solution_generation(
    task,
    pre_hook: Callable,
) -> "SolutionOutput":
    """
    Generate solution for a task using {{ project_name }} agent.

    Args:
        task: Evaluation task
        pre_hook: Pre-execution hook

    Returns:
        SolutionOutput with agent response
    """
    from agentscope.evaluate import SolutionOutput
    from agentscope.message import Msg

    # Create agent instance
    agent = create_{{ agent_type }}_agent()

    # Register hook if provided
    if pre_hook:
        agent.register_instance_hook("pre_print", "save_logging", pre_hook)

    # Execute agent
    msg_input = Msg("user", task.input, role="user")
    response = await agent(msg_input)

    return SolutionOutput(
        success=True,
        output=response.content,
        trajectory=[task.input, response.content],
    )


async def main():
    """Run evaluation."""
    config = load_config()

    # Initialize benchmark
    benchmark = CustomBenchmark()

    # Choose evaluator based on config
    evaluator_class = RayEvaluator if config.get("use_ray", False) else GeneralEvaluator

    evaluator = evaluator_class(
        name=config.get("evaluator_name", "{{ project_name }} Evaluation"),
        benchmark=benchmark,
        n_repeat=config.get("n_repeat", 1),
        storage=FileEvaluatorStorage(
            save_dir=config.get("output_dir", "./evaluation/reports"),
        ),
        n_workers=config.get("n_workers", 1),
    )

    # Run evaluation
    await evaluator.run(solution_generation)

    print(f"Evaluation complete! Results saved to {config.get('output_dir')}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Template: `evaluation/benchmarks/custom_benchmark.py.jinja2`**

```python
"""
Custom benchmark for {{ project_name }}.

Implements BenchmarkBase from agentscope.evaluate.
"""

from typing import Generator
from agentscope.evaluate import (
    Task,
    BenchmarkBase,
)

from {{ package_name }}.evaluation.metrics.custom_metrics import (
    CustomMetric,
)


class CustomBenchmark(BenchmarkBase):
    """
    Custom benchmark for evaluating {{ project_name }} agents.

    Attributes:
        dataset: List of evaluation tasks
    """

    def __init__(self):
        """Initialize the benchmark."""
        super().__init__(
            name="{{ project_name }} Benchmark",
            description="Custom benchmark for {{ project_name }} agent evaluation",
        )
        self.dataset = self._load_data()

    def _load_data(self) -> list[Task]:
        """
        Load benchmark tasks.

        Returns:
            List of Task objects
        """
        tasks = []

        # Example tasks - replace with your benchmark data
        benchmark_data = [
            {
                "id": "task_1",
                "input": "Example question 1",
                "ground_truth": "Expected answer 1",
                "tags": {"category": "general", "difficulty": "easy"},
            },
            {
                "id": "task_2",
                "input": "Example question 2",
                "ground_truth": "Expected answer 2",
                "tags": {"category": "general", "difficulty": "medium"},
            },
        ]

        for data in benchmark_data:
            task = Task(
                id=data["id"],
                input=data["input"],
                ground_truth=data["ground_truth"],
                tags=data.get("tags", {}),
                metrics=[
                    CustomMetric(
                        ground_truth=data["ground_truth"],
                    ),
                ],
                metadata={},
            )
            tasks.append(task)

        return tasks

    def __iter__(self) -> Generator[Task, None, None]:
        """Iterate over benchmark tasks."""
        yield from self.dataset

    def __getitem__(self, index: int) -> Task:
        """Get task by index."""
        return self.dataset[index]

    def __len__(self) -> int:
        """Get number of tasks."""
        return len(self.dataset)
```

**Template: `evaluation/metrics/custom_metrics.py.jinja2`**

```python
"""
Custom metrics for {{ project_name }} evaluation.

Implements MetricBase from agentscope.evaluate.
"""

from agentscope.evaluate import (
    MetricBase,
    MetricResult,
    MetricType,
)


class CustomMetric(MetricBase):
    """
    Custom metric for evaluating agent responses.

    Attributes:
        ground_truth: Expected answer for comparison
    """

    def __init__(
        self,
        ground_truth: str,
    ):
        """Initialize the metric."""
        super().__init__(
            name="custom_correctness",
            metric_type=MetricType.NUMERICAL,
            description="Checks if agent response matches ground truth",
            categories=["accuracy"],
        )
        self.ground_truth = ground_truth

    async def __call__(
        self,
        solution: "SolutionOutput",
    ) -> MetricResult:
        """
        Evaluate the solution.

        Args:
            solution: Agent's solution output

        Returns:
            MetricResult with score (0.0 or 1.0)
        """
        # Simple string matching - customize as needed
        if solution.output.strip().lower() == self.ground_truth.strip().lower():
            return MetricResult(
                name=self.name,
                result=1.0,
                message="Correct",
            )
        else:
            return MetricResult(
                name=self.name,
                result=0.0,
                message=f"Incorrect. Expected: {self.ground_truth}",
            )
```

### Optional: OpenJudge Integration

**Template: `evaluation/metrics/openjudge_metrics.py.jinja2`**

```python
"""
OpenJudge integration for {{ project_name }} evaluation.

Provides OpenJudgeMetric adapter to use OpenJudge Graders
as AgentScope metrics.
"""

from agentscope.evaluate import (
    MetricBase,
    MetricType,
    MetricResult,
    SolutionOutput,
)
from openjudge.graders.base_grader import BaseGrader
from openjudge.utils.mapping import parse_data_with_mapper


class OpenJudgeMetric(MetricBase):
    """
    Adapter to use OpenJudge Graders as AgentScope metrics.

    Wraps any OpenJudge BaseGrader (e.g., RelevanceGrader,
    CorrectnessGrader, HallucinationGrader) as an AgentScope Metric.

    Attributes:
        grader_cls: OpenJudge Grader class
        data: Static task data
        mapper: Data mapping between AgentScope and OpenJudge formats
        grader: Instantiated OpenJudge Grader
    """

    def __init__(
        self,
        grader_cls: type[BaseGrader],
        data: dict,
        mapper: dict,
        name: str | None = None,
        description: str | None = None,
        **grader_kwargs,
    ):
        """
        Initialize the OpenJudge metric.

        Args:
            grader_cls: OpenJudge Grader class to wrap
            data: Static task data
            mapper: Data mapping (AgentScope -> OpenJudge)
            name: Metric name
            description: Metric description
            **grader_kwargs: Additional arguments for grader
        """
        self.grader = grader_cls(**grader_kwargs)
        super().__init__(
            name=name or self.grader.name,
            metric_type=MetricType.NUMERICAL,
            description=description or self.grader.description,
        )
        self.data = data
        self.mapper = mapper

    async def __call__(
        self,
        solution: SolutionOutput,
    ) -> MetricResult:
        """
        Evaluate solution using OpenJudge Grader.

        Args:
            solution: Agent's solution output

        Returns:
            MetricResult with score and reasoning
        """
        if not solution.success:
            return MetricResult(
                name=self.name,
                result=0.0,
                message="Solution failed",
            )

        try:
            # Build combined data context
            combined_data = {
                "data": self.data,
                "solution": {
                    "output": solution.output,
                    "meta": solution.meta,
                    "trajectory": getattr(solution, "trajectory", []),
                },
            }

            # Map data for Grader
            grader_inputs = parse_data_with_mapper(
                combined_data,
                self.mapper,
            )

            # Run evaluation
            result = await self.grader.aevaluate(**grader_inputs)

            # Format result
            if hasattr(result, "score"):
                return MetricResult(
                    name=self.name,
                    result=result.score,
                    message=result.reason or "",
                )
            else:
                return MetricResult(
                    name=self.name,
                    result=0.0,
                    message="Unknown result type",
                )

        except Exception as e:
            return MetricResult(
                name=self.name,
                result=0.0,
                message=f"Exception: {str(e)}",
            )
```

---

## Extension Points Configuration

### Extension Points Overview

All AgentScope extension points are configurable through Web UI and CLI.

**Extension Points:**
1. Model (single-select)
2. Memory (split into short-term + long-term, both single-select)
3. Tools (multi-select)
4. Skills (multi-select)
5. Formatter (single-select)
6. Hooks (multi-select)
7. Pipeline (single-select)
8. RAG (single-select)

### Selection Types

**Single-Select (Radio Buttons)**:
- Model Provider (openai/dashscope/anthropic/gemini/ollama)
- Short-term Memory (in-memory/redis/oceanbase)
- Long-term Memory (mem0/zep/oceanbase/none)
- Formatter (DashScopeChatFormatter/OpenAIChatFormatter/none)
- Pipeline (SequentialPipeline/DistributedPipeline/none)
- RAG (BasicRAG/AdvancedRAG/none)

**Multi-Select (Checkboxes)**:
- Tools (execute_python_code/execute_shell_command/web_search/browser_navigate/...)
- Skills (file_io/web_api/data_analysis/...)
- Hooks (logging_input/logging_output/save_logging/...)

### Web UI Configuration Panel

```
┌─────────────────────────────────────────────────────────┐
│ ⚙️ Extension Points Configuration                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Model Provider (single-select)                          │
│ ○ OpenAI    ○ DashScope    ○ Anthropic                 │
│ ○ Gemini    ○ Ollama                                    │
│                                                          │
│ ────────────────────────────────────────────────────── │
│                                                          │
│ Short-term Memory (single-select)                       │
│ ○ in-memory    ○ redis    ○ oceanbase                  │
│                                                          │
│ Long-term Memory (single-select)                        │
│ ○ mem0    ○ zep    ○ oceanbase    ○ none               │
│                                                          │
│ ────────────────────────────────────────────────────── │
│                                                          │
│ Tools (multi-select)                                    │
│ ☑ execute_python_code                                   │
│ ☑ execute_shell_command                                 │
│ ☐ web_search                                            │
│ ☐ browser_navigate                                      │
│                                                          │
│ ────────────────────────────────────────────────────── │
│                                                          │
│ Skills (multi-select)                                   │
│ ☐ file_io                                               │
│ ☐ web_api                                               │
│ ☐ data_analysis                                         │
│                                                          │
│ ────────────────────────────────────────────────────── │
│                                                          │
│ Formatter (single-select)                               │
│ ○ DashScopeChatFormatter                                │
│ ○ OpenAIChatFormatter                                   │
│ ○ None                                                  │
│                                                          │
│ ────────────────────────────────────────────────────── │
│                                                          │
│ Hooks (multi-select)                                    │
│ ☐ logging_input                                         │
│ ☐ logging_output                                        │
│ ☐ save_logging                                          │
│                                                          │
│ Pipeline (single-select)                                │
│ ○ SequentialPipeline                                    │
│ ○ DistributedPipeline                                   │
│ ○ None                                                  │
│                                                          │
│ RAG (single-select)                                     │
│ ○ BasicRAG                                              │
│ ○ AdvancedRAG                                           │
│ ○ None                                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### AgentScopeMetadata Model

```python
@dataclass
class AgentScopeMetadata:
    # Basic settings
    project_name: str
    description: str = ""
    author: str = ""
    package_name: str = field(init=False)

    # Project structure
    layout: ProjectLayout = ProjectLayout.STANDARD
    agent_type: AgentType = AgentType.BASIC
    python_version: str = "3.11"

    # Model configuration (single-select)
    model_provider: ModelProvider = ModelProvider.OPENAI
    model_config: Dict[str, Any] = field(default_factory=dict)

    # Memory configuration (split into two single-select)
    enable_memory: bool = True
    short_term_memory_type: Optional[str] = None
    long_term_memory_type: Optional[str] = None

    # Tools configuration (multi-select)
    enable_tools: bool = True
    tools: List[str] = field(default_factory=list)

    # Skills configuration (multi-select)
    enable_skills: bool = False
    skills: List[str] = field(default_factory=list)

    # Hooks configuration (multi-select)
    enable_hooks: bool = False
    hooks: List[str] = field(default_factory=list)

    # Formatter configuration (single-select)
    enable_formatter: bool = False
    formatter_type: Optional[str] = None

    # RAG configuration (single-select)
    enable_rag: bool = False
    rag_config: Optional[Dict[str, Any]] = None

    # Pipeline configuration (single-select)
    enable_pipeline: bool = False
    pipeline_config: Optional[Dict[str, Any]] = None

    # Testing & evaluation
    generate_tests: bool = False
    generate_evaluation: bool = False
    evaluator_type: str = "general"
    enable_openjudge: bool = False
    openjudge_graders: List[str] = field(default_factory=list)
    initial_benchmark_tasks: int = 0

    def __post_init__(self):
        """Compute package name from project name."""
        self.package_name = self.project_name.replace("-", "_")
```

---

## Deployment & Operations

### Docker Deployment

**Dockerfile**:

```dockerfile
# Multi-stage build for AgentScope Initializr Web Service
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Build frontend assets
COPY initializr-web/ ./
RUN npm install && npm run build

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[web]"

# Copy built artifacts from builder
COPY --from=builder /app/initializr-web/dist ./initializr-web/dist
COPY --from=builder /app/initializr-* ./initializr-*

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

**docker-compose.yml**:

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
      - MAX_UPLOAD_SIZE=100MB
      - OUTPUT_DIR=/app/output
      - ALLOW_ORIGINS=http://localhost:5173,http://localhost:8080
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: agentscope-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./initializr-web/dist:/usr/share/nginx/html:ro
    depends_on:
      - agentscope-initializr
    restart: unless-stopped
```

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Nginx / Load Balancer                    │
│                    (SSL Termination, Static Files)              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
┌───────────────▼──────────────┐  ┌────▼──────────────────────────┐
│   AgentScope Initializr      │  │  Docker Container (App)       │
│   Web Service (FastAPI)      │  │  - FastAPI Backend            │
│   - Port 8000                │  │  - Vue.js Frontend (Built)    │
│   - Multi-instance           │  │  - Template Files             │
└───────────────┬──────────────┘  └───────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────────────┐
│              Persistent Storage                                 │
│  - Project Output Directory (generated projects)                │
│  - Configuration Files                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Operations & Monitoring

**Health Check Endpoints:**

```python
@app.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "AgentScope Initializr",
        "version": "0.2.0",
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics."""
    import psutil

    return {
        "status": "healthy",
        "service": "AgentScope Initializr",
        "version": "0.2.0",
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
        },
        "projects": {
            "total_generated": len(list(output_dir.glob("*.zip"))),
            "storage_used": sum(
                f.stat().st_size for f in output_dir.glob("*")
            ),
        },
    }
```

**Logging Configuration:**

```python
import logging

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "info").upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agentscope-initializr.log"),
        logging.StreamHandler(),
    ],
)
```

**Automatic Cleanup:**

```python
async def cleanup_old_projects():
    """Remove projects older than 1 hour."""
    import time
    import shutil
    max_age = 3600  # 1 hour
    now = time.time()

    for project_dir in output_dir.iterdir():
        if project_dir.is_dir():
            if now - project_dir.stat().st_mtime > max_age:
                shutil.rmtree(project_dir, ignore_errors=True)
                zip_path = output_dir / f"{project_dir.name}.zip"
                zip_path.unlink(missing_ok=True)

async def _periodic_cleanup():
    """Run cleanup every 30 minutes."""
    import asyncio
    while True:
        await asyncio.sleep(1800)  # 30 minutes
        await cleanup_old_projects()
```

---

## API Reference

### RESTful API Endpoints

#### Project Generation

**POST /api/v1/projects/generate**

Generate a new AgentScope project.

**Request Body:**
```json
{
  "name": "my-agent",
  "description": "My custom agent",
  "author": "John Doe",
  "layout": "standard",
  "agent_type": "multi-agent",
  "model_provider": "openai",
  "model_config": {
    "model": "gpt-4",
    "temperature": 0.7
  },
  "enable_memory": true,
  "short_term_memory": "in-memory",
  "long_term_memory": "mem0",
  "enable_tools": true,
  "tools": ["execute_python_code", "web_search"],
  "enable_skills": true,
  "skills": ["file_io", "web_api"],
  "generate_tests": true,
  "generate_evaluation": true,
  "evaluator_type": "ray",
  "enable_openjudge": true,
  "openjudge_graders": ["RelevanceGrader", "CorrectnessGrader"],
  "initial_benchmark_tasks": 5
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Project generated successfully",
  "download_url": "/api/v1/projects/download/my-agent_a1b2c3d4",
  "project_id": "my-agent_a1b2c3d4"
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Failed to generate project: Invalid agent type"
}
```

#### Download Project

**GET /api/v1/projects/download/{project_id}**

Download a generated project as a ZIP file.

**Response:** ZIP file (application/zip)

**Response (404 Not Found):**
```json
{
  "detail": "Project not found"
}
```

#### List Templates

**GET /api/v1/templates**

List all available project templates.

**Response (200 OK):**
```json
{
  "templates": [
    {
      "id": "basic",
      "name": "Basic ReAct Agent",
      "description": "基础 ReAct 智能体，支持对话和工具调用"
    },
    {
      "id": "multi-agent",
      "name": "Multi-Agent System",
      "description": "多智能体协作系统，支持智能体间通信和任务分配"
    }
  ]
}
```

#### List Models

**GET /api/v1/models**

List available model providers.

**Response (200 OK):**
```json
{
  "providers": [
    {
      "id": "openai",
      "name": "Openai"
    },
    {
      "id": "dashscope",
      "name": "Dashscope"
    }
  ]
}
```

#### List Extensions

**GET /api/v1/extensions**

List available extension point options.

**Response (200 OK):**
```json
{
  "memory": {
    "short_term": ["in-memory", "redis", "oceanbase"],
    "long_term": ["mem0", "zep", "oceanbase", "none"]
  },
  "tools": {
    "execute_python_code": "Execute Python code",
    "execute_shell_command": "Execute shell commands",
    "web_search": "Web search (Tavily)",
    "browser_navigate": "Browser navigation"
  },
  "formatters": ["DashScopeChatFormatter", "OpenAIChatFormatter"],
  "evaluators": ["general", "ray"],
  "openjudge_graders": [
    "RelevanceGrader",
    "CorrectnessGrader",
    "HallucinationGrader",
    "SafetyGrader",
    "CodeQualityGrader"
  ]
}
```

#### Health Check

**GET /health**

Basic health check.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "AgentScope Initializr",
  "version": "0.2.0"
}
```

**GET /health/detailed**

Detailed health check with system metrics.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "AgentScope Initializr",
  "version": "0.2.0",
  "system": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_usage": 62.1
  },
  "projects": {
    "total_generated": 127,
    "storage_used": 2147483648
  }
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Implementation Phases

### Phase 1: Core Web Service (Priority 1)

**Duration**: 1-2 weeks

**Tasks**:
1. Set up FastAPI project structure
2. Implement basic API endpoints (health, templates, models)
3. Implement project generation endpoint
4. Create Docker configuration
5. Implement shared core logic (extract from CLI)
6. Basic testing

**Deliverables**:
- Working FastAPI backend
- Docker image
- API documentation
- Basic tests

### Phase 2: Frontend UI (Priority 1)

**Duration**: 2-3 weeks

**Tasks**:
1. Set up Vue.js 3 + TypeScript project
2. Create configuration form components
3. Implement template selection UI
4. Implement extension point configuration UI
5. Add project download functionality
6. Add progress indicators
7. Styling and polish

**Deliverables**:
- Working Vue.js frontend
- Multi-step configuration form
- Real-time validation
- Project download feature

### Phase 3: Skills System (Priority 2)

**Duration**: 1-2 weeks

**Tasks**:
1. Design skills directory structure
2. Create skill templates (skill.py, README.md, tools.py, tests.py)
3. Implement Skills Registry
4. Implement skill auto-import to agent configuration
5. Create pre-built skills (file_io, web_api, data_analysis)
6. Update agent templates to use skills

**Deliverables**:
- Skills templates
- Skills Registry implementation
- 3-5 pre-built skills
- Updated agent templates

### Phase 4: Testing & Evaluation (Priority 2)

**Duration**: 1-2 weeks

**Tasks**:
1. Create pytest module templates
2. Implement agentscope.evaluate integration
3. Create BenchmarkBase templates
4. Create MetricBase templates
5. Implement OpenJudge integration (optional)
6. Create evaluation configuration templates
7. Update CLI and Web UI to support testing/evaluation options

**Deliverables**:
- Testing module templates
- Evaluation module templates
- OpenJudge integration templates
- Updated CLI/Web UI

### Phase 5: Advanced Features (Priority 3)

**Duration**: 2-3 weeks

**Tasks**:
1. Implement multi-instance deployment
2. Add load balancing support
3. Create monitoring dashboards
4. Implement project versioning
5. Add configuration export/import
6. Performance optimization
7. Advanced security features

**Deliverables**:
- Multi-instance deployment guide
- Monitoring dashboard
- Configuration management features
- Performance improvements

---

## Summary

This design provides a comprehensive upgrade to AgentScope Initializr with:

1. **Dual Mode Operation**: Maintains CLI functionality while adding Web UI
2. **Web Service Deployment**: FastAPI + Vue.js with Docker containerization
3. **Skills System**: Atomic ability units following AutoGen/CrewAI pattern
4. **Testing & Evaluation**: pytest + agentscope.evaluate integration
5. **Extension Points**: Full AgentScope framework configuration
6. **Industry Alignment**: Matches CrewAI, LangChain, AutoGen structures

**Key Benefits**:
- Team collaboration via web interface
- Standardized project scaffolding
- Comprehensive configuration options
- Evaluation-ready projects
- Future-proof modular design

**Next Steps**: Create detailed implementation plan using writing-plans skill.

---

**References**:
- [AgentScope Documentation](https://doc.agentscope.io)
- [AgentScope Task Evaluation](https://doc.agentscope.io/tutorial/task_eval.html)
- [OpenJudge Integration](https://doc.agentscope.io/zh_CN/tutorial/task_eval_openjudge.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vue.js Documentation](https://vuejs.org)
