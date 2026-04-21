<template>
  <div class="home">
    <div class="home-container">
      <!-- 头部区域 -->
      <div class="unified-header-card">
        <div class="header-background">
          <el-icon :size="36" color="#FFFFFF" class="header-icon"><Monitor /></el-icon>
          <div class="header-content">
            <h2 class="header-title">快速构建 AgentScope 智能体项目</h2>
            <p class="header-description">通过可视化配置界面，一键生成完整的 AgentScope 项目代码包。配置模型、知识库、记忆、工具链等核心组件，快速启动智能体开发。</p>
          </div>
          <el-tag type="primary" size="large" effect="dark">Web 工具</el-tag>
        </div>
      </div>

      <!-- 操作入口区 -->
      <div class="section-block">
        <el-row :gutter="16">
          <el-col :span="16">
            <el-card shadow="hover" class="action-card">
              <div class="action-content">
                <div class="action-text">
                  <div class="action-title">立即开始创建项目</div>
                  <div class="action-desc">配置参数 → 生成代码 → 下载使用，全程可视化操作</div>
                </div>
                <el-button type="primary" size="large" @click="startConfiguration">
                  <el-icon><Upload /></el-icon>
                  开始创建项目
                </el-button>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" class="offline-card">
              <div class="offline-content">
                <div class="offline-icon">
                  <el-icon :size="28" color="#E6A23C"><Download /></el-icon>
                </div>
                <div class="offline-text">
                  <div class="offline-title">离线环境安装</div>
                  <div class="offline-desc">运行 <code>setup-pip-source.sh</code>（Linux/Mac）或 <code>setup-pip-source.bat</code>（Windows）即可自动配置 pip 私服地址</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 功能特性 -->
      <div class="section-block">
        <div class="section-header">
          <el-icon :size="18" color="#409EFF"><Key /></el-icon>
          <span>核心配置</span>
        </div>
        <el-row :gutter="16">
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#409EFF"><Connection /></el-icon>
              <div class="feature-name">模型配置</div>
              <div class="feature-desc">DeepSeek / Qwen / DashScope 等多种模型可选</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#67C23A"><Box /></el-icon>
              <div class="feature-name">知识库配置</div>
              <div class="feature-desc">KBase / Qdrant 向量检索，支持 RAG 增强</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#E6A23C"><Cpu /></el-icon>
              <div class="feature-name">记忆配置</div>
              <div class="feature-desc">短时记忆 + 长期记忆，可选持久化存储</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#F56C6C"><Tools /></el-icon>
              <div class="feature-name">扩展配置</div>
              <div class="feature-desc">Hooks / Pipeline / Skill 完整扩展体系</div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 使用流程 -->
      <div class="section-block">
        <div class="section-header">
          <el-icon :size="18" color="#409EFF"><Guide /></el-icon>
          <span>使用流程</span>
        </div>
        <div class="steps-row">
          <div v-for="(step, i) in steps" :key="i" class="step-item">
            <div class="step-num-circle">{{ i + 1 }}</div>
            <div class="step-body">
              <div class="step-title">{{ step.title }}</div>
              <div class="step-desc">{{ step.desc }}</div>
            </div>
            <div v-if="i < 3" class="step-arrow">
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
        </div>
      </div>

      <!-- 开发指南 -->
      <div class="section-block">
        <div class="section-header">
          <el-icon :size="18" color="#67C23A"><Document /></el-icon>
          <span>生成代码后如何开发</span>
        </div>
        <el-row :gutter="16">
          <!-- 环境配置 -->
          <el-col :span="12">
            <el-card shadow="hover" class="guide-card">
              <template #header>
                <div class="card-header-row">
                  <el-icon :size="18" color="#409EFF"><Setting /></el-icon>
                  <span>配置环境</span>
                </div>
              </template>
              <div class="guide-item">
                <div class="guide-label">1. 复制环境变量模板</div>
                <div class="code-block">cp .env.example .env</div>
              </div>
              <div class="guide-item">
                <div class="guide-label">2. 编辑 .env 文件</div>
                <div class="code-block">
MODEL_NAME=deepseek-qwen-32b-NPU
API_KEY=your-api-key-here
BASE_URL=http://203.3.234.97:8082/v1
KBASE_URL=http://203.3.221.154:32734
                </div>
              </div>
              <div class="guide-item">
                <div class="guide-label">3. 安装依赖</div>
                <div class="code-block">pip install -r requirements.txt</div>
              </div>
            </el-card>
          </el-col>

          <!-- 运行项目 -->
          <el-col :span="12">
            <el-card shadow="hover" class="guide-card">
              <template #header>
                <div class="card-header-row">
                  <el-icon :size="18" color="#67C23A"><VideoPlay /></el-icon>
                  <span>运行项目</span>
                </div>
              </template>
              <div class="guide-item">
                <div class="guide-label">方式一：直接运行</div>
                <div class="code-block">python src/main.py</div>
              </div>
              <div class="guide-item">
                <div class="guide-label">方式二：Agentscope CLI</div>
                <div class="code-block">agentscope run src/main.py</div>
              </div>
              <div class="guide-item">
                <div class="guide-label">方式三：Docker 部署</div>
                <div class="code-block">docker build -t my-agent .
docker run -d -p 8000:8000 --env-file .env my-agent</div>
              </div>
            </el-card>
          </el-col>

          <!-- 定制开发 -->
          <el-col :span="12">
            <el-card shadow="hover" class="guide-card">
              <template #header>
                <div class="card-header-row">
                  <el-icon :size="18" color="#E6A23C"><Edit /></el-icon>
                  <span>定制开发</span>
                </div>
              </template>
              <div class="guide-item">
                <div class="guide-label">📁 项目结构</div>
                <div class="code-block">
my-agent/
├── src/
│   ├── main.py          # 入口文件
│   ├── model.py         # 模型配置
│   └── agent.py         # Agent 逻辑
├── config/settings.py   # 配置类
└── requirements.txt     # 依赖清单
                </div>
              </div>
              <div class="guide-item">
                <div class="guide-label">🔧 常用定制</div>
                <ul class="guide-list">
                  <li>修改 <code>src/model.py</code> 调整模型参数</li>
                  <li>编辑 <code>src/agent.py</code> 定制 Agent 行为</li>
                  <li>在 <code>src/tools/</code> 下添加自定义工具</li>
                  <li>修改 <code>config/settings.py</code> 调整配置类</li>
                </ul>
              </div>
            </el-card>
          </el-col>

          <!-- 测试部署 -->
          <el-col :span="12">
            <el-card shadow="hover" class="guide-card">
              <template #header>
                <div class="card-header-row">
                  <el-icon :size="18" color="#909399"><Coin /></el-icon>
                  <span>测试与发布</span>
                </div>
              </template>
              <div class="guide-item">
                <div class="guide-label">本地测试</div>
                <div class="code-block">pytest tests/ -v
python -m agentscope run src/main.py</div>
              </div>
              <div class="guide-item">
                <div class="guide-label">打包发布</div>
                <div class="code-block">python -m build
twine upload dist/*</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import {
  Monitor,
  Key,
  Connection,
  Box,
  Cpu,
  Tools,
  Guide,
  Document,
  Setting,
  VideoPlay,
  Edit,
  Coin,
  Upload,
  Download,
  ArrowRight,
} from '@element-plus/icons-vue'

const router = useRouter()

const startConfiguration = () => {
  router.push('/configure')
}

const steps = [
  { title: '配置项目参数', desc: '在向导中选择 Agent 类型、模型、知识库、记忆等配置项' },
  { title: '生成并下载代码', desc: '点击生成按钮，系统自动渲染模板并打包为 ZIP 文件供下载' },
  { title: '配置运行环境', desc: '复制 .env.example 为 .env，填入模型 API Key 等信息' },
  { title: '安装依赖并启动', desc: '执行 pip install 后，运行 python src/main.py 启动项目' },
]
</script>

<style scoped>
.home {
  height: 100%;
  overflow-y: auto;
  background: #f5f7fa;
}

.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 统一头部卡片 */
.unified-header-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-background {
  background: linear-gradient(135deg, #409EFF 0%, #53a8ff 100%);
  padding: 32px 32px 28px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  color: #ffffff;
}

.header-icon {
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.header-title {
  margin: 0 0 10px 0;
  font-size: 22px;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.3;
}

.header-description {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.88);
  line-height: 1.7;
}

/* 分区块 */
.section-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  padding: 0 4px;
}

/* 功能卡片 */
.feature-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: box-shadow 0.3s;
}

.feature-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.feature-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.feature-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

/* 步骤卡片 */
.steps-card {
  border-radius: 12px;
}

/* 横向步骤组 */
.steps-row {
  display: flex;
  align-items: center;
  background: #ffffff;
  border-radius: 12px;
  padding: 24px 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  gap: 0;
}

.step-item {
  display: flex;
  align-items: center;
  flex: 1;
  gap: 12px;
}

.step-num-circle {
  width: 40px;
  height: 40px;
  min-width: 40px;
  border-radius: 50%;
  background: #409EFF;
  color: #ffffff;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.35);
}

.step-body {
  flex: 1;
  min-width: 0;
}

.step-title {
  font-size: 14px;
  font-weight: 700;
  color: #303133;
  line-height: 1.4;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  white-space: normal;
}

.step-arrow {
  color: #409EFF;
  font-size: 18px;
  margin: 0 12px;
  flex-shrink: 0;
  opacity: 0.6;
}

:deep(.el-step__title) {
  font-size: 14px;
  font-weight: 600;
}

:deep(.el-step__description) {
  font-size: 12px;
}

/* 指南卡片 */
.guide-card {
  border-radius: 12px;
}

.card-header-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.guide-item {
  margin-bottom: 16px;
}

.guide-item:last-child {
  margin-bottom: 0;
}

.guide-label {
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 8px;
  line-height: 1.5;
}

.code-block {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 10px 14px;
  border-radius: 6px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 12px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-all;
}

.guide-list {
  margin: 0;
  padding-left: 20px;
  line-height: 2;
  color: #606266;
  font-size: 13px;
}

.guide-list code {
  background: #f5f7fa;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 12px;
  color: #409EFF;
}

/* 底部操作卡片 */
.action-card {
  border-radius: 12px;
}

.action-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.action-desc {
  font-size: 13px;
  color: #909399;
}

/* 离线环境卡片 */
.offline-card {
  border-radius: 12px;
}

.offline-content {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 4px 0;
}

.offline-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  background: #fdf6ec;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.offline-text {
  flex: 1;
}

.offline-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.offline-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

.offline-desc code {
  background: #f5f7fa;
  padding: 1px 4px;
  border-radius: 4px;
  font-size: 11px;
  color: #409EFF;
}

/* 提示框 */
.tips-alert {
  border-radius: 12px;
}

.tips-text {
  font-size: 13px;
  line-height: 1.7;
  color: #606266;
}

.tips-text code {
  background: rgba(64, 158, 255, 0.1);
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 12px;
  color: #409EFF;
}

/* Element Plus 覆盖 */
:deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-step__icon) {
  border: none;
  background: #f5f7fa;
}

:deep(.el-step__icon.is-text) {
  background: #409EFF;
  color: #fff;
  border: none;
}

:deep(.el-step__icon-inner) {
  font-weight: 600;
}

/* 响应式 */
@media (max-width: 900px) {
  .home-container {
    padding: 16px;
  }

  .header-background {
    flex-direction: column;
    text-align: center;
    padding: 24px 20px;
  }

  .action-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .feature-card {
    padding: 16px 12px;
  }

  .feature-name {
    font-size: 14px;
  }
}
</style>
