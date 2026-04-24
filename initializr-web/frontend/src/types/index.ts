// initializr-web/frontend/src/types/index.ts

export interface HookItem {
  name: string
  hook_type: string
  enabled: boolean
}

export interface ProjectRequest {
  name: string
  description?: string
  author?: string
  agent_type?: string
  python_version?: string
  model_provider?: string
  model_settings?: Record<string, any>
  enable_memory?: boolean
  short_term_memory?: string | null
  long_term_memory?: string | null
  redis_config?: Record<string, any> | null
  enable_knowledge?: boolean
  knowledge_config?: Record<string, any> | null
  enable_tools?: boolean
  tools?: string[]
  enable_skills?: boolean
  skills?: string[]
  enable_hooks?: boolean
  hooks?: HookItem[]
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
  enable_ragas_evaluation?: boolean
  evaluation_csv_filename?: string
  evaluation_metrics?: string[]
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

export interface ModelInfo {
  id: string
  name: string
  url: string
  is_embedding: boolean
}

export interface ModelProviderInfo {
  id: string
  name: string
  models: ModelInfo[]
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
