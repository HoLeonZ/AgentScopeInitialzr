<template>
  <div class="model-settings">
    <el-form :model="form" label-width="150px" size="large">
      <el-form-item label="Model Provider" required>
        <el-select
          v-model="form.model_provider"
          placeholder="Select provider"
          @change="updateField('model_provider', $event)"
        >
          <el-option
            v-for="provider in providers"
            :key="provider.id"
            :value="provider.id"
            :label="provider.name"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="Model Name">
        <el-input
          :model-value="form.model_config?.model"
          placeholder="e.g., gpt-4, claude-3-sonnet"
          @input="updateModelConfig('model', $event)"
        />
        <span class="hint">Specific model to use (e.g., gpt-4, claude-3-sonnet)</span>
      </el-form-item>

      <el-form-item label="API Key">
        <el-input
          :model-value="form.model_config?.api_key"
          type="password"
          placeholder="Your API key"
          show-password
          @input="updateModelConfig('api_key', $event)"
        />
        <span class="hint">API key for authentication (stored in .env file)</span>
      </el-form-item>

      <el-form-item label="Temperature">
        <el-slider
          :model-value="form.model_config?.temperature ?? 0.7"
          :min="0"
          :max="2"
          :step="0.1"
          :marks="{ 0: 'Precise', 1: 'Balanced', 2: 'Creative' }"
          @change="updateModelConfig('temperature', $event)"
        />
        <span class="hint">Controls randomness: 0 = focused, 2 = creative</span>
      </el-form-item>

      <el-form-item label="Max Tokens">
        <el-input-number
          :model-value="form.model_config?.max_tokens ?? 2000"
          :min="1"
          :max="128000"
          :step="1000"
          @change="updateModelConfig('max_tokens', $event)"
        />
        <span class="hint">Maximum response length</span>
      </el-form-item>
    </el-form>

    <!-- Live Preview -->
    <el-divider content-position="left">
      <el-icon><View /></el-icon>
      Live Preview - Configuration Code
    </el-divider>

    <div class="preview-container">
      <el-tabs v-model="activePreviewTab">
        <el-tab-pane label=".env File" name="env">
          <div class="code-preview">
            <pre><code>{{ envPreview }}</code></pre>
          </div>
        </el-tab-pane>

        <el-tab-pane label="config.json" name="config">
          <div class="code-preview">
            <pre><code>{{ configPreview }}</code></pre>
          </div>
        </el-tab-pane>

        <el-tab-pane label="Project Structure" name="structure">
          <div class="structure-preview">
            <pre><code>{{ structurePreview }}</code></pre>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import { View } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const providers = ref<any[]>([])
const activePreviewTab = ref('env')

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const updateModelConfig = (key: string, value: any) => {
  configStore.setField('model_config', {
    ...form.value.model_config,
    [key]: value
  })
}

// Live preview computations
const envPreview = computed(() => {
  const provider = form.value.model_provider || 'openai'
  const apiKey = form.value.model_config?.api_key || 'your-api-key-here'

  const envVars: Record<string, string> = {
    openai: `# OpenAI Configuration
OPENAI_API_KEY=${apiKey}
OPENAI_API_BASE=https://api.openai.com/v1`,
    dashscope: `# DashScope Configuration
DASHSCOPE_API_KEY=${apiKey}`,
    gemini: `# Gemini Configuration
GEMINI_API_KEY=${apiKey}`,
    anthropic: `# Anthropic Configuration
ANTHROPIC_API_KEY=${apiKey}`,
    ollama: `# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434`
  }

  return envVars[provider] || envVars.openai
})

const configPreview = computed(() => {
  const model = form.value.model_config?.model || 'gpt-4'
  const temperature = form.value.model_config?.temperature ?? 0.7
  const maxTokens = form.value.model_config?.max_tokens ?? 2000

  return JSON.stringify({
    model: {
      config_name: model,
      temperature: temperature,
      max_tokens: maxTokens
    }
  }, null, 2)
})

const structurePreview = computed(() => {
  const packageName = form.value.name.replace(/-/g, '_') || 'my_agent'
  return `${packageName}/
├── src/
│   └── ${packageName}/
│       ├── config/
│       │   ├── config.json          # Model configuration
│       │   └── .env.example         # Environment variables template
│       ├── agents/
│       │   └── agent.py             # Agent with model configuration
│       └── main.py
├── .env                             # API keys (not in git)
└── .env.example                     # Template for env vars`
})

onMounted(async () => {
  try {
    const response = await api.getModels()
    providers.value = response.providers
  } catch (error) {
    console.error('Failed to load model providers:', error)
  }
})
</script>

<style scoped>
.model-settings {
  padding: 20px 0;
}

.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
}

.preview-container {
  margin-top: 30px;
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
}

.code-preview,
.structure-preview {
  background: #1e1e1e;
  border-radius: 4px;
  padding: 15px;
  overflow-x: auto;
}

pre {
  margin: 0;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  line-height: 1.5;
}

code {
  color: inherit;
}

:deep(.el-slider__marks-text) {
  font-size: 0.8em;
}
</style>
