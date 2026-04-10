#!/bin/bash
# 在 ARM64 机器上重新构建和部署脚本

set -e

echo "=== AgentScope Initializr ARM64 重新构建和部署 ==="
echo ""

# 1. 清理旧镜像
echo "1️⃣  清理旧镜像..."
echo "-------------------------------------------"
docker stop agentscope-initializr 2>/dev/null || true
docker rm agentscope-initializr 2>/dev/null || true
docker rmi agentscope-initializr:latest 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# 2. 重新构建镜像
echo "2️⃣  重新构建 ARM64 镜像..."
echo "-------------------------------------------"
DOCKER_BUILDKIT=1 docker build \
    --platform linux/arm64 \
    --no-cache \
    -t agentscope-initializr:latest \
    .

echo "✅ 构建完成"
echo ""

# 3. 验证镜像架构
echo "3️⃣  验证镜像架构..."
echo "-------------------------------------------"
ARCH=$(docker inspect agentscope-initializr:latest --format='{{.Architecture}}')
echo "镜像架构: $ARCH"

if [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then
    echo "✅ 架构正确！"
else
    echo "❌ 架构错误: $ARCH (期望: arm64)"
    echo "您的机器架构: $(uname -m)"
    exit 1
fi
echo ""

# 4. 启动容器
echo "4️⃣  启动容器..."
echo "-------------------------------------------"
docker run -d \
    --name agentscope-initializr \
    -p 8000:8000 \
    --restart unless-stopped \
    agentscope-initializr:latest

echo "✅ 容器已启动"
echo ""

# 5. 等待服务就绪
echo "5️⃣  等待服务启动..."
echo "-------------------------------------------"
sleep 10

# 6. 健康检查
echo "6️⃣  健康检查..."
echo "-------------------------------------------"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ /health 端点正常"
else
    echo "❌ /health 端点异常"
fi

if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ /docs 端点正常"
else
    echo "❌ /docs 端点异常"
fi

echo ""
echo "========================================"
echo "部署完成！"
echo "========================================"
echo ""
echo "访问地址："
echo "  主页: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo "  健康检查: http://localhost:8000/health"
echo ""
echo "管理命令："
echo "  查看日志: docker logs agentscope-initializr -f"
echo "  重启容器: docker restart agentscope-initializr"
echo "  停止容器: docker stop agentscope-initializr"
echo ""
