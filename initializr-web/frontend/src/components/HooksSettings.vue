<template>
  <el-card class="hooks-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#E6A23C"><Link /></el-icon>
          <span class="card-title">Hooks</span>
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
      <div class="hooks-flow-diagram">
        <div class="flow-container">
          <div class="flow-step">
            <div class="step-box input">
              <span>用户输入</span>
            </div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="hook-group">
            <div class="flow-step">
              <div class="step-box hook pre">
                <span>观察前</span>
                <div class="hook-dot"></div>
              </div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
              <div class="step-box llm">
                <span>LLM</span>
              </div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
              <div class="step-box hook post">
                <span>观察后</span>
                <div class="hook-dot"></div>
              </div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
              <div class="step-box hook pre">
                <span>回复前</span>
                <div class="hook-dot"></div>
              </div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
              <div class="step-box hook post">
                <span>回复后</span>
                <div class="hook-dot"></div>
              </div>
            </div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="step-box output">
              <span>回复</span>
            </div>
          </div>
        </div>
      </div>

      <el-divider />

      <div class="hooks-toolbar">
        <el-button type="primary" size="small" @click="addHook">
          <el-icon><Plus /></el-icon> 新增钩子
        </el-button>
        <span class="hooks-count">共 {{ localForm.hooks.length }} 个钩子</span>
      </div>

      <el-table
        :data="localForm.hooks"
        style="width: 100%"
        size="small"
        class="hooks-table"
        row-key="id"
      >
        <el-table-column width="50">
          <template #default>
            <el-icon class="drag-handle"><Rank /></el-icon>
          </template>
        </el-table-column>
        <el-table-column label="钩子名称" min-width="200">
          <template #default="{ row }">
            <el-input
              v-model="row.name"
              placeholder="请输入钩子名称"
              @change="updateHooks"
            />
          </template>
        </el-table-column>
        <el-table-column label="执行时机" width="160">
          <template #default="{ row }">
            <el-select v-model="row.hook_type" style="width: 140px" @change="updateHooks">
              <el-option label="回复前" value="pre_reply" />
              <el-option label="回复后" value="post_reply" />
              <el-option label="观察前" value="pre_observe" />
              <el-option label="观察后" value="post_observe" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="启用" width="80">
          <template #default="{ row }">
            <el-switch v-model="row.enabled" size="small" @change="updateHooks" />
          </template>
        </el-table-column>
        <el-table-column width="60">
          <template #default="{ row }">
            <el-button type="danger" size="small" text @click="removeHook(row)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { Link, Plus, Rank, Delete } from '@element-plus/icons-vue'
import type { HookItem } from '@/types'

const configStore = useConfigStore()

let hookIdCounter = 0

const localForm = reactive({
  enable_hooks: configStore.form.enable_hooks ?? false,
  hooks: (configStore.form.hooks || []) as HookItem[],
})

const addHook = () => {
  const newHook: HookItem & { id?: number } = {
    id: ++hookIdCounter,
    name: '',
    hook_type: 'pre_reply',
    enabled: true,
  }
  localForm.hooks.push(newHook)
  updateHooks()
}

const removeHook = (hook: HookItem & { id?: number }) => {
  const index = localForm.hooks.indexOf(hook)
  if (index > -1) {
    localForm.hooks.splice(index, 1)
  }
  updateHooks()
}

const updateHooks = () => {
  updateField('hooks', [...localForm.hooks])
}

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

onMounted(() => {
  localForm.enable_hooks = configStore.form.enable_hooks ?? false
  localForm.hooks = (configStore.form.hooks || []) as HookItem[]
})
</script>

<style scoped>
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

.hooks-flow-diagram {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.flow-container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hook-group {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border: 2px dashed #303133;
  border-radius: 12px;
  position: relative;
}

.step-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  min-width: 90px;
  min-height: 50px;
  position: relative;
  background: #909399;
  border: 2px solid #909399;
  color: #fff;
  box-sizing: border-box;
}

.step-box.input {
  background: #909399;
  border-color: #909399;
  color: #fff;
}

.step-box.output {
  background: #909399;
  border-color: #909399;
  color: #fff;
}

.step-box.llm {
  background: #ff4d4f;
  border-color: #ff4d4f;
  color: #fff;
}

.step-box.hook.pre {
  background: #909399;
  border-color: #909399;
  color: #fff;
}

.step-box.hook.post {
  background: #909399;
  border-color: #909399;
  color: #fff;
}

.hook-dot {
  width: 8px;
  height: 8px;
  background: currentColor;
  border-radius: 50%;
  margin-top: 4px;
}

.llm-icon {
  font-size: 16px;
  margin-top: 4px;
}

.flow-arrow {
  color: #909399;
  font-size: 18px;
  font-weight: bold;
}

.hooks-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.hooks-count {
  color: #909399;
  font-size: 14px;
}

.hooks-table {
  border-radius: 8px;
  overflow: hidden;
}

.hooks-table :deep(.el-table__row) {
  background: #ffffff;
}

.drag-handle {
  color: #c0c4cc;
  cursor: move;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>
