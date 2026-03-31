<template>
  <div class="configuration-form">
    <el-steps :active="currentStep - 1" finish-status="success" align-center>
      <el-step title="Basic Settings" />
      <el-step title="Model & Memory" />
      <el-step title="Extensions" />
      <el-step title="Testing & Eval" />
    </el-steps>

    <div class="form-content">
      <!-- Step 1: Basic Settings -->
      <div v-show="currentStep === 1" class="step-content">
        <TemplateSelector />
        <BasicSettings />
      </div>

      <!-- Step 2: Model & Memory -->
      <div v-show="currentStep === 2" class="step-content">
        <ModelSettings />
        <MemorySettings />
      </div>

      <!-- Step 3: Extensions -->
      <div v-show="currentStep === 3" class="step-content">
        <ExtensionsSettings />
      </div>

      <!-- Step 4: Testing & Evaluation -->
      <div v-show="currentStep === 4" class="step-content">
        <TestingSettings />
      </div>
    </div>

    <!-- Navigation buttons -->
    <div class="form-actions">
      <el-button v-if="currentStep > 1" @click="prevStep">
        Previous
      </el-button>
      <el-button
        v-if="currentStep < totalSteps"
        type="primary"
        :disabled="!isValid"
        @click="nextStep"
      >
        Next
      </el-button>
      <el-button
        v-if="currentStep === totalSteps"
        type="success"
        :loading="loading"
        :disabled="!isValid"
        @click="handleGenerate"
      >
        Generate Project
      </el-button>
    </div>

    <!-- Error display -->
    <el-alert
      v-if="error"
      type="error"
      :title="error"
      :closable="false"
      style="margin-top: 20px"
    />

    <!-- Download Success Dialog -->
    <el-dialog
      v-model="showDownloadDialog"
      title="🎉 Project Generated Successfully!"
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="success-content">
        <el-result
          icon="success"
          title="Your project is ready!"
          sub-title="The AgentScope project has been generated with your configuration."
        >
          <template #extra>
            <el-descriptions :column="1" border class="project-info">
              <el-descriptions-item label="Project ID">
                {{ generatedProjectId }}
              </el-descriptions-item>
              <el-descriptions-item label="Project Name">
                {{ form.name }}
              </el-descriptions-item>
              <el-descriptions-item label="Agent Type">
                {{ form.agent_type }}
              </el-descriptions-item>
              <el-descriptions-item label="Model Provider">
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
            What's inside your project:
          </template>
          <ul class="project-contents">
            <li>✅ Complete source code with your configurations</li>
            <li>✅ README.md with setup instructions</li>
            <li>✅ requirements.txt with all dependencies</li>
            <li>✅ .env.example for environment variables</li>
            <li>✅ pytest configuration (if tests enabled)</li>
          </ul>
        </el-alert>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showDownloadDialog = false">
            Close
          </el-button>
          <el-button type="primary" @click="downloadProject" :loading="downloading">
            <el-icon><Download /></el-icon>
            Download ZIP
          </el-button>
          <el-button @click="resetAndStartOver">
            Start Over
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import TemplateSelector from './TemplateSelector.vue'
import BasicSettings from './BasicSettings.vue'
import ModelSettings from './ModelSettings.vue'
import MemorySettings from './MemorySettings.vue'
import ExtensionsSettings from './ExtensionsSettings.vue'
import TestingSettings from './TestingSettings.vue'

const configStore = useConfigStore()
const currentStep = computed(() => configStore.currentStep)
const totalSteps = computed(() => configStore.totalSteps)
const isValid = computed(() => configStore.isValid)
const loading = computed(() => configStore.loading)
const error = computed(() => configStore.error)
const form = computed(() => configStore.form)

// Download dialog state
const showDownloadDialog = ref(false)
const generatedProjectId = ref('')
const downloadUrl = ref('')
const downloading = ref(false)

const nextStep = () => {
  configStore.nextStep()
}

const prevStep = () => {
  configStore.prevStep()
}

const handleGenerate = async () => {
  const response = await configStore.generateProject()
  if (response && response.success) {
    // Show download dialog
    generatedProjectId.value = response.project_id || ''
    downloadUrl.value = response.download_url || ''
    showDownloadDialog.value = true

    ElMessage.success({
      message: 'Project generated successfully!',
      duration: 3000,
    })
  }
}

const downloadProject = () => {
  if (!downloadUrl.value) {
    ElMessage.error('Download URL not available')
    return
  }

  downloading.value = true

  try {
    // Create download link
    const link = document.createElement('a')
    link.href = downloadUrl.value
    link.download = `${form.value.name}_${generatedProjectId.value}.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    ElMessage.success('Download started!')
  } catch (error) {
    console.error('Download error:', error)
    ElMessage.error('Failed to download project')
  } finally {
    downloading.value = false
  }
}

const resetAndStartOver = () => {
  showDownloadDialog.value = false
  configStore.resetForm()
  configStore.setCurrentStep(1)
  ElMessage.info('Form reset. You can start a new project.')
}
</script>

<style scoped>
.configuration-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.form-content {
  margin: 40px 0;
  min-height: 400px;
}

.step-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-actions {
  text-align: center;
  margin-top: 40px;
  border-top: 1px solid #dcdfe6;
  padding-top: 20px;
}

.subtitle {
  color: #606266;
  margin-bottom: 20px;
}

/* Success Dialog Styles */
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
</style>
