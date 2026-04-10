#!/bin/bash

#############################################################################
# AgentScope Initializr - ARM64 快速安装脚本
# 适用于 Linux ARM64 系统的自动化安装
#############################################################################

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

print_step() {
    echo -e "${BLUE}${BOLD}[步骤] $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ 错误: $1${NC}"
}

# 检查是否为 ARM64 架构
check_architecture() {
    print_step "检查系统架构"

    local arch=$(uname -m)
    if [ "$arch" != "aarch64" ] && [ "$arch" != "arm64" ]; then
        print_error "此脚本仅支持 ARM64 架构，当前架构: $arch"
        exit 1
    fi

    print_success "架构检查通过: $arch"
}

# 检查 Docker
check_docker() {
    print_step "检查 Docker"

    if ! command -v docker &> /dev/null; then
        echo "Docker 未安装，正在安装 Docker..."

        # 检测 Linux 发行版
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
        else
            print_error "无法检测操作系统"
            exit 1
        fi

        case $OS in
            ubuntu|debian)
                echo "在 Ubuntu/Debian 系统上安装 Docker..."
                curl -fsSL https://get.docker.com -o get-docker.sh
                sudo sh get-docker.sh
                sudo usermod -aG docker $USER
                rm get-docker.sh
                ;;
            centos|rhel|fedora)
                echo "在 CentOS/RHEL/Fedora 系统上安装 Docker..."
                sudo yum install -y docker
                sudo systemctl start docker
                sudo systemctl enable docker
                sudo usermod -aG docker $USER
                ;;
            *)
                print_error "不支持的操作系统: $OS"
                print_error "请手动安装 Docker: https://docs.docker.com/get-docker/"
                exit 1
                ;;
        esac

        print_success "Docker 安装完成"
        echo -e "${YELLOW}请注销并重新登录以使 Docker 组权限生效${NC}"
    else
        print_success "Docker 已安装: $(docker --version)"
    fi
}

# 检查 Docker Compose
check_docker_compose() {
    print_step "检查 Docker Compose"

    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose 未安装，正在安装..."

        # 获取最新版本
        local COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)

        sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose

        print_success "Docker Compose 安装完成"
    else
        print_success "Docker Compose 已安装: $(docker-compose --version)"
    fi
}

# 创建项目目录
setup_project_directory() {
    print_step "设置项目目录"

    local INSTALL_DIR="/opt/agentscope-initializr"

    if [ ! -d "$INSTALL_DIR" ]; then
        sudo mkdir -p "$INSTALL_DIR"
        sudo chown $USER:$USER "$INSTALL_DIR"
        print_success "创建项目目录: $INSTALL_DIR"
    else
        print_success "项目目录已存在: $INSTALL_DIR"
    fi

    echo "$INSTALL_DIR"
}

# 下载部署脚本
download_scripts() {
    local install_dir=$1
    print_step "下载部署脚本"

    # 如果是本地文件，直接复制
    if [ -f "./deploy-arm64.sh" ]; then
        cp ./deploy-arm64.sh "$install_dir/"
        cp ./health-check.sh "$install_dir/"
        print_success "脚本文件已复制"
    else
        print_success "跳过脚本下载（假设已存在）"
    fi

    chmod +x "$install_dir/deploy-arm64.sh"
    chmod +x "$install_dir/health-check.sh"
}

# 查找镜像文件
find_image() {
    print_step "查找 ARM64 镜像文件"

    local image_files=(
        "./agentscope-initializr-arm64.tar.gz"
        "/tmp/agentscope-initializr-arm64.tar.gz"
        "~/*/agentscope-initializr-arm64.tar.gz"
    )

    for image_file in "${image_files[@]}"; do
        expanded_path=$(eval echo "$image_file")
        if [ -f "$expanded_path" ]; then
            print_success "找到镜像文件: $expanded_path"
            echo "$expanded_path"
            return 0
        fi
    done

    echo ""
}

# 运行部署
run_deployment() {
    local install_dir=$1
    local image_file=$2

    cd "$install_dir"

    if [ -n "$image_file" ]; then
        print_step "开始部署服务"

        if [ "$image_file" != "$install_dir/agentscope-initializr-arm64.tar.gz" ]; then
            cp "$image_file" "$install_dir/"
        fi

        ./deploy-arm64.sh
    else
        print_step "准备部署环境"

        echo -e "${YELLOW}未找到镜像文件${NC}"
        echo "请将 agentscope-initializr-arm64.tar.gz 放置到以下位置之一:"
        echo "  - ./agentscope-initializr-arm64.tar.gz"
        echo "  - /tmp/agentscope-initializr-arm64.tar.gz"
        echo ""
        echo "然后运行: cd $install_dir && ./deploy-arm64.sh"
    fi
}

# 设置系统服务（可选）
setup_system_service() {
    print_step "设置系统服务"

    local install_dir=$1
    local service_file="/etc/systemd/system/agentscope.service"

    if [ -f "./agentscope.service" ]; then
        # 替换工作目录
        sed "s|/opt/agentscope-initializr|$install_dir|g" ./agentscope.service | sudo tee "$service_file" > /dev/null

        sudo systemctl daemon-reload
        print_success "系统服务已配置"
        echo "启用服务: sudo systemctl enable agentscope.service"
        echo "启动服务: sudo systemctl start agentscope.service"
    else
        print_success "跳过系统服务配置"
    fi
}

# 显示后续步骤
show_next_steps() {
    local install_dir=$1

    echo -e "\n${GREEN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}  安装完成！${NC}"
    echo -e "${GREEN}${BOLD}═══════════════════════════════════════════════════════════${NC}\n"

    echo "项目位置: $install_dir"
    echo ""
    echo "接下来的步骤:"
    echo "  1. cd $install_dir"
    echo "  2. ./deploy-arm64.sh  # 如果还没有部署"
    echo "  3. ./manage.sh status  # 检查服务状态"
    echo "  4. ./health-check.sh   # 运行健康检查"
    echo ""
    echo "管理服务:"
    echo "  cd $install_dir"
    echo "  ./manage.sh            # 查看所有管理命令"
    echo ""
    echo "访问服务:"
    echo "  http://$(hostname -I | awk '{print $1}'):8000"
    echo ""
    echo -e "${YELLOW}提示: 如果还没有镜像文件，请先将 agentscope-initializr-arm64.tar.gz 复制到 $install_dir${NC}"
}

# 主函数
main() {
    echo -e "${BLUE}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}${BOLD}  AgentScope Initializr - ARM64 快速安装${NC}"
    echo -e "${BLUE}${BOLD}═══════════════════════════════════════════════════════════${NC}\n"

    # 检查架构
    check_architecture

    # 检查依赖
    check_docker
    check_docker_compose

    # 设置项目目录
    INSTALL_DIR=$(setup_project_directory)

    # 下载脚本
    download_scripts "$INSTALL_DIR"

    # 查找镜像
    IMAGE_FILE=$(find_image)

    # 运行部署
    run_deployment "$INSTALL_DIR" "$IMAGE_FILE"

    # 设置系统服务（询问用户）
    echo -e "\n${YELLOW}是否设置为系统服务? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        setup_system_service "$INSTALL_DIR"
    fi

    # 显示后续步骤
    show_next_steps "$INSTALL_DIR"
}

# 执行主函数
main
