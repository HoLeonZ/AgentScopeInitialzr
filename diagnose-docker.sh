#!/bin/bash
# Docker 诊断和修复脚本

echo "=== Docker 诊断和修复工具 ==="
echo ""

# 1. 检查 Docker 进程
echo "1️⃣  检查 Docker 相关进程："
echo "-------------------------------------------"
ps aux | grep -E "docker|containerd" | grep -v grep
echo ""

# 2. 检查 Docker socket 状态
echo "2️⃣  检查 Docker socket 状态："
echo "-------------------------------------------"
if [ -S /var/run/docker.sock ]; then
    echo "✅ Docker socket 存在"
    ls -l /var/run/docker.sock
    echo ""
    echo "Socket 详情："
    stat /var/run/docker.sock
else
    echo "❌ Docker socket 不存在"
fi
echo ""

# 3. 检查端口占用
echo "3️⃣  检查 Docker 相关端口："
echo "-------------------------------------------"
netstat -tlnp 2>/dev/null | grep -E "2375|2376" || ss -tlnp 2>/dev/null | grep -E "2375|2376"
echo ""

# 4. 检查 Docker 锁文件
echo "4️⃣  检查 Docker 锁文件："
echo "-------------------------------------------"
ls -l /var/lib/docker/*.json 2>/dev/null || echo "没有找到锁文件"
echo ""

# 5. 提供修复建议
echo "5️⃣  修复建议："
echo "-------------------------------------------"
echo "如果您看到有 dockerd 或 containerd 进程在运行，"
echo "请选择以下方案之一："
echo ""
echo "方案A: 清理并重启 Docker（推荐）"
echo "  sudo pkill -9 dockerd containerd dockerd-rootless.sh"
echo "  sudo rm -f /var/run/docker.sock /var/lib/docker/*.json"
echo "  sudo dockerd &"
echo ""
echo "方案B: 使用现有的 Docker 守护进程"
echo "  如果已经有 dockerd 在运行，检查您的用户权限："
echo "  sudo usermod -aG docker \$USER"
echo "  newgrp docker"
echo ""
echo "方案C: 检查为什么无法连接到现有守护进程"
echo "  sudo ls -l /var/run/docker.sock"
echo "  如果 socket 存在但权限不对："
echo "  sudo chmod 666 /var/run/docker.sock"
echo ""

# 6. 一键修复选项
read -p "是否执行自动清理和重启？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔧 执行清理和重启..."

    # 停止所有 Docker 进程
    echo "停止 Docker 相关进程..."
    sudo pkill -9 dockerd 2>/dev/null
    sudo pkill -9 containerd 2>/dev/null
    sudo pkill -9 containerd-shim 2>/dev/null
    sleep 2

    # 清理 socket
    echo "清理旧的 socket..."
    sudo rm -f /var/run/docker.sock

    # 启动 Docker 守护进程
    echo "启动 Docker 守护进程..."
    sudo dockerd > /tmp/dockerd.log 2>&1 &
    DOCKERD_PID=$!

    echo "等待 Docker 启动..."
    sleep 5

    # 验证
    if sudo docker version > /dev/null 2>&1; then
        echo "✅ Docker 启动成功！"
        sudo docker version
        echo ""
        echo "Docker 守护进程 PID: $DOCKERD_PID"
    else
        echo "❌ Docker 启动失败，查看日志："
        echo "-------------------------------------------"
        sudo tail -30 /tmp/dockerd.log
    fi
fi
