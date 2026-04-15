<template>
  <div class="hooks-card">
    <div class="header-background">
      <el-icon :size="28" color="#FFFFFF" class="header-icon"><Link /></el-icon>
      <div class="header-content">
        <h2 class="header-title">Hooks</h2>
        <p class="header-description">生命周期拦截点，在 LLM 调用前后执行自定义逻辑</p>
      </div>
      <el-switch
        v-model="localForm.enable_hooks"
        size="large"
        @change="updateField('enable_hooks', $event)"
      />
    </div>

    <template v-if="localForm.enable_hooks">
      <div class="hooks-flow-diagram">
        <div class="flow-container">
          <div class="flow-step">
            <div class="step-box input">
              <span>用户输入</span>
            </div>
          </div>
          <div class="flow-arrow">→</div>
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
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="step-box output">
              <span>回复</span>
            </div>
          </div>
        </div>
        <div class="flow-legend">
          <span class="legend-item"><span class="legend-dot hook"></span> Hook 拦截点</span>
          <span class="legend-item"><span class="legend-dot llm"></span> LLM 调用</span>
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
  </div>
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
  overflow: hidden;
  background: #fff;
}

.header-background {
  background: linear-gradient(135deg, #E6A23C 0%, #f5a623 100%);
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
  color: rgba(255, 255, 255, 0.85);
}

.hooks-flow-diagram {
  padding: 20px;
  background: #f5f7fa;
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

.step-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  min-width: 80px;
  position: relative;
}

.step-box.input {
  background: #e6f7ff;
  border: 2px solid #1890ff;
  color: #1890ff;
}

.step-box.output {
  background: #f6ffed;
  border: 2px solid #52c41a;
  color: #52c41a;
}

.step-box.llm {
  background: #fff7e6;
  border: 2px solid #fa8c16;
  color: #fa8c16;
  min-width: 100px;
}

.step-box.hook {
  background: #fff1f0;
  border: 2px solid #ff4d4f;
  color: #ff4d4f;
}

.step-box.hook.post {
  background: #f9f0ff;
  border-color: #722ed1;
  color: #722ed1;
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

.flow-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 12px;
  font-size: 12px;
  color: #606266;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 4px;
}

.legend-dot.hook {
  background: #fff1f0;
  border: 2px solid #ff4d4f;
}

.legend-dot.llm {
  background: #fff7e6;
  border: 2px solid #fa8c16;
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
