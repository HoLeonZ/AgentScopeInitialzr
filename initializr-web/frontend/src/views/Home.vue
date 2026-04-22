<template>
  <div class="home">
    <div class="home-container">
      <!-- 头部区域 -->
      <div class="home-header">
        <div class="header-title-row">
          <el-icon :size="32" class="header-icon"><Monitor /></el-icon>
          <h1 class="header-title">快速构建智能体项目</h1>
        </div>
        <p class="header-description">通过可视化配置界面，一键生成完整的智能体项目代码包</p>
      </div>

      <!-- 操作入口区 -->
      <div class="section-block">
        <el-row :gutter="16">
          <el-col :span="16">
            <div class="action-card" @click="startConfiguration">
              <div class="action-bg"></div>
              <div class="action-content">
                <div class="action-left">
                  <div class="action-icon">
                    <el-icon :size="28"><Upload /></el-icon>
                  </div>
                  <div class="action-text">
                    <div class="action-title">立即开始创建项目</div>
                    <div class="action-desc">配置参数 → 生成代码 → 下载使用，全程可视化操作</div>
                  </div>
                </div>
                <div class="action-btn">
                  <span>开始创建</span>
                  <el-icon><ArrowRight /></el-icon>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="offline-card">
              <div class="offline-content">
                <div class="offline-icon">
                  <el-icon :size="20"><Download /></el-icon>
                </div>
                <div class="offline-text">
                  <div class="offline-title">离线环境安装</div>
                  <div class="offline-desc">运行 <code>setup-pip-source.sh</code>（Linux/Mac）或 <code>setup-pip-source.bat</code>（Windows）即可自动配置</div>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 功能特性 -->
      <div class="section-block">
        <div class="section-header">
          <el-icon :size="18" color="#667eea"><Key /></el-icon>
          <span>核心配置</span>
        </div>
        <el-row :gutter="16" class="feature-row">
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#667eea"><Connection /></el-icon>
              <div class="feature-name">模型配置</div>
              <div class="feature-desc">DeepSeek / Qwen 等多种模型可选</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#764ba2"><Box /></el-icon>
              <div class="feature-name">知识库配置</div>
              <div class="feature-desc">KBase / Qdrant 向量检索，支持 RAG 增强</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#667eea"><Cpu /></el-icon>
              <div class="feature-name">记忆配置</div>
              <div class="feature-desc">短时记忆 + 长期记忆，可选持久化存储</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="feature-card">
              <el-icon :size="28" color="#764ba2"><Tools /></el-icon>
              <div class="feature-name">扩展配置</div>
              <div class="feature-desc">Hooks / Pipeline / Skill 完整扩展体系</div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 使用流程 -->
      <div class="section-block">
        <div class="section-header">
          <el-icon :size="18" color="#667eea"><Guide /></el-icon>
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
          <el-icon :size="18" color="#667eea"><Document /></el-icon>
          <span>生成代码后如何开发</span>
        </div>
        <el-row :gutter="16" class="guide-row">
          <!-- 环境配置 -->
          <el-col :span="12">
            <div class="guide-card-col">
              <el-card shadow="hover" class="guide-card">
                <template #header>
                  <div class="card-header-row">
                    <el-icon :size="18" color="#667eea"><Setting /></el-icon>
                    <span>配置环境</span>
                  </div>
                </template>
                <div class="guide-item">
                  <div class="guide-label">1. 复制环境变量模板</div>
                  <div class="code-block">cp .env.example .env</div>
                </div>
                <div class="guide-item">
                  <div class="guide-label">2. 编辑 .env 文件</div>
                  <div class="code-block">MODEL_NAME=deepseek-qwen-32b-NPU
API_KEY=your-api-key-here
BASE_URL=http://203.3.234.97:8082/v1
KBASE_URL=http://203.4.129.4:6201/http_rag_kbase</div>
                </div>
                <div class="guide-item">
                  <div class="guide-label">3. 安装依赖</div>
                  <div class="code-block">pip install -r requirements.txt</div>
                </div>
              </el-card>
            </div>
          </el-col>

          <!-- 运行项目 -->
          <el-col :span="12">
            <div class="guide-card-col">
              <el-card shadow="hover" class="guide-card">
                <template #header>
                  <div class="card-header-row">
                    <el-icon :size="18" color="#764ba2"><VideoPlay /></el-icon>
                    <span>运行项目</span>
                  </div>
                </template>
                <div class="guide-item">
                  <div class="guide-label">方式一：直接运行</div>
                  <div class="code-block">python src/main.py</div>
                </div>
                <div class="guide-item">
                  <div class="guide-label">方式二：Docker 部署</div>
                  <div class="code-block">docker build -t my-agent .<br>docker run -d -p 8000:8000 --env-file .env my-agent</div>
                </div>
              </el-card>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="16" class="guide-row">
          <!-- 定制开发 -->
          <el-col :span="12">
            <div class="guide-card-col">
              <el-card shadow="hover" class="guide-card">
                <template #header>
                  <div class="card-header-row">
                    <el-icon :size="18" color="#E6A23C"><Edit /></el-icon>
                    <span>定制开发</span>
                  </div>
                </template>
                <div class="guide-item">
                  <div class="guide-label">📁 项目结构</div>
                  <div class="code-block">my-agent/<br>├── src/<br>│   ├── main.py      # 入口文件<br>│   ├── model.py     # 模型配置<br>│   └── agent.py     # Agent 逻辑<br>├── config/<br>│   └── settings.py  # 配置类<br>└── requirements.txt  # 依赖清单</div>
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
            </div>
          </el-col>

          <!-- 测试部署 -->
          <el-col :span="12">
            <div class="guide-card-col">
              <el-card shadow="hover" class="guide-card">
                <template #header>
                  <div class="card-header-row">
                    <el-icon :size="18" color="#909399"><Coin /></el-icon>
                    <span>效果评测</span>
                  </div>
                </template>
                <div class="guide-item">
                  <div class="guide-label">1. 准备评测数据</div>
                  <div class="code-block">上传 CSV 文件<br>（包含 question, answer, context, reference 列）</div>
                </div>
                <div class="guide-item">
                  <div class="guide-label">2. 启动评测</div>
                  <div class="code-block">python -m ragas_eval</div>
                </div>
                <div class="guide-item">
                  <div class="guide-label">3. 查看评测结果</div>
                  <div class="code-block">Faithfulness / Answer Relevancy<br>Context Precision / Context Recall<br>等多项指标</div>
                </div>
              </el-card>
            </div>
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

/* 首页头部 */
.home-header {
  padding: 8px 4px 20px 4px;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.header-icon {
  color: #667eea;
}

.header-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1.3;
}

.header-description {
  margin: 0;
  padding-left: 46px;
  font-size: 15px;
  color: #909399;
  line-height: 1.6;
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
.feature-row {
  display: flex;
  align-items: stretch;
}

.feature-row .el-col {
  display: flex;
  flex-direction: column;
}

.feature-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  flex: 1;
  border: 1px solid transparent;
}

.feature-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
  transform: translateY(-2px);
}

.feature-name {
  font-size: 14px;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
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
  color: #667eea;
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
.guide-row {
  display: flex;
  align-items: stretch;
}

.guide-row .el-col {
  display: flex;
  flex-direction: column;
}

.guide-card-col {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.guide-card {
  border-radius: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.guide-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
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
  white-space: pre-line;
  overflow-x: auto;
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
  color: #667eea;
}

/* 底部操作卡片 - 主按钮风格 */
.action-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.3);
  transition: all 0.3s ease;
  min-height: 90px;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(64, 158, 255, 0.4);
}

.action-bg {
  display: none;
}

.action-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  min-height: 90px;
}

.action-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.action-icon {
  width: 44px;
  height: 44px;
  min-width: 44px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.action-text {
  flex: 1;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.action-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.5;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: #fff;
  color: #409EFF;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.action-card:hover .action-btn {
  transform: translateX(4px);
}

.action-arrow {
  display: none;
}

/* 离线环境卡片 - 提示风格 */
.offline-card {
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  border: 1px solid #ebeef5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  min-height: 90px;
}

.offline-card:hover {
  border-color: #E6A23C;
  box-shadow: 0 4px 12px rgba(230, 162, 60, 0.15);
}

.offline-bg {
  display: none;
}

.offline-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  min-height: 90px;
}

.offline-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  background: #fdf6ec;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #E6A23C;
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
  line-height: 1.4;
}

.offline-desc code {
  background: #fdf6ec;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 11px;
  color: #E6A23C;
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

  .action-left {
    flex-direction: column;
    gap: 8px;
  }

  .action-btn {
    display: none;
  }
}

@media (max-width: 768px) {
  .header-title {
    font-size: 22px;
  }

  .header-description {
    padding-left: 0;
    font-size: 14px;
  }

  .feature-card {
    padding: 16px 12px;
  }

  .feature-name {
    font-size: 14px;
  }

  .action-content,
  .offline-content {
    padding: 16px 20px;
    min-height: 80px;
  }
}
</style>
