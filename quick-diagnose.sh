#!/bin/bash
# 快速诊断 Docker 容器和服务状态

echo "=== Docker 容器和服务诊断 ==="
echo ""

# 1. 检查容器状态
echo "1️⃣  检查容器状态："
echo "-------------------------------------------"
docker ps -a | grep agentscope
echo ""

# 2. 检查端口映射
echo "2️⃣  检查端口映射："
echo "-------------------------------------------"
docker port agentscope-initializr 2>/dev/null || echo "容器不存在或未运行"
echo ""

# 3. 查看容器日志（重要！）
echo "3️⃣  查看容器启动日志："
echo "-------------------------------------------"
docker logs agentscope-initializr --tail 50
echo ""

# 4. 检查容器内进程
echo "4️⃣  检查容器内运行的进程："
echo "-------------------------------------------"
docker exec agentscope-initializr ps aux 2>/dev/null || echo "无法执行"
echo ""

# 5. 测试容器内服务
echo "5️⃣  测试容器内服务："
echo "-------------------------------------------"
echo "从容器内测试 /health 端点："
docker exec agentscope-initializr curl -s http://localhost:8000/health 2>/dev/null || echo "❌ 容器内服务无响应"
echo ""

echo "从容器内测试 /docs 端点："
docker exec agentscope-initializr curl -s -o /dev/null -w "HTTP状态: %{http_code}\n" http://localhost:8000/docs 2>/dev/null || echo "❌ 容器内服务无响应"
echo ""

# 6. 从主机测试
echo "6️⃣  从主机测试服务："
echo "-------------------------------------------"
echo "测试 /health 端点："
curl -s -w "\nHTTP状态: %{http_code}\n" http://localhost:8000/health 2>/dev/null || echo "❌ 主机无法连接"
echo ""

echo "测试 /docs 端点："
curl -s -o /dev/null -w "HTTP状态: %{http_code}\n" http://localhost:8000/docs 2>/dev/null || echo "❌ 主机无法连接"
echo ""

# 7. 检查容器网络
echo "7️⃣  检查容器网络配置："
echo "-------------------------------------------"
docker inspect agentscope-initializr --format='{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} -> {{(index $conf 0).HostPort}}{{println}}{{end}}' 2>/dev/null
echo ""

# 8. 提供修复建议
echo "8️⃣  问题诊断和修复建议："
echo "-------------------------------------------"

# 检查服务是否在容器内运行
if docker exec agentscope-initializr ps aux | grep -q "python.*app.py\|gunicorn\|uvicorn"; then
    echo "✅ Python 服务进程正在运行"
else
    echo "❌ Python 服务进程未找到"
    echo ""
    echo "可能的问题："
    echo "1. 容器启动命令配置错误"
    echo "2. 容器内服务启动失败"
    echo "3. 缺少依赖或配置文件"
fi

# 检查容器内端口监听
if docker exec agentscope-initializr netstat -tlnp 2>/dev/null | grep -q ":8000"; then
    echo "✅ 容器内端口 8000 正在监听"
else
    echo "❌ 容器内端口 8000 未监听"
fi

echo ""
echo "建议的修复步骤："
echo "1. 查看完整日志：docker logs agentscope-initializr"
echo "2. 进入容器检查：docker exec -it agentscope-initializr bash"
echo "3. 手动启动服务：docker exec agentscope-initializr python /app/app.py"
echo "4. 如果配置有问题，重启容器：docker restart agentscope-initializr"
