<template>
  <el-card class="openjudge-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon :size="20" color="#E6A23C"><Trophy /></el-icon>
        <span class="card-title">OpenJudge集成</span>
        <el-tag size="small" type="warning">高级功能</el-tag>
      </div>
    </template>

    <el-form :model="form" label-width="140px" size="large">
      <el-form-item label="启用OpenJudge">
        <el-switch
          v-model="localForm.enable_openjudge"
          @change="updateField('enable_openjudge', $event)"
        />
        <span class="hint">自动评分系统，评估智能体响应</span>
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
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { ExtensionsResponse } from '@/types'
import { Trophy } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  enable_openjudge: form.value.enable_openjudge ?? false,
  openjudge_graders: form.value.openjudge_graders || [],
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

const formatGraderName = (name: string) => {
  return name.replace(/([A-Z])/g, ' $1').trim()
}

const getGraderDescription = (grader: string) => {
  const descriptions: Record<string, string> = {
    RelevanceGrader: '评估响应相关性',
    CorrectnessGrader: '检查事实正确性',
    HallucinationGrader: '检测生成内容中的幻觉',
    SafetyGrader: '评估安全性和合规性',
    CodeQualityGrader: '评估代码质量',
  }
  return descriptions[grader] || ''
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
.openjudge-card {
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

.graders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
  margin-top: 12px;
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

::deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

::deep(.el-card__body) {
  padding: 20px;
}
</style>

