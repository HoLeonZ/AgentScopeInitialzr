#!/bin/bash

#############################################################################
# AgentScope Initializr - ARM64 部署脚本
# 优雅的自动化部署解决方案
#############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# 状态标识（使用ASCII字符以确保兼容性）
SUCCESS="[OK]"
ERROR="[ERROR]"
WARNING="[WARNING]"
INFO="[INFO]"
PROCESSING="[PROCESSING]"

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_FILE="agentscope-initializr-arm64.tar.gz"
COMPOSE_FILE="docker-compose.arm64.yml"
OUTPUT_DIR="./output"
LOG_FILE="deploy-$(date +%Y%m%d-%H%M%S).log"

# 函数：打印带颜色的消息
print_header() {
    echo -e "\n${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}${BOLD}  $1${NC}"
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_step() {
    echo -e "${BLUE}${BOLD}[步骤] $1${NC}"
}

print_info() {
    echo -e "${PURPLE}${INFO} $1${NC}"
}

print_success() {
    echo -e "${GREEN}${SUCCESS} $1${NC}"
}

print_error() {
    echo -e "${RED}${ERROR} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING} $1${NC}"
}

print_progress() {
    echo -ne "${CYAN}${PROCESSING} $1...${NC}\r"
}

# 函数：检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 函数：检查依赖
check_dependencies() {
    print_step "检查系统依赖"

    local missing_deps=()

    if ! command_exists docker; then
        missing_deps+=("docker")
    fi

    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "缺少以下依赖: ${missing_deps[*]}"
        print_info "请安装缺少的依赖后重试"
        exit 1
    fi

    print_success "所有依赖已就绪"

    # 检查 Docker 是否运行
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker 服务未运行"
        print_info "请启动 Docker 服务: sudo systemctl start docker"
        exit 1
    fi

    print_success "Docker 服务运行正常"
}

# 函数：查找镜像文件
find_image_file() {
    print_step "查找 ARM64 镜像文件"

    local possible_paths=(
        "$SCRIPT_DIR/$IMAGE_FILE"
        "$SCRIPT_DIR/../$IMAGE_FILE"
        "/tmp/$IMAGE_FILE"
        "./$IMAGE_FILE"
    )

    for path in "${possible_paths[@]}"; do
        if [ -f "$path" ]; then
            IMAGE_FILE_PATH="$path"
            print_success "找到镜像文件: $path"
            return 0
        fi
    done

    print_error "无法找到镜像文件: $IMAGE_FILE"
    print_info "请确保 $IMAGE_FILE 文件存在于以下位置之一:"
    for path in "${possible_paths[@]}"; do
        echo "  - $path"
    done
    exit 1
}

# 函数：加载镜像
load_image() {
    print_step "加载 Docker 镜像"

    print_info "镜像文件: $IMAGE_FILE_PATH"
    print_info "这可能需要几分钟时间..."

    if docker load -i "$IMAGE_FILE_PATH"; then
        print_success "镜像加载成功"

        # 显示加载的镜像信息
        echo -e "\n${CYAN}可用的镜像:${NC}"
        docker images | grep agentscope
    else
        print_error "镜像加载失败"
        exit 1
    fi
}

# 函数：获取镜像名称
get_image_name() {
    local image_info=$(docker images | grep agentscope | head -1)
    if [ -z "$image_info" ]; then
        print_error "无法找到加载的镜像"
        exit 1
    fi

    IMAGE_NAME=$(echo "$image_info" | awk '{print $1}')
    IMAGE_TAG=$(echo "$image_info" | awk '{print $2}')

    if [ "$IMAGE_TAG" == "<none>" ]; then
        IMAGE_TAG="latest"
        # 重新标记镜像
        docker tag "$IMAGE_NAME" "${IMAGE_NAME}:latest"
        IMAGE_NAME="${IMAGE_NAME}:latest"
    else
        IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
    fi

    print_success "使用镜像: $IMAGE_NAME"
}

# 函数：创建必要的目录
create_directories() {
    print_step "创建必要的目录"

    mkdir -p "$OUTPUT_DIR"
    mkdir -p logs

    print_success "目录创建完成"
}

# 函数：生成 docker-compose 文件
generate_compose_file() {
    print_step "生成 Docker Compose 配置"

    cat > "$COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  agentscope-initializr:
    image: ${IMAGE_NAME}
    container_name: agentscope-initializr
    ports:
      - "8000:8000"
    volumes:
      # 持久化输出目录
      - ./output:/app/output
      # 日志目录（可选）
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=info
      - OUTPUT_DIR=/app/output
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    # 资源限制（可选）
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    # 日志配置
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  default:
    name: agentscope-network
EOF

    # 替换镜像名称
    sed -i.bak "s|\${IMAGE_NAME}|$IMAGE_NAME|g" "$COMPOSE_FILE"
    rm -f "${COMPOSE_FILE}.bak"

    print_success "配置文件已生成: $COMPOSE_FILE"
}

# 函数：启动服务
start_services() {
    print_step "启动服务"

    if docker-compose -f "$COMPOSE_FILE" up -d; then
        print_success "服务启动成功"
    else
        print_error "服务启动失败"
        exit 1
    fi
}

# 函数：等待服务就绪
wait_for_service() {
    print_step "等待服务就绪"

    local max_attempts=30
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
            print_success "服务已就绪"
            return 0
        fi

        print_progress "等待服务启动 ($((attempt + 1))/$max_attempts)"
        sleep 2
        ((attempt++))
    done

    print_warning "服务启动超时，但容器可能仍在初始化"
    print_info "请使用 'docker-compose logs -f' 查看详细日志"
}

# 函数：显示服务信息
show_service_info() {
    print_header "部署完成"

    # 获取本机IP
    local ip_address=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$ip_address" ]; then
        ip_address="your-server-ip"
    fi

    echo -e "${GREEN}${BOLD}[SUCCESS] AgentScope Initializr 已成功部署!${NC}\n"

    echo -e "${BOLD}服务信息:${NC}"
    echo -e "  状态: ${BLUE}$(docker-compose -f "$COMPOSE_FILE" ps | grep agentscope | awk '{print $NF}')${NC}"
    echo -e "  容器: ${BLUE}agentscope-initializr${NC}"
    echo -e "  镜像: ${BLUE}$IMAGE_NAME${NC}"

    echo -e "\n${BOLD}访问地址:${NC}"
    echo -e "  本地: ${CYAN}http://localhost:8000${NC}"
    echo -e "  远程: ${CYAN}http://$ip_address:8000${NC}"
    echo -e "  API文档: ${CYAN}http://$ip_address:8000/docs${NC}"
    echo -e "  健康检查: ${CYAN}http://$ip_address:8000/health${NC}"

    echo -e "\n${BOLD}常用命令:${NC}"
    echo -e "  查看日志: ${YELLOW}docker-compose -f $COMPOSE_FILE logs -f${NC}"
    echo -e "  停止服务: ${YELLOW}docker-compose -f $COMPOSE_FILE down${NC}"
    echo -e "  重启服务: ${YELLOW}docker-compose -f $COMPOSE_FILE restart${NC}"
    echo -e "  查看状态: ${YELLOW}docker-compose -f $COMPOSE_FILE ps${NC}"

    echo -e "\n${BOLD}文件位置:${NC}"
    echo -e "  配置文件: ${CYAN}$COMPOSE_FILE${NC}"
    echo -e "  输出目录: ${CYAN}$OUTPUT_DIR${NC}"
    echo -e "  日志目录: ${CYAN}logs/${NC}"
}

# 函数：生成管理脚本
generate_management_script() {
    cat > "manage.sh" << 'EOF'
#!/bin/bash

# AgentScope Initializr 管理脚本
# 使用方法: ./manage.sh [command]

COMPOSE_FILE="docker-compose.arm64.yml"

case "$1" in
    start|up)
        echo "启动服务..."
        docker-compose -f "$COMPOSE_FILE" up -d
        ;;
    stop|down)
        echo "停止服务..."
        docker-compose -f "$COMPOSE_FILE" down
        ;;
    restart)
        echo "重启服务..."
        docker-compose -f "$COMPOSE_FILE" restart
        ;;
    logs|log)
        echo "查看日志..."
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    status|ps)
        echo "服务状态..."
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
    health|check)
        echo "健康检查..."
        curl -s http://localhost:8000/health | jq '.' || echo "服务未就绪"
        ;;
    update)
        echo "更新服务..."
        read -p "请输入新的镜像文件路径: " image_file
        if [ -f "$image_file" ]; then
            docker-compose -f "$COMPOSE_FILE" down
            docker load -i "$image_file"
            ./manage.sh update-image
            docker-compose -f "$COMPOSE_FILE" up -d
        else
            echo "文件不存在: $image_file"
        fi
        ;;
    shell|sh)
        echo "进入容器..."
        docker exec -it agentscope-initializr /bin/bash
        ;;
    clean)
        echo "清理服务和数据..."
        read -p "确定要删除所有数据吗? (y/N): " confirm
        if [ "$confirm" = "y" ]; then
            docker-compose -f "$COMPOSE_FILE" down -v
            rm -rf output/*
            echo "清理完成"
        else
            echo "取消清理"
        fi
        ;;
    *)
        echo "AgentScope Initializr 管理脚本"
        echo ""
        echo "使用方法: ./manage.sh [command]"
        echo ""
        echo "可用命令:"
        echo "  start, up      - 启动服务"
        echo "  stop, down     - 停止服务"
        echo "  restart        - 重启服务"
        echo "  logs, log      - 查看日志"
        echo "  status, ps     - 查看状态"
        echo "  health, check  - 健康检查"
        echo "  shell, sh      - 进入容器"
        echo "  clean          - 清理服务和数据"
        echo ""
        ;;
esac
EOF

    chmod +x "manage.sh"
    print_success "管理脚本已生成: manage.sh"
}

# 函数：清理临时文件
cleanup() {
    print_step "清理临时文件"
    # 可选的清理操作
}

# 主流程
main() {
    print_header "AgentScope Initializr - ARM64 部署"

    # 执行部署步骤
    check_dependencies
    find_image_file
    load_image
    get_image_name
    create_directories
    generate_compose_file
    generate_management_script
    start_services
    wait_for_service
    show_service_info
    cleanup

    print_success "部署流程完成！"
}

# 信号处理
trap cleanup EXIT

# 执行主流程
main
