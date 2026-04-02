<template>
  <div class="basic-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="32" color="#FFFFFF" class="header-icon"><Document /></el-icon>
        <div class="header-content">
          <h2 class="header-title">项目基础信息</h2>
          <p class="header-description">配置您的 AgentScope 项目的基础信息，包括项目名称、类型和描述</p>
        </div>
        <el-tag type="info" size="large" effect="dark">必填配置</el-tag>
      </div>
    </div>

    <!-- 配置提示 -->
    <el-alert
      type="info"
      :closable="false"
      show-icon
      class="config-hint"
    >
      <template #default>
        <div class="hint-content">
          <div class="hint-title">💡 配置说明</div>
          <ul class="hint-list">
            <li>项目名称将作为生成代码的目录名和包名</li>
            <li>Basic Agent 适合单智能体场景，Multi-Agent 适合多智能体协作</li>
            <li>描述信息将出现在 README 文件中</li>
          </ul>
        </div>
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
          <el-option label="Basic Agent" value="basic">
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
import { Document } from '@element-plus/icons-vue'

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

/* 统一头部卡片 */
.unified-header-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-background {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  color: #FFFFFF;
}

.header-icon {
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.header-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #FFFFFF;
  line-height: 1.2;
}

.header-description {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.5;
}

/* 配置提示 */
.config-hint {
  margin-bottom: 24px;
  border-radius: 6px;
}

.hint-content {
  line-height: 1.6;
}

.hint-title {
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 8px;
}

.hint-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
  color: #606266;
}

.hint-list li {
  margin: 6px 0;
  line-height: 1.5;
}

/* 表单样式 */
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

/* 响应式设计 */
@media (max-width: 768px) {
  .header-background {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .header-icon {
    align-self: center;
  }

  .header-title {
    font-size: 18px;
  }

  .header-description {
    font-size: 13px;
  }
}
</style>
