#!/bin/bash

# 古文字破译系统 - 一键部署脚本
# 集成自动配置和部署功能

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo ""
    echo -e "${CYAN}======================================"
    echo -e "${CYAN}$1"
    echo -e "${CYAN}======================================"
    echo ""
}

# 检查 Docker 和 Docker Compose
check_dependencies() {
    log_step "步骤 1: 检查依赖"

    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装！"
        log_info "请先安装 Docker：https://docs.docker.com/get-docker/"
        exit 1
    fi

    log_success "Docker 已安装: $(docker --version)"

    # 检查 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装！"
        log_info "请先安装 Docker Compose：https://docs.docker.com/compose/install/"
        exit 1
    fi

    log_success "Docker Compose 已安装: $(docker-compose --version)"

    # 检查 openssl（用于生成密码）
    if ! command -v openssl &> /dev/null; then
        log_error "openssl 未安装！"
        log_info "请先安装 openssl"
        exit 1
    fi

    log_success "openssl 已安装"
}

# 配置环境变量
configure_environment() {
    log_step "步骤 2: 配置环境变量"

    # 检查 .env 文件
    if [ ! -f .env ]; then
        log_info ".env 文件不存在，从 .env.example 复制..."
        cp .env.example .env
    fi

    # 检查是否已配置
    if ! grep -q "your_moonshot_api_key_here" .env && \
       ! grep -q "your_strong_password_here" .env && \
       ! grep -q "change_this_to_a_random_secret" .env; then
        log_success "环境变量已配置，跳过配置步骤"
        return
    fi

    log_info "开始配置环境变量..."

    # 配置 Moonshot AI API Key
    log_info "配置 Moonshot AI API Key"
    echo "  访问: https://platform.moonshot.cn/console/api-keys"
    read -p "  请输入您的 Moonshot AI API Key: " api_key

    if [ -z "$api_key" ]; then
        log_error "API Key 不能为空！"
        exit 1
    fi

    sed -i "s|^COZE_WORKLOAD_IDENTITY_API_KEY=.*|COZE_WORKLOAD_IDENTITY_API_KEY=$api_key|" .env

    # 生成数据库密码
    log_info "生成数据库密码..."
    db_password=$(openssl rand -base64 24 | tr -d '/+=' | head -c 24)
    sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=$db_password|" .env
    sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql://ancienttext:$db_password@db:5432/ancienttext|" .env

    # 生成应用密钥
    log_info "生成应用密钥..."
    secret_key=$(openssl rand -hex 32)
    sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$secret_key|" .env

    # 生成 Redis 密码
    log_info "生成 Redis 密码..."
    redis_password=$(openssl rand -base64 16 | tr -d '/+=' | head -c 16)
    sed -i "s|^REDIS_PASSWORD=.*|REDIS_PASSWORD=$redis_password|" .env
    sed -i "s|^REDIS_URL=.*|REDIS_URL=redis://:$redis_password@redis:6379/0|" .env

    # 生成 JWT 密钥
    log_info "生成 JWT 密钥..."
    jwt_secret=$(openssl rand -hex 32)
    sed -i "s|^# JWT_SECRET=.*|JWT_SECRET=$jwt_secret|" .env

    # 设置文件权限
    chmod 600 .env

    log_success "环境变量配置完成"
}

# 拉取镜像
pull_images() {
    log_step "步骤 3: 拉取 Docker 镜像"

    log_info "拉取 PostgreSQL 镜像..."
    docker-compose pull db

    log_info "拉取 Redis 镜像..."
    docker-compose pull redis

    log_info "拉取 Nginx 镜像..."
    docker-compose pull nginx

    log_success "镜像拉取完成"
}

# 构建应用
build_application() {
    log_step "步骤 4: 构建应用镜像"

    log_info "构建应用镜像（这可能需要几分钟）..."
    docker-compose build web

    log_success "应用镜像构建完成"
}

# 启动服务
start_services() {
    log_step "步骤 5: 启动服务"

    log_info "启动所有服务..."
    docker-compose up -d

    log_success "服务已启动"
}

# 等待服务就绪
wait_for_services() {
    log_step "步骤 6: 等待服务就绪"

    log_info "等待数据库初始化（约30秒）..."
    sleep 30

    # 检查数据库
    log_info "检查数据库状态..."
    for i in {1..10}; do
        if docker-compose exec -T db pg_isready -U ancienttext -d ancienttext &> /dev/null; then
            log_success "数据库已就绪"
            break
        fi
        log_info "等待数据库... ($i/10)"
        sleep 3
    done

    # 检查 Redis
    log_info "检查 Redis 状态..."
    for i in {1..10}; do
        if docker-compose exec -T redis redis-cli ping &> /dev/null; then
            log_success "Redis 已就绪"
            break
        fi
        log_info "等待 Redis... ($i/10)"
        sleep 2
    done

    # 检查应用
    log_info "检查应用状态..."
    for i in {1..10}; do
        if curl -sf http://localhost:8000/health &> /dev/null; then
            log_success "应用已就绪"
            break
        fi
        log_info "等待应用... ($i/10)"
        sleep 3
    done

    log_success "所有服务已就绪"
}

# 验证部署
verify_deployment() {
    log_step "步骤 7: 验证部署"

    log_info "检查服务状态..."
    docker-compose ps

    echo ""

    # 测试数据库
    log_info "测试数据库连接..."
    if docker-compose exec -T db psql -U ancienttext -d ancienttext -c "SELECT version();" &> /dev/null; then
        log_success "数据库连接正常"
    else
        log_warning "数据库连接可能有问题"
    fi

    # 测试 Redis
    log_info "测试 Redis 连接..."
    if docker-compose exec -T redis redis-cli ping &> /dev/null; then
        log_success "Redis 连接正常"
    else
        log_warning "Redis 连接可能有问题"
    fi

    # 测试应用
    log_info "测试应用健康检查..."
    response=$(curl -s http://localhost:8000/health)
    if echo "$response" | grep -q "healthy"; then
        log_success "应用健康检查通过"
    else
        log_warning "应用健康检查可能有问题"
    fi

    log_success "部署验证完成"
}

# 显示部署摘要
show_summary() {
    log_step "部署完成"

    echo ""
    echo -e "${GREEN}======================================"
    echo -e "🎉 古文字破译系统部署成功！"
    echo -e "======================================${NC}"
    echo ""

    echo "服务访问地址："
    echo "  📡 API 文档: http://localhost:8000/docs"
    echo "  🌐 前端界面: http://localhost:8000/static/index.html"
    echo "  ❤️  健康检查: http://localhost:8000/health"
    echo ""

    echo "常用命令："
    echo "  📋 查看状态: docker-compose ps"
    echo "  📜 查看日志: docker-compose logs -f"
    echo "  🔄 重启服务: docker-compose restart"
    echo "  ⏹️  停止服务: docker-compose down"
    echo ""

    echo "服务信息："
    echo "  🗄️  数据库: localhost:5432"
    echo "  🔴 Redis: localhost:6379"
    echo "  🌐 Web 应用: localhost:8000"
    echo ""

    echo -e "${YELLOW}⚠️  重要提示：${NC}"
    echo "  • 请妥善保存配置信息（.env 文件）"
    echo "  • 不要将 .env 文件提交到 Git 仓库"
    echo "  • 定期更换 Token（建议每3-6个月）"
    echo "  • 定期备份数据（./scripts/backup.sh）"
    echo ""

    echo -e "${GREEN}部署已完成，系统可以正常使用！${NC}"
    echo ""
}

# 主函数
main() {
    echo ""
    echo -e "${CYAN}======================================"
    echo -e "古文字破译系统 - 一键部署脚本"
    echo -e "======================================"
    echo ""
    echo "此脚本将自动完成以下操作："
    echo "  1. 检查依赖（Docker、Docker Compose）"
    echo "  2. 配置环境变量（API Token、密码等）"
    echo "  3. 拉取 Docker 镜像"
    echo "  4. 构建应用镜像"
    echo "  5. 启动所有服务"
    echo "  6. 等待服务就绪"
    echo "  7. 验证部署"
    echo ""

    # 确认开始
    read -p "是否开始部署？(y/n): " confirm_start
    if [ "$confirm_start" != "y" ]; then
        log_info "已取消部署"
        exit 0
    fi

    # 执行部署步骤
    check_dependencies
    configure_environment
    pull_images
    build_application
    start_services
    wait_for_services
    verify_deployment
    show_summary
}

# 运行主函数
main
