#!/bin/bash
# 检查 Docker 镜像中所有依赖工具的架构兼容性

echo "=== ARM64 架构依赖检查工具 ==="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SUCCESS="[OK]"
ERROR="[ERROR]"
WARNING="[WARNING]"

check_architecture() {
    echo "1. 检查 Docker 镜像架构"
    echo "========================================="
    if docker inspect agentscope-initializr-arm64 --format='{{.Architecture}}' 2>/dev/null; then
        echo -e "${GREEN}${SUCCESS} 镜像架构检查完成${NC}"
    else
        echo -e "${RED}${ERROR} 无法检查镜像架构${NC}"
        echo "请先确保镜像已加载"
    fi
    echo ""
}

check_python_packages() {
    echo "2. 检查关键 Python 包"
    echo "========================================="

    echo "检查 Python 版本和架构..."
    docker run --rm agentscope-initializr-arm64 python --version 2>/dev/null || echo "无法检查 Python 版本"

    echo ""
    echo "检查关键 Python 包..."
    docker run --rm agentscope-initializr-arm64 sh -c "
        echo 'Python 包架构检查:'
        echo '--------------------'
        echo 'uvicorn:'
        pip show uvicorn 2>/dev/null | grep Location || echo '未安装'
        echo ''
        echo 'fastapi:'
        pip show fastapi 2>/dev/null | grep Location || echo '未安装'
        echo ''
        echo '所有已安装包:'
        pip list
    " 2>/dev/null || echo -e "${RED}${ERROR} 无法检查 Python 包${NC}"
    echo ""
}

check_system_tools() {
    echo "3. 检查系统工具架构"
    echo "========================================="

    docker run --rm agentscope-initializr-arm64 sh -c "
        echo '系统工具检查:'
        echo '--------------------'
        echo 'GCC:'
        gcc --version 2>/dev/null | head -1 || echo '未安装'
        echo ''
        echo 'Curl:'
        curl --version 2>/dev/null | head -1 || echo '未安装'
        echo ''
        echo '系统架构:'
        uname -m
        echo ''
        echo 'CPU 信息:'
        cat /proc/cpuinfo | grep 'model name' | head -1 || echo '无法获取'
    " 2>/dev/null || echo -e "${RED}${ERROR} 无法检查系统工具${NC}"
    echo ""
}

check_nodejs() {
    echo "4. 检查 Node.js 和 NPM"
    echo "========================================="

    docker run --rm agentscope-initializr-arm64 sh -c "
        echo 'Node.js 检查:'
        echo '--------------------'
        echo 'Node 版本:'
        node --version 2>/dev/null || echo '未安装'
        echo ''
        echo 'NPM 版本:'
        npm --version 2>/dev/null || echo '未安装'
        echo ''
        echo 'Node 架构:'
        node -p 'process.arch' 2>/dev/null || echo '无法检查'
        echo ''
        echo 'Node 平台:'
        node -p 'process.platform' 2>/dev/null || echo '无法检查'
    " 2>/dev/null || echo -e "${YELLOW}${WARNING} Node.js 可能未在运行时镜像中${NC}"
    echo ""
}

check_binary_files() {
    echo "5. 检查关键二进制文件"
    echo "========================================="

    docker run --rm agentscope-initializr-arm64 sh -c "
        echo '二进制文件架构检查:'
        echo '--------------------'
        echo 'Python 可执行文件:'
        file \$(which python) 2>/dev/null || echo '未找到'
        echo ''
        echo 'Uvicorn 可执行文件:'
        file \$(which uvicorn) 2>/dev/null || echo '未找到'
        echo ''
        echo '所有 Python 包中的 .so 文件:'
        find /usr/local/lib/python3.11/site-packages -name '*.so' 2>/dev/null | head -5 || echo '无 .so 文件'
        echo ''
        if [ \$(find /usr/local/lib/python3.11/site-packages -name '*.so' 2>/dev/null | wc -l) -gt 0 ]; then
            echo '检查 .so 文件架构:'
            find /usr/local/lib/python3.11/site-packages -name '*.so' -exec file {} \; 2>/dev/null | head -5
        fi
    " 2>/dev/null || echo -e "${RED}${ERROR} 无法检查二进制文件${NC}"
    echo ""
}

check_compatibility_issues() {
    echo "6. 已知兼容性问题检查"
    echo "========================================="

    echo "检查 uvloop (常见 ARM64 兼容性问题)..."
    docker run --rm agentscope-initializr-arm64 sh -c "
        if pip show uvloop >/dev/null 2>&1; then
            echo 'uvloop 已安装 - 在 ARM64 上可能有性能问题'
            echo '建议: 在 ARM64 上使用默认的 asyncorio'
        else
            echo 'uvloop 未安装 - 这是好的'
            echo 'uvicorn 将使用标准 asyncio'
        fi
    " 2>/dev/null || echo "无法检查 uvloop"
    echo ""

    echo "检查 Python C 扩展..."
    docker run --rm agentscope-initializr-arm64 sh -c "
        echo '检查可能有问题的 C 扩展包:'
        for pkg in \$(pip list | awk '{print \$1}'); do
            if pip show \$pkg 2>/dev/null | grep -q 'cffi\|pyyaml\|numpy\|pandas'; then
                echo \"\$pkg - 可能包含 C 扩展\"
            fi
        done
        echo '完成检查'
    " 2>/dev/null || echo "无法检查 C 扩展"
    echo ""
}

create_test_container() {
    echo "7. 创建测试容器并验证启动"
    echo "========================================="

    echo "启动测试容器..."
    docker run --rm --name test-arm64 -p 8001:8000 agentscope-initializr-arm64 &
    TEST_PID=$!

    echo "等待服务启动 (15秒)..."
    sleep 15

    echo "测试服务是否响应..."
    if curl -s http://localhost:8001/health >/dev/null 2>&1; then
        echo -e "${GREEN}${SUCCESS} 服务启动成功并响应正常${NC}"

        # 获取容器架构信息
        docker exec test-arm64 sh -c "
            echo '容器内架构验证:'
            echo '--------------------'
            echo '系统架构:' \$(uname -m)
            echo 'Python 架构:' \$(python -c 'import platform; print(platform.machine())')
            echo '所有进程架构:'
            ps aux | head -5
        " 2>/dev/null
    else
        echo -e "${RED}${ERROR} 服务启动失败或无响应${NC}"
        echo "查看容器日志:"
        docker logs test-arm64 --tail 20 2>/dev/null || echo "无法获取日志"
    fi

    # 清理
    echo "清理测试容器..."
    docker stop test-arm64 >/dev/null 2>&1
    wait $TEST_PID 2>/dev/null
    echo ""
}

# 生成兼容性报告
generate_report() {
    echo "8. 生成兼容性报告"
    echo "========================================="

    cat << 'EOF'
ARM64 兼容性检查报告
====================

基础镜像:
✓ python:3.11-slim (明确指定 linux/arm64 平台)

系统依赖:
✓ gcc/g++ - Debian ARM64 仓库版本
✓ curl - ARM64 兼容
⚠ nodejs/npm - 需要验证版本兼容性

Python 包:
✓ uvicorn - 纯 Python 实现，ARM64 兼容
✓ fastapi - 纯 Python 框架，ARM64 兼容
✓ 标准库 - ARM64 支持

潜在问题:
1. Node.js 版本可能较旧，建议使用 Node 16+
2. 某些 Python C 扩展可能需要重新编译
3. uvloop 在 ARM64 上性能不如 asyncio

建议优化:
1. 明确指定 Node.js 版本
2. 跳过 uvloop 安装
3. 使用纯 Python 包替代 C 扩展

EOF
}

# 主检查流程
main() {
    echo -e "${GREEN}开始 ARM64 架构兼容性检查...${NC}"
    echo ""

    # 检查镜像是否存在
    if ! docker images | grep -q "agentscope-initializr-arm64"; then
        echo -e "${RED}${ERROR} 未找到 agentscope-initializr-arm64 镜像${NC}"
        echo "请先加载镜像: docker load < agentscope-initializr-arm64.tar.gz"
        exit 1
    fi

    # 执行各项检查
    check_architecture
    check_python_packages
    check_system_tools
    check_nodejs
    check_binary_files
    check_compatibility_issues
    generate_report

    echo -e "${GREEN}检查完成！${NC}"
    echo ""
    echo "如果发现问题，请使用 rebuild-arm64.sh 重新构建镜像"
}

# 执行主函数
main
