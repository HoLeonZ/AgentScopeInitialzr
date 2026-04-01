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

      <el-form-item v-if="enableLongTerm && form.long_term_memory === 'mem0'" label="Mem0 API URL">
        <el-input
          v-model="mem0ApiUrl"
          placeholder="https://api.mem0.ai"
        />
        <span class="hint">Mem0 API endpoint URL (optional, uses default if not provided)</span>
      </el-form-item>

      <el-form-item v-if="enableLongTerm && form.long_term_memory === 'oceanbase'" label="OceanBase Connection String">
        <el-input
          v-model="oceanbaseConnectionString"
          placeholder="postgresql://user:password@localhost:2881/tenant"
        />
        <span class="hint">OceanBase database connection string</span>
      </el-form-item>

      <el-form-item v-if="enableLongTerm && form.long_term_memory === 'oceanbase'" label="Table Name">
        <el-input
          v-model="oceanbaseTableName"
          placeholder="agent_memory"
        />
        <span class="hint">Table name for storing agent memories</span>
      </el-form-item>

      <!-- Short-term Memory Configurations -->
      <el-form-item v-if="form.enable_memory && form.short_term_memory === 'redis'" label="Redis Connection Mode">
        <el-radio-group v-model="redisConnectionMode">
          <el-radio label="manual">Manual Configuration</el-radio>
          <el-radio label="url">URL Connection</el-radio>
        </el-radio-group>
        <span class="hint">Choose how to connect to Redis server</span>
      </el-form-item>

      <template v-if="form.enable_memory && form.short_term_memory === 'redis' && redisConnectionMode === 'manual'">
        <el-form-item label="Redis Host">
          <el-input
            v-model="redisHost"
            placeholder="localhost"
          />
          <span class="hint">Redis server hostname</span>
        </el-form-item>

        <el-form-item label="Redis Port">
          <el-input-number
            v-model="redisPort"
            :min="1"
            :max="65535"
            placeholder="6379"
          />
          <span class="hint">Redis server port</span>
        </el-form-item>

        <el-form-item label="Redis DB">
          <el-input-number
            v-model="redisDb"
            :min="0"
            :max="15"
            placeholder="0"
          />
          <span class="hint">Redis database number</span>
        </el-form-item>

        <el-form-item label="Redis Password (Optional)">
          <el-input
            v-model="redisPassword"
            type="password"
            placeholder="Leave empty if no authentication"
            show-password
          />
          <span class="hint">Redis server password</span>
        </el-form-item>
      </template>

      <el-form-item v-if="form.enable_memory && form.short_term_memory === 'redis' && redisConnectionMode === 'url'" label="Redis URL">
        <el-input
          v-model="redisUrl"
          placeholder="redis://localhost:6379/0 or rediss://user:pass@host:port/db"
        />
        <span class="hint">Complete Redis connection URL (for cloud services like Redis Cloud)</span>
      </el-form-item>

      <el-form-item v-if="form.enable_memory && form.short_term_memory === 'oceanbase'" label="OceanBase Connection String">
        <el-input
          v-model="oceanbaseShortTermConnectionString"
          placeholder="postgresql://user:password@localhost:2881/tenant"
        />
        <span class="hint">OceanBase database connection string</span>
      </el-form-item>

      <el-form-item v-if="form.enable_memory && form.short_term_memory === 'oceanbase'" label="Table Name">
        <el-input
          v-model="oceanbaseShortTermTableName"
          placeholder="agent_conversation"
        />
        <span class="hint">Table name for storing conversation history</span>
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
const mem0ApiUrl = ref('')

// OceanBase configurations
const oceanbaseConnectionString = ref('')
const oceanbaseTableName = ref('agent_memory')
const oceanbaseShortTermConnectionString = ref('')
const oceanbaseShortTermTableName = ref('agent_conversation')

// Redis configurations
const redisConnectionMode = ref('manual')
const redisHost = ref('localhost')
const redisPort = ref(6379)
const redisDb = ref(0)
const redisPassword = ref('')
const redisUrl = ref('')

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

  if (shortTerm && shortTerm !== 'in-memory') {
    if (shortTerm === 'redis') {
      if (redisConnectionMode.value === 'url') {
        code += `

# Configure Redis memory with URL
from agentscope.memory import RedisMemory

memory = RedisMemory(
    url="${redisUrl.value || 'redis://localhost:6379/0'}"
)`
      } else {
        code += `

# Configure Redis memory with manual settings
from agentscope.memory import RedisMemory

memory = RedisMemory(
    host="${redisHost.value || 'localhost'}",
    port=${redisPort.value || 6379},
    db=${redisDb.value || 0},
    ${redisPassword.value ? `password="${redisPassword.value}",` : ''}
)`
      }
    } else if (shortTerm === 'oceanbase') {
      code += `

# Configure OceanBase short-term memory
from agentscope.memory import OceanBaseMemory

memory = OceanBaseMemory(
    connection_string="${oceanbaseShortTermConnectionString.value || 'postgresql://user:password@localhost:2881/tenant'}",
    table_name="${oceanbaseShortTermTableName.value || 'agent_conversation'}",
)`
    }
  } else if (shortTerm === 'in-memory') {
    code += `

# Configure in-memory storage
from agentscope.memory import InMemoryMemory

memory = InMemoryMemory()`
  }

  if (longTerm && longTerm !== 'none') {
    code += `

# Configure long-term memory with ${formatMemoryName(longTerm)}
agent.memory.add_long_term(
    type="${longTerm}",
    config={
        "api_key": "${mem0ApiKey.value || 'your-api-key'}"${mem0ApiUrl.value ? `,
        "api_url": "${mem0ApiUrl.value}"` : ''}
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
    if (form.value.short_term_memory === 'redis') {
      if (redisConnectionMode.value === 'url') {
        config.short_term_memory.url = redisUrl.value || 'redis://localhost:6379/0'
      } else {
        config.short_term_memory.host = redisHost.value || 'localhost'
        config.short_term_memory.port = redisPort.value || 6379
        config.short_term_memory.db = redisDb.value || 0
        if (redisPassword.value) {
          config.short_term_memory.password = redisPassword.value
        }
      }
    } else if (form.value.short_term_memory === 'oceanbase') {
      config.short_term_memory.connection_string = oceanbaseShortTermConnectionString.value || 'postgresql://user:password@localhost:2881/tenant'
      config.short_term_memory.table_name = oceanbaseShortTermTableName.value || 'agent_conversation'
    }
  }

  if (enableLongTerm.value && form.value.long_term_memory) {
    config.long_term_memory = {
      type: form.value.long_term_memory
    }
    if (form.value.long_term_memory === 'mem0') {
      config.long_term_memory.api_key = mem0ApiKey.value || 'your-api-key'
      if (mem0ApiUrl.value) {
        config.long_term_memory.api_url = mem0ApiUrl.value
      }
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
