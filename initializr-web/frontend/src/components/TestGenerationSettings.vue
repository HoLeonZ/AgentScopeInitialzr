<template>
  <el-card class="test-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#409EFF"><DocumentChecked /></el-icon>
          <span class="card-title">测试套件生成</span>
          <el-tag size="small" type="primary">pytest</el-tag>
        </div>
        <el-switch
          v-model="localForm.generate_tests"
          size="large"
          @change="updateField('generate_tests', $event)"
        />
      </div>
    </template>

    <template v-if="localForm.generate_tests">
      <el-form :model="form" label-width="140px" size="large">
        <el-form-item label="测试框架">
          <el-select v-model="testFramework" disabled style="width: 100%">
            <el-option label="pytest" value="pytest" />
          </el-select>
          <span class="hint">当前支持pytest框架</span>
        </el-form-item>

        <el-form-item label="代码覆盖率">
          <el-switch v-model="includeCoverage" />
          <span class="hint">生成pytest-cov配置文件</span>
        </el-form-item>

        <el-divider content-position="left">生成的文件</el-divider>

        <div class="generated-files">
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>tests/test_&lt;project&gt;.py</span>
            <el-tag size="small" type="info">单元测试</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>tests/conftest.py</span>
            <el-tag size="small" type="info">测试夹具</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>pytest.ini</span>
            <el-tag size="small" type="info">配置文件</el-tag>
          </div>
        </div>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { DocumentChecked, Document } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  generate_tests: form.value.generate_tests ?? false,
})

const testFramework = ref('pytest')
const includeCoverage = ref(true)

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}
</script>

<style scoped>
.test-generation-settings {
  padding: 0;
}

.unified-header-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-background {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
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

.hint-list strong {
  color: #303133;
  font-weight: 600;
}

.test-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 24px;
}

.test-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
  line-height: 1.4;
}

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

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-divider__text) {
  font-size: 0.95em;
  font-weight: 600;
  color: #409EFF;
}

:deep(.el-divider--horizontal) {
  margin: 24px 0 20px 0;
}

@media (max-width: 768px) {
  .test-sections {
    gap: 16px;
  }

  .test-card {
    margin: 0;
  }

  .header-background {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .header-title {
    font-size: 18px;
  }

  .header-description {
    font-size: 13px;
  }
}
</style>
