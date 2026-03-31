<template>
  <div class="testing-settings">
    <!-- Test Generation -->
    <el-card class="testing-card test-gen-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#409EFF"><DocumentChecked /></el-icon>
            <span class="header-title">Test Generation</span>
            <el-tag size="small" type="success">Recommended</el-tag>
          </div>
          <el-switch
            v-model="localForm.generate_tests"
            size="large"
            @change="updateField('generate_tests', $event)"
          />
        </div>
        <div class="card-description">
          Generate comprehensive test suite with pytest framework
        </div>
      </template>

      <template v-if="localForm.generate_tests">
        <el-alert
          type="success"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Generated test module will include unit tests, integration tests, and pytest configuration.
        </el-alert>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Test Framework">
              <el-select v-model="testFramework" disabled size="large">
                <el-option label="pytest" value="pytest" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="Include Coverage">
              <el-switch v-model="includeCoverage" size="large" />
              <span class="hint">Generate pytest-cov configuration</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <el-icon><Document /></el-icon>
          What will be generated
        </el-divider>

        <div class="generated-files-preview">
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>tests/test_&lt;project&gt;.py</span>
            <el-tag size="small" type="info">Unit Tests</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>tests/conftest.py</span>
            <el-tag size="small" type="info">Test Fixtures</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>pytest.ini</span>
            <el-tag size="small" type="info">Configuration</el-tag>
          </div>
        </div>
      </template>
    </el-card>

    <!-- Evaluation Configuration -->
    <el-card class="testing-card eval-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#67C23A"><DataAnalysis /></el-icon>
            <span class="header-title">Evaluation Module</span>
            <el-tag size="small" type="success">Recommended</el-tag>
          </div>
          <el-switch
            v-model="localForm.generate_evaluation"
            size="large"
            @change="updateField('generate_evaluation', $event)"
          />
        </div>
        <div class="card-description">
          Generate evaluation framework for agent performance testing
        </div>
      </template>

      <template v-if="localForm.generate_evaluation">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Evaluation module helps measure agent performance and quality metrics.
        </el-alert>

        <el-form-item label="Evaluator Type">
          <el-select
            v-model="localForm.evaluator_type"
            placeholder="Select evaluator type"
            size="large"
            @change="updateField('evaluator_type', $event)"
          >
            <el-option
              v-for="evaluator in extensions.evaluators"
              :key="evaluator"
              :label="formatLabel(evaluator)"
              :value="evaluator"
            >
              <div class="option-item">
                <div class="option-label">{{ formatLabel(evaluator) }}</div>
                <div class="option-desc">{{ getEvaluatorDescription(evaluator) }}</div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-alert
          v-if="localForm.evaluator_type === 'ray'"
          type="warning"
          :closable="false"
          show-icon
        >
          Ray evaluator requires cluster configuration. Ensure you have Ray installed.
        </el-alert>
      </template>
    </el-card>

    <!-- OpenJudge Integration -->
    <el-card class="testing-card openjudge-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#E6A23C"><Trophy /></el-icon>
            <span class="header-title">OpenJudge Integration</span>
            <el-tag size="small" type="warning">Advanced</el-tag>
          </div>
          <el-switch
            v-model="localForm.enable_openjudge"
            size="large"
            @change="updateField('enable_openjudge', $event)"
          />
        </div>
        <div class="card-description">
          Automated grading system for agent response evaluation
        </div>
      </template>

      <template v-if="localForm.enable_openjudge">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          OpenJudge provides automated graders to evaluate agent responses on multiple criteria.
        </el-alert>

        <el-form-item label="Available Graders">
          <el-checkbox-group
            v-model="localForm.openjudge_graders"
            @change="updateField('openjudge_graders', $event)"
          >
            <div class="graders-grid">
              <div
                v-for="grader in extensions.openjudge_graders"
                :key="grader"
                class="grader-item"
                :class="{ 'is-checked': localForm.openjudge_graders.includes(grader) }"
              >
                <el-checkbox :label="grader" class="grader-checkbox">
                  <div class="grader-content">
                    <div class="grader-header">
                      <el-icon class="grader-icon"><Medal /></el-icon>
                      <span class="grader-name">{{ formatGraderName(grader) }}</span>
                    </div>
                    <span class="grader-desc">{{ getGraderDescription(grader) }}</span>
                  </div>
                </el-checkbox>
              </div>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <el-alert
          type="warning"
          :closable="false"
          show-icon
        >
          OpenJudge integration requires additional dependencies and API configuration.
        </el-alert>
      </template>
    </el-card>

    <!-- Benchmark Configuration -->
    <el-card class="testing-card benchmark-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon" color="#F56C6C"><Timer /></el-icon>
            <span class="header-title">Benchmark Tasks</span>
          </div>
          <el-switch
            v-model="enableBenchmarks"
            size="large"
            @change="handleBenchmarkToggle"
          />
        </div>
        <div class="card-description">
          Generate initial benchmark tasks for performance testing
        </div>
      </template>

      <template v-if="enableBenchmarks">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 20px"
        >
          Benchmark tasks will be generated based on your agent type and configuration.
        </el-alert>

        <el-form-item label="Number of Tasks">
          <el-input-number
            v-model="localForm.initial_benchmark_tasks"
            :min="0"
            :max="100"
            :step="5"
            size="large"
            @change="updateField('initial_benchmark_tasks', $event)"
          />
          <span class="hint">Number of benchmark tasks to generate (0 = skip)</span>
        </el-form-item>

        <template v-if="localForm.initial_benchmark_tasks > 0">
          <el-form-item label="Benchmark Suite">
            <el-select v-model="benchmarkSuite" placeholder="Select benchmark suite" size="large">
              <el-option label="Custom Tasks" value="custom">
                <div class="option-item">
                  <div class="option-label">Custom Tasks</div>
                  <div class="option-desc">Generate custom benchmark tasks</div>
                </div>
              </el-option>
              <el-option label="MMLU Sample" value="mmlu">
                <div class="option-item">
                  <div class="option-label">MMLU Sample</div>
                  <div class="option-desc">Massive Multitask Language Understanding</div>
                </div>
              </el-option>
              <el-option label="GSM8K Sample" value="gsm8k">
                <div class="option-item">
                  <div class="option-label">GSM8K Sample</div>
                  <div class="option-desc">Grade school math problems</div>
                </div>
              </el-option>
              <el-option label="Custom Dataset" value="custom_dataset">
                <div class="option-item">
                  <div class="option-label">Custom Dataset</div>
                  <div class="option-desc">Load from external URL</div>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item v-if="benchmarkSuite === 'custom_dataset'" label="Dataset URL">
            <el-input
              v-model="datasetUrl"
              placeholder="https://example.com/dataset.json"
              size="large"
            />
          </el-form-item>

          <el-divider content-position="left">
            <el-icon><Document /></el-icon>
            What will be generated
          </el-divider>

          <div class="generated-files-preview">
            <div class="file-item">
              <el-icon><Document /></el-icon>
              <span>tests/test_benchmarks.py</span>
              <el-tag size="small" type="success">{{ localForm.initial_benchmark_tasks }} Tasks</el-tag>
            </div>
          </div>
        </template>
      </template>
    </el-card>

    <!-- Advanced Options -->
    <el-card class="testing-card advanced-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Setting /></el-icon>
            <span class="header-title">Advanced Options</span>
          </div>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="Enable Logging">
            <el-switch v-model="enableLogging" size="large" />
          </el-form-item>
        </el-col>

        <el-col :span="8">
          <el-form-item label="Test Output Format">
            <el-select v-model="testOutputFormat" size="large">
              <el-option label="JSON" value="json" />
              <el-option label="JUnit XML" value="junit" />
              <el-option label="HTML Report" value="html" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="8">
          <el-form-item label="Parallel Execution">
            <el-switch v-model="parallelTests" size="large" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item v-if="parallelTests" label="Max Workers">
        <el-input-number
          v-model="maxWorkers"
          :min="2"
          :max="16"
          :step="2"
          size="large"
        />
        <span class="hint">Maximum number of parallel test workers</span>
      </el-form-item>
    </el-card>

    <!-- Summary Card -->
    <el-card class="summary-card" shadow="never">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><InfoFilled /></el-icon>
          <span class="header-title">Testing & Evaluation Summary</span>
        </div>
      </template>

      <el-descriptions :column="3" border>
        <el-descriptions-item label="Test Generation">
          <el-tag :type="localForm.generate_tests ? 'success' : 'info'" size="large">
            <el-icon v-if="localForm.generate_tests"><Select /></el-icon>
            {{ localForm.generate_tests ? 'Enabled' : 'Disabled' }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Evaluation">
          <el-tag :type="localForm.generate_evaluation ? 'success' : 'info'" size="large">
            <el-icon v-if="localForm.generate_evaluation"><Select /></el-icon>
            {{ localForm.generate_evaluation ? localForm.evaluator_type : 'Disabled' }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="OpenJudge">
          <el-tag :type="localForm.enable_openjudge ? 'warning' : 'info'" size="large">
            <el-icon v-if="localForm.enable_openjudge"><Select /></el-icon>
            {{ localForm.enable_openjudge ? `${localForm.openjudge_graders.length} Graders` : 'Disabled' }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Benchmark Tasks" :span="3">
          <el-tag :type="localForm.initial_benchmark_tasks > 0 ? 'success' : 'info'" size="large">
            {{ localForm.initial_benchmark_tasks }} Tasks
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { ExtensionsResponse } from '@/types'
import {
  DocumentChecked,
  DataAnalysis,
  Trophy,
  Timer,
  Setting,
  InfoFilled,
  Document,
  Medal,
  Select
} from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

// Local form state
const localForm = reactive({
  generate_tests: form.value.generate_tests ?? false,
  generate_evaluation: form.value.generate_evaluation ?? false,
  evaluator_type: form.value.evaluator_type || 'general',
  enable_openjudge: form.value.enable_openjudge ?? false,
  openjudge_graders: form.value.openjudge_graders || [],
  initial_benchmark_tasks: form.value.initial_benchmark_tasks || 0,
})

// Additional options
const testFramework = ref('pytest')
const includeCoverage = ref(true)
const benchmarkSuite = ref('custom')
const datasetUrl = ref('')
const enableBenchmarks = ref(localForm.initial_benchmark_tasks > 0)
const enableLogging = ref(true)
const testOutputFormat = ref('json')
const parallelTests = ref(false)
const maxWorkers = ref(4)

// Extensions data from API
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

// Fetch extensions from API
const fetchExtensions = async () => {
  try {
    const response = await api.getExtensions()
    extensions.value = response
  } catch (error) {
    console.error('Failed to fetch extensions:', error)
  }
}

// Update field in store
const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

// Handle benchmark toggle
const handleBenchmarkToggle = (value: boolean) => {
  if (!value) {
    updateField('initial_benchmark_tasks', 0)
  } else if (localForm.initial_benchmark_tasks === 0) {
    updateField('initial_benchmark_tasks', 5)
  }
}

// Format label for display
const formatLabel = (label: string) => {
  return label.split('_').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

// Format grader name
const formatGraderName = (name: string) => {
  return name.replace(/([A-Z])/g, ' $1').trim()
}

// Get evaluator description
const getEvaluatorDescription = (evaluator: string) => {
  const descriptions: Record<string, string> = {
    'general': 'General-purpose evaluator for common tasks',
    'ray': 'Distributed evaluation using Ray framework',
  }
  return descriptions[evaluator] || ''
}

// Get grader description
const getGraderDescription = (grader: string) => {
  const descriptions: Record<string, string> = {
    'RelevanceGrader': 'Evaluates response relevance to query',
    'CorrectnessGrader': 'Checks factual correctness of responses',
    'HallucinationGrader': 'Detects hallucinations in generated content',
    'SafetyGrader': 'Evaluates safety and policy compliance',
    'CodeQualityGrader': 'Assesses code quality and best practices',
  }
  return descriptions[grader] || ''
}

// Initialize
onMounted(() => {
  fetchExtensions()
})
</script>

<style scoped>
.testing-settings {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 20px 0;
}

/* Testing Card Styles */
.testing-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.testing-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
}

.testing-card.test-gen-card {
  border-left: 4px solid #409EFF;
}

.testing-card.eval-card {
  border-left: 4px solid #67C23A;
}

.testing-card.openjudge-card {
  border-left: 4px solid #E6A23C;
}

.testing-card.benchmark-card {
  border-left: 4px solid #F56C6C;
}

.testing-card.advanced-card {
  border-left: 4px solid #909399;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 24px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.card-description {
  margin-top: 8px;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

/* Graders Grid */
.graders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.grader-item {
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s ease;
  background: #ffffff;
}

.grader-item:hover {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.grader-item.is-checked {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.grader-checkbox {
  width: 100%;
}

.grader-checkbox :deep(.el-checkbox__label) {
  width: 100%;
  padding-left: 8px;
}

.grader-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.grader-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.grader-icon {
  color: #E6A23C;
  font-size: 18px;
}

.grader-name {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}

.grader-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

/* Option Items */
.option-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.option-label {
  font-weight: 600;
  color: #303133;
}

.option-desc {
  font-size: 12px;
  color: #909399;
}

/* Generated Files Preview */
.generated-files-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 13px;
}

.file-item .el-icon {
  color: #409EFF;
}

/* Summary Card */
.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.summary-card :deep(.el-card__header) {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.summary-card .header-title {
  color: white;
}

.summary-card .header-icon {
  color: white;
}

.summary-card :deep(.el-card__body) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
}

/* Divider */
:deep(.el-divider__text) {
  font-size: 1em;
  font-weight: 600;
  color: #606266;
}

:deep(.el-divider__text .el-icon) {
  margin-right: 4px;
}

/* Form Items */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}

/* Hint */
.hint {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

/* Alerts */
:deep(.el-alert) {
  border-radius: 8px;
}

:deep(.el-alert__content) {
  line-height: 1.6;
}
</style>
