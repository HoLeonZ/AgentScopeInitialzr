<template>
  <el-card class="ragas-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#67C23A"><DataAnalysis /></el-icon>
          <span class="card-title">评测配置</span>
          <el-tag size="small" type="success">可选</el-tag>
        </div>
        <el-switch
          v-model="localForm.enable_ragas_evaluation"
          size="large"
          @change="updateField('enable_ragas_evaluation', $event)"
        />
      </div>
    </template>

    <template v-if="localForm.enable_ragas_evaluation">
      <el-form :model="localForm" label-width="140px" size="large">
        <el-form-item label="数据集文件">
          <el-input
            v-model="localForm.evaluation_csv_filename"
            placeholder="evaluation_data.csv"
            style="width: 280px"
            @change="updateField('evaluation_csv_filename', $event)"
          />
          <span class="hint">CSV 文件需包含: question, answer, context, reference 列</span>
        </el-form-item>

        <el-form-item label="评测指标">
          <el-checkbox-group
            v-model="localForm.evaluation_metrics"
            @change="handleMetricsChange"
          >
            <el-checkbox label="faithfulness">Faithfulness</el-checkbox>
            <el-checkbox label="answer_relevancy">Answer Relevancy</el-checkbox>
            <el-checkbox label="context_precision">Context Precision</el-checkbox>
            <el-checkbox label="context_recall">Context Recall</el-checkbox>
          </el-checkbox-group>
          <span class="hint">选择要计算的评测指标</span>
        </el-form-item>

        <el-divider content-position="left">
          <el-icon><Document /></el-icon>
          生成的文件
        </el-divider>

        <div class="generated-files">
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>evaluation/ragas_evaluator.py</span>
            <el-tag size="small" type="info">评测脚本</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>evaluation/requirements.txt</span>
            <el-tag size="small" type="info">依赖</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>evaluation/README.md</span>
            <el-tag size="small" type="info">使用说明</el-tag>
          </div>
        </div>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { DataAnalysis, Document } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  enable_ragas_evaluation: form.value.enable_ragas_evaluation ?? false,
  evaluation_csv_filename: form.value.evaluation_csv_filename || 'evaluation_data.csv',
  evaluation_metrics: form.value.evaluation_metrics || [
    'faithfulness',
    'answer_relevancy',
    'context_precision',
    'context_recall'
  ]
})

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const handleMetricsChange = (value: string[]) => {
  if (value.length === 0) {
    localForm.evaluation_metrics = ['faithfulness']
    updateField('evaluation_metrics', ['faithfulness'])
  } else {
    updateField('evaluation_metrics', value)
  }
}
</script>

<style scoped>
.ragas-card {
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

.generated-files {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
}

.file-item span {
  flex: 1;
  font-family: monospace;
  font-size: 13px;
}

::deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

::deep(.el-card__body) {
  padding: 20px;
}
</style>
