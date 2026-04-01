<template>
  <div class="basic-settings">
    <el-alert
      title="📋 项目基础信息"
      type="info"
      :closable="false"
      show-icon
      class="settings-alert"
    >
      <template #default>
        <p class="overview-text">
          配置您的 AgentScope 项目的基础信息。
        </p>
      </template>
    </el-alert>

    <el-form :model="form" label-width="140px" size="large" class="settings-form">
      <el-form-item label="项目名称" required>
        <el-input
          v-model="form.name"
          placeholder="我的智能体"
          @input="updateField('name', $event)"
        />
        <span class="hint">使用小写字母和连字符（例如：my-agent、chat-assistant）</span>
      </el-form-item>

      <el-form-item label="项目类型" required>
        <el-select
          v-model="form.agent_type"
          placeholder="选择项目类型"
          @change="updateField('agent_type', $event)"
          style="width: 100%"
        >
          <el-option label="Basic Agent" value="basic-agent">
            <div class="option-content">
              <div class="option-label">Basic Agent</div>
              <div class="option-desc">单个智能体，适合简单的对话和任务处理场景</div>
            </div>
          </el-option>
          <el-option label="Multi-Agent" value="multi-agent">
            <div class="option-content">
              <div class="option-label">Multi-Agent</div>
              <div class="option-desc">多个智能体协作，适合复杂任务的分工和并行处理</div>
            </div>
          </el-option>
        </el-select>
        <span class="hint">选择最适合您使用场景的智能体架构</span>
      </el-form-item>

      <el-form-item label="项目描述">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="简要描述您的智能体的功能和用途"
          @input="updateField('description', $event)"
        />
        <span class="hint">帮助用户了解您智能体的目的和功能</span>
      </el-form-item>

      <el-form-item label="Python 版本">
        <div class="version-display">
          <el-tag type="success" size="large">3.14.3</el-tag>
          <span class="hint">兼容 AgentScope 的固定版本</span>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useConfigStore } from '@/stores/config'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}
</script>

<style scoped>
.basic-settings {
  padding: 0;
}

.settings-alert {
  margin-bottom: 24px;
}

.overview-text {
  margin: 0;
  line-height: 1.6;
  color: #606266;
}

.settings-form {
  padding: 0 8px;
}

.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
  line-height: 1.4;
}

.version-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.option-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-label {
  font-weight: 600;
  color: #303133;
}

.option-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

:deep(.el-select-dropdown__item) {
  height: auto;
  padding: 8px 12px;
}
</style>
