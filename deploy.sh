#!/bin/bash
# TCD Origin - 一键部署脚本

set -e

echo "=========================================="
echo " TCD Origin - 一键部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数定义
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Docker
check_docker() {
    print_info "检查 Docker 安装..."
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        print_success "Docker 已安装: $DOCKER_VERSION"
    else
        print_error "Docker 未安装，正在安装..."
        install_docker
    fi
}

# 安装 Docker
install_docker() {
    print_info "安装 Docker..."
    curl -fsSL https://get.docker.com | sudo sh
    sudo systemctl start docker
    sudo systemctl enable docker
    print_success "Docker 安装完成"
}

# 检查 Docker Compose
check_docker_compose() {
    print_info "检查 Docker Compose..."
    if command -v docker-compose &> /dev/null; then
        COMPOSE_VERSION=$(docker-compose --version)
        print_success "Docker Compose 已安装: $COMPOSE_VERSION"
    else
        print_warning "Docker Compose 未安装，使用 Docker 内置 Compose"
    fi
}

# 创建环境变量文件
setup_env() {
    print_info "检查环境变量配置..."
    if [ ! -f .env ]; then
        if [ -f .env.docker ]; then
            print_info "复制 .env.docker 为 .env"
            cp .env.docker .env
            print_warning "请编辑 .env 文件，配置必要的环境变量"
        else
            print_warning "未找到 .env 配置文件"
        fi
    else
        print_success "环境变量文件已存在"
    fi
}

# 构建 Docker 镜像
build_images() {
    print_info "构建 Docker 镜像..."
    docker-compose build
    print_success "镜像构建完成"
}

# 启动服务
start_services() {
    print_info "启动服务..."
    docker-compose up -d
    print_success "服务启动完成"
}

# 等待服务就绪
wait_for_services() {
    print_info "等待服务就绪..."
    
    # 等待 API 服务
    for i in {1..30}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            print_success "API 服务已就绪"
            break
        fi
        echo -n "."
        sleep 1
    done
    echo ""
    
    # 等待 Web 服务
    for i in {1..30}; do
        if curl -f http://localhost:7860 &> /dev/null; then
            print_success "Web 服务已就绪"
            break
        fi
        echo -n "."
        sleep 1
    done
    echo ""
}

# 显示服务状态
show_status() {
    echo ""
    echo "=========================================="
    echo " 服务状态"
    echo "=========================================="
    docker-compose ps
    echo ""
    echo "=========================================="
    echo " 访问地址"
    echo "=========================================="
    echo " API 文档: ${GREEN}http://localhost:8000/docs${NC}"
    echo " Web 界面: ${GREEN}http://localhost:7860${NC}"
    echo " 健康检查: ${GREEN}http://localhost:8000/health${NC}"
    echo ""
}

# 主函数
main() {
    echo ""
    print_info "开始 TCD Origin 部署..."
    echo ""
    
    # 检查 Docker
    check_docker
    check_docker_compose
    
    # 设置环境变量
    setup_env
    
    # 构建镜像
    build_images
    
    # 启动服务
    start_services
    
    # 等待服务就绪
    wait_for_services
    
    # 显示状态
    show_status
    
    print_success "部署完成！"
    echo ""
    echo "=========================================="
    echo " 后续步骤"
    echo "=========================================="
    echo "1. 编辑 .env 文件配置环境变量（可选）"
    echo "2. 访问 Web 界面开始使用"
    echo "3. 查看 API 文档: http://localhost:8000/docs"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
    echo "  重新构建: docker-compose build --no-cache"
    echo ""
}

# 执行主函数
main
