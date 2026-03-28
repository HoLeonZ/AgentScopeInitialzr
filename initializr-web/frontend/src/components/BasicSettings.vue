<template>
  <el-form :model="form" label-width="150px" size="large">
    <el-form-item label="Project Name" required>
      <el-input
        v-model="form.name"
        placeholder="my-agent"
        @input="updateField('name', $event)"
      />
      <span class="hint">Lowercase, hyphens allowed (e.g., my-agent)</span>
    </el-form-item>

    <el-form-item label="Description">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="3"
        placeholder="Brief project description"
        @input="updateField('description', $event)"
      />
    </el-form-item>

    <el-form-item label="Author">
      <el-input
        v-model="form.author"
        placeholder="Your name"
        @input="updateField('author', $event)"
      />
    </el-form-item>

    <el-form-item label="Project Layout">
      <el-radio-group v-model="form.layout" @change="updateField('layout', $event)">
        <el-radio value="standard">
          <strong>Standard (src/)</strong>
          <div class="radio-description">
            Recommended: Organized structure with src/ directory
          </div>
        </el-radio>
        <el-radio value="lightweight">
          <strong>Lightweight</strong>
          <div class="radio-description">
            Simple structure: files in project root
          </div>
        </el-radio>
      </el-radio-group>
    </el-form-item>

    <el-form-item label="Python Version">
      <el-select v-model="form.python_version" @change="updateField('python_version', $event)">
        <el-option value="3.10" label="Python 3.10" />
        <el-option value="3.11" label="Python 3.11 (Recommended)" />
        <el-option value="3.12" label="Python 3.12" />
      </el-select>
    </el-form-item>
  </el-form>
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
.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
}

.radio-description {
  font-size: 0.9em;
  color: #606266;
  margin-top: 4px;
}

:deep(.el-radio) {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
  height: auto;
}

:deep(.el-radio__label) {
  line-height: 1.5;
}
</style>
