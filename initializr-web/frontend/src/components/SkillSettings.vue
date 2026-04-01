<template>
  <div class="skill-settings">
    <!-- 技能配置概述 -->
    <el-alert
      title="🛠️ 技能配置"
      type="info"
      :closable="false"
      show-icon
      class="skill-overview"
    >
      <template #default>
        <p class="overview-text">
          配置专业技能以扩展智能体的能力。从下方可选技能中选择您想要启用的技能。
        </p>
      </template>
    </el-alert>

    <!-- 详细配置区块 -->
    <div class="skill-sections">
      <!-- 启用开关 -->
      <el-card class="skill-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon :size="20" color="#67C23A"><Star /></el-icon>
              <span class="card-title">启用技能</span>
            </div>
            <el-switch
              v-model="localForm.enable_skills"
              size="large"
              @change="updateField('enable_skills', $event)"
            />
          </div>
        </template>

        <template v-if="localForm.enable_skills">
          <el-alert
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 24px"
          >
            选择您想要为智能体启用的技能。每个技能都提供特定的能力。
          </el-alert>

          <!-- 可用技能列表 -->
          <el-divider content-position="left">
            <el-icon><Grid /></el-icon>
            可用技能
          </el-divider>

          <el-table
            ref="skillTableRef"
            :data="paginatedSkills"
            style="width: 100%"
            @selection-change="handleSelectionChange"
            :row-class-name="getRowClassName"
          >
            <el-table-column type="selection" width="55" />

            <el-table-column label="技能名称" width="280">
              <template #default="{ row }">
                <div class="table-skill-name">
                  <el-icon class="table-skill-icon" :size="20">
                    <component :is="row.icon" />
                  </el-icon>
                  <span class="name-text">{{ row.name }}</span>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="描述" min-width="300">
              <template #default="{ row }">
                <div class="table-skill-desc">{{ row.description }}</div>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50]"
              :total="availableSkills.length"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, ref, watch, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import type { ElTable } from 'element-plus'
import {
  Star,
  Grid,
  ChatLineRound,
  Document,
  Tools,
  Monitor,
  Picture,
  VideoPlay,
  Search
} from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

// Table ref
const skillTableRef = ref<InstanceType<typeof ElTable>>()

// Local form state
const localForm = reactive({
  enable_skills: form.value.enable_skills ?? false,
  skills: form.value.skills || [],
})

// Pagination state
const currentPage = ref(1)
const pageSize = ref(10)

// Paginated skills
const paginatedSkills = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return availableSkills.slice(start, end)
})

// 可用技能列表（静态演示数据）
const availableSkills = [
  {
    id: 'conversational_response',
    name: '对话响应',
    description: '处理自然语言对话交互，提供流畅的对话体验',
    category: '对话',
    requires_api: false,
    icon: ChatLineRound
  },
  {
    id: 'analyze_input',
    name: '输入分析',
    description: '解析和理解用户输入，提取关键信息和意图',
    category: '分析',
    requires_api: false,
    icon: Document
  },
  {
    id: 'summarize_text',
    name: '文本摘要',
    description: '生成文本内容的摘要，快速提取核心要点',
    category: '文本处理',
    requires_api: false,
    icon: Document
  },
  {
    id: 'code_interpreter',
    name: '代码执行',
    description: '支持多种编程语言的代码执行和结果返回',
    category: '代码',
    requires_api: false,
    icon: Tools
  },
  {
    id: 'web_search',
    name: '网页搜索',
    description: '搜索网络信息，获取实时数据和在线资源',
    category: '搜索',
    requires_api: true,
    icon: Search
  },
  {
    id: 'data_analysis',
    name: '数据分析',
    description: '处理和分析数据，生成可视化报告和洞察',
    category: '分析',
    requires_api: false,
    icon: Monitor
  },
  {
    id: 'image_processing',
    name: '图像处理',
    description: '处理和分析图像，提取特征和理解内容',
    category: '多媒体',
    requires_api: false,
    icon: Picture
  },
  {
    id: 'video_analysis',
    name: '视频分析',
    description: '分析和理解视频内容，提取关键帧和场景信息',
    category: '多媒体',
    requires_api: true,
    icon: VideoPlay
  }
]

// Handle selection change
const handleSelectionChange = (selection: any[]) => {
  const selectedIds = selection.map(item => item.id)
  localForm.skills = selectedIds
  updateField('skills', selectedIds)
}

// Get row class name
const getRowClassName = ({ row }: any) => {
  return localForm.skills.includes(row.id) ? 'selected-row' : ''
}

// Update field in store
const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

// Get skill name by id
const getSkillName = (skillId: string) => {
  const skill = availableSkills.find(s => s.id === skillId)
  return skill?.name || skillId
}

// Handle page size change
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

// Handle current page change
const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// Sync table selection with form.skills
onMounted(() => {
  if (skillTableRef.value && localForm.skills.length > 0) {
    availableSkills.forEach(row => {
      if (localForm.skills.includes(row.id)) {
        skillTableRef.value!.toggleRowSelection(row, true)
      }
    })
  }
})
</script>

<style scoped>
.skill-settings {
  padding: 0;
}

/* 总（Overview）样式 */
.skill-overview {
  margin-bottom: 32px;
}

.overview-text {
  margin: 0;
  line-height: 1.8;
  color: #606266;
  font-size: 15px;
}

/* 分（Detailed Configuration）样式 */
.skill-sections {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.skill-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}

.hint {
  font-size: 0.9em;
  color: #909399;
  display: block;
  margin-top: 8px;
  line-height: 1.6;
}

/* Skills Grid */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.skill-item {
  border: 2px solid #dcdfe6;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
  background: #ffffff;
}

.skill-item:hover {
  border-color: #67C23A;
  background: #f0f9ff;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(103, 194, 58, 0.25);
}

.skill-item.is-checked {
  border-color: #67C23A;
  background: #f0f9ff;
}

.skill-checkbox {
  width: 100%;
}

.skill-checkbox :deep(.el-checkbox__label) {
  width: 100%;
  padding-left: 12px;
}

.skill-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skill-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.skill-icon {
  color: #67C23A;
  font-size: 22px;
}

.skill-name {
  font-weight: 600;
  font-size: 16px;
  color: #303133;
}

.skill-desc {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin: 6px 0;
  padding-left: 34px;
}

.skill-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-left: 34px;
}

:deep(.el-card__header) {
  padding: 20px 24px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 28px 24px;
}

:deep(.el-divider__text) {
  font-size: 1em;
  font-weight: 600;
  color: #67C23A;
}

:deep(.el-divider--horizontal) {
  margin: 32px 0 24px 0;
}

:deep(.el-tag) {
  font-size: 13px;
  padding: 4px 10px;
}

.selected-skills-list {
  margin-top: 12px;
}

/* 表格样式 */
:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table__header) {
  font-size: 15px;
}

:deep(.el-table th.el-table__cell) {
  background: #fafafa;
  font-weight: 600;
  color: #303133;
}

:deep(.el-table__row) {
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

:deep(.el-table__row.selected-row) {
  background-color: #f0f9ff;
}

:deep(.el-table__row.selected-row:hover) {
  background-color: #e0f2fe;
}

.table-skill-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-skill-icon {
  color: #67C23A;
  flex-shrink: 0;
}

.table-skill-name .name-text {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.table-skill-desc {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

:deep(.el-table__cell) {
  padding: 16px 0;
}

:deep(.el-checkbox__inner) {
  width: 18px;
  height: 18px;
}

:deep(.el-checkbox__inner::after) {
  height: 9px;
  left: 6px;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  padding: 20px 0;
}

/* 分页组件 */
:deep(.el-pagination) {
  justify-content: center;
}

:deep(.el-pagination__total) {
  font-weight: 500;
}

:deep(.el-pager li) {
  min-width: 32px;
  height: 32px;
  line-height: 32px;
  border-radius: 4px;
}

:deep(.el-pager li.is-active) {
  background-color: #409EFF;
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .skill-sections {
    gap: 16px;
  }

  .skill-card {
    margin: 0;
  }

  .skills-grid {
    grid-template-columns: 1fr;
  }
}
</style>
