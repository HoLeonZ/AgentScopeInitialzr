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
      <el-form :model="localForm" label-width="120px" size="large">
        <el-form-item label="评测数据集">
          <div class="dataset-section">
            <div class="dataset-file-row">
              <el-input
                v-model="localForm.evaluation_csv_filename"
                placeholder="evaluation_data.csv"
                style="width: 240px"
                @change="updateField('evaluation_csv_filename', $event)"
              />
              <el-button type="primary" @click="downloadSampleCsv">
                <el-icon><Download /></el-icon> 下载示例 CSV
              </el-button>
              <el-upload
                class="csv-uploader"
                :auto-upload="false"
                :show-file-list="false"
                accept=".csv"
                :on-change="handleFileChange"
              >
                <el-button type="warning" plain>
                  <el-icon><Upload /></el-icon> 上传 CSV
                </el-button>
              </el-upload>
            </div>
            <div class="upload-row">
              <span class="upload-hint">CSV 文件需包含列：question, answer, context, reference</span>
            </div>
          </div>
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
        </el-form-item>

        <el-divider content-position="left">
          <el-icon><InfoFilled /></el-icon>
          指标说明
        </el-divider>

        <div class="metrics-explanation">
          <div class="metric-item">
            <h4>Faithfulness（忠诚度）</h4>
            <p>衡量生成答案与给定上下文的事实一致性。分数越高表示答案越忠于上下文内容。</p>
          </div>
          <div class="metric-item">
            <h4>Answer Relevancy（答案相关性）</h4>
            <p>衡量生成答案与原始问题的相关程度。分数越高表示答案越切题。</p>
          </div>
          <div class="metric-item">
            <h4>Context Precision（上下文精确度）</h4>
            <p>衡量上下文中文档按相关性排序的准确性。分数越高表示排序越合理。</p>
          </div>
          <div class="metric-item">
            <h4>Context Recall（上下文召回率）</h4>
            <p>衡量上下文是否包含回答问题所需的所有信息。分数越高表示召回越全面。</p>
          </div>
        </div>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, computed, ref } from 'vue'
import { useConfigStore } from '@/stores/config'
import { DataAnalysis, Download, Upload, InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const hasDownloaded = ref(false)

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

const downloadSampleCsv = () => {
  const headers = ['question', 'answer', 'context', 'reference']
  const rows = []
  for (let i = 1; i <= 100; i++) {
    rows.push([
      `示例问题 ${i}：这个问题的答案是什么？`,
      `这是问题 ${i} 的回答内容，包含详细的解释和说明。`,
      `【上下文 ${i}】这是一个相关的上下文文档，包含了回答问题所需的背景知识...`,
      `标准参考答案 ${i}：正确的回答应该包含...`
    ])
  }

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell.replace(/"/g, '""')}"`).join(','))
  ].join('\n')

  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = localForm.evaluation_csv_filename
  link.click()
  URL.revokeObjectURL(url)
  hasDownloaded.value = true
  ElMessage.success('示例 CSV 已下载，请上传包含相同格式的评测数据')
}

const handleFileChange = (file: any) => {
  const fileName = file.name
  localForm.evaluation_csv_filename = fileName
  updateField('evaluation_csv_filename', fileName)
  ElMessage.success(`已选择文件: ${fileName}`)
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

.dataset-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dataset-file-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.upload-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
}

.metrics-explanation {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0 8px;
}

.metric-item {
  background: #f5f7fa;
  padding: 12px 16px;
  border-radius: 6px;
  border-left: 3px solid #67C23A;
}

.metric-item h4 {
  margin: 0 0 6px 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.metric-item p {
  margin: 0;
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
}

::deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

::deep(.el-card__body) {
  padding: 20px;
}

::deep(.el-divider__text) {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
}
</style>
