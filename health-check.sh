#!/bin/bash

#############################################################################
# AgentScope Initializr - 健康检查脚本
# 用于监控服务状态和性能指标
#############################################################################

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# 配置
BASE_URL="${HEALTH_CHECK_URL:-http://localhost:8000}"
TIMEOUT=5
MAX_RETRIES=3

# 状态标识（使用ASCII字符以确保兼容性）
SUCCESS="[OK]"
ERROR="[ERROR]"
WARNING="[WARNING]"
INFO="[INFO]"

# 函数：打印状态
print_status() {
    local status=$1
    local message=$2

    case $status in
        "ok")
            echo -e "${GREEN}${SUCCESS} $message${NC}"
            ;;
        "error")
            echo -e "${RED}${ERROR} $message${NC}"
            ;;
        "warning")
            echo -e "${YELLOW}${WARNING} $message${NC}"
            ;;
        "info")
            echo -e "${PURPLE}${INFO} $message${NC}"
            ;;
    esac
}

# 函数：检查端点
check_endpoint() {
    local endpoint=$1
    local description=$2
    local url="${BASE_URL}${endpoint}"

    echo -e "\n${BLUE}检查: $description${NC}"
    echo "URL: $url"

    local response=$(curl -s -w "\n%{http_code}" --connect-timeout $TIMEOUT "$url" 2>/dev/null)
    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" = "200" ]; then
        print_status "ok" "状态正常 (HTTP $http_code)"
        if [ -n "$body" ]; then
            echo "响应: $body" | jq '.' 2>/dev/null || echo "响应: $body"
        fi
        return 0
    else
        print_status "error" "异常响应 (HTTP $http_code)"
        return 1
    fi
}

# 函数：检查容器状态
check_container() {
    echo -e "\n${BLUE}检查: Docker 容器状态${NC}"

    local container_name="agentscope-initializr"
    local container_status=$(docker inspect -f '{{.State.Status}}' "$container_name" 2>/dev/null)

    if [ "$container_status" = "running" ]; then
        print_status "ok" "容器运行中"

        # 获取容器信息
        local uptime=$(docker inspect -f '{{.State.StartedAt}}' "$container_name" | xargs date -d 2>/dev/null || echo "未知")
        local health=$(docker inspect -f '{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "无健康检查")

        echo "启动时间: $uptime"
        echo "健康状态: $health"

        # 资源使用
        echo -e "\n${PURPLE}资源使用情况:${NC}"
        docker stats "$container_name" --no-stream --format "table CPU: {{.CPUPerc}}\n内存: {{.MemUsage}}\n网络: {{.NetIO}}\n块I/O: {{.BlockIO}}"
    else
        print_status "error" "容器未运行 (状态: $container_status)"
        return 1
    fi
}

# 函数：检查端口
check_port() {
    echo -e "\n${BLUE}检查: 端口连接${NC}"

    local port=8000
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        print_status "ok" "端口 $port 正在监听"
    else
        print_status "warning" "无法检测端口 $port"
    fi

    # 测试端口连接
    if timeout 1 bash -c "cat < /dev/null > /dev/tcp/localhost/$port" 2>/dev/null; then
        print_status "ok" "端口 $port 连接正常"
    else
        print_status "error" "端口 $port 无法连接"
    fi
}

# 函数：性能测试
performance_test() {
    echo -e "\n${BLUE}性能测试${NC}"

    local test_url="${BASE_URL}/health"
    echo "测试端点: $test_url"

    # 响应时间
    local response_time=$(curl -o /dev/null -s -w '%{time_total}' "$test_url")
    print_status "info" "响应时间: ${response_time}s"

    if (( $(echo "$response_time < 0.5" | bc -l) )); then
        print_status "ok" "响应时间优秀"
    elif (( $(echo "$response_time < 1.0" | bc -l) )); then
        print_status "warning" "响应时间一般"
    else
        print_status "error" "响应时间过慢"
    fi

    # 并发测试（简单）
    echo -e "\n${PURPLE}并发测试 (10个并发请求):${NC}"
    local start_time=$(date +%s.%N)

    for i in {1..10}; do
        curl -s "$test_url" > /dev/null &
    done

    wait

    local end_time=$(date +%s.%N)
    local total_time=$(echo "$end_time - $start_time" | bc)
    print_status "info" "完成 10 个请求，总耗时: ${total_time}s"
}

# 函数：日志分析
analyze_logs() {
    echo -e "\n${BLUE}最近的日志 (最后10行)${NC}"

    if docker logs agentscope-initializr --tail 10 2>/dev/null; then
        print_status "ok" "日志获取成功"
    else
        print_status "warning" "无法获取日志"
    fi

    # 检查错误日志
    echo -e "\n${PURPLE}错误检查:${NC}"
    local error_count=$(docker logs agentscope-initializr --tail 100 2>&1 | grep -i "error\|exception\|failed" | wc -l)

    if [ "$error_count" -eq 0 ]; then
        print_status "ok" "最近100行日志中没有发现错误"
    else
        print_status "warning" "发现 $error_count 个错误"
    fi
}

# 函数：生成报告
generate_report() {
    echo -e "\n${BOLD}${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${GREEN}  健康检查报告${NC}"
    echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════════════${NC}\n"

    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "检查时间: $timestamp"
    echo "服务地址: $BASE_URL"

    # 主要检查
    local health_ok=1

    check_endpoint "/health" "健康检查端点" || health_ok=0
    check_endpoint "/docs" "API文档" || health_ok=0
    check_container || health_ok=0
    check_port || health_ok=0

    # 可选检查
    if [ "$1" = "--full" ]; then
        performance_test
        analyze_logs
    fi

    # 总结
    echo -e "\n${BOLD}${GREEN}═══════════════════════════════════════════════════════════${NC}"

    if [ $health_ok -eq 1 ]; then
        echo -e "${GREEN}${BOLD}总体状态: 健康 [OK]${NC}"
        return 0
    else
        echo -e "${RED}${BOLD}总体状态: 异常 [ERROR]${NC}"
        return 1
    fi
}

# 函数：持续监控
continuous_monitor() {
    echo -e "${PURPLE}持续监控模式 (Ctrl+C 退出)${NC}\n"

    local iteration=0
    while true; do
        ((iteration++))
        echo -e "${BOLD}[监控周期 #$iteration] $(date '+%H:%M:%S')${NC}"

        if check_endpoint "/health" "服务健康检查"; then
            print_status "ok" "服务运行正常"
        else
            print_status "error" "服务异常"
            # 可选：发送告警
            # send_alert "AgentScope Initializr 服务异常"
        fi

        echo -e "${YELLOW}───────────────────────────────────────────────────────${NC}"
        sleep 30
    done
}

# 函数：显示帮助
show_help() {
    echo "AgentScope Initializr - 健康检查脚本"
    echo ""
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --full       完整检查（包括性能测试和日志分析）"
    echo "  --monitor    持续监控模式（每30秒检查一次）"
    echo "  --help       显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  HEALTH_CHECK_URL  服务地址 (默认: http://localhost:8000)"
    echo ""
    echo "示例:"
    echo "  $0                    # 基本健康检查"
    echo "  $0 --full             # 完整检查"
    echo "  $0 --monitor          # 持续监控"
    echo "  HEALTH_CHECK_URL=http://remote-server:8000 $0"
}

# 主函数
main() {
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}  AgentScope Initializr - 健康检查工具${NC}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════${NC}"

    case "$1" in
        --full)
            generate_report "--full"
            ;;
        --monitor)
            continuous_monitor
            ;;
        --help|-h)
            show_help
            ;;
        "")
            generate_report
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
