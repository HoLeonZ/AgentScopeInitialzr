#!/bin/bash
# 快速验证 Docker 镜像的 ARM64 兼容性

echo "=== ARM64 快速验证工具 ==="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SUCCESS="[OK]"
ERROR="[ERROR]"
WARNING="[WARNING]"

# 检查镜像是否存在
if ! docker images | grep -q "agentscope"; then
    echo -e "${RED}${ERROR} 未找到 agentscope 镜像${NC}"
    echo "请先确保镜像已加载"
    exit 1
fi

# 1. 检查镜像架构
echo "1. 镜像架构检查"
echo "-------------------------------------------"
ARCH=$(docker inspect agentscope-initializr-arm64 --format='{{.Architecture}}' 2>/dev/null)
if [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then
    echo -e "${GREEN}${SUCCESS} 镜像架构: $ARCH${NC}"
else
    echo -e "${RED}${ERROR} 镜像架构: $ARCH (期望: arm64)${NC}"
fi
echo ""

# 2. 检查关键组件
echo "2. 关键组件检查"
echo "-------------------------------------------"

# Python 架构
PYTHON_ARCH=$(docker run --rm agentscope-initializr-arm64 python -c 'import platform; print(platform.machine())' 2>/dev/null)
if [ "$PYTHON_ARCH" = "aarch64" ]; then
    echo -e "${GREEN}${SUCCESS} Python 架构: $PYTHON_ARCH${NC}"
else
    echo -e "${YELLOW}${WARNING} Python 架构: $PYTHON_ARCH${NC}"
fi

# Node.js 架构
NODE_ARCH=$(docker run --rm agentscope-initializr-arm64 node -p 'process.arch' 2>/dev/null)
if [ "$NODE_ARCH" = "arm64" ]; then
    echo -e "${GREEN}${SUCCESS} Node.js 架构: $NODE_ARCH${NC}"
else
    echo -e "${YELLOW}${WARNING} Node.js 架构: $NODE_ARCH${NC}"
fi

# Node.js 版本
NODE_VERSION=$(docker run --rm agentscope-initializr-arm64 node --version 2>/dev/null)
echo "Node.js 版本: $NODE_VERSION"

# uvloop 检查 (关键!)
UVLOOP_CHECK=$(docker run --rm agentscope-initializr-arm64 sh -c "pip show uvloop 2>/dev/null | wc -l" 2>/dev/null)
if [ "$UVLOOP_CHECK" -eq 0 ]; then
    echo -e "${GREEN}${SUCCESS} uvloop 未安装 (这是好的!)${NC}"
else
    echo -e "${RED}${ERROR} uvloop 已安装 (ARM64 性能问题!)${NC}"
fi
echo ""

# 3. 二进制文件检查
echo "3. 二进制文件架构检查"
echo "-------------------------------------------"
PYTHON_FILE=$(docker run --rm agentscope-initializr-arm64 sh -c "file \$(which python)" 2>/dev/null)
echo "$PYTHON_FILE" | grep -q "aarch64\|ARM" && echo -e "${GREEN}${SUCCESS} Python 是 ARM64 二进制${NC}" || echo -e "${YELLOW}${WARNING} Python 可能不是 ARM64 二进制${NC}"

UVICORN_FILE=$(docker run --rm agentscope-initializr-arm64 sh -c "file \$(which uvicorn)" 2>/dev/null)
echo "$UVICORN_FILE" | grep -q "aarch64\|ARM\|script" && echo -e "${GREEN}${SUCCESS} uvicorn 是 ARM64 兼容${NC}" || echo -e "${YELLOW}${WARNING} uvicorn 架构未知${NC}"
echo ""

# 4. 服务启动测试
echo "4. 服务启动测试"
echo "-------------------------------------------"
echo "启动测试容器..."
docker run --rm -d --name test-arm64 -p 8001:8000 agentscope-initializr-arm64 >/dev/null 2>&1

echo "等待服务启动 (10秒)..."
sleep 10

# 测试健康检查
if curl -s http://localhost:8001/health >/dev/null 2>&1; then
    echo -e "${GREEN}${SUCCESS} 服务启动成功并响应${NC}"

    # 检查进程架构
    echo "容器内进程:"
    docker exec test-arm64 sh -c "ps aux | head -5" 2>/dev/null

    docker stop test-arm64 >/dev/null 2>&1
else
    echo -e "${RED}${ERROR} 服务启动失败${NC}"
    echo "查看日志:"
    docker logs test-arm64 --tail 20 2>/dev/null
    docker stop test-arm64 >/dev/null 2>&1
fi
echo ""

# 5. 生成建议
echo "5. 优化建议"
echo "-------------------------------------------"

if [ "$UVLOOP_CHECK" -gt 0 ]; then
    echo -e "${YELLOW}${WARNING} 发现 uvloop - 建议重新构建镜像${NC}"
    echo "使用: ./rebuild-arm64.sh"
else
    echo -e "${GREEN}${SUCCESS} 未发现 ARM64 兼容性问题${NC}"
fi

if ! echo "$NODE_VERSION" | grep -qE "v1[6-9]|v2[0-9]"; then
    echo -e "${YELLOW}${WARNING} Node.js 版本较旧: $NODE_VERSION${NC}"
    echo "建议使用 Node.js 16+ 以获得更好的 ARM64 支持"
fi

echo ""
echo "=== 验证完成 ==="
echo ""
echo "详细分析请查看: ARM64-ARCHITECTURE-ANALYSIS.md"
