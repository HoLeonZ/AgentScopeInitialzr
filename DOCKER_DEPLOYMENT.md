# Docker 部署指南

本指南说明如何构建和部署 AgentScope Initializr Docker 镜像到 Linux ARM64 机器。

## 文件说明

| 文件 | 说明 |
|------|------|
| `agentscope-initializr-arm64.tar.gz` | Docker 镜像文件（112MB） |
| `build_docker.py` | 构建镜像脚本（Python） |
| `docker-run.sh` | 运行容器脚本（部署用） |
| `docker-verify.sh` | 验证镜像脚本（可选） |

## 构建新镜像（开发用）

修改代码后，重新构建镜像：

```bash
python3 build_docker.py
```

可选参数：
- `--no-cache`: 不使用 Docker 缓存，强制重新构建
- `--check-only`: 仅检查 Docker 是否运行

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
