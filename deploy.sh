#!/bin/bash
# AgentScope Initializr 部署脚本
# 停止旧容器 -> 删除旧文件和镜像 -> 加载新镜像 -> 启动服务

set -e

IMAGE_NAME="agentscope-initializr"
IMAGE_TAG="latest"
CONTAINER_NAME="agentscope"
PORT=8000
IMAGE_FILE="${IMAGE_NAME}-amd64.tar.gz"

echo "========================================"
echo "AgentScope Initializr 部署"
echo "========================================"
echo ""

# Step 1: 检查镜像文件
if [ ! -f "${IMAGE_FILE}" ]; then
    echo "错误: 镜像文件不存在: ${IMAGE_FILE}"
    exit 1
fi

# Step 2: 停止并删除旧容器
echo "[1/5] 停止并删除旧容器..."
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
    echo "  已删除容器: ${CONTAINER_NAME}"
else
    echo "  无旧容器需要删除"
fi

# Step 3: 删除旧镜像文件
echo "[2/5] 删除旧镜像文件..."
if [ -f "${IMAGE_FILE}" ]; then
    rm -f ${IMAGE_FILE}
    echo "  已删除镜像文件: ${IMAGE_FILE}"
else
    echo "  无旧镜像文件需要删除"
fi

# Step 4: 删除旧镜像
echo "[3/5] 删除旧镜像..."
if docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} > /dev/null 2>&1; then
    docker rmi ${IMAGE_NAME}:${IMAGE_TAG} > /dev/null 2>&1 || true
    echo "  已删除旧镜像"
else
    echo "  无旧镜像需要删除"
fi

# Step 5: 加载新镜像
echo "[4/5] 加载新镜像..."
docker load < ${IMAGE_FILE}
echo "  镜像加载完成"

# Step 6: 启动服务
echo "[5/5] 启动服务..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    -e LOG_LEVEL=info \
    --restart unless-stopped \
    ${IMAGE_NAME}:${IMAGE_TAG}

# 等待服务启动
sleep 3

# 健康检查
echo ""
if curl -f http://localhost:${PORT}/health > /dev/null 2>&1; then
    echo "========================================"
    echo "部署成功!"
    echo "========================================"
    echo "访问地址: http://localhost:${PORT}"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker logs -f ${CONTAINER_NAME}"
    echo "  停止服务: docker stop ${CONTAINER_NAME}"
    echo "  重新部署: ./deploy.sh"
else
    echo "警告: 健康检查失败，请查看日志: docker logs ${CONTAINER_NAME}"
fi
