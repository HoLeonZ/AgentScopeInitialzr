<template>
  <div class="memory-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="32" color="#FFFFFF" class="header-icon"><Memo /></el-icon>
        <div class="header-content">
          <h2 class="header-title">记忆配置</h2>
          <p class="header-description">配置智能体如何存储和检索信息，支持短期和长期记忆</p>
        </div>
        <el-tag type="success" size="large" effect="dark">可选配置</el-tag>
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
            <li><strong>短期记忆：</strong>在当前会话期间存储对话历史（支持 Redis、OceanBase）</li>
            <li><strong>长期记忆：</strong>跨多个会话持久化知识（支持 Mem0、OceanBase）</li>
            <li>根据使用场景选择合适的记忆存储方案</li>
          </ul>
        </div>
      </template>
    </el-alert>

    <!-- 详细配置区块 -->
    <div class="memory-sections">
      <!-- 短期记忆区块 -->
      <el-card class="memory-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon :size="20" color="#409EFF"><Memo /></el-icon>
              <span class="card-title">短期记忆</span>
              <el-tag size="small" type="primary">基于会话</el-tag>
            </div>
            <el-switch
              v-model="form.enable_memory"
              size="large"
              @change="updateField('enable_memory', $event)"
            />
          </div>
        </template>

        <template v-if="form.enable_memory">
          <el-form :model="form" label-width="140px" size="large">
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
                    controls-position="right"
                    style="width: 200px"
                  />
                </el-form-item>

                <el-form-item label="Key 前缀" required>
                  <el-input
                    v-model="redisKeyPrefix"
                    placeholder="agent:"
                  />
                  <span class="hint">Redis key 的前缀，不可为空</span>
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
          </el-form>
        </template>
      </el-card>

      <!-- 长期记忆区块 -->
      <el-card class="memory-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon :size="20" color="#67C23A"><FolderOpened /></el-icon>
              <span class="card-title">长期记忆</span>
              <el-tag size="small" type="success">持久化</el-tag>
            </div>
            <el-switch
              v-model="enableLongTerm"
              size="large"
              @change="handleLongTermToggle"
            />
          </div>
        </template>

        <template v-if="enableLongTerm">
          <el-form :model="form" label-width="140px" size="large">
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
          </el-form>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
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
const redisHost = ref('203.1.173.220')
const redisPort = ref(6379)
const redisKeyPrefix = ref('agent:')
const redisPassword = ref('Red@2023')
const redisUrl = ref('')

const validateRedisKeyPrefix = () => {
  if (!redisKeyPrefix.value || redisKeyPrefix.value.trim() === '') {
    redisKeyPrefix.value = 'agent:'
  }
}

// 同步 Redis 配置到 store
const syncRedisConfig = () => {
  configStore.setField('redis_config', {
    redis_host: redisHost.value,
    redis_port: redisPort.value,
    redis_db: 0,
    redis_key_prefix: redisKeyPrefix.value,
    redis_password: redisPassword.value,
    redis_url: redisUrl.value,
  })
}

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
  // 确保 Redis key 前缀不为空
  validateRedisKeyPrefix()
  // 加载已保存的 Redis 配置
  if (form.redis_config) {
    redisHost.value = form.redis_config.redis_host || '203.1.173.220'
    redisPort.value = form.redis_config.redis_port || 6379
    redisKeyPrefix.value = form.redis_config.redis_key_prefix || 'agent:'
    redisPassword.value = form.redis_config.redis_password || 'Red@2023'
    redisUrl.value = form.redis_config.redis_url || ''
  }
  // 同步初始配置
  syncRedisConfig()
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

/* 统一头部卡片 */
.unified-header-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-background {
  background: linear-gradient(135deg, #67C23A 0%, #85ce61 100%);
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
  color: #67C23A;
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
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
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
}
</style>
