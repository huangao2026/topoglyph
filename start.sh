#!/bin/bash

# 古文字破译系统 - 快速启动脚本
# 包含数据库初始化

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# 检查环境变量
check_env() {
    log_info "检查环境变量..."
    
    if [ ! -f .env ]; then
        log_warning ".env 文件不存在，从 .env.example 复制..."
        cp .env.example .env
        log_warning "请编辑 .env 文件，填入您的配置！"
        return 1
    fi
    
    # 检查必需的环境变量
    if grep -q "your_moonshot_api_key_here" .env; then
        log_error "请先在 .env 文件中配置 Moonshot API Key！"
        return 1
    fi
    
    log_success "环境变量检查通过"
    return 0
}

# 启动数据库服务
start_database() {
    log_info "启动数据库服务..."
    
    # 启动 PostgreSQL 和 Redis
    docker-compose up -d db redis
    
    # 等待数据库就绪
    log_info "等待数据库就绪..."
    sleep 5
    
    # 检查数据库连接
    if docker-compose ps db | grep -q "Up"; then
        log_success "数据库服务启动成功"
    else
        log_error "数据库服务启动失败"
        return 1
    fi
    
    if docker-compose ps redis | grep -q "Up"; then
        log_success "Redis 服务启动成功"
    else
        log_error "Redis 服务启动失败"
        return 1
    fi
    
    return 0
}

# 初始化数据库
init_database() {
    log_info "初始化数据库..."
    
    # 运行初始化脚本
    docker-compose exec app python scripts/init_db.py <<EOF
5
EOF
    
    if [ $? -eq 0 ]; then
        log_success "数据库初始化成功"
    else
        log_error "数据库初始化失败"
        return 1
    fi
    
    return 0
}

# 启动应用
start_app() {
    log_info "启动应用服务..."
    
    # 构建镜像（如果需要）
    if [ "$1" = "--build" ]; then
        log_info "构建 Docker 镜像..."
        docker-compose build
    fi
    
    # 启动应用
    docker-compose up -d app
    
    # 等待应用就绪
    log_info "等待应用就绪..."
    sleep 5
    
    # 检查应用状态
    if docker-compose ps app | grep -q "Up"; then
        log_success "应用服务启动成功"
    else
        log_error "应用服务启动失败"
        return 1
    fi
    
    return 0
}

# 显示状态
show_status() {
    log_info "系统状态："
    echo ""
    
    docker-compose ps
    echo ""
    
    log_info "服务地址："
    echo "  - API 文档: http://localhost:${PORT:-8000}/docs"
    echo "  - 前端界面: http://localhost:${PORT:-8000}/static/index.html"
    echo "  - 健康检查: http://localhost:${PORT:-8000}/health"
    echo ""
}

# 显示日志
show_logs() {
    docker-compose logs -f
}

# 停止服务
stop_services() {
    log_info "停止所有服务..."
    docker-compose down
    log_success "所有服务已停止"
}

# 重启服务
restart_services() {
    log_info "重启所有服务..."
    docker-compose restart
    log_success "所有服务已重启"
}

# 清理数据
clean_data() {
    log_warning "⚠️  即将清理所有数据，包括数据库！"
    read -p "确认清理？(yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        log_info "清理数据..."
        docker-compose down -v
        log_success "数据已清理"
    else
        log_info "操作已取消"
    fi
}

# 显示帮助
show_help() {
    cat << EOF
古文字破译系统 - 快速启动脚本

用法: ./start.sh [选项]

选项:
    start           启动所有服务（默认）
    stop            停止所有服务
    restart         重启所有服务
    status          显示服务状态
    logs            查看服务日志
    build           重新构建镜像
    clean           清理所有数据
    help            显示此帮助信息

示例:
    ./start.sh                    # 启动所有服务
    ./start.sh start              # 启动所有服务
    ./start.sh stop               # 停止所有服务
    ./start.sh restart            # 重启所有服务
    ./start.sh logs               # 查看日志
    ./start.sh build              # 重新构建并启动
    ./start.sh clean              # 清理所有数据

环境变量:
    PORT           服务端口（默认：8000）
    LOG_LEVEL      日志级别（默认：INFO）
    MAX_MESSAGES   最大消息数（默认：40）

EOF
}

# 主函数
main() {
    echo ""
    echo "======================================"
    echo "古文字破译系统 - 快速启动"
    echo "======================================"
    echo ""
    
    case "${1:-start}" in
        start)
            if check_env; then
                start_database
                init_database
                start_app --build
                show_status
                log_success "系统启动完成！"
            fi
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        build)
            start_app --build
            show_status
            ;;
        clean)
            clean_data
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
