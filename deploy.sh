#!/bin/bash

# 古文字破译系统 - 一键部署脚本
# 适用于 Ubuntu 22.04 LTS

set -e  # 遇到错误立即退出

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

# 检查是否为 root 用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用 root 用户运行此脚本"
        exit 1
    fi
}

# 询问配置信息
ask_config() {
    log_info "======================================"
    log_info "古文字破译系统部署配置"
    log_info "======================================"
    echo ""

    # 询问域名
    read -p "请输入域名 (如 example.com): " DOMAIN
    if [ -z "$DOMAIN" ]; then
        log_warning "未提供域名，将跳过 HTTPS 配置"
        SKIP_HTTPS=true
    fi

    # 询问 API Key
    read -p "请输入 Moonshot AI API Key: " API_KEY
    if [ -z "$API_KEY" ]; then
        log_error "必须提供 API Key"
        exit 1
    fi

    # 询问邮箱
    read -p "请输入邮箱 (用于 SSL 证书): " EMAIL
    if [ -z "$EMAIL" ] && [ "$SKIP_HTTPS" != true ]; then
        log_error "必须提供邮箱地址"
        exit 1
    fi

    # 确认配置
    echo ""
    log_info "======================================"
    log_info "配置信息"
    log_info "======================================"
    echo "域名: ${DOMAIN:-未配置}"
    echo "API Key: ${API_KEY:0:10}..."
    echo "邮箱: ${EMAIL:-未配置}"
    echo ""
    read -p "确认配置？(y/n): " CONFIRM
    if [ "$CONFIRM" != "y" ]; then
        log_info "已取消部署"
        exit 0
    fi
}

# 更新系统
update_system() {
    log_info "更新系统..."
    apt update && apt upgrade -y
    log_success "系统更新完成"
}

# 安装基础软件
install_base_packages() {
    log_info "安装基础软件..."
    apt install -y git curl wget vim htop net-tools unzip ufw fail2ban
    log_success "基础软件安装完成"
}

# 安装 Docker
install_docker() {
    log_info "安装 Docker..."
    
    if command -v docker &> /dev/null; then
        log_warning "Docker 已安装，跳过..."
    else
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl start docker
        systemctl enable docker
        log_success "Docker 安装完成"
    fi
    
    docker --version
}

# 安装 Docker Compose
install_docker_compose() {
    log_info "安装 Docker Compose..."
    
    if command -v docker-compose &> /dev/null; then
        log_warning "Docker Compose 已安装，跳过..."
    else
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
        log_success "Docker Compose 安装完成"
    fi
    
    docker-compose --version
}

# 克隆代码
clone_code() {
    log_info "克隆代码仓库..."
    
    cd /opt
    
    if [ -d "ancient-script" ]; then
        log_warning "项目目录已存在，将使用现有代码"
    else
        read -p "请输入代码仓库地址 (如 https://github.com/user/repo.git): " REPO_URL
        if [ -z "$REPO_URL" ]; then
            log_error "必须提供代码仓库地址"
            exit 1
        fi
        
        git clone "$REPO_URL" ancient-script
        log_success "代码克隆完成"
    fi
    
    cd ancient-script
}

# 配置环境变量
configure_env() {
    log_info "配置环境变量..."
    
    if [ ! -f .env ]; then
        cp .env.example .env
    fi
    
    # 写入配置
    sed -i "s|COZE_WORKSPACE_PATH=.*|COZE_WORKSPACE_PATH=/opt/ancient-script|g" .env
    sed -i "s|COZE_WORKLOAD_IDENTITY_API_KEY=.*|COZE_WORKLOAD_IDENTITY_API_KEY=$API_KEY|g" .env
    sed -i "s|PORT=.*|PORT=8000|g" .env
    sed -i "s|HOST=.*|HOST=0.0.0.0|g" .env
    
    log_success "环境变量配置完成"
}

# 构建并启动服务
build_and_start() {
    log_info "构建并启动服务..."
    
    docker-compose build
    docker-compose up -d
    
    log_success "服务启动完成"
}

# 配置防火墙
configure_firewall() {
    log_info "配置防火墙..."
    
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    
    log_success "防火墙配置完成"
}

# 安装并配置 Nginx
install_nginx() {
    log_info "安装并配置 Nginx..."
    
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
    
    # 创建站点配置
    cat > /etc/nginx/sites-available/ancient-script <<EOF
server {
    listen 80;
    server_name ${DOMAIN:-_};

    access_log /var/log/nginx/ancient-script-access.log;
    error_log /var/log/nginx/ancient-script-error.log;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    location /static/ {
        alias /opt/ancient-script/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location ~ /\. {
        deny all;
    }
}
EOF
    
    # 启用配置
    ln -sf /etc/nginx/sites-available/ancient-script /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # 测试并重启
    nginx -t
    systemctl restart nginx
    
    log_success "Nginx 配置完成"
}

# 配置 HTTPS
configure_https() {
    if [ "$SKIP_HTTPS" = true ]; then
        log_warning "跳过 HTTPS 配置"
        return
    fi
    
    log_info "配置 HTTPS..."
    
    apt install -y certbot python3-certbot-nginx
    
    # 获取证书
    certbot --nginx -d "$DOMAIN" -m "$EMAIL" --agree-tos --no-eff-email
    
    # 配置自动续期
    (crontab -l 2>/dev/null; echo "0 0 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -
    
    log_success "HTTPS 配置完成"
}

# 配置监控
configure_monitoring() {
    log_info "配置监控..."
    
    mkdir -p /opt/monitoring
    mkdir -p /opt/backups/ancient-script
    
    # 创建监控脚本
    cat > /opt/monitoring/monitor.sh <<'MONITOR_EOF'
#!/bin/bash

LOG_FILE="/var/log/ancient-script-monitor.log"
API_URL="http://localhost:8000/health"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_service() {
    if ! docker-compose -f /opt/ancient-script/docker-compose.yml ps | grep -q "Up"; then
        log "❌ 容器未运行"
        cd /opt/ancient-script
        docker-compose restart
    else
        log "✅ 容器运行正常"
    fi
}

check_api() {
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
    if [ "$response" != "200" ]; then
        log "❌ API不健康: $response"
    else
        log "✅ API健康"
    fi
}

check_disk() {
    disk_usage=$(df /opt/ancient-script | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 80 ]; then
        log "⚠️ 磁盘使用率: ${disk_usage}%"
    else
        log "✅ 磁盘正常"
    fi
}

main() {
    log "=================================="
    check_service
    check_api
    check_disk
    log "=================================="
}

main
MONITOR_EOF
    
    chmod +x /opt/monitoring/monitor.sh
    
    # 创建备份脚本
    cat > /opt/monitoring/backup.sh <<'BACKUP_EOF'
#!/bin/bash

BACKUP_DIR="/opt/backups/ancient-script"
SOURCE_DIR="/opt/ancient-script"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

backup_configs() {
    log "备份配置文件..."
    tar -czf "$BACKUP_DIR/configs_$DATE.tar.gz" \
        "$SOURCE_DIR/.env" \
        "$SOURCE_DIR/docker-compose.yml" \
        2>/dev/null
}

cleanup_old_backups() {
    log "清理旧备份..."
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
}

main() {
    log "=================================="
    backup_configs
    cleanup_old_backups
    log "=================================="
}

main
BACKUP_EOF
    
    chmod +x /opt/monitoring/backup.sh
    
    # 配置定时任务
    (crontab -l 2>/dev/null; echo "*/5 * * * * /opt/monitoring/monitor.sh") | crontab -
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/monitoring/backup.sh") | crontab -
    
    log_success "监控配置完成"
}

# 验证部署
verify_deployment() {
    log_info "验证部署..."
    
    # 等待服务启动
    sleep 10
    
    # 检查容器
    if docker-compose -f /opt/ancient-script/docker-compose.yml ps | grep -q "Up"; then
        log_success "容器运行正常"
    else
        log_error "容器未运行"
        return 1
    fi
    
    # 检查 API
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        log_success "API 正常"
    else
        log_error "API 不正常"
        return 1
    fi
    
    # 检查 Nginx
    if systemctl is-active --quiet nginx; then
        log_success "Nginx 运行正常"
    else
        log_error "Nginx 未运行"
        return 1
    fi
    
    return 0
}

# 显示部署结果
show_result() {
    echo ""
    log_info "======================================"
    log_info "部署完成！"
    log_info "======================================"
    echo ""
    
    if [ "$SKIP_HTTPS" = true ]; then
        log_info "访问地址: http://${DOMAIN:-your-server-ip}"
    else
        log_info "访问地址: https://${DOMAIN}"
    fi
    
    echo ""
    log_info "可用服务："
    echo "  - API 文档: https://${DOMAIN}/docs"
    echo "  - 前端界面: https://${DOMAIN}/static/index.html"
    echo "  - 健康检查: https://${DOMAIN}/health"
    echo ""
    log_info "常用命令："
    echo "  - 查看日志: cd /opt/ancient-script && docker-compose logs -f"
    echo "  - 重启服务: cd /opt/ancient-script && docker-compose restart"
    echo "  - 查看监控: tail -f /var/log/ancient-script-monitor.log"
    echo "  - 查看备份: ls -lh /opt/backups/ancient-script/"
    echo ""
    log_success "部署成功！"
    echo ""
}

# 主函数
main() {
    echo ""
    log_info "======================================"
    log_info "古文字破译系统 - 一键部署脚本"
    log_info "======================================"
    echo ""
    
    # 检查 root 权限
    check_root
    
    # 询问配置
    ask_config
    
    # 执行部署步骤
    update_system
    install_base_packages
    install_docker
    install_docker_compose
    clone_code
    configure_env
    build_and_start
    configure_firewall
    install_nginx
    configure_https
    configure_monitoring
    
    # 验证部署
    if verify_deployment; then
        show_result
    else
        log_error "部署验证失败，请检查日志"
        exit 1
    fi
}

# 运行主函数
main
