# Project Generation Flow - Detailed Sequence

## Complete Project Generation Sequence

```mermaid
sequenceDiagram
    autonumber

    actor User as 👤 User
    participant Vue as 🖥️ Vue.js Frontend
    participant Store as 📦 Pinia Store
    participant Router as 🧭 Vue Router
    participant API as 🌐 API Client
    participant FastAPI as ⚡ FastAPI Backend
    participant Pydantic as 🔍 Pydantic Validator
    participant Converter as 🔄 Model Converter
    participant Registry as 📋 Template Registry
    participant Generator as 🏗️ Project Generator
    participant Jinja2 as 🎨 Jinja2 Engine
    participant FS as 💾 File System
    participant Zip as 📦 ZIP Creator

    Note over User,Zip: Phase 1: Initial Configuration

    User->>Vue: Navigate to /configure
    Router->>Vue: Load Configure View
    Vue->>Store: Initialize Config
    Store->>Store: Set defaults

    Note over User,Zip: Phase 2: Fetch Metadata

    Vue->>API: GET /api/v1/templates
    API->>FastAPI: HTTP GET /api/v1/templates
    FastAPI->>Registry: List templates
    Registry->>FastAPI: Template list
    FastAPI->>API: 200 TemplatesResponse
    API->>Store: Save templates
    Store->>Vue: Update UI

    Vue->>API: GET /api/v1/models
    API->>FastAPI: HTTP GET /api/v1/models
    FastAPI->>Registry: List models
    Registry->>FastAPI: Model providers
    FastAPI->>API: 200 ModelsResponse
    API->>Store: Save models
    Store->>Vue: Update UI

    Vue->>API: GET /api/v1/extensions
    API->>FastAPI: HTTP GET /api/v1/extensions
    FastAPI->>Registry: List extensions
    Registry->>FastAPI: Extension options
    FastAPI->>API: 200 ExtensionsResponse
    API->>Store: Save extensions
    Store->>Vue: Update UI

    Note over User,Zip: Phase 3: User Input

    User->>Vue: Fill project name
    User->>Vue: Select template
    User->>Vue: Configure model
    User->>Vue: Enable extensions
    Vue->>Store: Update config

    Note over User,Zip: Phase 4: Project Generation

    User->>Vue: Click "Generate"
    Vue->>Store: Get final config
    Store->>Vue: Return config
    Vue->>API: POST /api/v1/projects/generate
    API->>FastAPI: HTTP POST with JSON

    FastAPI->>Pydantic: Validate request
    Pydantic->>Pydantic: Check required fields
    Pydantic->>Pydantic: Validate patterns
    Pydantic->>Pydantic: Check constraints

    alt Validation Fails
        Pydantic->>FastAPI: ValidationError
        FastAPI->>API: 422 Error Response
        API->>Vue: Error details
        Vue->>User: Show validation errors
    else Validation Passes
        Pydantic->>FastAPI: Valid ProjectRequest
        FastAPI->>Converter: Convert request
        Converter->>Converter: Map fields to metadata
        Converter->>Converter: Transform tool list
        Converter->>Converter: Create AgentScopeMetadata
        Converter->>FastAPI: Return metadata

        FastAPI->>Generator: Generate project
        Generator->>Generator: Create output directory
        Generator->>Generator: Initialize file structure

        loop For each template file
            Generator->>Jinja2: Render template
            Jinja2->>Jinja2: Process variables
            Jinja2->>Jinja2: Apply filters
            Jinja2->>Generator: Rendered content
            Generator->>FS: Write file
            FS->>Generator: File written
        end

        Generator->>Generator: Create requirements.txt
        Generator->>Generator: Create README.md
        Generator->>Generator: Create .env.example
        Generator->>FS: Write metadata files

        Generator->>Zip: Create ZIP archive
        Zip->>FS: Add all files
        Zip->>Zip: Compress data
        Zip->>Generator: Return ZIP path

        Generator->>Generator: Generate project_id
        Generator->>FastAPI: Return project_id, download_url

        FastAPI->>API: 200 GenerateResponse
        API->>Store: Save project_id
        API->>Vue: Success response
        Vue->>User: Show success + download link

        Note over User,Zip: Phase 5: Download

        User->>Vue: Click download link
        Vue->>API: GET /api/v1/projects/download/{id}
        API->>FastAPI: HTTP GET with project_id
        FastAPI->>FS: Check if project exists

        alt Project Not Found
            FS->>FastAPI: File not found
            FastAPI->>API: 404 Error
            API->>Vue: Error response
            Vue->>User: Show error
        else Project Found
            FS->>FastAPI: Return ZIP file
            FastAPI->>API: application/zip stream
            API->>Vue: Binary data
            Vue->>User: Trigger browser download
            User->>User: Save ZIP file
        end
    end
```

## Component Interaction Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PROJECT GENERATION FLOW                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│    CLIENT    │
│              │  ┌──────────────────────────────────────────────────────────┐
│  ┌────────┐  │  │ Phase 1: INITIALIZATION                                 │
│  │ Browser│──┼──┤ • User navigates to /configure                         │
│  └────────┘  │  │ • Vue Router loads Configure View                      │
│              │  │ • Pinia Store initializes with defaults                 │
└──────┬───────┘  └──────────────────────────────────────────────────────────┘
       │
       │ HTTP Request
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER (Vue.js)                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │  BasicSettings  │    │TemplateSelector │    │ConfigurationForm│         │
│  │     .vue        │◄───│     .vue        │◄───│     .vue        │         │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘         │
│           │                      │                      │                    │
│           └──────────────────────┴──────────────────────┘                    │
│                                  │                                           │
│                                  ▼                                           │
│                      ┌─────────────────────┐                                 │
│                      │   Config Store      │                                 │
│                      │    (Pinia)          │                                 │
│                      │  - Project name     │                                 │
│                      │  - Template type    │                                 │
│                      │  - Model provider   │                                 │
│                      │  - Extensions       │                                 │
│                      └──────────┬──────────┘                                 │
└─────────────────────────────────┼──────────────────────────────────────────┘
                                  │
                                  │ API Calls
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          API LAYER (Axios)                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Health API  │  │Templates API │  │  Models API  │  │Projects API  │    │
│  │              │  │              │  │              │  │              │    │
│  │ GET /health  │  │ GET /templates│ │ GET /models  │  │ POST /generate│   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────┬───────┘    │
│                                                                  │            │
└──────────────────────────────────────────────────────────────────┼────────────┘
                                                                   │
                                                                   │ REST API
                                                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        BACKEND LAYER (FastAPI)                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         API Router                                   │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │  │ Health  │  │Template │  │ Models  │  │Extension│  │Projects │   │   │
│  │  │ Router  │  │ Router  │  │ Router  │  │ Router  │  │ Router  │   │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │   │
│  └───────┼────────────┼────────────┼────────────┼────────────┼──────────┘   │
│          │            │            │            │            │              │
│          └────────────┴────────────┴────────────┴────────────┘              │
│                                   │                                           │
│                                   ▼                                           │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                      Pydantic Validator                            │     │
│  │  • Validate request structure                                      │     │
│  │  • Check field constraints                                         │     │
│  │  • Type validation                                                 │     │
│  │  • Return ValidationError or ProjectRequest                        │     │
│  └───────────────────────────┬──────────────────────────────────────┘     │
└──────────────────────────────┼──────────────────────────────────────────────┘
                               │
                               │ Valid Request
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       BUSINESS LOGIC LAYER                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                        Model Converter                              │     │
│  │  ProjectRequest → AgentScopeMetadata                                │     │
│  │  • Map field names                                                  │     │
│  │  • Transform tool list to ToolConfig objects                        │     │
│  │  • Convert enum values                                              │     │
│  │  • Create memory configuration                                      │     │
│  └───────────────────────────┬──────────────────────────────────────┘     │
│                              │                                              │
│                              ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                      Project Generator                              │     │
│  │  • Create output directory                                         │     │
│  │  • Load Jinja2 templates                                           │     │
│  │  • Render template files                                           │     │
│  │  • Write generated files to disk                                   │     │
│  │  • Create ZIP archive                                              │     │
│  │  • Generate unique project_id                                       │     │
│  └───────────────────────────┬──────────────────────────────────────┘     │
└──────────────────────────────┼──────────────────────────────────────────────┘
                               │
                               │ File I/O
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Jinja2     │    │  File System │    │ZIP Creator   │                   │
│  │  Templates   │    │              │    │              │                   │
│  │              │    │ /output/     │    │ .zip files   │                   │
│  │ • basic/     │    │              │    │              │                   │
│  │ • multi/     │    │ {project_id}/│    │ project.zip  │                   │
│  │ • research/  │    │   └── ...    │    │              │                   │
│  │ • browser/   │    │              │    │              │                   │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                          RESPONSE FLOW                                        │
└──────────────────────────────────────────────────────────────────────────────┘

Success Path:
  Generator → project_id → FastAPI → GenerateResponse → API → Vue → User

Error Path:
  Validator → ValidationError → FastAPI → 422 Error → API → Vue → User
  Generator → Exception → FastAPI → 500 Error → API → Vue → User

Download Path:
  User → Vue → API → FastAPI → File System → ZIP stream → Browser → Download
```

## State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle: Application Start

    Idle --> FetchingMetadata: User navigates to /configure
    FetchingMetadata --> Idle: Fetch error
    FetchingMetadata --> Configuring: Metadata loaded successfully

    Configuring --> Configuring: User updates fields
    Configuring --> Validating: User clicks "Generate"
    Configuring --> Idle: User cancels

    Validating --> ValidationError: Validation fails
    Validating --> Generating: Validation passes

    ValidationError --> Configuring: User fixes errors

    Generating --> GenerationError: Generator fails
    Generating --> Ready: Generation succeeds

    GenerationError --> Configuring: User retries

    Ready --> Downloading: User clicks download
    Ready --> [*]: User closes
    Ready --> Configuring: User generates new project

    Downloading --> Ready: Download completes
    Downloading --> DownloadError: Download fails

    DownloadError --> Ready: User retries download

    note right of FetchingMetadata
        Fetch templates, models, extensions
        from backend API
    end note

    note right of Validating
        Pydantic validates all fields
        Checks constraints and patterns
    end note

    note right of Generating
        ProjectGenerator creates files
        Jinja2 renders templates
        ZIP archive created
    end note

    note right of Ready
        project_id available
        download_url generated
        Ready for download
    end note
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     ERROR HANDLING STRATEGY                      │
└─────────────────────────────────────────────────────────────────┘

CLIENT ERRORS (4xx)
┌─────────────────────────────────────────────────────────────────┐
│ ValidationError (422)                                           │
├─────────────────────────────────────────────────────────────────┤
│ Source: Pydantic validation                                     │
│ Trigger: Invalid request body                                   │
│ Response:                                                       │
│   {                                                             │
│     "detail": [                                                │
│       {                                                         │
│         "loc": ["body", "name"],                               │
│         "msg": "field required",                               │
│         "type": "value_error.missing"                          │
│       }                                                         │
│     ]                                                           │
│   }                                                             │
│ Action: Show inline validation errors in form                   │
└─────────────────────────────────────────────────────────────────┘

SERVER ERRORS (5xx)
┌─────────────────────────────────────────────────────────────────┐
│ GenerationError (500)                                           │
├─────────────────────────────────────────────────────────────────┤
│ Source: ProjectGenerator exception                              │
│ Trigger: Template rendering failure, file I/O error             │
│ Response:                                                       │
│   {                                                             │
│     "detail": "Failed to generate project: ..."                │
│   }                                                             │
│ Action: Show error message, offer retry button                  │
└─────────────────────────────────────────────────────────────────┘

NETWORK ERRORS
┌─────────────────────────────────────────────────────────────────┐
│ NetworkError                                                    │
├─────────────────────────────────────────────────────────────────┤
│ Source: Axios network error                                    │
│ Trigger: Connection timeout, server unreachable                 │
│ Action: Show error message, offer retry with exponential backoff│
└─────────────────────────────────────────────────────────────────┘

NOT FOUND ERRORS
┌─────────────────────────────────────────────────────────────────┐
│ NotFoundError (404)                                             │
├─────────────────────────────────────────────────────────────────┤
│ Source: Project download endpoint                               │
│ Trigger: Invalid project_id, expired project                    │
│ Response:                                                       │
│   {                                                             │
│     "detail": "Project not found or has expired"               │
│   }                                                             │
│ Action: Show error, redirect to configure page                 │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Optimization Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE OPTIMIZATION                      │
└─────────────────────────────────────────────────────────────────┘

FRONTEND OPTIMIZATION
├─ Lazy Loading
│  └─ Components loaded on demand
│
├─ Code Splitting
│  └─ Separate bundles per route
│
├─ Caching
│  └─ Metadata cached in Pinia store
│
└─ Debouncing
   └─ Input changes debounced (300ms)

BACKEND OPTIMIZATION
├─ Async I/O
│  └─ Non-blocking file operations
│
├─ Template Caching
│  └─ Jinja2 templates cached in memory
│
├─ Response Compression
│  └─ Gzip for JSON responses
│
└─ Streaming
   └─ ZIP files streamed, not buffered

DATABASE OPTIMIZATION (Future)
├─ Redis Cache
│  └─ Template registry cached
│
├─ Connection Pooling
│  └─ Reuse database connections
│
└─ Query Optimization
   └─ Index on project_id
```

---

**Document Version**: 1.0
**Last Updated**: 2026-03-27
