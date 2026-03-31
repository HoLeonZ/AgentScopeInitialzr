# AgentScope 扩展点配置指南

## 概述

AgentScope Initializr 支持丰富的扩展点配置，包括 Model、Memory、Toolkit、Formatter、Skills、RAG 和 Pipeline 等。

## 快速开始

### 启动 Web 服务

```bash
# 使用 Docker（推荐）
docker-compose up

# 或手动启动
pip install -e ".[web]"
agentscope-web

# 访问
# 前端: http://localhost:555
# 后端: http://localhost:8000/docs
```

### 配置项目

访问 Web 界面，按照 4 步向导配置：

1. **Basic Settings** - 项目名称、模板选择
2. **Model & Memory** - 模型提供商、内存配置
3. **Extensions** - 工具、格式化器、Hooks、Skills、RAG、Pipeline
4. **Testing & Evaluation** - 测试和评估配置

## 扩展点说明

### Memory Configuration
- **短期内存**: in-memory, redis, oceanbase
- **长期内存**: mem0, zep, oceanbase, none

### Tools Configuration
- Execute Python Code
- Execute Shell Command
- Web Search (Tavily)
- Browser Automation

### Formatter Configuration
- DashScopeChatFormatter
- OpenAIChatFormatter

### Hooks Configuration
- Pre Reply - Agent 回复前执行
- Post Reply - Agent 回复后执行
- Pre Observe - Agent 观察前执行
- Post Observe - Agent 观察后执行

### Skills Configuration
- 预设技能: coding, writing, analysis, research, math, translation
- 支持自定义技能

### RAG Configuration
- 向量存储: Chroma, FAISS, Pinecone
- 嵌入模型: openai:text-embedding-ada-002
- 分块配置: Chunk Size, Chunk Overlap

### Pipeline Configuration
- 类型: Sequential, Parallel, Conditional
- 错误处理: Stop on Error, Continue on Error, Retry

## 使用生成的项目

```bash
# 解压并进入项目
unzip your-project.zip
cd your-project

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 添加 API 密钥

# 运行
python main.py
```

## 版本历史

### v0.2.0 (2026-03-31)
- 实现完整的扩展点配置 UI
- 支持 Memory、Tools、Formatter、Hooks 配置
- 支持 Skills、RAG、Pipeline 配置
- 实现完整的后端转换和代码生成
