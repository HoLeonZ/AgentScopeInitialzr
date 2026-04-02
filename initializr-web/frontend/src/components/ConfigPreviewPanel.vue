<template>
  <div class="config-preview-panel">
    <div class="preview-header">
      <div class="header-left">
        <el-icon :size="20"><View /></el-icon>
        <span class="header-title">配置预览</span>
      </div>
    </div>

    <div class="preview-content">
      <div class="preview-layout">
        <!-- 左侧：已配置模块 -->
        <div class="left-panel">
          <div class="configured-modules">
            <div class="modules-header">
              <el-icon :size="18" color="#67C23A"><CircleCheck /></el-icon>
              <span class="header-title">已配置模块</span>
            </div>

            <div class="modules-list">
              <!-- 项目基础 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#409EFF"><Document /></el-icon>
                  <span class="module-title">项目基础</span>
                </div>
                <div v-if="isSectionComplete('basic')" class="module-content">
                  <div v-if="form.name" class="module-detail">
                    <span class="detail-label">名称:</span>
                    <span class="detail-value">{{ form.name }}</span>
                  </div>
                  <div v-if="form.agent_type" class="module-detail">
                    <span class="detail-label">类型:</span>
                    <span class="detail-value">{{ formatAgentType(form.agent_type) }}</span>
                  </div>
                  <div v-if="form.description" class="module-detail">
                    <span class="detail-label">描述:</span>
                    <span class="detail-value">{{ form.description }}</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：项目名称和描述</span>
                </div>
              </div>

              <!-- 模型配置 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#67C23A"><Connection /></el-icon>
                  <span class="module-title">模型配置</span>
                </div>
                <div v-if="isSectionComplete('model')" class="module-content">
                  <div v-if="form.model_provider" class="module-detail">
                    <span class="detail-label">Provider:</span>
                    <span class="detail-value">{{ form.model_provider }}</span>
                  </div>
                  <div v-if="form.model_config?.model" class="module-detail">
                    <span class="detail-label">Model:</span>
                    <span class="detail-value">{{ form.model_config.model }}</span>
                  </div>
                  <div v-if="form.model_config?.base_url" class="module-detail">
                    <span class="detail-label">API地址:</span>
                    <span class="detail-value">{{ form.model_config.base_url }}</span>
                  </div>
                  <div v-if="form.model_config?.temperature !== undefined" class="module-detail">
                    <span class="detail-label">Temperature:</span>
                    <span class="detail-value">{{ form.model_config.temperature }}</span>
                  </div>
                  <div v-if="form.model_config?.max_tokens" class="module-detail">
                    <span class="detail-label">Max Tokens:</span>
                    <span class="detail-value">{{ form.model_config.max_tokens }}</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：提供商、模型名称和API密钥</span>
                </div>
              </div>

              <!-- 记忆配置 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#E6A23C"><Memo /></el-icon>
                  <span class="module-title">记忆配置</span>
                </div>
                <div v-if="isSectionComplete('memory')" class="module-content">
                  <div v-if="form.enable_memory !== undefined" class="module-detail">
                    <span class="detail-label">短期记忆:</span>
                    <span class="detail-value">
                      {{ form.enable_memory ? (form.short_term_memory || 'in-memory') : '未启用' }}
                    </span>
                  </div>
                  <div v-if="form.long_term_memory" class="module-detail">
                    <span class="detail-label">长期记忆:</span>
                    <span class="detail-value">{{ form.long_term_memory }}</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：启用或禁用记忆功能</span>
                </div>
              </div>

              <!-- 知识库 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#409EFF"><Reading /></el-icon>
                  <span class="module-title">知识库配置</span>
                </div>
                <div v-if="isSectionComplete('knowledge')" class="module-content">
                  <div v-if="form.enable_knowledge !== undefined" class="module-detail">
                    <span class="detail-label">状态:</span>
                    <span class="detail-value">{{ form.enable_knowledge ? '已启用' : '未启用' }}</span>
                  </div>
                  <div v-if="form.knowledge_config?.type" class="module-detail">
                    <span class="detail-label">类型:</span>
                    <span class="detail-value">{{ form.knowledge_config.type }}</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：启用或禁用知识库</span>
                </div>
              </div>

              <!-- Skill配置 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#67C23A"><Star /></el-icon>
                  <span class="module-title">Skill配置</span>
                </div>
                <div v-if="isSectionComplete('skills')" class="module-content">
                  <div v-if="form.enable_skills !== undefined" class="module-detail">
                    <span class="detail-label">状态:</span>
                    <span class="detail-value">{{ form.enable_skills ? '已启用' : '未启用' }}</span>
                  </div>
                  <div v-if="form.skills && form.skills.length > 0" class="module-detail">
                    <span class="detail-label">技能数:</span>
                    <span class="detail-value">{{ form.skills.length }} 个</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：启用或禁用技能</span>
                </div>
              </div>

              <!-- 扩展功能 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#F56C6C"><Tools /></el-icon>
                  <span class="module-title">扩展功能</span>
                </div>
                <div v-if="isSectionComplete('extensions')" class="module-content">
                  <div v-if="form.enable_formatter !== undefined" class="module-detail">
                    <span class="detail-label">格式化:</span>
                    <span class="detail-value">{{ form.enable_formatter ? '已启用' : '未启用' }}</span>
                  </div>
                  <div v-if="form.enable_hooks !== undefined" class="module-detail">
                    <span class="detail-label">钩子:</span>
                    <span class="detail-value">{{ form.enable_hooks ? '已启用' : '未启用' }}</span>
                  </div>
                  <div v-if="form.enable_pipeline !== undefined" class="module-detail">
                    <span class="detail-label">管道:</span>
                    <span class="detail-value">{{ form.enable_pipeline ? '已启用' : '未启用' }}</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：启用格式化器、钩子或管道</span>
                </div>
              </div>

              <!-- 测试评估 -->
              <div class="module-item">
                <div class="module-header">
                  <el-icon :size="16" color="#909399"><DataAnalysis /></el-icon>
                  <span class="module-title">测试评估</span>
                </div>
                <div v-if="isSectionComplete('testing')" class="module-content">
                  <div v-if="form.generate_tests !== undefined" class="module-detail">
                    <span class="detail-label">测试:</span>
                    <span class="detail-value">{{ form.generate_tests ? '已启用' : '未启用' }}</span>
                  </div>
                  <div v-if="form.generate_evaluation !== undefined" class="module-detail">
                    <span class="detail-label">评估:</span>
                    <span class="detail-value">{{ form.generate_evaluation ? `已启用 (${form.evaluator_type})` : '未启用' }}</span>
                  </div>
                </div>
                <div v-else class="module-pending-hint">
                  <span>待配置：启用测试或评估功能</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：.env 预览 或 项目结构 -->
        <div class="right-panel">
          <div class="preview-tabs-header">
            <el-button-group size="small">
              <el-button
                :type="activeTab === 'env' ? 'primary' : ''"
                @click="activeTab = 'env'"
              >
                <el-icon><Document /></el-icon>
                .env 配置
              </el-button>
              <el-button
                :type="activeTab === 'structure' ? 'primary' : ''"
                @click="activeTab = 'structure'"
              >
                <el-icon><Folder /></el-icon>
                项目结构
              </el-button>
            </el-button-group>
          </div>

          <div class="right-content">
            <!-- .env 预览 -->
            <div v-show="activeTab === 'env'" class="preview-section">
              <div class="code-preview">
                <pre><code>{{ envPreview }}</code></pre>
              </div>
            </div>

            <!-- 项目结构 -->
            <div v-show="activeTab === 'structure'" class="preview-section">
              <div class="structure-preview">
                <pre><code>{{ structurePreview }}</code></pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  Document,
  Folder,
  DataAnalysis,
  CircleCheck,
  Clock,
  Connection,
  Memo,
  Tools,
  Reading,
  Star
} from '@element-plus/icons-vue'
import { useConfigStore } from '@/stores/config'

const configStore = useConfigStore()
const form = computed(() => configStore.form)
const activeTab = ref('env')

// 判断区块是否完成
const isSectionComplete = (sectionId: string): boolean => {
  switch (sectionId) {
    case 'basic':
      return !!(form.value.name && form.value.description)
    case 'model':
      return !!(form.value.model_provider && form.value.model_config?.model && form.value.model_config?.api_key)
    case 'memory':
      return form.value.enable_memory !== undefined
    case 'knowledge':
      return form.value.enable_knowledge !== undefined
    case 'skills':
      return form.value.enable_skills !== undefined
    case 'extensions':
      return form.value.enable_formatter !== undefined || form.value.enable_hooks !== undefined || form.value.enable_pipeline !== undefined
    case 'testing':
      return form.value.generate_tests !== undefined
    default:
      return false
  }
}

// 已完成的模块数量
const totalCompletedModules = computed(() => {
  const sections = ['basic', 'model', 'memory', 'knowledge', 'skills', 'extensions', 'testing']
  return sections.filter(id => isSectionComplete(id)).length
})

// 格式化 Agent 类型
const formatAgentType = (type: string) => {
  const typeMap: Record<string, string> = {
    'basic-agent': 'Basic Agent',
    'multi-agent': 'Multi Agent',
    'research-agent': 'Research Agent',
    'browser-agent': 'Browser Agent'
  }
  return typeMap[type] || type
}

// .env 预览
const envPreview = computed(() => {
  const provider = form.value.model_provider || 'openai'
  const apiKey = form.value.model_config?.api_key || 'your-api-key-here'

  const envVars: Record<string, string> = {
    openai: `# OpenAI Configuration
OPENAI_API_KEY=${apiKey}
LOG_LEVEL=INFO`,
    dashscope: `# DashScope Configuration
DASHSCOPE_API_KEY=${apiKey}
LOG_LEVEL=INFO`,
    gemini: `# Gemini Configuration
GEMINI_API_KEY=${apiKey}
LOG_LEVEL=INFO`,
    anthropic: `# Anthropic Configuration
ANTHROPIC_API_KEY=${apiKey}
LOG_LEVEL=INFO`,
    ollama: `# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO`
  }

  return envVars[provider] || envVars.openai
})

// 项目结构预览
const structurePreview = computed(() => {
  const packageName = (form.value.name || 'my-agent').replace(/-/g, '_')
  const hasTests = form.value.generate_tests
  const hasEval = form.value.generate_evaluation

  let structure = `${form.value.name || 'my-agent'}/
├── src/
│   └── ${packageName}/
│       ├── __init__.py
│       ├── main.py                 # 主入口（简化版）
│       ├── example_usage.py        # 使用示例
│       ├── agent_factory.py        # Agent 创建工厂
│       ├── agents/
│       │   └── agent.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   └── lifecycle.py
│       └── utils/
│           └── logging.py
├── tests/                          ${hasTests ? '# ✅ 已配置' : ''}`

  if (hasTests) {
    structure += `
│   ├── test_${packageName}.py
│   └── conftest.py`
  }

  if (hasEval) {
    structure += `
├── evaluation/                     # ✅ 评估模块
│   └── evaluators.py`
  }

  structure += `
├── .env                            # 环境变量
├── .env.example                    # 环境变量模板
├── requirements.txt
├── pyproject.toml
└── README.md                       # 项目文档`

  return structure
})
</script>

<style scoped>
.config-preview-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.preview-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  background: #fafafa;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.preview-content {
  flex: 1;
  overflow: hidden;
  padding: 20px;
}

/* 左右布局 */
.preview-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

/* 左侧面板 */
.left-panel {
  flex: 0 0 380px;
  overflow-y: auto;
  padding-right: 4px;
}

/* 右侧面板 */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.preview-tabs-header {
  display: flex;
  justify-content: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 16px;
}

.right-content {
  flex: 1;
  overflow: hidden;
}

/* 渐进式预览样式 */
.configured-modules {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 16px;
}

.modules-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e4e7ed;
}

.modules-header .header-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.modules-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.module-item {
  background: #ffffff;
  border-radius: 6px;
  padding: 12px;
  border-left: 3px solid #409EFF;
  transition: all 0.3s;
}

.module-pending-hint {
  padding-left: 24px;
  font-size: 12px;
  color: #909399;
  font-style: italic;
}

.pending-modules {
  padding: 12px;
  text-align: center;
  background: #f5f7fa;
  border-radius: 6px;
  margin-top: 8px;
}

.module-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.module-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  flex: 1;
}

.module-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-left: 24px;
}

.module-detail {
  display: flex;
  gap: 8px;
  font-size: 13px;
}

.detail-label {
  color: #909399;
  min-width: 80px;
}

.detail-value {
  color: #303133;
  font-weight: 500;
}

.empty-state {
  padding: 20px 0;
  text-align: center;
}

.preview-section {
  height: 100%;
}

.code-preview,
.structure-preview {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  overflow-y: auto;
  height: 100%;
  margin: 0;
}

pre {
  margin: 0;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  line-height: 1.6;
}

code {
  color: inherit;
}

/* 滚动条样式 */
.preview-content::-webkit-scrollbar,
.left-panel::-webkit-scrollbar,
.right-content::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.preview-content::-webkit-scrollbar-thumb,
.left-panel::-webkit-scrollbar-thumb,
.right-content::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 4px;
}

.preview-content::-webkit-scrollbar-thumb:hover,
.left-panel::-webkit-scrollbar-thumb:hover,
.right-content::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .preview-layout {
    flex-direction: column;
  }

  .left-panel {
    flex: 0 0 auto;
    max-height: 400px;
  }

  .right-panel {
    flex: 1;
  }
}
</style>
