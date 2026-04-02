<template>
  <div class="extensions-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="28" color="#FFFFFF" class="header-icon"><Tools /></el-icon>
        <div class="header-content">
          <h2 class="header-title">扩展功能配置</h2>
          <p class="header-description">配置格式化器、钩子和管道等高级扩展</p>
        </div>
        <el-tag type="primary" size="large" effect="dark">高级配置</el-tag>
      </div>
    </div>

    <el-alert
      type="info"
      :closable="false"
      show-icon
      class="config-hint"
    >
      <template #default>
        <div class="hint-content">
          <div class="hint-title">💡 模块说明</div>
          <ul class="hint-list">
            <li><strong>格式化器：</strong>根据模型提供商调整消息格式</li>
            <li><strong>生命周期钩子：</strong>在回复/观察关键点拦截并扩展逻辑</li>
            <li><strong>多智能体管道：</strong>仅在多智能体模式下启用协作工作流</li>
          </ul>
        </div>
      </template>
    </el-alert>

    <!-- 逐模块渲染：每个模块独立占用 1 个组件 -->
    <div class="extensions-sections">
      <FormatterSettings />
      <HooksSettings />
      <PipelineSettings v-if="form.agent_type === 'multi-agent'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { Tools } from '@element-plus/icons-vue'
import FormatterSettings from '@/components/FormatterSettings.vue'
import HooksSettings from '@/components/HooksSettings.vue'
import PipelineSettings from '@/components/PipelineSettings.vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)
</script>

<style scoped>
.extensions-settings {
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
  background: linear-gradient(135deg, #909399 0%, #b3b8bd 100%);
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
  margin-bottom: 8px;
  color: #303133;
}

.hint-list {
  margin: 0;
  padding-left: 20px;
  color: #606266;
}

.hint-list li {
  margin: 6px 0;
  line-height: 1.5;
}

.hint-list strong {
  color: #303133;
}

/* 模块列表 */
.extensions-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 24px;
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

/* Hooks Grid */
.hooks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.hook-item {
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.2s;
  background: #ffffff;
}

.hook-item:hover {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.hook-item.is-checked {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.hook-checkbox {
  width: 100%;
}

.hook-checkbox :deep(.el-checkbox__label) {
  width: 100%;
  padding-left: 8px;
}

.hook-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hook-name {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
}

.hook-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

/* 控件行 */
.control-row {
  display: flex;
  gap: 16px;
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

  .hooks-grid {
    grid-template-columns: 1fr;
  }

  .control-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>
