# AgentScope Initializr - 方案A升级指南

## 🎯 升级概述

我们已成功将AgentScope Initializr升级为采用业界标准的**src/布局**，与主流agent框架（如CrewAI、LangChain）的目录格式对齐。

## 📊 新旧目录结构对比

### 📁 旧版布局 (Lightweight)
```bash
my-agent/
├── my_agent/              # Python package
│   ├── __init__.py
│   ├── agents/           # Agent implementations
│   ├── tools/            # Custom tools
│   └── config/           # Configuration
├── tests/                # Tests
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

### 📁 新版布局 (Standard - 推荐) ⭐
```bash
my-agent/
├── src/
│   └── my_agent/              # Main package
│       ├── __init__.py
│       ├── agents/           # Agent implementations
│       │   ├── __init__.py
│       │   └── react_agent.py
│       ├── tools/            # Custom tools
│       │   ├── __init__.py
│       │   └── custom_tools.py
│       ├── prompts/          # Prompt templates ✨新增
│       │   ├── __init__.py
│       │   └── system_prompts.py
│       ├── config/           # Configuration
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   └── agents.yaml   # YAML配置 ✨新增
│       └── main.py          # Entry point
├── tests/                   # Tests
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_tools.py
├── examples/                # Usage examples ✨新增
│   ├── basic_usage.py
│   └── advanced_multiagent.py
├── scripts/                 # Utility scripts ✨新增
│   ├── setup.sh
│   └── deploy.sh
├── docs/                    # Documentation ✨新增
│   └── architecture.md
├── pyproject.toml          # Project config
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🚀 新功能特性

### 1. **src/ 布局支持** ✨
- 遵循Python社区最佳实践
- 便于打包和分发
- 更清晰的代码组织

### 2. **prompts/ 模块** ✨
```python
# prompts/system_prompts.py
DEFAULT_SYSTEM_PROMPT = "..."
REACT_AGENT_PROMPT = "..."
MULTI_AGENT_COORDINATOR_PROMPT = "..."
RESEARCH_AGENT_PROMPT = "..."
```

### 3. **YAML配置支持** ✨
```yaml
# config/agents.yaml
agents:
  - name: my-agent
    type: basic
    model_provider: openai
    model: gpt-4
```

### 4. **示例代码** ✨
- `examples/basic_usage.py` - 基础用法
- `examples/advanced_multiagent.py` - 高级多agent协作

### 5. **工具脚本** ✨
- `scripts/setup.sh` - 自动化设置
- `scripts/deploy.sh` - 部署脚本

### 6. **文档增强** ✨
- `docs/architecture.md` - 架构文档

## 🛠️ CLI使用方式

### 创建标准布局项目 (推荐)
```bash
agentscope-init create --name my-agent --layout standard
```

### 创建轻量级布局项目
```bash
agentscope-init create --name my-agent --layout lightweight
```

### 交互式向导
```bash
agentscope-init wizard --name my-agent
# 向导会提示选择布局选项
```

## 📈 与业界标准对比

### CrewAI标准结构 ✅
```bash
# CrewAI
my_project/
├── src/
│   └── my_project/
│       ├── main.py
│       ├── crew.py
│       └── config/
│           ├── agents.yaml
│           └── tasks.yaml

# AgentScope Initializr (现在兼容) ✅
my_agent/
├── src/
│   └── my_agent/
│       ├── main.py
│       ├── agents/
│       └── config/
│           └── agents.yaml
```

### LangChain项目结构 ✅
```bash
# LangChain
langchain_project/
├── src/
│   └── project_name/
│       ├── agents/
│       ├── tools/
│       └── prompts/

# AgentScope Initializr (现在兼容) ✅
my_agent/
├── src/
│   └── my_agent/
│       ├── agents/
│       ├── tools/
│       └── prompts/
```

## 🎁 升级优势

### ✅ 符合Python社区标准
- `src/`布局是Python项目推荐结构
- 便于打包、测试和分发

### ✅ 清晰的关注点分离
- `agents/` - Agent实现
- `tools/` - 工具函数
- `prompts/` - 提示词管理
- `config/` - 配置文件

### ✅ 丰富的示例和文档
- `examples/` - 使用示例
- `docs/` - 详细文档
- `scripts/` - 便捷脚本

### ✅ 配置文件外置
- 支持YAML配置
- 便于环境切换
- 配置即文档

### ✅ 与主流框架对齐
- 与CrewAI、LangChain结构相似
- 降低学习成本
- 便于项目迁移

## 🔄 迁移指南

### 从旧版升级到新版

如果你有旧版项目，可以按以下步骤升级：

1. **创建新项目**
```bash
agentscope-init create --name my-new-agent --layout standard
```

2. **迁移代码**
- 将`agents/`代码移到`src/my_agent/agents/`
- 将`tools/`代码移到`src/my_agent/tools/`
- 将`config/`代码移到`src/my_agent/config/`

3. **添加新功能**
- 创建`prompts/`目录管理提示词
- 添加`examples/`目录提供使用示例
- 添加`scripts/`目录自动化任务

4. **更新导入**
```python
# 旧版
from my_agent.config import get_model

# 新版 (src/布局)
from my_agent.config import get_model  # 导入路径相同！
```

## 🎯 推荐使用场景

### 使用Standard布局 (推荐) 当：
- 🔧 构建生产级应用
- 📦 需要打包分发
- 👥 团队协作开发
- 🏗️ 复杂项目结构
- 📚 需要详细文档

### 使用Lightweight布局 当：
- 🎯 快速原型开发
- 📝 学习和教学
- 🧪 小型实验项目
- 🚀 快速验证想法

## 📊 兼容性说明

- ✅ **完全向后兼容** - 旧版项目仍可正常使用
- ✅ **导入路径一致** - 无论哪种布局，导入路径相同
- ✅ **功能对等** - 两种布局功能完全一致
- ✅ **自由选择** - 根据需求选择合适布局

## 🚀 下一步

1. **尝试新布局**
```bash
agentscope-init create --name test-agent --layout standard
cd test-agent
./scripts/setup.sh
```

2. **查看示例**
```bash
python examples/basic_usage.py
python examples/advanced_multiagent.py
```

3. **阅读文档**
```bash
cat docs/architecture.md
```

4. **开始开发**
```bash
python -m test_agent.main
```

## 📝 总结

这次升级使AgentScope Initializr生成的项目结构与业界主流agent框架（CrewAI、LangChain、AutoGen）保持一致，提供了：

- 🏗️ **更标准的目录结构**
- 📦 **更好的可维护性**
- 🔧 **更丰富的工具支持**
- 📚 **更完善的文档体系**
- 🎯 **更对齐的业界实践**

同时保持了向后兼容性和使用灵活性，让你可以根据项目需求选择最合适的布局。

---

**升级完成！享受更专业的agent应用开发体验！** 🎉
