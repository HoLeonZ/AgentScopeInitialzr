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
        <h3>Extension Points</h3>
        <p class="subtitle">Configure AgentScope framework extensions</p>
        <el-alert type="info" :closable="false">
          Extension configuration UI - Simplified for MVP
        </el-alert>
      </div>

      <!-- Step 4: Testing & Evaluation -->
      <div v-show="currentStep === 4" class="step-content">
        <h3>Testing & Evaluation</h3>
        <p class="subtitle">Configure test generation and evaluation setup</p>
        <el-alert type="info" :closable="false">
          Testing configuration UI - Simplified for MVP
        </el-alert>
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
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'
import TemplateSelector from './TemplateSelector.vue'
import BasicSettings from './BasicSettings.vue'
import ModelSettings from './ModelSettings.vue'
import MemorySettings from './MemorySettings.vue'

const configStore = useConfigStore()
const currentStep = computed(() => configStore.currentStep)
const totalSteps = computed(() => configStore.totalSteps)
const isValid = computed(() => configStore.isValid)
const loading = computed(() => configStore.loading)
const error = computed(() => configStore.error)

const nextStep = () => {
  configStore.nextStep()
}

const prevStep = () => {
  configStore.prevStep()
}

const handleGenerate = async () => {
  const response = await configStore.generateProject()
  if (response && response.success) {
    ElMessage.success('Project generated successfully!')
    // TODO: Show download button
  }
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
</style>
