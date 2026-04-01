# AgentScope Initializr

> 快速生成基于 AgentScope 的 AI Agent 项目的脚手架工具

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ 特性

- 🚀 **4步配置向导** - 简单直观的 Web 界面
- 🎯 **多种模板** - Basic、Multi-Agent、Research、Browser
- 🔧 **丰富扩展点** - Model、Memory、Tools、Formatter、Skills、RAG、Pipeline
- 📦 **一键生成** - 自动生成完整项目结构
- 🧪 **测试支持** - 自动生成测试和评估模块
- 📱 **实时预览** - 配置时实时预览生成的代码

## 🎯 快速开始

### 使用 Docker（推荐）

```bash
git clone https://github.com/your-org/agentscope-initializr.git
cd agentscope-initializr
docker-compose up
```

访问 http://localhost:555 开始配置项目。

### 使用 Python

```bash
# 安装
pip install agentscope-initializr[web]

# 启动 Web 服务
agentscope-web

# 或使用 CLI
agentscope-init my-agent --template basic
```

详细说明请查看 [快速开始](QUICKSTART.md)。

## 📚 文档

- **[扩展点配置指南](docs/extensions.md)** - 完整的扩展点配置说明
- **[快速开始](QUICKSTART.md)** - 快速上手指南
- **[架构文档](docs/architecture.md)** - 系统架构说明
- **[API 参考](docs/api-reference.md)** - RESTful API 文档
- **[部署指南](docs/deployment-guide.md)** - 部署和安装说明

更多文档请查看 [docs/](docs/)。

## 🎨 支持的扩展点

| 扩展点 | 说明 |
|--------|------|
| **Model** | OpenAI、DashScope、Gemini、Anthropic、Ollama |
| **Memory** | In-Memory、Redis、Mem0、Zep、OceanBase |
| **Tools** | Python 执行、Shell 命令、Web 搜索、浏览器自动化 |
| **Formatter** | OpenAI、DashScope 格式化器 |
| **Skills** | Coding、Writing、Analysis、Research、Math、Translation |
| **RAG** | Chroma、FAISS、Pinecone 向量存储 |
| **Pipeline** | Sequential、Parallel、Conditional 流水线 |

## 🔧 开发

### 环境要求

- Python 3.11+
- Node.js 16+
- npm 或 yarn

### 克隆仓库

```bash
git clone https://github.com/your-org/agentscope-initializr.git
cd agentscope-initializr
```

### 后端启动

```bash
# 进入后端目录
cd initializr-web

# 安装依赖（推荐使用虚拟环境）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# 启动后端服务（运行在 http://localhost:8000）
python -m initializr_web.main
# 或安装后使用命令
agentscope-web
```

### 前端启动

```bash
# 进入前端目录
cd initializr-web/frontend

# 安装依赖
npm install

# 启动开发服务器（运行在 http://localhost:5173）
npm run dev

# 构建生产版本
npm run build

# 类型检查
npm run type-check
```

### 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 📝 变更日志

查看 [CHANGELOG.md](docs/changelog.md) 了解版本变更。

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- [AgentScope](https://github.com/modelscope/agentscope) - AI Agent 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
