<template>
  <div class="config-navigation">
    <div class="nav-header">
      <el-icon :size="20"><Menu /></el-icon>
      <span class="header-title">配置导航</span>
    </div>

    <div class="nav-content">
      <div
        v-for="section in sections"
        :key="section.id"
        class="nav-section"
        :class="{ 'is-active': modelValue === section.id }"
        @click="selectSection(section.id)"
      >
        <div class="nav-section-header">
          <div class="section-left">
            <el-icon class="section-icon" :size="18">
              <component :is="section.icon" />
            </el-icon>
            <span class="section-title">{{ section.title }}</span>
          </div>
          <div class="section-right">
            <el-icon v-if="isSectionComplete(section.id)" color="#67C23A" :size="18">
              <CircleCheck />
            </el-icon>
            <el-icon v-else color="#909399" :size="18">
              <Clock />
            </el-icon>
          </div>
        </div>
      </div>
    </div>

    <div class="nav-footer">
      <div class="completion-summary">
        <el-text size="small" type="info">
          已完成: {{ completedSections }}/{{ sections.length }} 项
        </el-text>
      </div>

      <el-button
        type="primary"
        :disabled="!isAllComplete"
        @click="handleGenerate"
        size="large"
        style="width: 100%; margin-top: 12px"
      >
        <el-icon><DocumentAdd /></el-icon>
        生成项目
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Menu,
  Document,
  Memo,
  Tools,
  DataAnalysis,
  DocumentAdd,
  Connection,
  CircleCheck,
  Clock,
  Reading,
  Star
} from '@element-plus/icons-vue'
import { useConfigStore } from '@/stores/config'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'generate': []
}>()

const configStore = useConfigStore()

// 配置分区定义
const sections = [
  {
    id: 'basic',
    title: '项目基础',
    icon: Document
  },
  {
    id: 'model',
    title: '模型配置',
    icon: Connection
  },
  {
    id: 'memory',
    title: '记忆配置',
    icon: Memo
  },
  {
    id: 'knowledge',
    title: '知识库配置',
    icon: Reading
  },
  {
    id: 'skills',
    title: 'Skill配置',
    icon: Star
  },
  {
    id: 'extensions',
    title: '扩展功能',
    icon: Tools
  },
  {
    id: 'testing',
    title: '测试评估',
    icon: DataAnalysis
  }
]

// 选择配置区块
const selectSection = (sectionId: string) => {
  emit('update:modelValue', sectionId)
}

// 判断区块是否完成
const isSectionComplete = (sectionId: string): boolean => {
  const form = configStore.form

  switch (sectionId) {
    case 'basic':
      return !!(form.name && form.description)
    case 'model':
      return !!(form.model_provider && form.model_config?.model && form.model_config?.api_key)
    case 'memory':
      return form.enable_memory !== undefined
    case 'knowledge':
      return form.enable_knowledge !== undefined
    case 'skills':
      return form.enable_skills !== undefined
    case 'extensions':
      return form.enable_tools !== undefined || form.enable_formatter !== undefined
    case 'testing':
      return form.generate_tests !== undefined
    default:
      return false
  }
}

// 已完成区块数量
const completedSections = computed(() => {
  return sections.filter(section => isSectionComplete(section.id)).length
})

// 是否全部完成
const isAllComplete = computed(() => {
  return completedSections.value === sections.length
})

// 生成项目
const handleGenerate = () => {
  emit('generate')
}
</script>

<style scoped>
.config-navigation {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-right: 1px solid #e4e7ed;
}

.nav-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
}

.nav-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px 0;
}

.nav-section {
  margin-bottom: 4px;
}

.nav-section-header {
  padding: 12px 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
  user-select: none;
}

.nav-section-header:hover {
  background: #f5f7fa;
}

.nav-section.is-active .nav-section-header {
  background: #ecf5ff;
  border-right: 3px solid #409eff;
}

.section-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-icon {
  color: #606266;
}

.section-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.section-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-footer {
  padding: 20px;
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}

.completion-summary {
  margin-bottom: 12px;
}

.summary-text {
  display: block;
  margin-top: 8px;
  text-align: center;
}

/* 滚动条样式 */
.nav-content::-webkit-scrollbar {
  width: 6px;
}

.nav-content::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 3px;
}

.nav-content::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}
</style>
