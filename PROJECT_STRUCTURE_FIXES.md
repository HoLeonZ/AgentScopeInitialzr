# 项目结构改进说明

## 需要修复的问题

### 1. ✅ 已完成：移除 Advanced Options
- Commit: f6b9c29
- 已从 TestingSettings.vue 中删除

### 2. ⚠️ 需要手动改进：项目生成结构

#### 问题 A: 日志代码位置
**当前**: `src/package_name/utils/logging.py`
**目标**: `src/package_name/log/logger.py` 和 `log/__init__.py`

**修改位置**: `initializr-core/initializr_core/generator/engine.py`

**修改步骤**:

1. 在 `_generate_source_code` 方法中（约第187行），添加调用：
```python
# Generate log folder
self._generate_log_folder(pkg_dir, metadata)
```

2. 在 `_generate_examples` 之前（约第1475行），添加新函数：
```python
def _generate_log_folder(self, pkg_dir: Path, metadata: AgentScopeMetadata):
    """Generate logging module in separate log folder."""
    log_dir = pkg_dir / "log"
    log_dir.mkdir(exist_ok=True)
    
    # __init__.py
    (log_dir / "__init__.py").write_text('''"""
Logging module for {name}.
"""
from .logger import setup_logging, get_logger
__all__ = ["setup_logging", "get_logger"]
'''.format(name=metadata.name))
    
    # logger.py
    (log_dir / "logger.py").write_text('''import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

class LoggerConfig:
    LOG_DIR = Path("logs")
    LOG_FILE_MAX_BYTES = 10 * 1024 * 1024
    
def setup_logging(level: str = "INFO"):
    logger = logging.getLogger("{name}")
    logger.setLevel(getattr(logging, level.upper()))
    # ... add file and console handlers
    return logger
'''.format(name=metadata.package_name))
```

3. 修改 `_generate_utils` 函数，删除日志部分（第807-1046行）

#### 问题 B: YAML配置改为.env
**当前**: `src/package_name/config/agents.yaml`
**目标**: `src/package_name/config/.env` 和 `.env.example`

**修改位置**: `initializr-core/initializr_core/generator/engine.py`

**修改步骤**:

1. 找到 `_generate_config` 函数（约第1448行）

2. 删除YAML生成部分（第1553-1576行）：
```python
# 删除这部分：
yaml_config = f'''# AgentScope Configuration...
'''
(pkg_dir / "config" / "agents.yaml").write_text(yaml_config)
```

3. 添加.env生成：
```python
# Generate .env configuration
env_config = f'''# Environment Configuration
AGENT_NAME={metadata.name}
MODEL_PROVIDER={metadata.model_provider.value}
MODEL={self._get_default_model(metadata.model_provider.value)}
OPENAI_API_KEY=your_api_key_here

LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_TO_CONSOLE=true
'''
(pkg_dir / "config" / ".env").write_text(env_config)

# Generate .env.example
env_example = env_config.replace("your_api_key_here", "")
(pkg_dir / "config" / ".env.example").write_text(env_example)
```

## 验证方法

生成测试项目后检查结构：
```bash
# 应该有这些文件
src/package_name/log/__init__.py
src/package_name/log/logger.py
src/package_name/config/.env
src/package_name/config/.env.example

# 不应该有这些文件
src/package_name/utils/logging.py
src/package_name/config/agents.yaml
```

## 优先级

1. ⭐⭐⭐ **高优先级**: `.env` 配置（影响所有项目，最重要）
2. ⭐⭐ **中优先级**: 日志文件夹重构（代码组织优化）
