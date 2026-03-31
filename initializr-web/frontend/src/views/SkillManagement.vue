<template>
  <div class="skill-management">
    <el-container>
      <el-header>
        <h1>
          <el-icon><Collection /></el-icon>
          Skill 管理后台
        </h1>
      </el-header>

      <el-main>
        <!-- Upload Section -->
        <el-card class="upload-section" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>上传 Skill 包</span>
              <el-button type="primary" @click="showUploadDialog = true">
                <el-icon><Upload /></el-icon>
                上传新 Skill
              </el-button>
            </div>
          </template>

          <el-alert
            title="Skill 包要求"
            type="info"
            :closable="false"
            show-icon
          >
            <template #default>
              <ul>
                <li>必须是 ZIP 格式</li>
                <li>包含标准的 AgentScope skill 结构（SKILL.md 文件）</li>
                <li>SKILL.md 必须包含 YAML frontmatter（name, description, version）</li>
                <li>可以包含 scripts/、resources/、examples/ 目录</li>
              </ul>
            </template>
          </el-alert>
        </el-card>

        <!-- Skills List -->
        <el-card class="skills-list" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>已上传的 Skills ({{ filteredSkills.length }})</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索 skills..."
                style="width: 300px"
                clearable
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </template>

          <el-table
            :data="paginatedSkills"
            v-loading="loading"
            stripe
            style="width: 100%"
          >
            <el-table-column prop="name" label="Name" width="200">
              <template #default="{ row }">
                <div class="skill-name">
                  <el-tag size="small">{{ row.version }}</el-tag>
                  <strong>{{ row.name }}</strong>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="description" label="Description" show-overflow-tooltip />

            <el-table-column prop="tags" label="Tags" width="200">
              <template #default="{ row }">
                <el-tag
                  v-for="tag in row.tags"
                  :key="tag"
                  size="small"
                  style="margin-right: 5px"
                >
                  {{ tag }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column prop="uploaded_at" label="Uploaded" width="180">
              <template #default="{ row }">
                {{ formatDate(row.uploaded_at) }}
              </template>
            </el-table-column>

            <el-table-column label="Actions" width="150" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  @click="viewSkill(row)"
                  link
                >
                  查看
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="confirmDelete(row)"
                  link
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Pagination -->
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            :total="filteredSkills.length"
            layout="total, sizes, prev, pager, next, jumper"
            style="margin-top: 20px; justify-content: center"
          />
        </el-card>
      </el-main>
    </el-container>

    <!-- Upload Dialog -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传 Skill 包"
      width="500px"
    >
      <el-upload
        ref="uploadRef"
        class="upload-demo"
        drag
        action="#"
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
        accept=".zip"
        :file-list="fileList"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传 ZIP 文件，且不超过 10MB
          </div>
        </template>
      </el-upload>

      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button
          type="primary"
          @click="uploadSkill"
          :loading="uploading"
          :disabled="!selectedFile"
        >
          上传
        </el-button>
      </template>
    </el-dialog>

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
        <el-descriptions-item label="Size">
          {{ formatBytes(currentSkill.size_bytes) }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Collection,
  Upload,
  Search,
  UploadFilled
} from '@element-plus/icons-vue'
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

const loading = ref(false)
const skills = ref<Skill[]>([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const showUploadDialog = ref(false)
const showDetailDialog = ref(false)
const uploading = ref(false)
const selectedFile = ref<File | null>(null)
const fileList = ref<any[]>([])
const currentSkill = ref<Skill | null>(null)

const filteredSkills = computed(() => {
  if (!searchQuery.value) {
    return skills.value
  }
  const query = searchQuery.value.toLowerCase()
  return skills.value.filter(skill =>
    skill.name.toLowerCase().includes(query) ||
    skill.description.toLowerCase().includes(query) ||
    skill.tags.some(tag => tag.toLowerCase().includes(query))
  )
})

const paginatedSkills = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredSkills.value.slice(start, end)
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

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
  fileList.value = [file]
}

const uploadSkill = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择要上传的文件')
    return
  }

  uploading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await axios.post('/api/skills/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    ElMessage.success('Skill 上传成功！')
    showUploadDialog.value = false
    fileList.value = []
    selectedFile.value = null
    await fetchSkills()
  } catch (error: any) {
    ElMessage.error('上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploading.value = false
  }
}

const viewSkill = (skill: Skill) => {
  currentSkill.value = skill
  showDetailDialog.value = true
}

const confirmDelete = (skill: Skill) => {
  ElMessageBox.confirm(
    `确定要删除 skill "${skill.name}" 吗？此操作不可恢复。`,
    '确认删除',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await axios.delete(`/api/skills/${skill.skill_id}`)
      ElMessage.success('删除成功')
      await fetchSkills()
    } catch (error: any) {
      ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }).catch(() => {
    // User cancelled
  })
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const formatBytes = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

onMounted(() => {
  fetchSkills()
})
</script>

<style scoped>
.skill-management {
  padding: 20px;
}

.el-header {
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
}

.el-header h1 {
  font-size: 24px;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.upload-section {
  margin-bottom: 20px;
}

.skills-list {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.skill-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-demo {
  width: 100%;
}

.el-icon--upload {
  font-size: 67px;
  color: #409eff;
  margin: 20px 0;
}
</style>
