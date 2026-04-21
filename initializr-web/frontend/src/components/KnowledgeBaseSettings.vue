<template>
  <div class="knowledge-base-settings">
    <!-- 统一头部卡片 -->
    <div class="unified-header-card">
      <div class="header-background">
        <el-icon :size="32" color="#FFFFFF" class="header-icon"><Reading /></el-icon>
        <div class="header-content">
          <h2 class="header-title">知识库配置</h2>
          <p class="header-description">启用知识库以提供外部信息检索能力，配置向量数据库和检索参数</p>
        </div>
        <el-tag type="warning" size="large" effect="dark">可选配置</el-tag>
      </div>
    </div>

    <!-- 配置提示 -->
    <el-alert
      type="info"
      :closable="false"
      show-icon
      class="config-hint"
    >
      <template #default>
        <div class="hint-content">
          <div class="hint-title">💡 配置说明</div>
          <ul class="hint-list">
            <li><strong>KBase：</strong>企业知识库服务，只需提供服务地址</li>
            <li><strong>Qdrant：</strong>高性能向量数据库，需配置连接信息和参数</li>
            <li>知识库通过向量相似度搜索为智能体提供外部知识检索能力</li>
          </ul>
        </div>
      </template>
    </el-alert>

    <!-- 详细配置区块 -->
    <div class="knowledge-sections">
      <!-- 启用开关 -->
      <el-card class="knowledge-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon :size="20" color="#409EFF"><Reading /></el-icon>
              <span class="card-title">启用知识库</span>
            </div>
            <el-switch
              v-model="localForm.enable_knowledge"
              size="large"
              @change="updateField('enable_knowledge', $event)"
            />
          </div>
        </template>

        <template v-if="localForm.enable_knowledge">
          <el-alert
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 24px"
          >
            知识库通过向量相似度搜索为智能体提供外部知识检索能力。
          </el-alert>

          <!-- 知识库类型选择 -->
          <el-divider content-position="left">
            <el-icon><Setting /></el-icon>
            知识库类型
          </el-divider>

          <el-form-item label="知识库类型">
            <el-select
              v-model="knowledgeConfig.type"
              placeholder="选择知识库类型"
              @change="updateKnowledgeConfig"
              style="width: 100%"
            >
              <el-option
                value="kbase"
                label="KBase - 企业知识库服务"
              >
                <div class="option-content">
                  <div class="option-label">KBase</div>
                  <div class="option-desc">企业知识库服务</div>
                </div>
              </el-option>
              <el-option
                value="qdrant"
                label="Qdrant - 高性能向量数据库"
              >
                <div class="option-content">
                  <div class="option-label">Qdrant</div>
                  <div class="option-desc">高性能向量数据库</div>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <!-- KBase 配置 -->
          <template v-if="knowledgeConfig.type === 'kbase'">
            <el-divider content-position="left">
              <el-icon><Setting /></el-icon>
              KBase 配置
            </el-divider>

            <el-form-item label="服务地址">
              <el-input
                v-model="knowledgeConfig.kbase_url"
                placeholder="http://203.3.221.154:32734"
                @input="updateKnowledgeConfig"
              />
              <span class="hint">KBase服务地址</span>
            </el-form-item>
          </template>

          <!-- Qdrant 配置 -->
          <template v-if="knowledgeConfig.type === 'qdrant'">
            <el-divider content-position="left">
              <el-icon><Setting /></el-icon>
              Qdrant 配置
            </el-divider>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="主机地址">
                  <el-input
                    v-model="knowledgeConfig.qdrant_host"
                    placeholder="localhost"
                    @input="updateKnowledgeConfig"
                  />
                  <span class="hint">Qdrant服务器地址</span>
                </el-form-item>
              </el-col>

              <el-col :span="12">
                <el-form-item label="端口">
                  <div style="display: block">
                    <el-input-number
                      v-model="knowledgeConfig.qdrant_port"
                      :min="1"
                      :max="65535"
                      placeholder="6333"
                      style="width: 100%"
                      @change="updateKnowledgeConfig"
                    />
                    <span class="hint">Qdrant服务器端口</span>
                  </div>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="集合名称">
                  <el-input
                    v-model="knowledgeConfig.collection_name"
                    placeholder="agent_knowledge"
                    @input="updateKnowledgeConfig"
                  />
                  <span class="hint">向量集合名称</span>
                </el-form-item>
              </el-col>

              <el-col :span="12">
                <el-form-item label="嵌入模型">
                  <el-input
                    v-model="knowledgeConfig.embedding_model"
                    placeholder="text-embedding-ada-002"
                    @input="updateKnowledgeConfig"
                  />
                  <span class="hint">向量嵌入模型</span>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="向量维度" label-width="120px">
                  <el-input-number
                    v-model="knowledgeConfig.dimension"
                    :min="128"
                    :max="3072"
                    :step="128"
                    style="width: 100%"
                    @change="updateKnowledgeConfig"
                  />
                  <span class="hint">向量维度</span>
                </el-form-item>
              </el-col>
            </el-row>
          </template>

          <!-- 检索设置 -->
          <el-divider content-position="left">
            <el-icon><Operation /></el-icon>
            检索设置
          </el-divider>

          <el-form-item label="返回数量" label-width="120px">
            <div style="display: block">
              <el-input-number
                v-model="knowledgeConfig.top_k"
                :min="1"
                :max="20"
                style="width: 200px"
                @change="updateKnowledgeConfig"
              />
              <span class="hint">返回最相关的 K 个结果</span>
            </div>
          </el-form-item>

          <el-form-item label="相似度阈值" label-width="120px">
            <div style="display: block">
              <el-input-number
                v-model="knowledgeConfig.similarity_threshold"
                :min="0"
                :max="1"
                :step="0.1"
                :precision="1"
                style="width: 200px"
                @change="updateKnowledgeConfig"
              />
              <span class="hint">相似度阈值</span>
            </div>
          </el-form-item>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import {
  Reading,
  Setting,
  Operation
} from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

// 本地表单状态
const localForm = reactive({
  enable_knowledge: form.value.enable_knowledge ?? false,
})

// 知识库配置
const knowledgeConfig = reactive({
  type: form.value.knowledge_config?.type || 'kbase',
  // KBase配置
  kbase_url: form.value.knowledge_config?.kbase_url || 'http://203.3.221.154:32734',
  // Qdrant配置
  qdrant_host: form.value.knowledge_config?.qdrant_host || 'localhost',
  qdrant_port: form.value.knowledge_config?.qdrant_port || 6333,
  collection_name: form.value.knowledge_config?.collection_name || 'agent_knowledge',
  embedding_model: form.value.knowledge_config?.embedding_model || 'text-embedding-ada-002',
  dimension: form.value.knowledge_config?.dimension || 1536,
  // 检索配置
  top_k: form.value.knowledge_config?.top_k || 5,
  similarity_threshold: form.value.knowledge_config?.similarity_threshold || 0.7,
})

// 更新字段到存储
const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
  // 同步 enable_knowledge <-> enable_rag（共用同一份配置）
  if (field === 'enable_knowledge') {
    configStore.setField('enable_rag' as any, value)
  }
}

// 更新知识库配置
const updateKnowledgeConfig = () => {
  configStore.setField('knowledge_config', { ...knowledgeConfig })
  // 同步到 rag_config（后端用 enable_rag + rag_config 判断是否生成 rag.py）
  configStore.setField('rag_config' as any, { ...knowledgeConfig })
}
</script>

<style scoped>
.knowledge-base-settings {
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

/* 分（Detailed Configuration）样式 */
.knowledge-sections {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.knowledge-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}

.hint {
  font-size: 0.9em;
  color: #909399;
  display: block;
  margin-top: 8px;
  line-height: 1.6;
}

/* Option Content for Select */
.option-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 4px 0;
}

.option-label {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.option-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

/* Option Items */
.option-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-label {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.option-desc {
  font-size: 13px;
  color: #909399;
}

:deep(.el-card__header) {
  padding: 20px 24px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 28px 24px;
}

:deep(.el-divider__text) {
  font-size: 1em;
  font-weight: 600;
  color: #409EFF;
}

:deep(.el-divider--horizontal) {
  margin: 32px 0 24px 0;
}

:deep(.el-form-item) {
  margin-bottom: 28px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  font-size: 15px;
  color: #303133;
}

:deep(.el-input__inner),
:deep(.el-input-number__input) {
  font-size: 14px;
}

/* Select Option Styles */
:deep(.el-select-dropdown__item) {
  padding: 8px 12px;
  height: auto;
}

/* Upload Area */
:deep(.el-upload-dragger) {
  width: 100%;
  min-height: 220px;
  padding: 40px 20px;
}

:deep(.el-upload__text) {
  font-size: 15px;
}

:deep(.el-upload__tip) {
  font-size: 14px;
  margin-top: 12px;
}

/* Slider */
:deep(.el-slider) {
  margin-top: 16px;
}

:deep(.el-slider__runway) {
  height: 8px;
}

:deep(.el-slider__button) {
  width: 20px;
  height: 20px;
}

/* Checkbox Group */
:deep(.el-checkbox-group) {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

:deep(.el-checkbox) {
  margin-right: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .knowledge-sections {
    gap: 16px;
  }

  .knowledge-card {
    margin: 0;
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
