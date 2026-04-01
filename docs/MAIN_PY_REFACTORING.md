# Main.py 重构说明

## 重构目标

遵循**单一职责原则 (SRP)**，将 main.py 中混杂的职责分离到独立的模块中。

## 重构前的问题

### 原始 main.py 包含的职责：

```python
# 1. 日志配置和初始化
logger = setup_logging(...)
cleanup_old_logs(...)

# 2. 应用生命周期管理
ApplicationLifecycle.initialize()
ApplicationLifecycle.shutdown()

# 3. Agent 创建和配置
agent_params = ApplicationLifecycle.get_agent_params()
agent = ReActAgent(
    name="{metadata.name}",
    sys_prompt=settings.SYSTEM_PROMPT,
    **agent_params
)

# 4. CLI 交互逻辑
while True:
    user_input = input("\n💬 You: ")
    if user_input.lower() == 'help':
        # 显示帮助
    elif user_input.lower() == 'stats':
        # 显示统计信息
    # ...
```

**问题**:
- 违反单一职责原则
- 难以测试
- 难以复用
- 代码可读性差

## 重构后的架构

### 模块划分

```
src/{package_name}/
├── main.py              # 🎯 主入口：协调各模块
├── agent_factory.py     # 🏭 工厂模式：创建 Agent
├── cli.py              # 💬 用户界面：处理交互
├── config/
│   └── lifecycle.py    # ♻️  生命周期管理
└── ...
```

### 1. `agent_factory.py` - Agent 创建模块

**职责**: 负责创建和配置 Agent 实例

```python
class AgentFactory:
    """工厂类：封装 Agent 创建逻辑"""

    @staticmethod
    def create_agent(name: str, sys_prompt: Optional[str] = None) -> ReActAgent:
        """创建并配置 Agent"""
        agent_params = ApplicationLifecycle.get_agent_params()
        prompt = sys_prompt or settings.SYSTEM_PROMPT

        agent = ReActAgent(
            name=name,
            sys_prompt=prompt,
            **agent_params
        )
        return agent
```

**优点**:
- 封装创建逻辑
- 便于单元测试
- 可复用于创建多个 Agent

**使用场景**:
- 创建主对话 Agent
- 创建专门的工具 Agent
- 测试时创建 Mock Agent

### 2. `cli.py` - 用户交互模块

**职责**: 处理所有用户输入/输出和命令

```python
class CLI:
    """CLI 类：管理用户交互"""

    def __init__(self, agent: ReActAgent, agent_name: str):
        self.agent = agent
        self.agent_name = agent_name

    def show_welcome(self):
        """显示欢迎信息"""
        print(f"🤖 {self.agent_name} is ready!")

    async def process_input(self, user_input: str) -> bool:
        """处理用户输入"""
        if user_input.lower() == 'help':
            self.show_help()
        elif user_input.lower() == 'stats':
            await self.show_stats()
        # ...

    async def run(self):
        """运行交互循环"""
        while True:
            user_input = input("\n💬 You: ")
            should_continue = await self.process_input(user_input)
            if not should_continue:
                break
```

**优点**:
- 分离 I/O 逻辑
- 便于添加新命令
- 易于测试交互逻辑

**可扩展性**:
```python
# 轻松添加新命令
async def process_input(self, user_input: str) -> bool:
    if user_input.lower() == 'export':
        await self.export_conversation()  # 导出对话
    elif user_input.lower() == 'clear':
        self.clear_memory()  # 清空记忆
    # ...
```

### 3. `main.py` - 主协调模块

**职责**: 初始化、创建 Agent、协调各模块

```python
async def main():
    """主入口：协调应用启动流程"""
    try:
        # Step 1: 初始化日志
        logger.info(f"Starting {metadata.name}...")
        cleanup_old_logs(...)

        # Step 2: 初始化生命周期
        ApplicationLifecycle.initialize()

        # Step 3: 创建 Agent（委托给工厂）
        agent = create_agent(name="{metadata.name}")

        # Step 4: 运行 CLI（委托给界面模块）
        await run_cli(agent, "{metadata.name}")

    finally:
        # Step 5: 清理资源
        ApplicationLifecycle.shutdown()
```

**优点**:
- 清晰的执行流程
- 易于理解和维护
- 错误处理集中

## 设计原则应用

### 1. 单一职责原则 (SRP)
- `main.py`: 应用启动和协调
- `agent_factory.py`: Agent 创建
- `cli.py`: 用户交互

### 2. 开闭原则 (OCP)
- 对扩展开放：易于添加新命令到 CLI
- 对修改封闭：添加新功能无需修改现有代码

### 3. 依赖倒置原则 (DIP)
- main.py 依赖抽象（工厂方法）
- 不依赖具体的 Agent 创建细节

## 测试性改进

### 重构前：难以测试

```python
# 无法单独测试 Agent 创建逻辑
# 无法模拟用户输入
# 无法单独测试 CLI 命令
```

### 重构后：易于测试

```python
# 测试 Agent 创建
def test_agent_factory():
    agent = AgentFactory.create_agent("test", "Hello")
    assert agent.name == "test"
    assert agent.sys_prompt == "Hello"

# 测试 CLI 命令
async def test_cli_help_command():
    mock_agent = Mock(spec=ReActAgent)
    cli = CLI(mock_agent, "test")
    result = await cli.process_input("help")
    assert result == True  # 应该继续运行

# 测试主流程
async def test_main_flow(monkeypatch):
    monkeypatch.setattr(sys, "exit", Mock())
    await main()
```

## 使用示例

### 扩展：创建多个 Agent

```python
# agent_factory.py
class AgentFactory:
    @staticmethod
    def create_researcher() -> ReActAgent:
        """创建研究型 Agent"""
        return create_agent(
            name="researcher",
            sys_prompt="You are a research specialist."
        )

    @staticmethod
    def create_writer() -> ReActAgent:
        """创建写作型 Agent"""
        return create_agent(
            name="writer",
            sys_prompt="You are a content writer."
        )

# main.py
async def main():
    researcher = AgentFactory.create_researcher()
    writer = AgentFactory.create_writer()

    # 协作完成任务
    await run_multi_agent_cli([researcher, writer])
```

### 扩展：添加 Web 界面

```python
# web.py
from fastapi import FastAPI
from agent_factory import create_agent

app = FastAPI()
agent = None  # 全局 Agent 实例

@app.on_event("startup")
async def startup():
    global agent
    agent = create_agent("web-agent")

@app.post("/chat")
async def chat(message: str):
    response = await agent(message)
    return {"response": response}

# CLI 界面仍然可用
# main.py 可以复用同一个 agent_factory
```

## 迁移指南

### 对于现有项目

如果需要将现有项目迁移到新架构：

1. **创建 agent_factory.py**
```python
# 将 Agent 创建逻辑移到工厂类
```

2. **创建 cli.py**
```python
# 将交互循环移到 CLI 类
```

3. **简化 main.py**
```python
# 只保留启动协调逻辑
```

### 向后兼容

如果需要保持向后兼容：

```python
# main.py
from agent_factory import create_agent
from cli import CLI

# 保留旧的函数签名
async def run_legacy_interface():
    """兼容旧版本"""
    agent = create_agent("legacy")
    cli = CLI(agent, "legacy")
    await cli.run()
```

## 总结

### 重构带来的好处

1. **可维护性**: 每个模块职责清晰，易于理解和修改
2. **可测试性**: 每个模块可以独立测试
3. **可复用性**: 工厂和 CLI 可以在其他场景复用
4. **可扩展性**: 易于添加新功能（新命令、新 Agent 类型）
5. **代码质量**: 遵循 SOLID 原则

### 架构演进路径

**当前版本**: 单体 CLI 应用
**下一步**:
- 添加 Web 界面（复用 agent_factory）
- 添加 REST API（复用 agent_factory）
- 添加多 Agent 协作（扩展工厂模式）

这种架构为未来的功能扩展奠定了良好的基础。
