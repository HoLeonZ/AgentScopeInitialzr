<template>
  <div class="skill-selector">
    <el-form-item label="可用 Skills" required>
      <el-alert
        title="从管理员上传的 skills 中选择"
        type="info"
        :closable="false"
        show-icon
        style="margin-bottom: 15px"
      />

      <div v-loading="loading" class="skills-container">
        <!-- Filter by tags -->
        <div class="filter-section" v-if="allTags.length > 0">
          <span>标签过滤：</span>
          <el-tag
            v-for="tag in allTags"
            :key="tag"
            :type="selectedTags.includes(tag) ? 'primary' : 'info'"
            :effect="selectedTags.includes(tag) ? 'dark' : 'plain'"
            style="margin-right: 8px; margin-bottom: 8px; cursor: pointer"
            @click="toggleTag(tag)"
          >
            {{ tag }}
          </el-tag>
        </div>

        <!-- Skills grid -->
        <el-checkbox-group v-model="selectedSkills" class="skills-grid">
          <el-checkbox
            v-for="skill in filteredSkills"
            :key="skill.skill_id"
            :label="skill.skill_id"
            :border="true"
            class="skill-checkbox"
          >
            <div class="skill-card">
              <div class="skill-header">
                <strong>{{ skill.name }}</strong>
                <el-tag size="small" type="success">{{ skill.version }}</el-tag>
              </div>

              <p class="skill-description">{{ skill.description }}</p>

              <div class="skill-meta">
                <el-tag
                  v-for="tag in skill.tags"
                  :key="tag"
                  size="small"
                  type="info"
                >
                  {{ tag }}
                </el-tag>
              </div>

              <div class="skill-actions">
                <el-button
                  type="primary"
                  size="small"
                  link
                  @click.stop="viewSkillDetail(skill)"
                >
                  查看详情
                </el-button>
              </div>
            </div>
          </el-checkbox>
        </el-checkbox-group>

        <!-- Empty state -->
        <el-empty
          v-if="filteredSkills.length === 0 && !loading"
          description="没有可用的 skills"
        >
          <el-button type="primary" @click="refreshSkills">刷新</el-button>
        </el-empty>
      </div>

      <!-- Selected skills summary -->
      <div class="selected-summary" v-if="selectedSkills.length > 0">
        <el-divider />
        <div class="summary-text">
          已选择 <strong>{{ selectedSkills.length }}</strong> 个 skills
        </div>
        <el-tag
          v-for="skillId in selectedSkills"
          :key="skillId"
          closable
          @close="removeSkill(skillId)"
          style="margin-right: 8px"
        >
          {{ getSkillName(skillId) }}
        </el-tag>
      </div>
    </el-form-item>

    <!-- Skill Detail Dialog -->
    <el-dialog
      v-model="showDetailDialog"
      :title="currentSkill?.name || 'Skill 详情'"
      width="600px"
    >
      <el-descriptions v-if="currentSkill" :column="1" border>
        <el-descriptions-item label="Name">
          {{ currentSkill.name }}
        </el-descriptions-item>
        <el-descriptions-item label="Version">
          <el-tag>{{ currentSkill.version }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Description">
          {{ currentSkill.description }}
        </el-descriptions-item>
        <el-descriptions-item label="License">
          {{ currentSkill.license }}
        </el-descriptions-item>
        <el-descriptions-item label="Author">
          {{ currentSkill.author || 'Unknown' }}
        </el-descriptions-item>
        <el-descriptions-item label="Tags">
          <el-tag
            v-for="tag in currentSkill.tags"
            :key="tag"
            size="small"
            style="margin-right: 5px"
          >
            {{ tag }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Uploaded">
          {{ formatDate(currentSkill.uploaded_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
        <el-button
          v-if="currentSkill && !selectedSkills.includes(currentSkill.skill_id)"
          type="primary"
          @click="selectCurrentSkill"
        >
          选择此 Skill
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

interface Skill {
  skill_id: string
  name: string
  description: string
  version: string
  license: string
  author: string
  tags: string[]
  uploaded_at: string
  size_bytes: number
}

interface Props {
  modelValue: string[]
}

interface Emits {
  (e: 'update:modelValue', value: string[]): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const loading = ref(false)
const skills = ref<Skill[]>([])
const selectedTags = ref<string[]>([])
const showDetailDialog = ref(false)
const currentSkill = ref<Skill | null>(null)

const selectedSkills = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const allTags = computed(() => {
  const tags = new Set<string>()
  skills.value.forEach(skill => {
    skill.tags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags).sort()
})

const filteredSkills = computed(() => {
  if (selectedTags.value.length === 0) {
    return skills.value
  }
  return skills.value.filter(skill =>
    selectedTags.value.some(tag => skill.tags.includes(tag))
  )
})

const fetchSkills = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/skills/')
    skills.value = response.data.skills
  } catch (error: any) {
    ElMessage.error('加载 skills 失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const toggleTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag)
  }
}

const viewSkillDetail = (skill: Skill) => {
  currentSkill.value = skill
  showDetailDialog.value = true
}

const selectCurrentSkill = () => {
  if (currentSkill.value) {
    selectedSkills.value = [...selectedSkills.value, currentSkill.value.skill_id]
    showDetailDialog.value = false
    ElMessage.success(`已选择 skill: ${currentSkill.value.name}`)
  }
}

const removeSkill = (skillId: string) => {
  selectedSkills.value = selectedSkills.value.filter(id => id !== skillId)
}

const getSkillName = (skillId: string) => {
  const skill = skills.value.find(s => s.skill_id === skillId)
  return skill?.name || skillId
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const refreshSkills = () => {
  fetchSkills()
}

// Expose refresh method
defineExpose({
  refreshSkills
})

onMounted(() => {
  fetchSkills()
})
</script>

<style scoped>
.skill-selector {
  width: 100%;
}

.skills-container {
  min-height: 200px;
}

.filter-section {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.filter-section span {
  font-weight: bold;
  margin-right: 10px;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.skill-checkbox {
  height: auto;
  width: 100%;
  margin: 0;
}

.skill-checkbox :deep(.el-checkbox__label) {
  width: 100%;
  padding-left: 10px;
}

.skill-card {
  width: 100%;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.skill-description {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.skill-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 8px;
}

.skill-actions {
  display: flex;
  justify-content: flex-end;
}

.selected-summary {
  margin-top: 15px;
}

.summary-text {
  margin-bottom: 10px;
  color: #606266;
}
</style>
