<template>
  <div class="model-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="28" color="#FFFFFF" class="header-icon"><Connection /></el-icon>
        <div class="header-content">
          <h2 class="header-title">模型配置</h2>
          <p class="header-description">选择模型并配置参数</p>
        </div>
        <el-tag type="primary" size="large" effect="dark">核心配置</el-tag>
      </div>
    </div>

    <!-- 配置表单 -->
    <div class="config-form">
      <el-form :model="form" label-width="120px" size="large" class="aligned-form">
        <!-- 模型选择 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#409EFF"><Connection /></el-icon>
            <span>模型选择</span>
          </div>

          <el-form-item label="模型名称" required>
            <el-select
              v-model="selectedModelId"
              placeholder="选择模型"
              filterable
              @change="onModelChange"
              style="width: 320px"
            >
              <el-option
                v-for="model in llmModels"
                :key="model.id"
                :value="model.id"
                :label="getDisplayName(model.name)"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="API密钥" required>
            <el-input
              :model-value="form.model_settings?.api_key"
              type="password"
              placeholder="输入API密钥"
              show-password
              style="width: 320px"
              @input="updateModelConfig('api_key', $event)"
            />
          </el-form-item>

          <el-form-item label="API地址">
            <el-input
              :model-value="form.model_settings?.base_url"
              placeholder="选择模型后自动填充（可手动修改）"
              style="width: 320px"
              @input="updateModelConfig('base_url', $event)"
            />
            <div class="inline-hint">选择模型后自动填充，可根据需要手动修改</div>
          </el-form-item>
        </div>

        <!-- 参数配置 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#67C23A"><Operation /></el-icon>
            <span>参数配置</span>
            <el-tag size="small" type="success" style="margin-left: auto">可选</el-tag>
          </div>

          <el-form-item label="温度">
            <div class="control-row">
              <el-input-number
                :model-value="form.model_settings?.temperature ?? 0.7"
                :min="0"
                :max="1"
                :step="0.1"
                :precision="2"
                controls-position="right"
                style="width: 140px"
                @change="updateModelConfig('temperature', $event)"
              />
              <div class="preset-values">
                <el-tag
                  v-for="preset in temperaturePresets"
                  :key="preset.value"
                  :type="(form.model_settings?.temperature ?? 0.7) === preset.value ? 'primary' : 'info'"
                  size="small"
                  class="preset-tag"
                  @click="setTemperature(preset.value)"
                >
                  {{ preset.label }}
                </el-tag>
              </div>
            </div>
            <div class="inline-hint">范围: 0.0-1.0，默认: 0.7</div>
          </el-form-item>

          <el-form-item label="最大令牌">
            <el-input-number
              :model-value="form.model_settings?.max_tokens ?? 2000"
              :min="1"
              :max="128000"
              :step="1000"
              controls-position="right"
              style="width: 140px"
              @change="updateModelConfig('max_tokens', $event)"
            />
            <div class="inline-hint">模型响应的最大令牌数</div>
          </el-form-item>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { ModelInfo } from '@/types'
import { Connection, Operation } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = configStore.form

const allModels = ref<ModelInfo[]>([])
const selectedModelId = ref<string>('')

// 去掉芯片架构相关后缀，只保留模型名称
const stripChipSuffix = (name: string): string => {
  return name.replace(/-(PPU|NPU|CPU|GPU)$/i, '')
}

// 显示用的模型名称（去掉架构后缀）
const getDisplayName = (name: string): string => {
  return stripChipSuffix(name)
}

const llmModels = computed<ModelInfo[]>(() => {
  return allModels.value.filter(m => !m.is_embedding)
})

const temperaturePresets = [
  { label: '0.3 专注', value: 0.3 },
  { label: '0.7 平衡', value: 0.7 },
  { label: '0.9 创意', value: 0.9 },
]

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const updateModelConfig = (key: string, value: any) => {
  configStore.setField('model_settings', {
    ...form.model_settings,
    [key]: value
  })
}

const setTemperature = (value: number) => {
  updateModelConfig('temperature', value)
}

// 选择模型时自动填充 API 地址
const onModelChange = (modelId: string) => {
  const model = llmModels.value.find(m => m.id === modelId)
  if (model) {
    const baseUrl = model.url.replace(/\/v1\/.*$/, '')
    // 使用去掉架构后缀的模型名称
    updateModelConfig('model', stripChipSuffix(model.name))
    updateModelConfig('base_url', baseUrl)
  }
}

onMounted(async () => {
  if (!form.model_settings) {
    updateModelConfig('model', undefined)
    updateModelConfig('api_key', undefined)
  }

  if (form.model_settings?.temperature === undefined) {
    updateModelConfig('temperature', 0.7)
  }

  if (form.model_settings?.max_tokens === undefined) {
    updateModelConfig('max_tokens', 2000)
  }

  try {
    const response = await api.getModels()
    // 收集所有 LLM 模型（从所有 provider）
    const llmList: ModelInfo[] = []
    for (const provider of response.providers) {
      llmList.push(...provider.models.filter((m: ModelInfo) => !m.is_embedding))
    }
    allModels.value = llmList

    // 如果已有模型名，尝试恢复选中状态
    if (form.model_settings?.model) {
      const matched = llmModels.value.find(m => stripChipSuffix(m.name) === form.model_settings?.model)
      if (matched) {
        selectedModelId.value = matched.id
      }
    }
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
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.header-background {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #FFFFFF;
}

.header-icon {
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.header-title {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
  color: #FFFFFF;
  line-height: 1.3;
}

.header-description {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.4;
}

/* 配置表单 */
.config-form {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 24px;
}

.aligned-form {
  margin: 0;
}

/* 表单区块 */
.form-section {
  margin-bottom: 32px;
}

.form-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 12px;
  margin-bottom: 20px;
  border-bottom: 2px solid #f0f2f5;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

/* 控件行 */
.control-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.preset-values {
  display: flex;
  gap: 8px;
}

.preset-tag {
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.preset-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 内联提示 */
.inline-hint {
  font-size: 12px;
  color: #909399;
  display: block;
  margin-top: 6px;
  line-height: 1.4;
}

/* 表单项样式统一 */
:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
  font-size: 14px;
}

:deep(.el-input-number) {
  line-height: normal;
}

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 6px;
}

/* 响应式 */
@media (max-width: 768px) {
  .unified-header-card {
    margin-bottom: 16px;
  }

  .header-background {
    flex-direction: column;
    text-align: center;
    padding: 16px;
  }

  .header-title {
    font-size: 16px;
  }

  .header-description {
    font-size: 12px;
  }

  .config-form {
    padding: 16px;
  }

  .control-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .preset-values {
    width: 100%;
    justify-content: space-between;
  }

  .preset-tag {
    flex: 1;
    text-align: center;
  }
}
</style>
