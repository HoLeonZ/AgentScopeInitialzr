<template>
  <el-card class="evaluation-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon :size="20" color="#67C23A"><DataAnalysis /></el-icon>
        <span class="card-title">评估配置</span>
        <el-tag size="small" type="success">Metrics</el-tag>
      </div>
    </template>

    <el-form :model="form" label-width="140px" size="large">
      <el-form-item label="启用评估">
        <el-switch
          v-model="localForm.generate_evaluation"
          @change="updateField('generate_evaluation', $event)"
        />
        <span class="hint">生成评估模块</span>
      </el-form-item>

      <template v-if="localForm.generate_evaluation">
        <el-form-item label="评估器类型">
          <el-select
            v-model="localForm.evaluator_type"
            placeholder="选择评估器"
            style="width: 100%"
            @change="updateField('evaluator_type', $event)"
          >
            <el-option
              v-for="evaluator in extensions.evaluators"
              :key="evaluator"
              :label="formatLabel(evaluator)"
              :value="evaluator"
            />
          </el-select>
          <span class="hint">选择评估器类型</span>
        </el-form-item>
      </template>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { ExtensionsResponse } from '@/types'
import { DataAnalysis } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  generate_evaluation: form.value.generate_evaluation ?? false,
  evaluator_type: form.value.evaluator_type || 'general',
})

const extensions = ref<ExtensionsResponse>({
  memory: { short_term: [], long_term: [] },
  tools: {},
  formatters: [],
  evaluators: [],
  openjudge_graders: [],
})

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const formatLabel = (label: string) => {
  return label.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
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
.evaluation-settings { padding: 0 }
.unified-header-card { margin-bottom: 20px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1) }
.header-background { background: linear-gradient(135deg, #67C23A 0%, #85ce61 100%); padding: 24px; display: flex; align-items: center; gap: 16px; color: #FFFFFF }
.header-icon { flex-shrink: 0 }
.header-content { flex: 1 }
.header-title { margin: 0 0 8px 0; font-size: 20px; font-weight: 600; color: #FFFFFF; line-height: 1.2 }
.header-description { margin: 0; font-size: 14px; color: rgba(255, 255, 255, 0.9); line-height: 1.5 }
.config-hint { margin-bottom: 24px; border-radius: 6px }
.hint-content { line-height: 1.6 }
.hint-title { font-weight: 600; color: #67C23A; margin-bottom: 8px }
.hint-list { margin: 8px 0 0 0; padding-left: 20px; color: #606266 }
.hint-list li { margin: 6px 0; line-height: 1.5 }
.hint-list strong { color: #303133; font-weight: 600 }
.evaluation-sections { display: flex; flex-direction: column; gap: 24px; margin-bottom: 24px }
.evaluation-card { border-radius: 8px }
.card-header { display: flex; align-items: center; gap: 12px }
.card-title { font-size: 16px; font-weight: 600; flex: 1 }
.hint { font-size: 0.85em; color: #909399; display: block; margin-top: 4px; line-height: 1.4 }
:deep(.el-card__header) { padding: 16px 20px; background: #f5f7fa; border-bottom: 1px solid #ebeef5 }
:deep(.el-card__body) { padding: 20px }
</style>
