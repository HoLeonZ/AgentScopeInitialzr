<template>
  <div class="testing-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="28" color="#FFFFFF" class="header-icon"><DocumentChecked /></el-icon>
        <div class="header-content">
          <h2 class="header-title">测试与评估配置</h2>
          <p class="header-description">配置测试框架、评估模块和基准测试</p>
        </div>
        <el-tag type="danger" size="large" effect="dark">质量保证</el-tag>
      </div>
    </div>

    <!-- 配置表单 -->
    <div class="config-form">
      <el-form :model="form" label-width="120px" size="large" class="aligned-form">
        <!-- Test Generation -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#409EFF"><DocumentChecked /></el-icon>
            <span>测试生成</span>
            <el-switch
              v-model="localForm.generate_tests"
              size="small"
              style="margin-left: auto"
              @change="updateField('generate_tests', $event)"
            />
          </div>

          <template v-if="localForm.generate_tests">
            <el-form-item label="测试框架">
              <el-select v-model="testFramework" disabled style="width: 200px">
                <el-option label="pytest" value="pytest" />
              </el-select>
              <div class="inline-hint">使用pytest框架生成综合测试套件</div>
            </el-form-item>

            <el-form-item label="代码覆盖率">
              <el-switch v-model="includeCoverage" />
              <div class="inline-hint">生成pytest-cov配置文件</div>
            </el-form-item>

            <div class="generated-files">
              <div class="file-item">
                <el-icon><Document /></el-icon>
                <span>tests/test_&lt;project&gt;.py</span>
                <el-tag size="small" type="info">单元测试</el-tag>
              </div>
              <div class="file-item">
                <el-icon><Document /></el-icon>
                <span>tests/conftest.py</span>
                <el-tag size="small" type="info">测试夹具</el-tag>
              </div>
            </div>
          </template>
        </div>

        <!-- Evaluation Configuration -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#67C23A"><DataAnalysis /></el-icon>
            <span>评估模块</span>
            <el-switch
              v-model="localForm.generate_evaluation"
              size="small"
              style="margin-left: auto"
              @change="updateField('generate_evaluation', $event)"
            />
          </div>

          <template v-if="localForm.generate_evaluation">
            <el-form-item label="评估器类型">
              <el-select
                v-model="localForm.evaluator_type"
                placeholder="选择评估器"
                style="width: 320px"
                @change="updateField('evaluator_type', $event)"
              >
                <el-option
                  v-for="evaluator in extensions.evaluators"
                  :key="evaluator"
                  :label="formatLabel(evaluator)"
                  :value="evaluator"
                />
              </el-select>
              <div class="inline-hint">评估智能体性能和质量指标</div>
            </el-form-item>
          </template>
        </div>

        <!-- OpenJudge Integration -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#E6A23C"><Trophy /></el-icon>
            <span>OpenJudge集成</span>
            <el-tag size="small" type="warning" style="margin-left: auto">高级功能</el-tag>
          </div>

          <el-form-item label="启用OpenJudge">
            <el-switch
              v-model="localForm.enable_openjudge"
              @change="updateField('enable_openjudge', $event)"
            />
            <div class="inline-hint">自动评分系统，评估智能体响应</div>
          </el-form-item>

          <template v-if="localForm.enable_openjudge">
            <el-form-item label="评分器">
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
                        <div class="grader-name">{{ formatGraderName(grader) }}</div>
                        <div class="grader-desc">{{ getGraderDescription(grader) }}</div>
                      </div>
                    </el-checkbox>
                  </div>
                </div>
              </el-checkbox-group>
            </el-form-item>
          </template>
        </div>

        <!-- Benchmark Tasks -->
        <div class="form-section">
          <div class="section-title">
            <el-icon :size="18" color="#F56C6C"><Timer /></el-icon>
            <span>基准测试</span>
            <el-switch
              v-model="enableBenchmarks"
              size="small"
              style="margin-left: auto"
              @change="handleBenchmarkToggle"
            />
          </div>

          <template v-if="enableBenchmarks">
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
              <div class="inline-hint">生成初始基准任务数量</div>
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
              </el-form-item>
            </template>
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
  DocumentChecked,
  DataAnalysis,
  Trophy,
  Timer,
  Document
} from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  generate_tests: form.value.generate_tests ?? false,
  generate_evaluation: form.value.generate_evaluation ?? false,
  evaluator_type: form.value.evaluator_type || 'general',
  enable_openjudge: form.value.enable_openjudge ?? false,
  openjudge_graders: form.value.openjudge_graders || [],
  initial_benchmark_tasks: form.value.initial_benchmark_tasks || 0,
})

const testFramework = ref('pytest')
const includeCoverage = ref(true)
const benchmarkSuite = ref('custom')
const enableBenchmarks = ref(localForm.initial_benchmark_tasks > 0)

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

const handleBenchmarkToggle = (value: boolean) => {
  if (!value) {
    updateField('initial_benchmark_tasks', 0)
  } else if (localForm.initial_benchmark_tasks === 0) {
    updateField('initial_benchmark_tasks', 5)
  }
}

const formatLabel = (label: string) => {
  return label.split('_').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

const formatGraderName = (name: string) => {
  return name.replace(/([A-Z])/g, ' $1').trim()
}

const getGraderDescription = (grader: string) => {
  const descriptions: Record<string, string> = {
    'RelevanceGrader': '评估响应相关性',
    'CorrectnessGrader': '检查事实正确性',
    'HallucinationGrader': '检测生成内容中的幻觉',
    'SafetyGrader': '评估安全性和合规性',
    'CodeQualityGrader': '评估代码质量'
  }
  return descriptions[grader] || ''
}

onMounted(() => {
  fetchExtensions()
})
</script>

<style scoped>
.testing-settings {
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
  background: linear-gradient(135deg, #F56C6C 0%, #ff8a8a 100%);
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

/* Generated Files */
.generated-files {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #606266;
}

.file-item .el-icon {
  color: #409EFF;
}

/* Graders Grid */
.graders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.grader-item {
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.2s;
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
  gap: 4px;
}

.grader-name {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
}

.grader-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
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

  .graders-grid {
    grid-template-columns: 1fr;
  }
}
</style>
