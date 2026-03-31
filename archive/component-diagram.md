# Component Architecture Diagram

## Frontend Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          VUE.JS APPLICATION ROOT                            │
│                                 App.vue                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │       Vue Router Navigation       │
                    └─────────────────┬─────────────────┘
                                      │
        ┌─────────────────────────────┴─────────────────────────────┐
        │                                                             │
┌───────▼────────┐                                      ┌──────────▼──────┐
│   Home View    │                                      │ Configure View  │
│   (Home.vue)   │                                      │(Configure.vue)  │
│                │                                      │                  │
│ ┌────────────┐ │                                      │ ┌──────────────┐│
│ │Welcome     │ │                                      │ │Configuration ││
│ │Message     │ │                                      │ │Form          ││
│ └────────────┘ │                                      │ └──────┬───────┘│
│                │                                      │        │         │
│ ┌────────────┐ │                                      │ ┌──────▼───────┐│
│ │Start       │ │                                      │ │Step 1:       ││
│ │Button      │ │                                      │ │BasicSettings ││
│ └────────────┘ │                                      │ └──────────────┘│
└────────────────┘                                      │                 │
                                                       │ ┌──────────────┐│
                                                       │ │Step 2:       ││
                                                       │ │Template      ││
                                                       │ │Selector      ││
                                                       │ └──────────────┘│
                                                       │                 │
                                                       │ ┌──────────────┐│
                                                       │ │Step 3:       ││
                                                       │ │Model Config  ││
                                                       │ └──────────────┘│
                                                       │                 │
                                                       │ ┌──────────────┐│
                                                       │ │Step 4:       ││
                                                       │ │Extensions    ││
                                                       │ └──────────────┘│
                                                       └─────────────────┘
```

## Backend Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI APPLICATION                                │
│                            (api.py)                                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                     Middleware Layer                                │  │
│  │  • CORS Middleware                                                  │  │
│  │  • Error Handlers                                                   │  │
│  │  • Request Logging                                                  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      API Router (/api/v1)                           │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│        ┌───────────────────────────┼───────────────────────────┐           │
│        │           │               │               │           │           │
│  ┌─────▼─────┐ ┌───▼────┐   ┌─────▼─────┐   ┌───▼──────┐   ┌─▼────────┐  │
│  │  Health   │ │Template│   │  Models   │   │Extension │   │ Projects │  │
│  │  Router   │ │ Router │   │  Router   │   │ Router   │   │  Router  │  │
│  └─────┬─────┘ └───┬────┘   └─────┬─────┘   └───┬──────┘   └────┬─────┘  │
│        │           │              │              │                │        │
└────────┼───────────┼──────────────┼──────────────┼────────────────┼────────┘
         │           │              │              │                │
         │           │              │              │                │
┌────────▼─────────▼──────────────▼──────────────▼────────────────▼────────┐
│                         BUSINESS LOGIC LAYER                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │
│  │ Pydantic         │  │ Model Converter  │  │ Project Generator    │   │
│  │ Validators       │  │                  │  │                      │   │
│  │                  │  │ ProjectRequest   │  │ • Template Engine    │   │
│  │ • HealthRequest  │  │    →             │  │ • File System        │   │
│  │ • ProjectRequest │  │ AgentScopeMeta   │  │ • ZIP Creator        │   │
│  │ • ...            │  │                  │  │                      │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
         │           │              │              │                │
         ▼           ▼              ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                        │
├──────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Template     │  │ Model        │  │ Extension    │  │ File System  │  │
│  │ Registry     │  │ Provider     │  │ Registry     │  │              │  │
│  │              │  │ Registry     │  │              │  │ /output/     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────────────────┘
```

## Detailed Component Specifications

### Frontend Components

#### 1. BasicSettings.vue
**Purpose**: Collect basic project information

**Props**: None

**State**:
```typescript
interface BasicSettingsState {
  projectName: string
  description: string
  author: string
  layout: 'standard' | 'lightweight'
  pythonVersion: string
}
```

**Emits**:
- `update:config` - When form data changes

**Validation**:
- Project name: 1-100 chars, alphanumeric + hyphens
- Python version: 3.10, 3.11, or 3.12

**Dependencies**:
- Element Plus form components
- Config store

---

#### 2. TemplateSelector.vue
**Purpose**: Display and select project templates

**Props**:
```typescript
interface Template {
  id: string
  name: string
  description: string
  icon: string
  tags: string[]
  suitable_for: string[]
}
```

**State**:
```typescript
interface TemplateSelectorState {
  selectedTemplate: string
  templates: Template[]
  loading: boolean
}
```

**Emits**:
- `select:template` - When template is selected

**Features**:
- Card-based layout
- Icon rendering
- Tag display
- Hover effects

---

#### 3. ConfigurationForm.vue
**Purpose**: Multi-step configuration form

**State**:
```typescript
interface ConfigFormState {
  currentStep: number
  totalSteps: number
  isValid: boolean
  isSubmitting: boolean
}
```

**Steps**:
1. Basic Settings
2. Template Selection
3. Model Configuration
4. Extension Configuration

**Navigation**:
- Next button (validates current step)
- Previous button
- Submit button (final step)

**Validation**:
- Step-specific validation
- Cross-step validation
- Real-time feedback

---

### Backend Components

#### 1. API Router (api.py)
**Purpose**: FastAPI application factory

**Responsibilities**:
- Initialize FastAPI app
- Configure CORS
- Include routers
- Register middleware
- Configure exception handlers

**Configuration**:
```python
app = FastAPI(
    title="AgentScope Initializr API",
    version="0.2.0",
    description="Project scaffolding API for AgentScope"
)
```

**Middleware Stack**:
1. CORS Middleware
2. Request ID Middleware (optional)
3. Logging Middleware (optional)
4. Error Handling Middleware

---

#### 2. Health Router (router/health.py)
**Purpose**: Health check endpoints

**Endpoints**:
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system info

**Response Models**:
```python
class HealthResponse(BaseModel):
    status: str
    version: str

class DetailedHealthResponse(HealthResponse):
    timestamp: datetime
    uptime_seconds: int
    system: dict
```

**Dependencies**: None (stateless)

---

#### 3. Templates Router (router/templates.py)
**Purpose**: Template listing endpoint

**Endpoints**:
- `GET /api/v1/templates` - List all templates

**Response Model**:
```python
class TemplateInfo(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    tags: List[str]
    suitable_for: List[str]

class TemplatesResponse(BaseModel):
    templates: List[TemplateInfo]
```

**Dependencies**:
- TemplateRegistry

**Caching**:
- In-memory cache
- TTL: 1 hour

---

#### 4. Projects Router (router/projects.py)
**Purpose**: Project generation and download

**Endpoints**:
- `POST /api/v1/projects/generate` - Generate project
- `GET /api/v1/projects/download/{project_id}` - Download project

**Request Model**:
```python
class ProjectRequest(BaseModel):
    name: str
    layout: str = "standard"
    agent_type: str = "basic"
    model_provider: str = "openai"
    model_config: Optional[ModelConfig] = None
    enable_memory: bool = True
    enable_tools: bool = True
    tools: List[str] = []
    python_version: str = "3.11"
    generate_tests: bool = True
```

**Response Model**:
```python
class ProjectResponse(BaseModel):
    success: bool
    project_id: str
    download_url: str
    message: str
```

**Dependencies**:
- Model Converter
- Project Generator
- File System

**Error Handling**:
- ValidationError (422)
- GenerationError (500)
- NotFoundError (404)

---

#### 5. Model Converter (converter.py)
**Purpose**: Convert API request to internal metadata

**Function Signature**:
```python
def project_request_to_metadata(
    request: ProjectRequest
) -> AgentScopeMetadata
```

**Mapping Rules**:
```
ProjectRequest.name → AgentScopeMetadata.name
ProjectRequest.layout → ProjectLayout(value)
ProjectRequest.agent_type → AgentType(value)
ProjectRequest.tools → List[ToolConfig]
ProjectRequest.model_config → ModelConfig
```

**Error Handling**:
- Invalid enum values → ValidationError
- Missing required fields → ValidationError

---

#### 6. Project Generator (generator.py)
**Purpose**: Generate project files and ZIP archive

**Key Functions**:

```python
async def generate_project(
    metadata: AgentScopeMetadata,
    output_dir: Path
) -> str:
    """Generate project and return project_id"""
```

```python
async def create_zip_archive(
    project_dir: Path,
    output_dir: Path
) -> Path:
    """Create ZIP archive from project directory"""
```

**Process Flow**:
1. Validate metadata
2. Create output directory
3. Load Jinja2 templates
4. Render each template
5. Write files to disk
6. Create requirements.txt
7. Create README.md
8. Create .env.example
9. Create ZIP archive
10. Generate unique project_id
11. Cleanup temporary files

**Template Context**:
```python
context = {
    'project_name': metadata.name,
    'agent_type': metadata.agent_type,
    'model_provider': metadata.model_provider,
    'tools': metadata.tools,
    'python_version': metadata.python_version,
    # ... additional fields
}
```

---

## Data Flow Diagram

```
User Input (Browser)
       │
       ▼
┌──────────────────┐
│ Vue.js Component │
│ (Form)           │
└────────┬─────────┘
         │ update:config
         ▼
┌──────────────────┐
│ Pinia Store      │
│ (Config State)   │
└────────┬─────────┘
         │ getState()
         ▼
┌──────────────────┐
│ API Client       │
│ (Axios)          │
└────────┬─────────┘
         │ POST /api/v1/projects/generate
         ▼
┌──────────────────┐
│ FastAPI          │
│ Router           │
└────────┬─────────┘
         │ Route to handler
         ▼
┌──────────────────┐
│ Pydantic         │
│ Validator        │
└────────┬─────────┘
         │ ProjectRequest (validated)
         ▼
┌──────────────────┐
│ Model Converter  │
└────────┬─────────┘
         │ AgentScopeMetadata
         ▼
┌──────────────────┐
│ Project          │
│ Generator        │
└────────┬─────────┘
         │ Render templates
         ▼
┌──────────────────┐
│ Jinja2           │
│ Templates        │
└────────┬─────────┘
         │ Rendered files
         ▼
┌──────────────────┐
│ File System      │
│ (/output/)       │
└────────┬─────────┘
         │ project_id
         ▼
┌──────────────────┐
│ ZIP Creator      │
└────────┬─────────┘
         │ ZIP file path
         ▼
┌──────────────────┐
│ Response         │
│ (JSON)           │
└──────────────────┘
```

## State Management Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PINIA STORE STRUCTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ConfigStore                                                    │
│  ├── state                                                     │
│  │   ├── projectName: string                                   │
│  │   ├── description: string                                   │
│  │   ├── author: string                                        │
│  │   ├── layout: string                                        │
│  │   ├── agentType: string                                     │
│  │   ├── modelProvider: string                                 │
│  │   ├── modelConfig: object                                   │
│  │   ├── enableMemory: boolean                                 │
│  │   ├── shortTermMemory: string                               │
│  │   ├── longTermMemory: string | null                         │
│  │   ├── enableTools: boolean                                  │
│  │   ├── tools: string[]                                       │
│  │   ├── pythonVersion: string                                 │
│  │   └── generateTests: boolean                                │
│  │                                                             │
│  ├── getters                                                   │
│  │   ├── isValid: boolean (computed)                           │
│  │   ├── selectedTemplate: Template (computed)                 │
│  │   └── configSummary: string (computed)                      │
│  │                                                             │
│  └── actions                                                   │
│      ├── updateField(field, value)                             │
│      ├── setTemplate(templateId)                               │
│      ├── setModelProvider(provider)                            │
│      ├── toggleTool(toolId)                                    │
│      ├── reset()                                               │
│      └── validate()                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Component Usage:
  • BasicSettings.vue: updateField('projectName', value)
  • TemplateSelector.vue: setTemplate('basic')
  • ConfigurationForm.vue: validate(), reset()
```

## Error Handling Chain

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING FLOW                          │
└─────────────────────────────────────────────────────────────────┘

1. CLIENT-SIDE VALIDATION (Vue.js)
   ├── Form validation rules
   ├── Field-specific validators
   └── Real-time feedback
   │
   │ If valid → Submit to API
   │ If invalid → Show inline errors
   │
   ▼
2. API LAYER (Axios)
   ├── Request interceptor
   ├── Response interceptor
   └── Error handler
   │
   │ If 4xx/5xx → Parse error
   │ If success → Return data
   │
   ▼
3. SERVER-SIDE VALIDATION (Pydantic)
   ├── Type checking
   ├── Constraint validation
   └── Custom validators
   │
   │ If valid → Process request
   │ If invalid → Return 422 ValidationError
   │
   ▼
4. BUSINESS LOGIC (Generator)
   ├── Template rendering
   ├── File I/O
   └── ZIP creation
   │
   │ If success → Return result
   │ If error → Raise GenerationError
   │
   ▼
5. ERROR RESPONSE
   ├── HTTP status code
   ├── Error details
   └── User-friendly message
   │
   ▼
6. UI FEEDBACK
   ├── Display error message
   ├── Highlight problematic fields
   └── Offer retry action
```

---

**Document Version**: 1.0
**Last Updated**: 2026-03-27
