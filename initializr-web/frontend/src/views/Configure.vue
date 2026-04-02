<template>
  <div class="configure">
    <el-container class="configure-container">
      <!-- 左侧导航 -->
      <el-aside width="280px" class="configure-aside">
        <ConfigNavigation
          v-model="activeSection"
          @generate="handleGenerate"
        />
      </el-aside>

      <!-- 右侧内容 -->
      <el-main class="configure-main">
        <div class="main-content">
          <!-- 右上：动态配置区域 -->
          <div class="config-dynamic-area">
            <!-- 项目基础配置 -->
            <transition name="fade-slide" mode="out-in">
              <div v-if="activeSection === 'basic'" key="basic" class="config-form-container">
                <BasicSettings />
              </div>

              <!-- 模型配置 -->
              <div v-else-if="activeSection === 'model'" key="model" class="config-form-container">
                <ModelSettings />
              </div>

              <!-- 记忆配置 -->
              <div v-else-if="activeSection === 'memory'" key="memory" class="config-form-container">
                <MemorySettings />
              </div>

              <!-- 知识库配置 -->
              <div v-else-if="activeSection === 'knowledge'" key="knowledge" class="config-form-container">
                <KnowledgeBaseSettings />
              </div>

              <!-- Skill配置 -->
              <div v-else-if="activeSection === 'skills'" key="skills" class="config-form-container">
                <SkillSettings />
              </div>

              <!-- 扩展功能配置 -->
              <div v-else-if="activeSection === 'extensions'" key="extensions" class="config-container">
                <ExtensionsSettings />
              </div>

              <!-- 测试评估配置 -->
              <div v-else-if="activeSection === 'testing'" key="testing" class="config-form-container">
                <TestingSettings />
              </div>
            </transition>
          </div>

          <!-- 右下：固定预览区域 -->
          <div class="config-preview-area">
            <ConfigPreviewPanel />
          </div>
        </div>
      </el-main>
    </el-container>

    <!-- 生成成功对话框 -->
    <el-dialog
      v-model="showDownloadDialog"
      title="🎉 项目生成成功！"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="success-content">
        <el-result
          icon="success"
          title="项目已成功生成"
          sub-title="您的 AgentScope 项目已准备就绪"
        >
          <template #extra>
            <el-descriptions :column="1" border class="project-info">
              <el-descriptions-item label="项目 ID">
                {{ generatedProjectId }}
              </el-descriptions-item>
              <el-descriptions-item label="项目名称">
                {{ form.name }}
              </el-descriptions-item>
              <el-descriptions-item label="Agent 类型">
                {{ form.agent_type }}
              </el-descriptions-item>
              <el-descriptions-item label="模型提供商">
                {{ form.model_provider }}
              </el-descriptions-item>
            </el-descriptions>
          </template>
        </el-result>

        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-top: 20px"
        >
          <template #title>
            项目内容
          </template>
          <ul class="project-contents">
            <li>✅ 完整的源代码和配置文件</li>
            <li>✅ README.md 和使用文档</li>
            <li>✅ requirements.txt 依赖清单</li>
            <li>✅ .env.example 环境变量模板</li>
            <li>✅ 优化的代码结构（符合单一职责原则）</li>
          </ul>
        </el-alert>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showDownloadDialog = false">
            关闭
          </el-button>
          <el-button type="primary" @click="downloadProject" :loading="downloading">
            <el-icon><Download /></el-icon>
            下载 ZIP
          </el-button>
          <el-button @click="resetAndStartOver">
            重新开始
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'
import {
  Document,
  Connection,
  Memo,
  Tools,
  DataAnalysis,
  Download,
  Reading,
  Star
} from '@element-plus/icons-vue'
import ConfigNavigation from '@/components/ConfigNavigation.vue'
import ConfigPreviewPanel from '@/components/ConfigPreviewPanel.vue'
import BasicSettings from '@/components/BasicSettings.vue'
import ModelSettings from '@/components/ModelSettings.vue'
import MemorySettings from '@/components/MemorySettings.vue'
import KnowledgeBaseSettings from '@/components/KnowledgeBaseSettings.vue'
import SkillSettings from '@/components/SkillSettings.vue'
import ExtensionsSettings from '@/components/ExtensionsSettings.vue'
import TestingSettings from '@/components/TestingSettings.vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

// 当前激活的配置区块
const activeSection = ref('basic')

// 下载对话框状态
const showDownloadDialog = ref(false)
const generatedProjectId = ref('')
const downloadUrl = ref('')
const downloading = ref(false)

// 生成项目
const handleGenerate = async () => {
  const response = await configStore.generateProject()
  if (response && response.success) {
    generatedProjectId.value = response.project_id || ''
    downloadUrl.value = response.download_url || ''
    showDownloadDialog.value = true

    ElMessage.success({
      message: '项目生成成功！',
      duration: 3000,
    })
  }
}

// 下载项目
const downloadProject = () => {
  if (!downloadUrl.value) {
    ElMessage.error('下载链接不可用')
    return
  }

  downloading.value = true

  try {
    // 构建完整的下载 URL
    const baseUrl = window.location.origin
    const fullDownloadUrl = downloadUrl.value.startsWith('http')
      ? downloadUrl.value
      : `${baseUrl}${downloadUrl.value}`

    const link = document.createElement('a')
    link.href = fullDownloadUrl
    link.download = `${form.value.name || 'project'}_${generatedProjectId.value}.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    ElMessage.success('下载已开始！')
  } catch (error) {
    console.error('下载错误:', error)
    ElMessage.error('下载失败')
  } finally {
    downloading.value = false
  }
}

// 重置并重新开始
const resetAndStartOver = () => {
  showDownloadDialog.value = false
  configStore.resetForm()
  activeSection.value = 'basic'
  ElMessage.info('表单已重置，可以开始新项目')
}
</script>

<style scoped>
.configure {
  height: 100vh;
  overflow: hidden;
}

.configure-container {
  height: 100%;
}

.configure-aside {
  background: #ffffff;
  border-right: 1px solid #e4e7ed;
  overflow: hidden;
}

.configure-main {
  padding: 0;
  overflow-y: auto;
  background: #f5f7fa;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  min-height: 100%;
}

/* 右上：动态配置区域 */
.config-dynamic-area {
  flex-shrink: 0;
}

.config-form-container {
  height: 65vh;
  overflow-y: auto;
  overflow-x: hidden;
}

.config-card {
  border-radius: 8px;
  height: 100%;
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

/* 右下：固定预览区域 */
.config-preview-area {
  flex: 1;
  min-height: 400px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: visible;
}

/* 过渡动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 成功对话框样式 */
.success-content {
  padding: 20px 0;
}

.project-info {
  margin-top: 20px;
}

.project-contents {
  margin: 10px 0 0 0;
  padding-left: 20px;
}

.project-contents li {
  margin: 8px 0;
  line-height: 1.6;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 滚动条样式 */
.config-form-container::-webkit-scrollbar {
  width: 6px;
}

.config-form-container::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 3px;
}

.config-form-container::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .configure-aside {
    width: 240px !important;
  }
}

@media (max-width: 768px) {
  .configure-container {
    flex-direction: column;
  }

  .configure-aside {
    width: 100% !important;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #e4e7ed;
  }

  .config-form-container {
    height: auto;
    max-height: 50vh;
  }
}
</style>

