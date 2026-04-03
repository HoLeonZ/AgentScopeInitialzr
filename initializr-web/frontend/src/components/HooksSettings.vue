<template>
  <el-card class="hooks-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#E6A23C"><Link /></el-icon>
          <span class="card-title">生命周期钩子</span>
          <el-tag size="small" type="warning">拦截点</el-tag>
        </div>
        <el-switch
          v-model="localForm.enable_hooks"
          size="large"
          @change="updateField('enable_hooks', $event)"
        />
      </div>
    </template>

    <template v-if="localForm.enable_hooks">
      <el-form :model="form" label-width="140px" size="large">
        <el-form-item label="可用钩子">
          <el-checkbox-group v-model="localForm.hooks" @change="updateField('hooks', $event)">
            <div class="hooks-grid">
              <div
                v-for="hook in availableHooks"
                :key="hook.value"
                class="hook-item"
                :class="{ 'is-checked': localForm.hooks.includes(hook.value) }"
              >
                <el-checkbox :label="hook.value" class="hook-checkbox">
                  <div class="hook-content">
                    <div class="hook-header">
                      <el-icon class="hook-icon"><Connection /></el-icon>
                      <span class="hook-name">{{ hook.label }}</span>
                    </div>
                    <div class="hook-desc">{{ hook.description }}</div>
                    <el-tag size="small" type="info">{{ hook.timing }}</el-tag>
                  </div>
                </el-checkbox>
              </div>
            </div>
          </el-checkbox-group>
        </el-form-item>

        <el-alert
          v-if="localForm.hooks.length > 0"
          type="success"
          :closable="false"
          show-icon
          style="margin-top: 16px"
        >
          已选择 {{ localForm.hooks.length }} 个钩子
        </el-alert>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { Link, Connection } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  enable_hooks: form.value.enable_hooks ?? false,
  hooks: form.value.hooks || [],
})

const availableHooks = [
  {
    value: 'pre_reply',
    label: '回复前',
    description: '在智能体生成响应前执行',
    timing: '执行时机: 回复前'
  },
  {
    value: 'post_reply',
    label: '回复后',
    description: '在智能体生成响应后执行',
    timing: '执行时机: 回复后'
  },
  {
    value: 'pre_observe',
    label: '观察前',
    description: '在智能体观察数据前拦截',
    timing: '执行时机: 观察前'
  },
  {
    value: 'post_observe',
    label: '观察后',
    description: '在智能体观察数据后处理',
    timing: '执行时机: 观察后'
  },
]

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}
</script>

<style scoped>
.hooks-settings {
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
  background: linear-gradient(135deg, #E6A23C 0%, #f0c78a 100%);
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
  color: #E6A23C;
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
.hooks-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 24px;
}

.hooks-card {
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

/* Hooks Grid */
.hooks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.hook-item {
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s ease;
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
  gap: 8px;
}

.hook-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hook-icon {
  color: #E6A23C;
  font-size: 18px;
}

.hook-name {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}

.hook-desc {
  font-size: 13px;
  color: #606266;
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
  .hooks-sections {
    gap: 16px;
  }

  .hooks-card {
    margin: 0;
  }

  .card-header {
    flex-wrap: wrap;
  }

  .hooks-grid {
    grid-template-columns: 1fr;
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
