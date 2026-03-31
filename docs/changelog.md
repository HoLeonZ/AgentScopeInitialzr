# AgentScope Initializr 变更日志

## [Unreleased]

## [0.2.0] - 2026-03-31

### Added
- 完整的扩展点配置系统
  - Memory 配置（短期/长期内存）
  - Tools 配置（Python、Shell、Web搜索、浏览器）
  - Formatter 配置
  - Hooks 生命周期配置
  - Skills 配置
  - RAG 配置（向量存储、嵌入模型）
  - Pipeline 配置（Sequential、Parallel、Conditional）
- Web UI 4步配置向导
- 实时代码预览
- 项目生成和下载
- 测试和评估模块生成

### Changed
- 优化 UI 布局，去除重复配置
- 改进表单验证
- 增强用户体验

### Fixed
- Memory 配置重复问题
- UI 显示问题

## [0.1.0] - 2026-03-XX

### Added
- 初始版本发布
- 基础项目生成功能
- CLI 工具
- 基础模板（basic、multi-agent、research、browser）
- Model 和 Memory 配置
