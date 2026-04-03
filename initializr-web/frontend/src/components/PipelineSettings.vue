<template>
  <el-card class="pipeline-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#909399"><Operation /></el-icon>
          <span class="card-title">管道配置</span>
          <el-tag size="small" type="info">工作流</el-tag>
        </div>
        <el-switch
          v-model="localForm.enable_pipeline"
          size="large"
          @change="updateField('enable_pipeline', $event)"
        />
      </div>
    </template>

    <template v-if="localForm.enable_pipeline">
      <el-form :model="form" label-width="140px" size="large">
        <el-form-item label="管道类型">
          <el-select
            v-model="pipelineConfig.type"
            placeholder="选择管道类型"
            style="width: 100%"
            @change="updatePipelineConfig"
          >
            <el-option label="顺序执行" value="sequential" />
            <el-option label="并行执行" value="parallel" />
            <el-option label="条件分支" value="conditional" />
          </el-select>
          <span class="hint">选择智能体的执行方式</span>
        </el-form-item>

        <el-form-item label="阶段数量">
          <el-input-number
            v-model="pipelineConfig.num_stages"
            :min="2"
            :max="10"
            style="width: 100%"
            @change="updatePipelineConfig"
          />
          <span class="hint">管道中的智能体阶段数量</span>
        </el-form-item>

        <el-alert
          type="success"
          :closable="false"
          show-icon
          style="margin-top: 16px"
        >
          当前配置：{{ pipelineConfig.type }} 模式，{{ pipelineConfig.num_stages }} 个阶段
        </el-alert>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { Operation } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  enable_pipeline: form.value.enable_pipeline ?? false,
})

const pipelineConfig = reactive({
  type: form.value.pipeline_config?.type || 'sequential',
  num_stages: form.value.pipeline_config?.num_stages || 3,
  error_handling: form.value.pipeline_config?.error_handling || 'stop',
})

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const updatePipelineConfig = () => {
  configStore.setField('pipeline_config', { ...pipelineConfig })
}
</script>

<style scoped>
.pipeline-settings {
  padding: 0;
}

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

.pipeline-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 24px;
}

.pipeline-card {
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

@media (max-width: 768px) {
  .pipeline-sections {
    gap: 16px;
  }

  .pipeline-card {
    margin: 0;
  }

  .header-background {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .header-title {
    font-size: 18px;
  }

  .header-description {
    font-size: 13px;
  }
}
</style>
