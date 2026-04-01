<template>
  <div class="config-preview-panel">
    <div class="preview-header">
      <div class="header-left">
        <el-icon :size="20"><View /></el-icon>
        <span class="header-title">配置预览</span>
      </div>
      <div class="header-right">
        <el-button-group size="small">
          <el-button
            :type="activeTab === 'env' ? 'primary' : ''"
            @click="activeTab = 'env'"
          >
            <el-icon><Document /></el-icon>
            .env
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
    </div>

    <div class="preview-content">
      <!-- 已配置模块摘要 -->
      <div class="configured-modules">
        <div class="modules-header">
          <el-icon :size="18" color="#67C23A"><CircleCheck /></el-icon>
          <span class="header-title">已配置模块</span>
        </div>

        <div class="modules-list">
          <!-- 项目基础 -->
          <div
            v-if="isSectionComplete('basic')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#409EFF"><Document /></el-icon>
              <span class="module-title">项目基础</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
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
          </div>

          <!-- 模型配置 -->
          <div
            v-if="isSectionComplete('model')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#67C23A"><Connection /></el-icon>
              <span class="module-title">模型配置</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
              <div v-if="form.model_provider" class="module-detail">
                <span class="detail-label">Provider:</span>
                <span class="detail-value">{{ form.model_provider }}</span>
              </div>
              <div v-if="form.model_config?.model" class="module-detail">
                <span class="detail-label">Model:</span>
                <span class="detail-value">{{ form.model_config.model }}</span>
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
          </div>

          <!-- 记忆配置 -->
          <div
            v-if="isSectionComplete('memory')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#E6A23C"><Memo /></el-icon>
              <span class="module-title">记忆配置</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
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
          </div>

          <!-- 知识库 -->
          <div
            v-if="isSectionComplete('knowledge')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#409EFF"><Reading /></el-icon>
              <span class="module-title">知识库</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
              <div v-if="form.enable_knowledge !== undefined" class="module-detail">
                <span class="detail-label">状态:</span>
                <span class="detail-value">{{ form.enable_knowledge ? '已启用' : '未启用' }}</span>
              </div>
              <div v-if="form.knowledge_config?.type" class="module-detail">
                <span class="detail-label">类型:</span>
                <span class="detail-value">{{ form.knowledge_config.type }}</span>
              </div>
            </div>
          </div>

          <!-- Skill配置 -->
          <div
            v-if="isSectionComplete('skills')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#67C23A"><Star /></el-icon>
              <span class="module-title">Skill配置</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
              <div v-if="form.enable_skills !== undefined" class="module-detail">
                <span class="detail-label">状态:</span>
                <span class="detail-value">{{ form.enable_skills ? '已启用' : '未启用' }}</span>
              </div>
              <div v-if="form.skills && form.skills.length > 0" class="module-detail">
                <span class="detail-label">技能数:</span>
                <span class="detail-value">{{ form.skills.length }} 个</span>
              </div>
            </div>
          </div>

          <!-- 扩展功能 -->
          <div
            v-if="isSectionComplete('extensions')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#F56C6C"><Tools /></el-icon>
              <span class="module-title">扩展功能</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
              <div v-if="form.enable_tools !== undefined" class="module-detail">
                <span class="detail-label">工具:</span>
                <span class="detail-value">{{ form.enable_tools ? `已启用 (${form.tools?.length || 0}个)` : '未启用' }}</span>
              </div>
              <div v-if="form.enable_formatter !== undefined" class="module-detail">
                <span class="detail-label">格式化:</span>
                <span class="detail-value">{{ form.enable_formatter ? '已启用' : '未启用' }}</span>
              </div>
            </div>
          </div>

          <!-- 测试评估 -->
          <div
            v-if="isSectionComplete('testing')"
            class="module-item"
          >
            <div class="module-header">
              <el-icon :size="16" color="#909399"><DataAnalysis /></el-icon>
              <span class="module-title">测试评估</span>
              <el-icon color="#67C23A" :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="module-content">
              <div v-if="form.generate_tests !== undefined" class="module-detail">
                <span class="detail-label">测试:</span>
                <span class="detail-value">{{ form.generate_tests ? '已启用' : '未启用' }}</span>
              </div>
              <div v-if="form.generate_evaluation !== undefined" class="module-detail">
                <span class="detail-label">评估:</span>
                <span class="detail-value">{{ form.generate_evaluation ? `已启用 (${form.evaluator_type})` : '未启用' }}</span>
              </div>
            </div>
          </div>

          <!-- 提示：未配置的模块 -->
          <div v-if="totalCompletedModules === 0" class="empty-state">
            <el-empty
              description="开始配置以查看模块摘要"
              :image-size="80"
            />
          </div>

          <!-- 未配置模块提示 -->
          <div v-else-if="totalCompletedModules < 7" class="pending-modules">
            <el-text size="small" type="info">
              <el-icon><Clock /></el-icon>
              还有 {{ 7 - totalCompletedModules }} 个模块未配置
            </el-text>
          </div>
        </div>
      </div>

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

    <div class="preview-footer">
      <div class="footer-left">
        <el-text size="small" type="info">
          <el-icon><InfoFilled /></el-icon>
          预览实时更新，配置完成后点击"生成项目"
        </el-text>
      </div>
      <div class="footer-right">
        <el-button size="small" @click="handleCopy">
          <el-icon><CopyDocument /></el-icon>
          复制
        </el-button>
        <el-button size="small" @click="handleDownload">
          <el-icon><Download /></el-icon>
          下载预览
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Document,
  Folder,
  DataAnalysis,
  InfoFilled,
  CopyDocument,
  Download,
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
      return form.value.enable_tools !== undefined || form.value.enable_formatter !== undefined
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

// 代码预览
const agentCodePreview = computed(() => {
  const packageName = (form.value.name || 'my-agent').replace(/-/g, '_')

  let code = `# Main entry point for ${form.value.name || 'my-agent'}
# This module follows Single Responsibility Principle

import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from ${packageName}.config import settings
from ${packageName}.config.lifecycle import ApplicationLifecycle
from ${packageName}.agent_factory import create_agent

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    log_dir=settings.LOG_DIR,
)

async def main():
    """Main entry point - demonstrates basic agent usage."""
    try:
        # Initialize application lifecycle
        ApplicationLifecycle.initialize()
        logger.info("Application lifecycle initialized")

        # Create agent (delegated to agent_factory)
        agent = create_agent(
            name="${form.value.name || 'my-agent'}",
            sys_prompt=settings.SYSTEM_PROMPT
        )
        logger.info("Agent created successfully")

        # Example usage
        print(f"🤖 Agent '${form.value.name || 'my-agent'}' is ready!")
        print(f"   See example_usage.py for more examples\\n")

        # Simple example
        response = await agent("Hello! Please introduce yourself.")
        print(f"Agent: {response}")
        logger.info("Example interaction completed")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        ApplicationLifecycle.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n\\n👋 Interrupted. Goodbye!")
        sys.exit(0)
`

  return code
})

// config.json 预览
const configJsonPreview = computed(() => {
  const config: any = {
    model: {
      config_name: form.value.model_config?.model || 'gpt-4',
      temperature: form.value.model_config?.temperature ?? 0.7,
      max_tokens: form.value.model_config?.max_tokens ?? 2000
    }
  }

  if (form.value.enable_memory && form.value.short_term_memory) {
    config.memory = {
      type: form.value.short_term_memory
    }
  }

  return JSON.stringify(config, null, 2)
})

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

// 复制功能
const handleCopy = () => {
  let content = ''
  switch (activeTab.value) {
    case 'code':
      content = agentCodePreview.value
      break
    case 'config':
      content = configJsonPreview.value
      break
    case 'env':
      content = envPreview.value
      break
    case 'structure':
      content = structurePreview.value
      break
  }

  navigator.clipboard.writeText(content).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

// 下载预览功能
const handleDownload = () => {
  let content = ''
  let filename = ''

  switch (activeTab.value) {
    case 'code':
      content = agentCodePreview.value
      filename = 'main.py'
      break
    case 'config':
      content = configJsonPreview.value
      filename = 'config.json'
      break
    case 'env':
      content = envPreview.value
      filename = '.env'
      break
    case 'structure':
      content = structurePreview.value
      filename = 'structure.txt'
      break
  }

  const blob = new Blob([content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)

  ElMessage.success(`已下载 ${filename}`)
}
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
  justify-content: space-between;
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
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.header-title {
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
  border-left: 3px solid #67c23a;
  transition: all 0.3s;
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

.preview-footer {
  padding: 12px 20px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
}

.generation-notes {
  margin: 10px 0 0 0;
  padding-left: 20px;
}

.generation-notes li {
  margin: 6px 0;
  line-height: 1.6;
}

code.inline-code {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  color: #409eff;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
}

/* 滚动条样式 */
.preview-content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.preview-content::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 4px;
}

.preview-content::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}
</style>
