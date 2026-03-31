# AgentScope Initializr 架构文档

## 系统架构

### 目录结构

```
agentscope-initializr/
├── initializr-core/              # 核心生成引擎
│   └── initializr_core/
│       ├── metadata/             # 元数据管理
│       │   ├── models.py         # 数据模型
│       │   └── templates.py      # 模板注册
│       ├── generator/            # 项目生成器
│       │   ├── engine.py         # 主生成器
│       │   └── extensions.py     # 扩展点生成
│       └── validator/            # 配置验证
│           └── validator.py      # 验证器
├── initializr-web/               # Web 服务
│   ├── initializr_web/
│   │   ├── main.py              # FastAPI 应用
│   │   ├── router/              # API 路由
│   │   └── converter.py         # 数据转换器
│   └── frontend/                # Vue.js 前端
│       └── src/
│           ├── components/      # Vue 组件
│           ├── router/          # 路由配置
│           └── stores/          # Pinia 状态管理
├── initializr-cli/               # CLI 工具
├── initializr-templates/         # 项目模板
└── docs/                        # 文档
```

### 系统组件

#### 1. 元数据层（Metadata）
- **AgentScopeMetadata**: 项目配置元数据
- **AgentType**: Agent 类型枚举
- **ModelProvider**: 模型提供商
- **MemoryType**: 内存类型
- **FormatterType**: 格式化器类型

#### 2. 验证层（Validator）
- **MetadataValidator**: 配置验证器
- 验证项目名称、依赖、工具配置等

#### 3. 生成层（Generator）
- **ProjectGenerator**: 主生成器
  - 目录结构生成
  - 配置文件生成
  - Agent 代码生成
  - 测试代码生成
- **ExtensionGenerator**: 扩展点生成器
  - Model 配置
  - Memory 配置
  - Toolkit 配置
  - Formatter 配置
  - Skills 配置
  - RAG 配置
  - Pipeline 配置

#### 4. Web 服务层
- **FastAPI 后端**
  - RESTful API
  - 项目生成接口
  - 配置验证接口
- **Vue.js 前端**
  - 4步配置向导
  - 实时代码预览
  - 项目下载

### 数据流

```
用户输入（Web UI）
    ↓
Pinia Store（状态管理）
    ↓
API Client（HTTP 请求）
    ↓
FastAPI Backend（接收请求）
    ↓
Converter（转换为 AgentScopeMetadata）
    ↓
Validator（验证配置）
    ↓
Generator（生成项目代码）
    ↓
ZIP 打包
    ↓
返回下载链接
```

### 扩展点架构

#### 配置阶段
1. **Basic Settings** - 基础配置
2. **Model & Memory** - 模型和内存
3. **Extensions** - 扩展点配置
   - Memory
   - Tools
   - Formatter
   - Hooks
   - Skills
   - RAG
   - Pipeline
4. **Testing** - 测试配置

#### 生成阶段
1. 创建目录结构
2. 生成配置模块
3. 生成 Agent 代码
4. 生成测试代码
5. 打包项目文件

### 技术栈

- **后端**: FastAPI, Python 3.14+
- **前端**: Vue.js 3, TypeScript, Element Plus, Pinia
- **构建**: Vite
- **数据库**: 无（状态管理）
- **部署**: Docker, Docker Compose

