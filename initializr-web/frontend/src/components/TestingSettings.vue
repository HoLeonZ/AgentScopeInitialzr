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
            <li><strong>测试生成：</strong>生成 pytest 测试套件与配置</li>
            <li><strong>评估模块：</strong>生成评估器与指标评估代码</li>
            <li><strong>OpenJudge集成：</strong>启用自动评分器体系（可选）</li>
            <li><strong>基准测试：</strong>生成初始基准任务（可选）</li>
          </ul>
        </div>
      </template>
    </el-alert>

    <!-- 逐模块渲染：每个模块独立占用 1 个组件 -->
    <div class="testing-sections">
      <TestGenerationSettings />
      <EvaluationSettings />
      <OpenJudgeSettings />
      <BenchmarkSettings />
    </div>
  </div>
</template>

<script setup lang="ts">
import { DocumentChecked } from '@element-plus/icons-vue'
import TestGenerationSettings from '@/components/TestGenerationSettings.vue'
import EvaluationSettings from '@/components/EvaluationSettings.vue'
import OpenJudgeSettings from '@/components/OpenJudgeSettings.vue'
import BenchmarkSettings from '@/components/BenchmarkSettings.vue'
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
.testing-sections {
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
