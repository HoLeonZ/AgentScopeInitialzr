<template>
  <div class="testing-settings">
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="28" color="#FFFFFF" class="header-icon"><DataAnalysis /></el-icon>
        <div class="header-content">
          <h2 class="header-title">评测配置</h2>
          <p class="header-description">评测模块，生成量化评估报告</p>
        </div>
        <el-tag type="success" size="large" effect="dark">质量评估</el-tag>
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
          <div class="hint-title">💡 使用说明</div>
          <ul class="hint-list">
            <li>生成项目后，将 CSV 数据文件放入 <code>evaluation/</code> 目录</li>
            <li>CSV 文件需包含列：<code>question</code>, <code>answer</code>, <code>context</code>, <code>reference</code></li>
            <li>运行评测脚本生成 HTML 格式的评估报告</li>
          </ul>
        </div>
      </template>
    </el-alert>

    <div class="testing-sections">
      <RagasEvaluationSettings />
    </div>
  </div>
</template>

<script setup lang="ts">
import { DataAnalysis } from '@element-plus/icons-vue'
import RagasEvaluationSettings from '@/components/RagasEvaluationSettings.vue'
</script>

<style scoped>
.testing-settings {
  padding: 0;
}

.unified-header-card {
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.header-background {
  background: linear-gradient(135deg, #67C23A 0%, #95d475 100%);
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
}

.hint-list code {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13px;
}

.testing-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
