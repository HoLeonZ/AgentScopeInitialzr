<template>
  <el-card class="formatter-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon :size="20" color="#67C23A"><Document /></el-icon>
        <span class="card-title">消息格式化器</span>
        <el-tag size="small" type="success">消息格式</el-tag>
      </div>
    </template>

    <el-form :model="form" label-width="140px" size="large">
      <el-form-item label="启用格式化器">
        <el-switch
          v-model="localForm.enable_formatter"
          @change="updateField('enable_formatter', $event)"
        />
        <span class="hint">启用自定义消息格式化器</span>
      </el-form-item>

      <template v-if="localForm.enable_formatter">
        <el-form-item label="格式化器类型">
          <el-select
            v-model="localForm.formatter"
            placeholder="选择格式化器"
            style="width: 100%"
            @change="updateField('formatter', $event)"
          >
            <el-option
              v-for="formatter in extensions.formatters"
              :key="formatter"
              :value="formatter"
              :label="formatter"
            />
          </el-select>
          <span class="hint">根据模型提供商选择对应的格式化器</span>
        </el-form-item>

        <el-alert
          type="success"
          :closable="false"
          show-icon
          style="margin-top: 16px"
        >
          已选择格式化器：{{ localForm.formatter || '未选择' }}
        </el-alert>
      </template>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { ExtensionsResponse } from '@/types'
import { Document } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  enable_formatter: form.value.enable_formatter ?? false,
  formatter: form.value.formatter || null,
})

const extensions = ref<ExtensionsResponse>({
  memory: {
    short_term: [],
    long_term: []
  },
  tools: {},
  formatters: [],
  evaluators: [],
  openjudge_graders: [],
})

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

onMounted(async () => {
  try {
    const response = await api.getExtensions()
    extensions.value = response
  } catch (error) {
    console.error('加载扩展失败:', error)
  }
})
</script>

<style scoped>
.formatter-settings {
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
  background: linear-gradient(135deg, #67C23A 0%, #85ce61 100%);
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
  color: #67C23A;
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

/* 配置区块 */
.formatter-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 24px;
}

.formatter-card {
  border-radius: 8px;
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

.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
  line-height: 1.4;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .formatter-sections {
    gap: 16px;
  }

  .formatter-card {
    margin: 0;
  }

  .card-header {
    flex-wrap: wrap;
  }

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
