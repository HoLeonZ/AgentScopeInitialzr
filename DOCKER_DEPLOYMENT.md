# Docker 部署指南

本指南说明如何构建、验证和部署 AgentScope Initializr Docker 镜像。

## 前置要求

### 开发机器（macOS Apple Silicon）
- Docker Desktop 已安装并运行
- 至少 4GB 可用磁盘空间

### 目标机器（Linux ARM64）
- Docker 已安装并运行
- 至少 2GB 可用内存

## 快速开始

### 1. 构建镜像

在 macOS 上运行：

```bash
./docker-build.sh
```

这将：
- 构建 ARM64 Docker 镜像
- 导出镜像为 `agentscope-initializr-arm64.tar.gz` 文件

预计耗时：5-10 分钟（取决于网络速度）

### 2. 验证镜像（可选但推荐）

在 macOS 上运行：

```bash
./docker-verify.sh
```

这将验证：
- 镜像架构是否正确（ARM64）
- 容器能否正常启动
- 服务健康检查是否通过
- 前端页面是否可访问
- API 接口是否正常工作

### 3. 部署到目标机器

将以下文件复制到目标 Linux ARM64 机器：
- `agentscope-initializr-arm64.tar.gz`
- `docker-run.sh`

在目标机器上运行：

```bash
# 加载镜像
docker load < agentscope-initializr-arm64.tar.gz

# 启动服务
./docker-run.sh
```

服务将在 http://localhost:8000 启动。

## 详细说明

### 构建脚本 (docker-build.sh)

构建脚本执行以下步骤：

1. 检查 Docker 是否运行
2. 创建/使用 buildx builder 实例
3. 构建 ARM64 Docker 镜像
4. 导出镜像为压缩文件

### 验证脚本 (docker-verify.sh)

验证脚本执行以下检查：

1. 检查镜像文件是否存在
2. 加载镜像到 Docker
3. 检查镜像架构
4. 启动容器
5. 执行健康检查
6. 测试前端访问
7. 测试 API 接口
8. 显示资源使用情况

### 运行脚本 (docker-run.sh)

运行脚本执行以下操作：

1. 检查镜像是否存在
2. 停止并删除已存在的容器
3. 启动新容器
4. 等待服务启动
5. 执行健康检查

## 配置选项

### 环境变量

可以通过环境变量配置服务：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| LOG_LEVEL | info | 日志级别 |
| OUTPUT_DIR | /app/output | 生成的项目输出目录 |
| ALLOW_ORIGINS | http://localhost:8000 | CORS 允许的源 |

### 端口映射

默认映射端口 8000。可以通过修改 `docker-run.sh` 中的 `PORT` 变量来更改。

### 数据持久化

容器将 `/app/output` 目录映射到宿主机的 `./output` 目录，用于持久化生成的项目文件。

## 故障排除

### 镜像加载失败

```bash
# 检查文件完整性
gzip -t agentscope-initializr-arm64.tar.gz

# 如果文件损坏，重新构建
./docker-build.sh
```

### 容器启动失败

```bash
# 查看容器日志
docker logs agentscope-initializr

# 检查端口是否被占用
lsof -i :8000
```

### 服务无法访问

```bash
# 检查容器是否运行
docker ps

# 检查健康状态
curl http://localhost:8000/health
```

## 常用命令

```bash
# 查看容器日志
docker logs -f agentscope-initializr

# 停止容器
docker stop agentscope-initializr

# 重启容器
docker restart agentscope-initializr

# 删除容器
docker rm -f agentscope-initializr

# 进入容器
docker exec -it agentscope-initializr /bin/bash
```

## 镜像信息

- **基础镜像**: python:3.11-slim
- **目标架构**: linux/arm64
- **预计大小**: 300-400MB (压缩后)
- **运行时大小**: 500-600MB

## 安全建议

1. 在生产环境中，建议使用 HTTPS
2. 配置适当的 CORS 策略
3. 定期更新基础镜像
4. 限制容器资源使用

## 更新镜像

当项目代码更新后，重新构建镜像：

```bash
# 在 macOS 上
./docker-build.sh

# 验证新镜像
./docker-verify.sh

# 在目标机器上
docker load < agentscope-initializr-arm64.tar.gz
docker stop agentscope-initializr
docker rm agentscope-initializr
./docker-run.sh
```
