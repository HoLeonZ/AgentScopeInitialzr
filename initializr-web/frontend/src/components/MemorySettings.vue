<template>
  <div class="memory-settings">
    <!-- 记忆系统概述 -->
    <el-alert
      title="📚 记忆配置"
      type="info"
      :closable="false"
      show-icon
      class="memory-overview"
    >
      <template #default>
        <p class="overview-text">
          配置智能体如何存储和检索信息。AgentScope 支持两种类型的记忆：
        </p>
        <ul class="overview-list">
          <li><strong>短期记忆：</strong>在当前会话期间存储对话历史（例如：Redis、OceanBase）</li>
          <li><strong>长期记忆：</strong>跨多个会话持久化知识（例如：Mem0、OceanBase）</li>
        </ul>
      </template>
    </el-alert>

    <!-- 详细配置区块 -->
    <div class="memory-sections">
      <!-- 短期记忆区块 -->
      <el-card class="memory-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="20" color="#409EFF"><Memo /></el-icon>
            <span class="card-title">短期记忆</span>
            <el-tag size="small" type="primary">基于会话</el-tag>
          </div>
        </template>

        <el-form :model="form" label-width="140px" size="large">
          <el-form-item label="启用">
            <el-switch
              v-model="form.enable_memory"
              @change="updateField('enable_memory', $event)"
            />
            <span class="hint">在会话期间将对话历史存储在内存中</span>
          </el-form-item>

          <template v-if="form.enable_memory">
            <el-form-item label="记忆类型">
              <el-select
                v-model="form.short_term_memory"
                placeholder="选择记忆类型"
                @change="updateField('short_term_memory', $event)"
                style="width: 100%"
              >
                <el-option
                  v-for="type in extensions.memory.short_term"
                  :key="type"
                  :value="type"
                  :label="formatMemoryName(type)"
                />
              </el-select>
              <span class="hint">选择对话历史的存储后端</span>
            </el-form-item>

            <!-- Redis 配置 -->
            <template v-if="form.short_term_memory === 'redis'">
              <el-divider content-position="left">Redis 配置</el-divider>

              <el-form-item label="连接模式">
                <el-radio-group v-model="redisConnectionMode">
                  <el-radio label="manual">手动配置</el-radio>
                  <el-radio label="url">URL 连接</el-radio>
                </el-radio-group>
                <span class="hint">选择如何连接到 Redis 服务器</span>
              </el-form-item>

              <template v-if="redisConnectionMode === 'manual'">
                <el-form-item label="主机">
                  <el-input
                    v-model="redisHost"
                    placeholder="localhost"
                  />
                </el-form-item>

                <el-form-item label="端口">
                  <el-input-number
                    v-model="redisPort"
                    :min="1"
                    :max="65535"
                    placeholder="6379"
                    style="width: 100%"
                  />
                </el-form-item>

                <el-form-item label="数据库">
                  <el-input-number
                    v-model="redisDb"
                    :min="0"
                    :max="15"
                    placeholder="0"
                    style="width: 100%"
                  />
                </el-form-item>

                <el-form-item label="密码">
                  <el-input
                    v-model="redisPassword"
                    type="password"
                    placeholder="如果不需要认证则留空"
                    show-password
                  />
                  <span class="hint">可选，仅当您的 Redis 需要认证时</span>
                </el-form-item>
              </template>

              <el-form-item v-if="redisConnectionMode === 'url'" label="连接 URL">
                <el-input
                  v-model="redisUrl"
                  placeholder="redis://localhost:6379/0 或 rediss://user:pass@host:port/db"
                />
                <span class="hint">用于云服务如 Redis Cloud</span>
              </el-form-item>
            </template>

            <!-- OceanBase 配置 -->
            <template v-if="form.short_term_memory === 'oceanbase'">
              <el-divider content-position="left">OceanBase 配置</el-divider>

              <el-form-item label="连接字符串">
                <el-input
                  v-model="oceanbaseShortTermConnectionString"
                  placeholder="postgresql://user:password@localhost:2881/tenant"
                />
                <span class="hint">OceanBase 的 PostgreSQL 兼容连接字符串</span>
              </el-form-item>

              <el-form-item label="表名">
                <el-input
                  v-model="oceanbaseShortTermTableName"
                  placeholder="agent_conversation"
                />
                <span class="hint">用于存储对话历史的表名</span>
              </el-form-item>
            </template>
          </template>
        </el-form>
      </el-card>

      <!-- 长期记忆区块 -->
      <el-card class="memory-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="20" color="#67C23A"><FolderOpened /></el-icon>
            <span class="card-title">长期记忆</span>
            <el-tag size="small" type="success">持久化</el-tag>
          </div>
        </template>

        <el-form :model="form" label-width="140px" size="large">
          <el-form-item label="启用">
            <el-switch
              v-model="enableLongTerm"
              @change="handleLongTermToggle"
            />
            <span class="hint">跨多个会话持久化记忆</span>
          </el-form-item>

          <template v-if="enableLongTerm">
            <el-form-item label="记忆类型">
              <el-select
                v-model="form.long_term_memory"
                placeholder="选择长期记忆类型"
                @change="updateField('long_term_memory', $event)"
                style="width: 100%"
              >
                <el-option
                  v-for="type in extensions.memory.long_term"
                  :key="type"
                  :value="type"
                  :label="formatMemoryName(type)"
                />
              </el-select>
              <span class="hint">选择长期知识的持久化存储</span>
            </el-form-item>

            <!-- Mem0 配置 -->
            <template v-if="form.long_term_memory === 'mem0'">
              <el-divider content-position="left">Mem0 配置</el-divider>

              <el-form-item label="API 密钥">
                <el-input
                  v-model="mem0ApiKey"
                  type="password"
                  placeholder="您的 Mem0 API 密钥"
                  show-password
                />
                <span class="hint">Mem0 记忆服务所需</span>
              </el-form-item>

              <el-form-item label="API 地址">
                <el-input
                  v-model="mem0ApiUrl"
                  placeholder="https://api.mem0.ai"
                />
                <span class="hint">可选，如果未提供则使用默认端点</span>
              </el-form-item>
            </template>

            <!-- OceanBase 长期配置 -->
            <template v-if="form.long_term_memory === 'oceanbase'">
              <el-divider content-position="left">OceanBase 配置</el-divider>

              <el-form-item label="连接字符串">
                <el-input
                  v-model="oceanbaseConnectionString"
                  placeholder="postgresql://user:password@localhost:2881/tenant"
                />
                <span class="hint">OceanBase 的 PostgreSQL 兼容连接字符串</span>
              </el-form-item>

              <el-form-item label="表名">
                <el-input
                  v-model="oceanbaseTableName"
                  placeholder="agent_memory"
                />
                <span class="hint">用于存储智能体记忆的表名</span>
              </el-form-item>
            </template>
          </template>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import { Memo, FolderOpened } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = configStore.form

const extensions = ref<any>({
  memory: {
    short_term: [],
    long_term: []
  }
})
const enableLongTerm = ref(false)
const mem0ApiKey = ref('')
const mem0ApiUrl = ref('')

// OceanBase 配置
const oceanbaseConnectionString = ref('')
const oceanbaseTableName = ref('agent_memory')
const oceanbaseShortTermConnectionString = ref('')
const oceanbaseShortTermTableName = ref('agent_conversation')

// Redis 配置
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

onMounted(async () => {
  try {
    const response = await api.getExtensions()
    extensions.value = response
  } catch (error) {
    console.error('加载扩展失败:', error)
  }
})
</script>

<style scoped>
.memory-settings {
  padding: 0;
}

/* 概述样式 */
.memory-overview {
  margin-bottom: 24px;
}

.overview-text {
  margin: 0 0 12px 0;
  line-height: 1.6;
  color: #606266;
}

.overview-list {
  margin: 0;
  padding-left: 20px;
  color: #606266;
}

.overview-list li {
  margin: 8px 0;
  line-height: 1.6;
}

/* 详细配置样式 */
.memory-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 24px;
}

.memory-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  flex: 1;
}

.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
  line-height: 1.4;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-divider__text) {
  font-size: 0.95em;
  font-weight: 600;
  color: #409EFF;
}

:deep(.el-divider--horizontal) {
  margin: 24px 0 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .memory-sections {
    gap: 16px;
  }

  .memory-card {
    margin: 0;
  }

  .card-header {
    flex-wrap: wrap;
  }
}
</style>
