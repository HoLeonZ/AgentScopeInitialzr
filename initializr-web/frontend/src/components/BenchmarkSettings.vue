<template>
  <el-card class="benchmark-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#F56C6C"><Timer /></el-icon>
          <span class="card-title">基准测试</span>
          <el-tag size="small" type="danger">可选</el-tag>
        </div>
        <el-switch
          v-model="enableBenchmarks"
          size="large"
          @change="handleBenchmarkToggle"
        />
      </div>
    </template>

    <template v-if="enableBenchmarks">
      <el-form :model="form" label-width="140px" size="large">
        <el-form-item label="任务数量">
          <el-input-number
            v-model="localForm.initial_benchmark_tasks"
            :min="0"
            :max="100"
            :step="5"
            controls-position="right"
            style="width: 140px"
            @change="updateField('initial_benchmark_tasks', $event)"
          />
        </el-form-item>

        <template v-if="localForm.initial_benchmark_tasks > 0">
          <el-form-item label="测试套件">
            <el-select
              v-model="benchmarkSuite"
              placeholder="选择测试套件"
              style="width: 240px"
            >
              <el-option label="自定义任务" value="custom" />
              <el-option label="MMLU示例" value="mmlu" />
              <el-option label="GSM8K示例" value="gsm8k" />
            </el-select>
            <span class="hint">目前仅用于 UI 展示</span>
          </el-form-item>
        </template>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { Timer } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  initial_benchmark_tasks: form.value.initial_benchmark_tasks || 0,
})

const benchmarkSuite = ref('custom')
const enableBenchmarks = ref(localForm.initial_benchmark_tasks > 0)

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const handleBenchmarkToggle = (value: boolean) => {
  if (!value) {
    localForm.initial_benchmark_tasks = 0
    enableBenchmarks.value = false
    updateField('initial_benchmark_tasks', 0)
    return
  }

  if (localForm.initial_benchmark_tasks === 0) {
    localForm.initial_benchmark_tasks = 5
  }
  enableBenchmarks.value = true
  updateField('initial_benchmark_tasks', localForm.initial_benchmark_tasks)
}
</script>

<style scoped>
.benchmark-card {
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

::deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

::deep(.el-card__body) {
  padding: 20px;
}
</style>

