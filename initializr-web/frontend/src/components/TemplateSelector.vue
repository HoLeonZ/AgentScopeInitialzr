<template>
  <div class="template-selector">
    <h3>Select Agent Type</h3>
    <p class="subtitle">Choose the type of agent you want to create</p>

    <el-row :gutter="20">
      <el-col
        v-for="template in templates"
        :key="template.id"
        :span="6"
      >
        <el-card
          :class="{ selected: form.agent_type === template.id }"
          class="template-card"
          shadow="hover"
          @click="selectTemplate(template.id)"
        >
          <div class="template-icon">{{ getIcon(template.id) }}</div>
          <h4>{{ template.name }}</h4>
          <p>{{ template.description }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { api } from '@/api'
import type { TemplateInfo } from '@/types'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const templates = ref<TemplateInfo[]>([])

const getIcon = (id: string): string => {
  const icons: Record<string, string> = {
    'basic': '🤖',
    'multi-agent': '👥',
    'research': '🔍',
    'browser': '🌐',
  }
  return icons[id] || '📦'
}

const selectTemplate = (id: string) => {
  configStore.setField('agent_type', id as any)
}

onMounted(async () => {
  try {
    const response = await api.getTemplates()
    templates.value = response.templates
  } catch (error) {
    console.error('Failed to load templates:', error)
  }
})
</script>

<style scoped>
.template-selector {
  margin-bottom: 30px;
}

.template-selector h3 {
  margin-top: 0;
}

.subtitle {
  color: #606266;
  margin-bottom: 20px;
}

.template-card {
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
  min-height: 150px;
}

.template-card:hover {
  transform: translateY(-4px);
}

.template-card.selected {
  border: 2px solid #409eff;
  background-color: #ecf5ff;
}

.template-icon {
  font-size: 3em;
  margin-bottom: 10px;
}

.template-card h4 {
  margin: 10px 0;
  font-size: 1.1em;
}

.template-card p {
  font-size: 0.85em;
  color: #606266;
  line-height: 1.4;
}
</style>
