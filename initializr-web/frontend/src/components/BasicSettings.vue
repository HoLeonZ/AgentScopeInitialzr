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

    <el-form-item label="Python Version">
      <el-input
        value="3.14.3"
        disabled
      />
      <span class="hint">Python 3.14.3 (fixed version)</span>
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
</style>
