<template>
  <div class="model-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="32" color="#FFFFFF" class="header-icon"><Connection /></el-icon>
        <div class="header-content">
          <h2 class="header-title">模型配置</h2>
          <p class="header-description">配置为智能体提供动力的语言模型，选择提供商、模型并调整参数</p>
        </div>
        <el-tag type="primary" size="large" effect="dark">核心配置</el-tag>
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
            <li>支持 Doubao、DeepSeek、DashScope 等主流模型提供商</li>
            <li>Temperature 控制输出的随机性，建议从默认值 0.7 开始</li>
            <li>API 密钥将安全保存在生成的 .env 文件中</li>
          </ul>
        </div>
      </template>
    </el-alert>

    <!-- 详细配置区块 -->
    <div class="model-sections">
      <!-- 模型选择区块 -->
      <el-card class="model-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="20" color="#409EFF"><Connection /></el-icon>
            <span class="card-title">模型选择</span>
          </div>
        </template>

        <el-form :model="form" label-width="140px" size="large">
          <el-form-item label="提供商" required>
            <el-select
              v-model="form.model_provider"
              placeholder="选择提供商"
              @change="updateField('model_provider', $event)"
              style="width: 100%"
            >
              <el-option
                v-for="provider in providers"
                :key="provider.id"
                :value="provider.id"
                :label="provider.name"
              />
            </el-select>
            <span class="hint">选择模型提供商（Doubao、DeepSeek、DashScope等）</span>
          </el-form-item>

          <el-form-item label="模型名称">
            <el-input
              :model-value="form.model_config?.model"
              placeholder="例如：gpt-4、claude-3-sonnet"
              @input="updateModelConfig('model', $event)"
            />
            <span class="hint">具体的模型标识符</span>
          </el-form-item>

          <el-form-item label="API密钥">
            <el-input
              :model-value="form.model_config?.api_key"
              type="password"
              placeholder="您的API密钥"
              show-password
              @input="updateModelConfig('api_key', $event)"
            />
            <span class="hint">认证密钥（将保存在.env文件中）</span>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 参数配置区块 -->
      <el-card class="model-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="20" color="#67C23A"><Operation /></el-icon>
            <span class="card-title">模型参数</span>
            <el-tag size="small" type="success">可选</el-tag>
          </div>
        </template>

        <el-form :model="form" label-width="140px" size="large">
          <el-form-item label="温度" required>
            <div class="temperature-config">
              <el-input-number
                :model-value="form.model_config?.temperature ?? 0.7"
                :min="0"
                :max="1"
                :step="0.01"
                :precision="2"
                controls-position="right"
                placeholder="0.7"
                style="width: 150px"
                @change="updateModelConfig('temperature', $event)"
              />

              <el-button-group class="preset-buttons">
                <el-button
                  size="small"
                  @click="setTemperature(0.3)"
                  :type="(form.model_config?.temperature ?? 0.7) === 0.3 ? 'primary' : ''"
                >
                  专注
                </el-button>
                <el-button
                  size="small"
                  @click="setTemperature(0.7)"
                  :type="(form.model_config?.temperature ?? 0.7) === 0.7 ? 'primary' : ''"
                >
                  平衡
                </el-button>
                <el-button
                  size="small"
                  @click="setTemperature(0.9)"
                  :type="(form.model_config?.temperature ?? 0.7) === 0.9 ? 'primary' : ''"
                >
                  创意
                </el-button>
              </el-button-group>
            </div>

            <div class="parameter-hint">
              <div class="hint-tags">
                <el-tag type="info" size="small">✓ 取值范围: 0.0 - 1.0</el-tag>
                <el-tag type="success" size="small">📍 默认值: 0.7</el-tag>
              </div>
              <div class="hint-description">
                <div>💡 <strong>使用建议：</strong></div>
                <div>• 0.0 - 0.3: 输出更确定、集中（适合代码生成）</div>
                <div>• 0.4 - 0.6: 平衡确定性和多样性</div>
                <div>• 0.7 - 1.0: 输出更多样、创意（适合创意写作）</div>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="最大令牌数">
            <el-input-number
              :model-value="form.model_config?.max_tokens ?? 2000"
              :min="1"
              :max="128000"
              :step="1000"
              style="width: 100%"
              @change="updateModelConfig('max_tokens', $event)"
            />
            <span class="hint">模型响应中的最大令牌数</span>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import { Connection, Operation } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = configStore.form

const providers = ref<any[]>([])

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const updateModelConfig = (key: string, value: any) => {
  configStore.setField('model_config', {
    ...form.model_config,
    [key]: value
  })
}

// 快速设置温度值
const setTemperature = (value: number) => {
  updateModelConfig('temperature', value)
}

// 初始化和加载
onMounted(async () => {
  // 确保 model_config 对象存在
  if (!form.model_config) {
    updateModelConfig('model', undefined)
    updateModelConfig('api_key', undefined)
  }

  // 确保 temperature 有默认值 0.7
  if (form.model_config?.temperature === undefined) {
    updateModelConfig('temperature', 0.7)
  }

  // 确保 max_tokens 有默认值
  if (form.model_config?.max_tokens === undefined) {
    updateModelConfig('max_tokens', 2000)
  }

  // 加载模型提供商列表
  try {
    const response = await api.getModels()
    providers.value = response.providers
  } catch (error) {
    console.error('加载模型提供商失败:', error)
  }
})
</script>

<style scoped>
.model-settings {
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
  background: linear-gradient(135deg, #409EFF 0%, #53a8ff 100%);
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
  color: #409EFF;
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

/* 分（Detailed Configuration）样式 */
.model-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.model-card {
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

/* Temperature 配置样式 */
.temperature-config {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.preset-buttons {
  display: flex;
  gap: 4px;
}

.parameter-hint {
  margin-top: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.hint-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.hint-description {
  font-size: 0.85em;
  color: #606266;
  line-height: 1.6;
}

.hint-description div {
  margin: 4px 0;
}

.hint-description strong {
  color: #303133;
  font-weight: 600;
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
  .model-sections {
    gap: 16px;
  }

  .model-card {
    margin: 0;
  }

  .card-header {
    flex-wrap: wrap;
  }

  .temperature-config {
    flex-direction: column;
    align-items: flex-start;
  }

  .preset-buttons {
    width: 100%;
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
