# Docker 部署指南

本指南说明如何构建和部署 AgentScope Initializr Docker 镜像到 Linux ARM64 机器。

## 文件说明

| 文件 | 说明 |
|------|------|
| `agentscope-initializr-arm64.tar.gz` | Docker 镜像文件（117MB） |
| `docker-build.sh` | 构建镜像脚本（开发用） |
| `docker-run.sh` | 运行容器脚本（部署用） |
| `docker-verify.sh` | 验证镜像脚本（可选） |

## 部署步骤

### 1. 复制文件到目标机器

```bash
scp agentscope-initializr-arm64.tar.gz docker-run.sh user@your-linux-arm64:~/
```

### 2. 加载镜像

```bash
docker load < agentscope-initializr-arm64.tar.gz
```

### 3. 启动服务

```bash
chmod +x docker-run.sh
./docker-run.sh
```

服务将在 `http://localhost:8000` 启动。

## 常用命令

```bash
# 查看容器状态
docker ps | grep agentscope

# 查看日志
docker logs -f agentscope-initializr

# 停止服务
docker stop agentscope-initializr

# 启动服务
docker start agentscope-initializr

# 重启服务
docker restart agentscope-initializr

# 删除容器
docker rm -f agentscope-initializr
```

## 构建新镜像（仅开发用）

如果您修改了代码，需要重新构建镜像：

```bash
./docker-build.sh
```

这将生成新的 `agentscope-initializr-arm64.tar.gz` 文件。
