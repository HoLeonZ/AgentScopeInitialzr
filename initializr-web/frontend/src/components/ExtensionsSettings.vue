<template>
  <div class="extensions-settings">
    <!-- Tools Extension -->
    <el-card class="extension-card tools-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#409EFF"><Tools /></el-icon>
            <span class="header-title">Tools Extension</span>
          </div>
          <el-switch
            v-model="localForm.enable_tools"
            size="large"
            @change="updateField('enable_tools', $event)"
          />
        </div>
        <div class="card-description">
          Enable tools to extend agent capabilities with powerful functions
        </div>
      </template>

      <template v-if="localForm.enable_tools">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Select tools to enable for your agent. Each tool provides specific capabilities.
        </el-alert>

        <el-form-item label="Available Tools">
          <el-checkbox-group v-model="localForm.tools" @change="updateField('tools', $event)">
            <div class="tools-grid">
              <div
                v-for="(desc, tool) in extensions.tools"
                :key="tool"
                class="tool-item"
                :class="{ 'is-checked': localForm.tools.includes(tool) }"
              >
                <el-checkbox :label="tool" class="tool-checkbox">
                  <div class="tool-content">
                    <div class="tool-header">
                      <el-icon class="tool-icon"><Operation /></el-icon>
                      <span class="tool-name">{{ formatToolName(tool) }}</span>
                    </div>
                    <span class="tool-desc">{{ desc }}</span>
                  </div>
                </el-checkbox>
              </div>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <!-- Code Preview -->
        <el-collapse style="margin-top: 20px">
          <el-collapse-item name="toolsPreview">
            <template #title>
              <div class="preview-title">
                <el-icon><View /></el-icon>
                <span>Code Preview - Tools Configuration</span>
              </div>
            </template>
            <div class="code-preview-container">
              <div class="code-preview">
                <pre><code>{{ toolsCodePreview }}</code></pre>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>

        <el-alert
          type="warning"
          :closable="false"
          show-icon
          v-if="localForm.tools.length > 0"
        >
          Selected {{ localForm.tools.length }} tool(s). Some tools may require additional API keys (e.g., TAVILY_API_KEY for web search).
        </el-alert>
      </template>
    </el-card>

    <!-- Formatter Extension -->
    <el-card class="extension-card formatter-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#67C23A"><Document /></el-icon>
            <span class="header-title">Formatter Extension</span>
          </div>
          <el-switch
            v-model="localForm.enable_formatter"
            size="large"
            @change="updateField('enable_formatter', $event)"
          />
        </div>
        <div class="card-description">
          Configure message formatting for different model providers
        </div>
      </template>

      <template v-if="localForm.enable_formatter">
        <el-form-item label="Formatter Type">
          <el-select
            v-model="localForm.formatter"
            placeholder="Select formatter type"
            size="large"
            @change="updateField('formatter', $event)"
          >
            <el-option
              v-for="formatter in extensions.formatters"
              :key="formatter"
              :label="formatter"
              :value="formatter"
            >
              <div class="option-item">
                <div class="option-label">{{ formatter }}</div>
                <div class="option-desc">{{ getFormatterDescription(formatter) }}</div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <!-- Code Preview -->
        <el-collapse style="margin-top: 20px">
          <el-collapse-item name="formatterPreview">
            <template #title>
              <div class="preview-title">
                <el-icon><View /></el-icon>
                <span>Code Preview - Formatter Configuration</span>
              </div>
            </template>
            <div class="code-preview-container">
              <div class="code-preview">
                <pre><code>{{ formatterCodePreview }}</code></pre>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </template>
    </el-card>

    <!-- Hooks Extension -->
    <el-card class="extension-card hooks-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#E6A23C"><Link /></el-icon>
            <span class="header-title">Hooks Extension</span>
          </div>
          <el-switch
            v-model="localForm.enable_hooks"
            size="large"
            @change="updateField('enable_hooks', $event)"
          />
        </div>
        <div class="card-description">
          Add lifecycle hooks to intercept agent execution at key points
        </div>
      </template>

      <template v-if="localForm.enable_hooks">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Hooks allow you to execute custom code at specific points during agent execution.
        </el-alert>

        <el-form-item label="Lifecycle Hooks">
          <el-checkbox-group v-model="localForm.hooks" @change="updateField('hooks', $event)">
            <div class="hooks-grid">
              <div
                v-for="hook in availableHooks"
                :key="hook.value"
                class="hook-item"
                :class="{ 'is-checked': localForm.hooks.includes(hook.value) }"
              >
                <el-checkbox :label="hook.value" class="hook-checkbox">
                  <div class="hook-content">
                    <div class="hook-header">
                      <el-icon class="hook-icon"><Connection /></el-icon>
                      <span class="hook-name">{{ hook.label }}</span>
                    </div>
                    <span class="hook-desc">{{ hook.description }}</span>
                    <el-tag size="small" type="info">{{ hook.timing }}</el-tag>
                  </div>
                </el-checkbox>
              </div>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <!-- Code Preview -->
        <el-collapse style="margin-top: 20px">
          <el-collapse-item name="hooksPreview">
            <template #title>
              <div class="preview-title">
                <el-icon><View /></el-icon>
                <span>Code Preview - Hooks Configuration</span>
              </div>
            </template>
            <div class="code-preview-container">
              <div class="code-preview">
                <pre><code>{{ hooksCodePreview }}</code></pre>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </template>
    </el-card>

    <!-- Skills Extension -->
    <el-card class="extension-card skills-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#F56C6C"><Star /></el-icon>
            <span class="header-title">Skills Extension</span>
          </div>
          <el-switch
            v-model="localForm.enable_skills"
            size="large"
            @change="updateField('enable_skills', $event)"
          />
        </div>
        <div class="card-description">
          Select specialized skills from the skill management system
        </div>
      </template>

      <template v-if="localForm.enable_skills">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Skills are uploaded by administrators via the Skill Management System. Select the skills you want to include in your project.
        </el-alert>

        <SkillSelector v-model="localForm.skills" @update:model-value="updateField('skills', $event)" />

        <!-- Code Preview -->
        <el-collapse style="margin-top: 20px">
          <el-collapse-item name="skillsPreview">
            <template #title>
              <div class="preview-title">
                <el-icon><View /></el-icon>
                <span>Code Preview - Skills Configuration</span>
              </div>
            </template>
            <div class="code-preview-container">
              <div class="code-preview">
                <pre><code>{{ skillsCodePreview }}</code></pre>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </template>
    </el-card>

    <!-- RAG Extension -->
    <el-card class="extension-card rag-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#909399"><Reading /></el-icon>
            <span class="header-title">RAG Extension</span>
            <el-tag size="small" type="warning">Advanced</el-tag>
          </div>
          <el-switch
            v-model="localForm.enable_rag"
            size="large"
            @change="updateField('enable_rag', $event)"
          />
        </div>
        <div class="card-description">
          Enable Retrieval-Augmented Generation for knowledge base integration
        </div>
      </template>

      <template v-if="localForm.enable_rag">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          RAG enhances your agent with external knowledge retrieval capabilities.
        </el-alert>

        <el-divider content-position="left">
          <el-icon><Setting /></el-icon>
          Vector Store Configuration
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Vector Store">
              <el-select
                v-model="ragConfig.store_type"
                placeholder="Select store"
                size="large"
                @change="updateRagConfig"
              >
                <el-option label="Qdrant" value="qdrant">
                  <div class="option-item">
                    <div class="option-label">Qdrant</div>
                    <div class="option-desc">High-performance vector database</div>
                  </div>
                </el-option>
                <el-option label="KBase" value="kbase">
                  <div class="option-item">
                    <div class="option-label">KBase</div>
                    <div class="option-desc">Enterprise knowledge base service</div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="Embedding Model">
              <el-input
                v-model="ragConfig.embedding_model"
                placeholder="openai:text-embedding-ada-002"
                @input="updateRagConfig"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- Qdrant Configuration -->
        <template v-if="ragConfig.store_type === 'qdrant'">
          <el-divider content-position="left">
            <el-icon><Setting /></el-icon>
            Qdrant Configuration
          </el-divider>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Qdrant Host">
                <el-input
                  v-model="ragConfig.qdrant_host"
                  placeholder="localhost"
                  @input="updateRagConfig"
                />
                <span class="hint">Qdrant server hostname</span>
              </el-form-item>
            </el-col>

            <el-col :span="12">
              <el-form-item label="Qdrant Port">
                <el-input-number
                  v-model="ragConfig.qdrant_port"
                  :min="1"
                  :max="65535"
                  placeholder="6333"
                  @change="updateRagConfig"
                />
                <span class="hint">Qdrant server port</span>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="Collection Name">
            <el-input
              v-model="ragConfig.collection_name"
              placeholder="agent_documents"
              @input="updateRagConfig"
            />
            <span class="hint">Qdrant collection name for storing documents</span>
          </el-form-item>
        </template>

        <!-- KBase Configuration -->
        <template v-if="ragConfig.store_type === 'kbase'">
          <el-divider content-position="left">
            <el-icon><Setting /></el-icon>
            KBase Configuration
          </el-divider>

          <el-form-item label="KBase Retrieval URL">
            <el-input
              v-model="ragConfig.kbase_retrieval_url"
              placeholder="https://kbase.example.com/api/retrieve"
              @input="updateRagConfig"
            />
            <span class="hint">KBase retrieval service URL</span>
          </el-form-item>
        </template>

        <el-divider content-position="left">
          <el-icon><Setting /></el-icon>
          Chunking Configuration
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Chunk Size">
              <el-input-number
                v-model="ragConfig.chunk_size"
                :min="100"
                :max="2000"
                :step="100"
                size="large"
                @change="updateRagConfig"
              />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="Chunk Overlap">
              <el-input-number
                v-model="ragConfig.chunk_overlap"
                :min="0"
                :max="500"
                :step="50"
                size="large"
                @change="updateRagConfig"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- Code Preview -->
        <el-collapse style="margin-top: 20px">
          <el-collapse-item name="ragPreview">
            <template #title>
              <div class="preview-title">
                <el-icon><View /></el-icon>
                <span>Code Preview - RAG Configuration</span>
              </div>
            </template>
            <div class="code-preview-container">
              <div class="code-preview">
                <pre><code>{{ ragCodePreview }}</code></pre>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </template>
    </el-card>

    <!-- Pipeline Extension -->
    <el-card class="extension-card pipeline-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#909399"><Operation /></el-icon>
            <span class="header-title">Pipeline Extension</span>
            <el-tag size="small" type="warning">Advanced</el-tag>
          </div>
          <el-switch
            v-model="localForm.enable_pipeline"
            size="large"
            @change="updateField('enable_pipeline', $event)"
          />
        </div>
        <div class="card-description">
          Enable multi-agent pipeline for complex workflow orchestration
        </div>
      </template>

      <template v-if="localForm.enable_pipeline">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Pipeline enables multiple agents to work together in a coordinated workflow.
        </el-alert>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="Pipeline Type">
              <el-select
                v-model="pipelineConfig.type"
                placeholder="Select type"
                size="large"
                @change="updatePipelineConfig"
              >
                <el-option label="Sequential" value="sequential">
                  <div class="option-item">
                    <div class="option-label">Sequential</div>
                    <div class="option-desc">Execute agents in order</div>
                  </div>
                </el-option>
                <el-option label="Parallel" value="parallel">
                  <div class="option-item">
                    <div class="option-label">Parallel</div>
                    <div class="option-desc">Execute agents simultaneously</div>
                  </div>
                </el-option>
                <el-option label="Conditional" value="conditional">
                  <div class="option-item">
                    <div class="option-label">Conditional</div>
                    <div class="option-desc">Branch based on conditions</div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="Number of Stages">
              <el-input-number
                v-model="pipelineConfig.num_stages"
                :min="2"
                :max="10"
                size="large"
                @change="updatePipelineConfig"
              />
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="Error Handling">
              <el-select
                v-model="pipelineConfig.error_handling"
                placeholder="Select strategy"
                size="large"
                @change="updatePipelineConfig"
              >
                <el-option label="Stop on Error" value="stop" />
                <el-option label="Continue on Error" value="continue" />
                <el-option label="Retry" value="retry" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- Code Preview -->
        <el-collapse style="margin-top: 20px">
          <el-collapse-item name="pipelinePreview">
            <template #title>
              <div class="preview-title">
                <el-icon><View /></el-icon>
                <span>Code Preview - Pipeline Configuration</span>
              </div>
            </template>
            <div class="code-preview-container">
              <div class="code-preview">
                <pre><code>{{ pipelineCodePreview }}</code></pre>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </template>
    </el-card>

    <!-- Summary Card -->
    <el-card class="summary-card" shadow="never">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><InfoFilled /></el-icon>
          <span class="header-title">Extensions Summary</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="Tools">
          <el-tag v-if="localForm.enable_tools" type="success">
            {{ localForm.tools.length }} Enabled
          </el-tag>
          <el-tag v-else type="info">Disabled</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Formatter">
          <el-tag v-if="localForm.enable_formatter" type="success">
            {{ localForm.formatter || 'Default' }}
          </el-tag>
          <el-tag v-else type="info">Disabled</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Hooks">
          <el-tag v-if="localForm.enable_hooks" type="success">
            {{ localForm.hooks.length }} Hooks
          </el-tag>
          <el-tag v-else type="info">Disabled</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Skills">
          <el-tag v-if="localForm.enable_skills" type="success">
            {{ localForm.skills.length }} Skills
          </el-tag>
          <el-tag v-else type="info">Disabled</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="RAG">
          <el-tag v-if="localForm.enable_rag" type="warning">
            {{ ragConfig.store_type || 'Not Configured' }}
          </el-tag>
          <el-tag v-else type="info">Disabled</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Pipeline">
          <el-tag v-if="localForm.enable_pipeline" type="warning">
            {{ pipelineConfig.type || 'Not Configured' }}
          </el-tag>
          <el-tag v-else type="info">Disabled</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { ExtensionsResponse } from '@/types'
import SkillSelector from './SkillSelector.vue'
import {
  Tools,
  Document,
  Link,
  Star,
  Reading,
  Operation,
  Setting,
  InfoFilled,
  Connection,
  Medal,
  View
} from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

// Local form state
const localForm = reactive({
  enable_tools: form.value.enable_tools ?? true,
  tools: form.value.tools || [],
  enable_formatter: form.value.enable_formatter ?? false,
  formatter: form.value.formatter || null,
  enable_hooks: form.value.enable_hooks ?? false,
  hooks: form.value.hooks || [],
  enable_skills: form.value.enable_skills ?? false,
  skills: form.value.skills || [],
  enable_rag: form.value.enable_rag ?? false,
  enable_pipeline: form.value.enable_pipeline ?? false,
})

const ragConfig = reactive({
  store_type: form.value.rag_config?.store_type || 'qdrant',
  embedding_model: form.value.rag_config?.embedding_model || 'openai:text-embedding-ada-002',
  chunk_size: form.value.rag_config?.chunk_size || 500,
  chunk_overlap: form.value.rag_config?.chunk_overlap || 50,
  // Qdrant configuration
  qdrant_host: form.value.rag_config?.qdrant_host || 'localhost',
  qdrant_port: form.value.rag_config?.qdrant_port || 6333,
  collection_name: form.value.rag_config?.collection_name || 'agent_documents',
  // KBase configuration
  kbase_retrieval_url: form.value.rag_config?.kbase_retrieval_url || '',
})

const pipelineConfig = reactive({
  type: form.value.pipeline_config?.type || 'sequential',
  num_stages: form.value.pipeline_config?.num_stages || 3,
  error_handling: form.value.pipeline_config?.error_handling || 'stop',
})

// Extensions data from API
const extensions = ref<ExtensionsResponse>({
  memory: {
    short_term: [],
    long_term: [],
  },
  tools: {},
  formatters: [],
  evaluators: [],
  openjudge_graders: [],
})

// Available hooks (static list)
const availableHooks = [
  {
    value: 'pre_reply',
    label: 'Pre Reply',
    description: 'Execute custom code before agent generates response',
    timing: 'Before Reply'
  },
  {
    value: 'post_reply',
    label: 'Post Reply',
    description: 'Process or log agent response after generation',
    timing: 'After Reply'
  },
  {
    value: 'pre_observe',
    label: 'Pre Observe',
    description: 'Intercept data before agent observation',
    timing: 'Before Observe'
  },
  {
    value: 'post_observe',
    label: 'Post Observe',
    description: 'Process observation results after agent observes',
    timing: 'After Observe'
  },
]

// Available skills (preset list)
const availableSkills = [
  'coding',
  'writing',
  'analysis',
  'research',
  'math',
  'translation',
]

// Fetch extensions from API
const fetchExtensions = async () => {
  try {
    const response = await api.getExtensions()
    extensions.value = response
  } catch (error) {
    console.error('Failed to fetch extensions:', error)
  }
}

// Update field in store
const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

// Update RAG config
const updateRagConfig = () => {
  configStore.setField('rag_config', { ...ragConfig })
}

// Update Pipeline config
const updatePipelineConfig = () => {
  configStore.setField('pipeline_config', { ...pipelineConfig })
}

// Format tool name for display
const formatToolName = (name: string) => {
  return name.split('_').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

// Get formatter description
const getFormatterDescription = (formatter: string) => {
  const descriptions: Record<string, string> = {
    'DashScopeChatFormatter': 'DashScope chat message formatting',
    'OpenAIChatFormatter': 'OpenAI chat message formatting',
  }
  return descriptions[formatter] || ''
}

// Code Preview Computations
const toolsCodePreview = computed(() => {
  if (!localForm.enable_tools || localForm.tools.length === 0) {
    return `# Tools Extension - Disabled

# No tools will be configured for this agent.`
  }

  let code = `# Tools Configuration

from agentscope.tools import Toolkit

def get_toolkit():
    """Get configured toolkit instance."""
    toolkit = Toolkit()

`
  for (const tool of localForm.tools) {
    const toolName = formatToolName(tool)
    code += `    # Register: ${toolName}\n`
    code += `    # toolkit.register(${tool})\n\n`
  }

  code += `    return toolkit`

  return code
})

const formatterCodePreview = computed(() => {
  if (!localForm.enable_formatter || !localForm.formatter) {
    return `# Formatter Extension - Disabled

# Using default formatter (ChatFormatter)`
  }

  return `# Formatter Configuration

from agentscope.formatters import ${localForm.formatter}

def get_formatter():
    """Get configured formatter instance."""
    return ${localForm.formatter}()
`
})

const hooksCodePreview = computed(() => {
  if (!localForm.enable_hooks || localForm.hooks.length === 0) {
    return `# Hooks Extension - Disabled

# No lifecycle hooks configured`
  }

  let code = `# Agent Hooks Configuration

# These hooks are called at specific points in the agent lifecycle

`

  for (const hook of localForm.hooks) {
    const hookInfo = availableHooks.find(h => h.value === hook)
    if (hookInfo) {
      code += `@agent.hook("${hook}")
async def ${hook}_hook(data):
    """${hookInfo.description}"""
    import logging
    logging.info(f"${hookInfo.timing} hook called")
    # Process data here if needed
    return data

`
    }
  }

  return code
})

const skillsCodePreview = computed(() => {
  if (!localForm.enable_skills || localForm.skills.length === 0) {
    return `# Skills Extension - Disabled

# No specialized skills configured`
  }

  let code = `# Skills Configuration

ENABLE_SKILLS = True
SKILLS = ${JSON.stringify(localForm.skills, null, 4)}

def get_skills():
    """Get configured skills list."""
    skills = []

`
  for (const skill of localForm.skills) {
    code += `    # skills.append(${skill})\n`
    code += `    # TODO: Implement ${skill} skill\n\n`
  }

  code += `    return skills`

  return code
})

const ragCodePreview = computed(() => {
  if (!localForm.enable_rag) {
    return `# RAG Extension - Disabled

# No RAG configuration`
  }

  return `# RAG Configuration

RAG_STORE_TYPE = "${ragConfig.store_type}"
RAG_EMBEDDING_MODEL = "${ragConfig.embedding_model}"
RAG_CHUNK_SIZE = ${ragConfig.chunk_size}
RAG_CHUNK_OVERLAP = ${ragConfig.chunk_overlap}

def get_rag_retriever():
    """Get configured RAG retriever instance."""
    from agentscope.rag import RAGRetriever

    return RAGRetriever(
        store_type="${ragConfig.store_type}",
        embedding_model="${ragConfig.embedding_model}",
        chunk_size=${ragConfig.chunk_size},
        chunk_overlap=${ragConfig.chunk_overlap},
    )
`
})

const pipelineCodePreview = computed(() => {
  if (!localForm.enable_pipeline) {
    return `# Pipeline Extension - Disabled

# No pipeline configuration`
  }

  return `# Pipeline Configuration

PIPELINE_TYPE = "${pipelineConfig.type}"
PIPELINE_NUM_STAGES = ${pipelineConfig.num_stages}
PIPELINE_ERROR_HANDLING = "${pipelineConfig.error_handling}"

def get_pipeline():
    """Get configured pipeline instance."""
    from agentscope.pipeline import Pipeline

    pipeline = Pipeline(
        type="${pipelineConfig.type}",
        num_stages=${pipelineConfig.num_stages},
        error_handling="${pipelineConfig.error_handling}",
    )

    return pipeline
`
})

// Initialize
onMounted(() => {
  fetchExtensions()
})
</script>

<style scoped>
.extensions-settings {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 20px 0;
}

/* Extension Card Styles */
.extension-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.extension-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
}

.extension-card.tools-card {
  border-left: 4px solid #409EFF;
}

.extension-card.formatter-card {
  border-left: 4px solid #67C23A;
}

.extension-card.hooks-card {
  border-left: 4px solid #E6A23C;
}

.extension-card.skills-card {
  border-left: 4px solid #F56C6C;
}

.extension-card.rag-card,
.extension-card.pipeline-card {
  border-left: 4px solid #909399;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 24px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.card-description {
  margin-top: 8px;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

/* Tools Grid */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.tool-item {
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s ease;
  background: #ffffff;
}

.tool-item:hover {
  border-color: #409EFF;
  background: #ecf5ff;
}

.tool-item.is-checked {
  border-color: #409EFF;
  background: #ecf5ff;
}

.tool-checkbox {
  width: 100%;
}

.tool-checkbox :deep(.el-checkbox__label) {
  width: 100%;
  padding-left: 8px;
}

.tool-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tool-icon {
  color: #409EFF;
  font-size: 18px;
}

.tool-name {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}

.tool-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

/* Hooks Grid */
.hooks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.hook-item {
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s ease;
  background: #ffffff;
}

.hook-item:hover {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.hook-item.is-checked {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.hook-checkbox {
  width: 100%;
}

.hook-checkbox :deep(.el-checkbox__label) {
  width: 100%;
  padding-left: 8px;
}

.hook-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hook-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hook-icon {
  color: #E6A23C;
  font-size: 18px;
}

.hook-name {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}

.hook-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

/* Option Items */
.option-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.option-label {
  font-weight: 600;
  color: #303133;
}

.option-desc {
  font-size: 12px;
  color: #909399;
}

/* Skill Option */
.skill-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Code Preview */
.preview-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}

.code-preview-container {
  margin-top: 16px;
}

.code-preview {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
}

.code-preview pre {
  margin: 0;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  line-height: 1.6;
}

.code-preview code {
  color: inherit;
}

/* Summary Card */
.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.summary-card :deep(.el-card__header) {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.summary-card .header-title {
  color: white;
}

.summary-card .header-icon {
  color: white;
}

.summary-card :deep(.el-card__body) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
}

/* Divider */
:deep(.el-divider__text) {
  font-size: 1em;
  font-weight: 600;
  color: #606266;
}

:deep(.el-divider__text .el-icon) {
  margin-right: 4px;
}

/* Form Items */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}

/* Collapse */
:deep(.el-collapse-item__header) {
  background: #f5f7fa;
  border-radius: 6px;
  padding: 12px 16px;
}

:deep(.el-collapse-item__content) {
  padding-top: 16px;
}
</style>
