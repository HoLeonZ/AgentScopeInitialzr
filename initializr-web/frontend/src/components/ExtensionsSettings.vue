<template>
  <div class="extensions-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="32" color="#FFFFFF" class="header-icon"><Tools /></el-icon>
        <div class="header-content">
          <h2 class="header-title">扩展功能配置</h2>
          <p class="header-description">配置高级扩展功能，包括工具、格式化器、生命周期钩子和管道</p>
        </div>
        <el-tag type="primary" size="large" effect="dark">高级配置</el-tag>
      </div>
    </div>

    <!-- 配置提示 -->
    <el-alert
      type="info"
      :closable="false"
      show-icon
      class="config-hint"
    >
      <template #default>
        <div class="hint-content">
          <div class="hint-title">💡 配置说明</div>
          <ul class="hint-list">
            <li><strong>Tools：</strong>扩展智能体能力，提供强大的功能函数</li>
            <li><strong>Formatter：</strong>为不同模型提供商配置消息格式化</li>
            <li><strong>Hooks：</strong>添加生命周期钩子以在关键点拦截智能体执行</li>
            <li><strong>Pipeline：</strong>多智能体管道，用于复杂的工作流编排</li>
          </ul>
        </div>
      </template>
    </el-alert>

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

    <!-- Pipeline Extension (Only for Multi-Agent) -->
    <el-card v-if="form.agent_type === 'multi-agent'" class="extension-card pipeline-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#909399"><Operation /></el-icon>
            <span class="header-title">Pipeline Extension</span>
            <el-tag size="small" type="warning">Multi-Agent Only</el-tag>
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

        <el-descriptions-item v-if="form.agent_type === 'multi-agent'" label="Pipeline">
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
import {
  Tools,
  Document,
  Link,
  Operation,
  Setting,
  InfoFilled,
  Connection,
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
  enable_pipeline: form.value.enable_pipeline ?? false,
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
  padding: 0;
}

/* 统一头部卡片 */
.unified-header-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-background {
  background: linear-gradient(135deg, #909399 0%, #b3b8bd 100%);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  color: #FFFFFF;
}

.header-icon {
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.header-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #FFFFFF;
  line-height: 1.2;
}

.header-description {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.5;
}

/* 配置提示 */
.config-hint {
  margin-bottom: 24px;
  border-radius: 6px;
}

.hint-content {
  line-height: 1.6;
}

.hint-title {
  font-weight: 600;
  color: #909399;
  margin-bottom: 8px;
}

.hint-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
  color: #606266;
}

.hint-list li {
  margin: 6px 0;
  line-height: 1.5;
}

.hint-list strong {
  color: #303133;
  font-weight: 600;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .header-background {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .header-icon {
    align-self: center;
  }

  .header-title {
    font-size: 18px;
  }

  .header-description {
    font-size: 13px;
  }

  .tools-grid,
  .hooks-grid {
    grid-template-columns: 1fr;
  }
}
</style>
