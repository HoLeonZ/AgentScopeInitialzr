# AgentScope扩展点配置 - 用户使用指南

## 快速开始

### 1. 启动Web服务

```bash
# 方式1: 使用Docker（推荐）
docker-compose up

# 方式2: 手动启动
pip install -e ".[web]"
agentscope-web

# 访问Web界面
# 前端: http://localhost:5173
# 后端API: http://localhost:8000/docs
```

### 2. 配置项目

访问 `http://localhost:5173`，按照4步向导配置项目：

#### Step 1: Basic Settings（基础设置）
- 选择项目模板（basic, multi-agent, research, browser）
- 填写项目名称、描述、作者信息

#### Step 2: Model & Memory（模型和内存）
- 选择模型提供商（OpenAI、DashScope、Gemini、Anthropic、Ollama）
- 配置模型参数
- **配置内存**：
  - 短期内存: in-memory, redis, oceanbase
  - 长期内存: mem0, zep, oceanbase, none

#### Step 3: Extensions（扩展点配置）

##### Memory Configuration（内存配置）
- 启用/禁用内存功能
- 选择短期内存类型
- 选择长期内存类型

##### Tools Configuration（工具配置）
- 启用/禁用工具功能
- 选择可用工具：
  - `Execute Python Code` - 执行Python代码
  - `Execute Shell Command` - 执行Shell命令
  - `Web Search` - 使用Tavily API进行网络搜索
  - `Browser Navigate/Click/Type/Screenshot` - 浏览器自动化

##### Formatter Configuration（格式化器配置）
- 启用/禁用格式化器
- 选择格式化器类型：
  - `DashScopeChatFormatter` - DashScope聊天格式化
  - `OpenAIChatFormatter` - OpenAI聊天格式化

##### Hooks Configuration（钩子配置）
- 启用/禁用钩子功能
- 选择生命周期钩子：
  - `Pre Reply` - Agent回复前执行
  - `Post Reply` - Agent回复后执行
  - `Pre Observe` - Agent观察前执行
  - `Post Observe` - Agent观察后执行

##### Skills Configuration（技能配置）
- 启用/禁用技能功能
- 添加技能模块：
  - 预设技能: coding, writing, analysis, research, math, translation
  - 或自定义技能模块

##### RAG Configuration（检索增强生成配置）
- 启用/禁用RAG功能
- 配置向量存储：Chroma, FAISS, Pinecone
- 配置嵌入模型：如 `openai:text-embedding-ada-002`
- 配置分块参数：
  - Chunk Size: 100-2000（默认500）
  - Chunk Overlap: 0-500（默认50）

##### Pipeline Configuration（管道配置）
- 启用/禁用Pipeline功能
- 配置管道类型：
  - `Sequential` - 顺序执行
  - `Parallel` - 并行执行
  - `Conditional` - 条件执行
- 配置Stage数量（2-10个）
- 配置错误处理策略：
  - `Stop on Error` - 遇到错误停止
  - `Continue on Error` - 遇到错误继续
  - `Retry` - 遇到错误重试

#### Step 4: Testing & Evaluation（测试和评估）

##### Test Generation（测试生成）
- 启用/禁用测试模块生成
- 选择测试框架：pytest（默认）
- 启用代码覆盖率报告

##### Evaluation Configuration（评估配置）
- 启用/禁用评估模块生成
- 选择评估器类型：
  - `General` - 通用评估器
  - `Ray` - 分布式评估器

##### OpenJudge Integration（OpenJudge集成）
- 启用/禁用OpenJudge集成
- 选择评估器：
  - `RelevanceGrader` - 相关性评估
  - `CorrectnessGrader` - 正确性评估
  - `HallucinationGrader` - 幻觉检测
  - `SafetyGrader` - 安全性评估
  - `CodeQualityGrader` - 代码质量评估

##### Benchmark Configuration（基准测试配置）
- 设置初始基准测试任务数量（0-100）
- 选择基准测试套件：
  - `Custom Tasks` - 自定义任务
  - `MMLU Sample` - MMLU示例
  - `GSM8K Sample` - GSM8K示例
  - `Custom Dataset` - 自定义数据集

### 3. 生成项目

点击 "Generate Project" 按钮，系统将：
1. 验证配置
2. 生成项目代码
3. 创建ZIP文件
4. 提供下载链接

### 4. 使用生成的项目

```bash
# 解压项目
unzip your-project.zip

# 进入项目目录
cd your-project

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加API密钥

# 运行项目
python main.py
```

## 配置示例

### 示例1: 基础ReAct Agent

```
Step 1:
- Template: basic
- Name: my-assistant
- Description: Personal AI assistant

Step 2:
- Model: OpenAI GPT-4
- Short-term Memory: in-memory
- Long-term Memory: none

Step 3:
- Tools: execute_python_code
- Other extensions: disabled

Step 4:
- Testing: disabled
- Evaluation: disabled
```

### 示例2: 研究Agent（带RAG）

```
Step 1:
- Template: research
- Name: research-bot
- Description: Research assistant with RAG

Step 2:
- Model: OpenAI GPT-4
- Short-term Memory: in-memory
- Long-term Memory: mem0

Step 3:
- Tools: web_search, execute_python_code
- RAG: enabled (Chroma + openai embeddings)
- Other extensions: disabled

Step 4:
- Testing: enabled
- Evaluation: enabled (general evaluator)
- Benchmarks: 10 tasks
```

### 示例3: 多Agent系统

```
Step 1:
- Template: multi-agent
- Name: agent-team
- Description: Collaborative agent team

Step 2:
- Model: DashScope Qwen-Max
- Short-term Memory: redis
- Long-term Memory: oceanbase

Step 3:
- Tools: all tools enabled
- Formatter: DashScopeChatFormatter
- Pipeline: enabled (sequential, 5 stages)
- Hooks: pre_reply, post_reply

Step 4:
- Testing: enabled
- Evaluation: enabled
- OpenJudge: enabled (all graders)
- Benchmarks: 20 tasks
```

## 常见问题

### Q: 如何添加自定义工具？
A: 生成的项目中，在 `src/your_package/tools/` 目录下添加自定义工具函数，使用 `@tool` 装饰器注册。

### Q: 如何配置RAG的向量存储？
A: 在 `.env` 文件中添加相应的API密钥：
- Chroma: 无需配置（默认本地存储）
- FAISS: 无需配置（默认本地存储）
- Pinecone: 添加 `PINECONE_API_KEY`

### Q: 如何运行测试？
A:
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_evaluation.py

# 生成覆盖率报告
pytest --cov=your_package --cov-report=html
```

### Q: 如何使用OpenJudge？
A: 需要配置OpenJudge API密钥，并在测试中实现具体的评估逻辑。

### Q: 生成的项目可以自定义吗？
A: 可以！生成的项目是一个标准的Python项目，可以根据需求自由修改和扩展。

## 技术支持

- 📖 文档: https://doc.agentscope.io/
- 🐛 问题反馈: https://github.com/agentscope-ai/initializr/issues
- 💬 讨论: https://github.com/agentscope-ai/initializr/discussions

## 更新日志

### v0.2.0 (2026-03-31)
- ✅ 实现完整的扩展点配置UI
- ✅ 支持Memory、Tools、Formatter、Hooks配置
- ✅ 支持Skills、RAG、Pipeline配置
- ✅ 支持Testing & Evaluation配置
- ✅ 实现完整的后端转换和代码生成
- ✅ 添加端到端测试验证
