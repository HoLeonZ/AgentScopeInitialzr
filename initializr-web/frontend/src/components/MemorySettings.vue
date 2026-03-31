<template>
  <div class="memory-settings">
    <el-form :model="form" label-width="180px" size="large">
      <!-- Short-term Memory -->
      <el-divider content-position="left">
        <el-icon><Memo /></el-icon>
        Short-term Memory
      </el-divider>

      <el-form-item label="Enable Short-term Memory">
        <el-switch
          v-model="form.enable_memory"
          @change="updateField('enable_memory', $event)"
        />
        <span class="hint">Store conversation history in memory</span>
      </el-form-item>

      <el-form-item v-if="form.enable_memory" label="Memory Type">
        <el-select
          v-model="form.short_term_memory"
          placeholder="Select memory type"
          @change="updateField('short_term_memory', $event)"
        >
          <el-option
            v-for="type in extensions.memory.short_term"
            :key="type"
            :value="type"
            :label="formatMemoryName(type)"
          />
        </el-select>
        <span class="hint">Storage backend for conversation history</span>
      </el-form-item>

      <!-- Long-term Memory -->
      <el-divider content-position="left">
        <el-icon><FolderOpened /></el-icon>
        Long-term Memory
      </el-divider>

      <el-form-item label="Enable Long-term Memory">
        <el-switch
          v-model="enableLongTerm"
          @change="handleLongTermToggle"
        />
        <span class="hint">Persist memories across sessions</span>
      </el-form-item>

      <el-form-item v-if="enableLongTerm" label="Long-term Memory Type">
        <el-select
          v-model="form.long_term_memory"
          placeholder="Select long-term memory"
          @change="updateField('long_term_memory', $event)"
        >
          <el-option
            v-for="type in extensions.memory.long_term"
            :key="type"
            :value="type"
            :label="formatMemoryName(type)"
          />
        </el-select>
        <span class="hint">Persistent storage for long-term knowledge</span>
      </el-form-item>

      <el-form-item v-if="enableLongTerm && form.long_term_memory === 'mem0'" label="Mem0 API Key">
        <el-input
          v-model="mem0ApiKey"
          type="password"
          placeholder="Your Mem0 API key"
          show-password
        />
        <span class="hint">Required for Mem0 memory service</span>
      </el-form-item>
    </el-form>

    <!-- Live Preview -->
    <el-divider content-position="left">
      <el-icon><View /></el-icon>
      Live Preview - Memory Configuration
    </el-divider>

    <div class="preview-container">
      <el-tabs v-model="activePreviewTab">
        <el-tab-pane label="Agent Code" name="agent">
          <div class="code-preview">
            <pre><code>{{ agentCodePreview }}</code></pre>
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
import { View, Memo, FolderOpened } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const extensions = ref<any>({
  memory: {
    short_term: [],
    long_term: []
  }
})
const activePreviewTab = ref('agent')
const enableLongTerm = ref(false)
const mem0ApiKey = ref('')

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const handleLongTermToggle = (value: boolean) => {
  enableLongTerm.value = value
  if (!value) {
    updateField('long_term_memory', null)
  } else {
    updateField('long_term_memory', 'mem0')
  }
}

const formatMemoryName = (type: string) => {
  return type
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// Live preview computations
const agentCodePreview = computed(() => {
  const shortTerm = form.value.enable_memory
    ? (form.value.short_term_memory || 'in-memory')
    : null

  const longTerm = enableLongTerm.value
    ? (form.value.long_term_memory || 'mem0')
    : null

  let code = `# Agent initialization with memory configuration`

  if (shortTerm) {
    const memoryClass = shortTerm === 'in-memory' ? 'Memory()' : 'Memory(name="conversation_mem")'
    code += `

from agentscope.memory import Memory

# Create ${formatMemoryName(shortTerm)} memory
memory = ${memoryClass}`
  }

  if (longTerm && longTerm !== 'none') {
    code += `

# Configure long-term memory with ${formatMemoryName(longTerm)}
agent.memory.add_long_term(
    type="${longTerm}",
    config={
        "api_key": "${mem0ApiKey.value || 'your-api-key'}"
    }
)`
  }

  if (!shortTerm && !longTerm) {
    code += `

# Memory is disabled for this agent`
  }

  return code
})

const configPreview = computed(() => {
  const config: any = {}

  if (form.value.enable_memory && form.value.short_term_memory) {
    config.short_term_memory = {
      type: form.value.short_term_memory
    }
  }

  if (enableLongTerm.value && form.value.long_term_memory) {
    config.long_term_memory = {
      type: form.value.long_term_memory
    }
    if (form.value.long_term_memory === 'mem0') {
      config.long_term_memory.api_key = mem0ApiKey.value || 'your-api-key'
    }
  }

  if (Object.keys(config).length === 0) {
    return `# Memory is disabled`
  }

  return JSON.stringify({ memory: config }, null, 2)
})

const structurePreview = computed(() => {
  const packageName = form.value.name.replace(/-/g, '_') || 'my_agent'
  const hasShortTerm = form.value.enable_memory && form.value.short_term_memory
  const hasLongTerm = enableLongTerm.value && form.value.long_term_memory && form.value.long_term_memory !== 'none'

  let structure = `${packageName}/
├── src/
│   └── ${packageName}/
│       ├── agents/
│       │   └── agent.py`

  if (hasShortTerm) {
    structure += `         # Agent with memory configuration`
  }

  if (hasLongTerm) {
    structure += `
│       ├── memory/
│       │   └── long_term_mem.py    # Long-term memory implementation`
  }

  structure += `
│       └── config/
│           └── config.json
└── .env`

  return structure
})

onMounted(async () => {
  try {
    const response = await api.getExtensions()
    extensions.value = response
  } catch (error) {
    console.error('Failed to load extensions:', error)
  }
})
</script>

<style scoped>
.memory-settings {
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

:deep(.el-divider__text) {
  font-size: 1.1em;
  font-weight: 600;
}
</style>
