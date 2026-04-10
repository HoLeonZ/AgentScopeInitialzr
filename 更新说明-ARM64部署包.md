# AgentScope Initializr ARM64 部署包更新说明

## 📦 更新版本：agentscope-initializr-arm64-updated

### 🎯 本次更新内容

#### 1. 修复 Docker 镜像架构支持
- **问题**：之前的镜像在某些 ARM64 系统上出现 "exec format error" 错误
- **解决**：在 Dockerfile 中明确指定 `--platform=linux/arm64`
- **影响**：确保 Docker 镜像在所有 ARM64 架构上正常运行

#### 2. 移除特殊Unicode字符
- **问题**：特殊字符（✓✗⚠ℹ）在某些终端环境下显示异常
- **解决**：将所有 Unicode 图标替换为 ASCII 文本标识
  - `✓` → `[OK]`
  - `✗` → `[ERROR]`
  - `⚠` → `[WARNING]`
  - `ℹ` → `[INFO]`
  - `→` → `[PROCESSING]`
- **影响**：确保在所有 Linux ARM64 终端环境中都能正确显示

#### 3. 新增诊断和修复工具
- **diagnose-docker.sh**：Docker 进程和 socket 诊断工具
- **quick-diagnose.sh**：快速容器和服务诊断脚本
- **rebuild-arm64.sh**：在 ARM64 机器上重新构建镜像的脚本

### 📁 包含文件

```
agentscope-initializr-arm64/
├── deploy-arm64.sh                    # 主部署脚本（推荐使用）
├── quick-start-arm64.sh               # 快速安装脚本
├── health-check.sh                    # 健康检查脚本
├── diagnose-docker.sh                 # Docker 诊断工具（新增）
├── quick-diagnose.sh                  # 快速诊断脚本（新增）
├── rebuild-arm64.sh                   # ARM64 重建脚本（新增）
├── agentscope.service                 # 系统服务配置
├── agentscope-initializr-arm64.tar.gz # Docker 镜像
├── ARM64-DEPLOYMENT.md                # 详细文档
├── README-ARM64.md                    # 快速指南
├── 部署说明书.md                      # 中文部署说明
└── 更新说明-ARM64部署包.md            # 本文档
```

### 🚀 使用方法

#### 基本部署流程
```bash
# 1. 解压部署包
tar -xzf agentscope-initializr-arm64-updated.tar.gz
cd agentscope-initializr-arm64

# 2. 添加执行权限
chmod +x *.sh

# 3. 运行部署脚本
./deploy-arm64.sh
```

#### 如果遇到架构问题
```bash
# 使用重建脚本在本地重新构建镜像
chmod +x rebuild-arm64.sh
./rebuild-arm64.sh
```

#### 诊断工具
```bash
# Docker 诊断
./diagnose-docker.sh

# 快速容器诊断
./quick-diagnose.sh

# 健康检查
./health-check.sh
```

### 🔧 主要修复

#### 修复 1：Docker 架构不匹配
```bash
# 错误信息：
# exec /usr/local/bin/uvicorn:exec format error

# 解决方案：
# 1. 停止旧容器
docker stop agentscope-initializr
docker rm agentscope-initializr

# 2. 使用重建脚本
./rebuild-arm64.sh
```

#### 修复 2：终端字符显示问题
```bash
# 所有脚本现在使用 ASCII 字符
# 输出示例：
[OK] 所有依赖已就绪
[INFO] Docker 服务运行正常
[WARNING] 端口 8000 已被占用
[ERROR] Docker 服务未运行
```

### 📊 兼容性

- **架构**：ARM64 (aarch64)
- **系统**：Linux (Ubuntu 20.04+, Debian 10+, CentOS 7+)
- **终端**：所有终端类型（包括不支持 Unicode 的终端）
- **Docker**：Docker 19.03+ / Docker Compose 1.25+

### 🆚 与旧版本的区别

| 功能 | 旧版本 | 新版本 |
|------|--------|--------|
| 架构支持 | 可能不匹配 | 明确指定 ARM64 |
| 终端兼容性 | 部分终端显示异常 | 完全兼容所有终端 |
| 诊断工具 | 基础健康检查 | 完整的诊断工具集 |
| 错误处理 | 基础错误信息 | 详细的错误诊断和修复建议 |

### 📞 技术支持

如遇到问题，请按以下顺序排查：

1. **运行诊断脚本**：`./diagnose-docker.sh`
2. **查看详细日志**：`docker logs agentscope-initializr`
3. **检查架构匹配**：`docker inspect agentscope-initializr --format='{{.Architecture}}'`
4. **使用重建脚本**：`./rebuild-arm64.sh`

### 📝 更新历史

- **v2.0 (2024-04-10)**: 修复架构支持，移除特殊字符，新增诊断工具
- **v1.0 (2024-04-10)**: 初始 ARM64 部署包

---

**部署完成后，请访问 http://your-server-ip:8000/docs 查看 API 文档！**

祝您部署顺利！ 🎉
