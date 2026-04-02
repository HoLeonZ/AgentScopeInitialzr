<template>
  <div class="extensions-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="28" color="#FFFFFF" class="header-icon"><Tools /></el-icon>
        <div class="header-content">
          <h2 class="header-title">扩展功能配置</h2>
          <p class="header-description">配置格式化器、钩子和管道等高级扩展</p>
        </div>
        <el-tag type="primary" size="large" effect="dark">高级配置</el-tag>
      </div>
    </div>

    <!-- 配置表单 -->
    <div class="config-form">
      <el-form :model="form" label-width="120px" size="large" class="aligned-form">
        <!-- Formatter Extension -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#67C23A"><Document /></el-icon>
            <span>格式化器</span>
            <el-switch
              v-model="localForm.enable_formatter"
              size="small"
              style="margin-left: auto"
              @change="updateField('enable_formatter', $event)"
            />
          </div>

          <template v-if="localForm.enable_formatter">
            <el-form-item label="格式化器">
              <el-select
                v-model="localForm.formatter"
                placeholder="选择格式化器"
                style="width: 320px"
                @change="updateField('formatter', $event)"
              >
                <el-option
                  v-for="formatter in extensions.formatters"
                  :key="formatter"
                  :label="formatter"
                  :value="formatter"
                />
              </el-select>
              <div class="inline-hint">不同模型提供商的消息格式化</div>
            </el-form-item>
          </template>
        </div>

        <!-- Hooks Extension -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#E6A23C"><Link /></el-icon>
            <span>生命周期钩子</span>
            <el-switch
              v-model="localForm.enable_hooks"
              size="small"
              style="margin-left: auto"
              @change="updateField('enable_hooks', $event)"
            />
          </div>

          <template v-if="localForm.enable_hooks">
            <el-form-item label="可用钩子">
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
                        <div class="hook-name">{{ hook.label }}</div>
                        <div class="hook-desc">{{ hook.description }}</div>
                      </div>
                    </el-checkbox>
                  </div>
                </div>
              </el-checkbox-group>
            </el-form-item>
          </template>
        </div>

        <!-- Pipeline Extension (Only for Multi-Agent) -->
        <div v-if="form.agent_type === 'multi-agent'" class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#909399"><Operation /></el-icon>
            <span>多智能体管道</span>
            <el-tag size="small" type="warning" style="margin-left: auto">仅多智能体</el-tag>
          </div>

          <el-form-item label="启用管道">
            <el-switch
              v-model="localForm.enable_pipeline"
              @change="updateField('enable_pipeline', $event)"
            />
            <div class="inline-hint">启用多智能体协作工作流</div>
          </el-form-item>

          <template v-if="localForm.enable_pipeline">
            <div class="control-row">
              <el-form-item label="管道类型" style="flex: 1">
                <el-select
                  v-model="pipelineConfig.type"
                  placeholder="选择类型"
                  @change="updatePipelineConfig"
                >
                  <el-option label="顺序执行" value="sequential" />
                  <el-option label="并行执行" value="parallel" />
                  <el-option label="条件分支" value="conditional" />
                </el-select>
              </el-form-item>

              <el-form-item label="阶段数" style="flex: 1">
                <el-input-number
                  v-model="pipelineConfig.num_stages"
                  :min="2"
                  :max="10"
                  controls-position="right"
                  style="width: 140px"
                  @change="updatePipelineConfig"
                />
              </el-form-item>
            </div>
          </template>
        </div>
      </el-form>
    </div>
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
  Operation
} from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
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

const availableHooks = [
  {
    value: 'pre_reply',
    label: '回复前',
    description: '在智能体生成响应前执行'
  },
  {
    value: 'post_reply',
    label: '回复后',
    description: '在智能体生成响应后执行'
  },
  {
    value: 'pre_observe',
    label: '观察前',
    description: '在智能体观察数据前拦截'
  },
  {
    value: 'post_observe',
    label: '观察后',
    description: '在智能体观察数据后处理'
  },
]

const fetchExtensions = async () => {
  try {
    const response = await api.getExtensions()
    extensions.value = response
  } catch (error) {
    console.error('Failed to fetch extensions:', error)
  }
}

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const updatePipelineConfig = () => {
  configStore.setField('pipeline_config', { ...pipelineConfig })
}

onMounted(() => {
  fetchExtensions()
})
</script>

<style scoped>
.extensions-settings {
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
  background: linear-gradient(135deg, #909399 0%, #b3b8bd 100%);
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

/* Hooks Grid */
.hooks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.hook-item {
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.2s;
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
  gap: 4px;
}

.hook-name {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
}

.hook-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

/* 控件行 */
.control-row {
  display: flex;
  gap: 16px;
}

/* 内联提示 */
.inline-hint {
  font-size: 12px;
  color: #909399;
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

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 6px;
}

/* 响应式 */
@media (max-width: 768px) {
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

  .hooks-grid {
    grid-template-columns: 1fr;
  }

  .control-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>
