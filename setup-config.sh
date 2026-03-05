#!/bin/bash

# 古文字破译系统 - 自动配置脚本
# 帮助用户快速配置所有 API Token 和敏感信息

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
    echo -e "${CYAN}======================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}======================================${NC}"
}

# 检查 .env 文件是否存在
check_env_file() {
    log_step "步骤 1: 检查配置文件"

    if [ ! -f .env ]; then
        log_info ".env 文件不存在，从 .env.example 复制..."

        if [ ! -f .env.example ]; then
            log_error ".env.example 文件不存在！"
            log_info "请确保在项目根目录运行此脚本"
            exit 1
        fi

        cp .env.example .env
        log_success ".env 文件已创建"
    else
        log_info ".env 文件已存在"
    fi
}

# 配置 Moonshot AI API Key
configure_moonshot_api_key() {
    log_step "步骤 2: 配置 Moonshot AI API Key"

    echo ""
    log_info "获取 Moonshot AI API Key："
    echo "  1. 访问 https://platform.moonshot.cn/console/api-keys"
    echo "  2. 登录或注册账号"
    echo "  3. 点击\"创建 API Key\""
    echo "  4. 复制生成的 API Key（格式：sk-xxxxx...）"
    echo ""

    read -p "请输入您的 Moonshot AI API Key: " api_key

    # 验证 API Key 格式
    if [[ ! $api_key =~ ^sk-[a-zA-Z0-9]{32,}$ ]]; then
        log_warning "API Key 格式可能不正确（应为 sk-xxxxx... 格式）"
        read -p "是否继续？(y/n): " confirm
        if [ "$confirm" != "y" ]; then
            log_info "已取消配置"
            exit 0
        fi
    fi

    # 替换 .env 文件中的 API Key
    sed -i "s|^COZE_WORKLOAD_IDENTITY_API_KEY=.*|COZE_WORKLOAD_IDENTITY_API_KEY=$api_key|" .env

    log_success "Moonshot AI API Key 已配置"
}

# 生成强密码
generate_password() {
    local length=$1
    openssl rand -base64 $length | tr -d '/+=' | head -c $length
}

# 配置数据库密码
configure_database_password() {
    log_step "步骤 3: 配置数据库密码"

    echo ""
    log_info "数据库密码用于保护您的数据安全"
    log_info "建议使用强密码（至少16位）"
    echo ""

    # 询问用户是否自动生成
    read -p "是否自动生成强密码？(y/n，推荐 y): " auto_gen

    if [ "$auto_gen" = "y" ]; then
        db_password=$(generate_password 24)
        log_info "已生成数据库密码: ${db_password:0:8}***（仅显示前8位）"
    else
        read -sp "请输入数据库密码（至少16位）: " db_password
        echo ""

        if [ ${#db_password} -lt 16 ]; then
            log_error "密码长度不足16位！"
            exit 1
        fi
    fi

    # 替换 .env 文件中的数据库密码
    sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=$db_password|" .env
    sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql://ancienttext:$db_password@db:5432/ancienttext|" .env

    log_success "数据库密码已配置"
}

# 配置应用密钥
configure_secret_key() {
    log_step "步骤 4: 配置应用密钥（SECRET_KEY）"

    log_info "应用密钥用于加密用户会话和数据"
    log_info "正在生成强密钥..."

    # 生成随机密钥
    secret_key=$(openssl rand -hex 32)

    # 替换 .env 文件中的 SECRET_KEY
    sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$secret_key|" .env

    log_success "应用密钥已配置"
}

# 配置 Redis 密码（可选）
configure_redis_password() {
    log_step "步骤 5: 配置 Redis 密码（可选）"

    echo ""
    read -p "是否配置 Redis 密码？(y/n，推荐 y): " configure_redis

    if [ "$configure_redis" = "y" ]; then
        # 生成 Redis 密码
        redis_password=$(generate_password 16)

        # 替换 .env 文件中的 Redis 密码
        sed -i "s|^REDIS_PASSWORD=.*|REDIS_PASSWORD=$redis_password|" .env
        sed -i "s|^REDIS_URL=.*|REDIS_URL=redis://:$redis_password@redis:6379/0|" .env

        log_success "Redis 密码已配置"
    else
        log_info "跳过 Redis 密码配置"
    fi
}

# 配置 JWT 密钥（可选）
configure_jwt_secret() {
    log_step "步骤 6: 配置 JWT 密钥（可选）"

    echo ""
    read -p "是否配置 JWT 密钥？(y/n，推荐 y): " configure_jwt

    if [ "$configure_jwt" = "y" ]; then
        # 生成 JWT 密钥
        jwt_secret=$(openssl rand -hex 32)

        # 取消注释并替换 JWT_SECRET
        sed -i "s|^# JWT_SECRET=.*|JWT_SECRET=$jwt_secret|" .env
        sed -i "s|^#* JWT_SECRET=.*|JWT_SECRET=$jwt_secret|" .env

        log_success "JWT 密钥已配置"
    else
        log_info "跳过 JWT 密钥配置"
    fi
}

# 配置 API Key（可选）
configure_api_key() {
    log_step "步骤 7: 配置外部 API Key（可选）"

    echo ""
    read -p "是否配置外部 API Key？(y/n): " configure_external_api

    if [ "$configure_external_api" = "y" ]; then
        # 生成 API Key
        api_key="ancient-text-$(openssl rand -hex 16)"

        # 取消注释并替换 API_KEY
        sed -i "s|^# API_KEY=.*|API_KEY=$api_key|" .env
        sed -i "s|^#* API_KEY=.*|API_KEY=$api_key|" .env

        log_success "外部 API Key 已配置: $api_key"
    else
        log_info "跳过外部 API Key 配置"
    fi
}

# 设置文件权限
set_file_permissions() {
    log_step "步骤 8: 设置文件权限"

    # 设置 .env 文件权限为仅当前用户可读写
    chmod 600 .env

    log_success "文件权限已设置（600）"
}

# 验证配置
verify_configuration() {
    log_step "步骤 9: 验证配置"

    log_info "检查配置文件..."

    # 检查是否还有默认值
    default_values_found=false

    if grep -q "your_moonshot_api_key_here" .env; then
        log_error "Moonshot AI API Key 未配置！"
        default_values_found=true
    fi

    if grep -q "your_strong_password_here" .env; then
        log_error "数据库密码未配置！"
        default_values_found=true
    fi

    if grep -q "change_this_to_a_random_secret" .env; then
        log_error "应用密钥未配置！"
        default_values_found=true
    fi

    if [ "$default_values_found" = true ]; then
        log_error "配置验证失败！"
        exit 1
    fi

    log_success "配置验证通过"
}

# 显示配置摘要
show_summary() {
    log_step "配置完成"

    echo ""
    echo -e "${GREEN}✅ 所有 Token 已配置完成！${NC}"
    echo ""
    echo "已配置的项目："
    echo "  ✅ Moonshot AI API Key"
    echo "  ✅ 数据库密码"
    echo "  ✅ 应用密钥（SECRET_KEY）"
    echo "  ✅ Redis 密码（如配置）"
    echo "  ✅ JWT 密钥（如配置）"
    echo "  ✅ 外部 API Key（如配置）"
    echo ""
    echo "安全措施："
    echo "  ✅ .env 文件权限已设置为 600"
    echo "  ⚠️  请确保 .env 已添加到 .gitignore"
    echo "  ⚠️  请妥善保存配置信息"
    echo ""
    echo "下一步操作："
    echo "  1. 启动服务: docker-compose up -d"
    echo "  2. 查看日志: docker-compose logs -f"
    echo "  3. 测试 API: curl http://localhost:8000/health"
    echo ""
    echo -e "${YELLOW}⚠️  重要提示：${NC}"
    echo "  • 请将配置信息保存到安全的地方"
    echo "  • 不要将 .env 文件提交到 Git 仓库"
    echo "  • 定期更换 Token（建议每3-6个月）"
    echo ""
    echo -e "${GREEN}配置脚本执行完成！${NC}"
}

# 主函数
main() {
    echo ""
    echo -e "${CYAN}======================================"
    echo -e "古文字破译系统 - 自动配置脚本"
    echo -e "======================================"
    echo ""
    echo "此脚本将帮助您配置所有必要的 API Token 和敏感信息"
    echo ""

    # 确认开始
    read -p "是否开始配置？(y/n): " confirm_start
    if [ "$confirm_start" != "y" ]; then
        log_info "已取消配置"
        exit 0
    fi

    # 执行配置步骤
    check_env_file
    configure_moonshot_api_key
    configure_database_password
    configure_secret_key
    configure_redis_password
    configure_jwt_secret
    configure_api_key
    set_file_permissions
    verify_configuration
    show_summary
}

# 运行主函数
main
