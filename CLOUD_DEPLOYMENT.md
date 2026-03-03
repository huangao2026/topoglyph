# 云服务器部署完整指南

古文字破译系统 - 云服务器部署指南

## 📋 目录

1. [部署前准备](#部署前准备)
2. [服务器初始化](#服务器初始化)
3. [应用部署](#应用部署)
4. [Nginx 配置](#nginx-配置)
5. [HTTPS 配置](#https-配置)
6. [监控配置](#监控配置)
7. [备份配置](#备份配置)
8. [安全加固](#安全加固)
9. [故障排查](#故障排查)
10. [维护手册](#维护手册)

---

## 部署前准备

### 1. 服务器选择

#### 推荐配置

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 2核 | 4核 |
| 内存 | 4GB | 8GB |
| 磁盘 | 40GB SSD | 80GB SSD |
| 带宽 | 5Mbps | 10Mbps |
| 系统 | Ubuntu 22.04 | Ubuntu 22.04 |

#### 云服务商推荐

| 服务商 | 优势 | 价格 |
|--------|------|------|
| 阿里云 | 国内访问快 | ¥50/月起 |
| 腾讯云 | 性价比高 | ¥45/月起 |
| 华为云 | 企业级服务 | ¥60/月起 |
| AWS | 全球服务 | $10/月起 |

### 2. 域名准备

- 购买域名（如阿里云、腾讯云）
- 解析域名到服务器IP
- 等待DNS生效（通常10-30分钟）

### 3. 准备工作

- [ ] 准备服务器IP地址
- [ ] 准备域名
- [ ] 准备 Moonshot AI API Key
- [ ] 准备 SSH 客户端

---

## 服务器初始化

### 1. 连接服务器

```bash
# SSH 连接
ssh root@your-server-ip

# 或使用密钥
ssh -i ~/.ssh/your-key.pem root@your-server-ip
```

### 2. 更新系统

```bash
# 更新软件包
apt update && apt upgrade -y

# 设置时区
timedatectl set-timezone Asia/Shanghai

# 安装基础软件
apt install -y git curl wget vim htop net-tools unzip
```

### 3. 创建用户（可选但推荐）

```bash
# 创建用户
adduser deploy

# 添加到 sudo 组
usermod -aG sudo deploy

# 切换到 deploy 用户
su - deploy
```

### 4. 配置 SSH 密钥（可选）

```bash
# 在本地生成密钥
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# 复制公钥到服务器
ssh-copy-id deploy@your-server-ip

# 测试登录
ssh deploy@your-server-ip
```

---

## 应用部署

### 1. 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 启动 Docker
systemctl start docker
systemctl enable docker

# 验证安装
docker --version
```

### 2. 安装 Docker Compose

```bash
# 下载 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 添加执行权限
chmod +x /usr/local/bin/docker-compose

# 创建软链接
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 验证安装
docker-compose --version
```

### 3. 克隆代码

```bash
# 进入工作目录
cd /opt

# 克隆代码（替换为您的仓库）
git clone https://github.com/your-username/your-repo.git ancient-script

# 进入项目目录
cd ancient-script
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

**重要配置**：
```bash
COZE_WORKSPACE_PATH=/opt/ancient-script
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-api-key-here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
```

### 5. 启动服务

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 退出日志（Ctrl+C）
```

### 6. 验证部署

```bash
# 检查容器状态
docker-compose ps

# 测试健康检查
curl http://localhost:8000/health

# 测试 API
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "测试"}'
```

---

## Nginx 配置

### 1. 安装 Nginx

```bash
apt install -y nginx

# 启动 Nginx
systemctl start nginx
systemctl enable nginx
```

### 2. 配置站点

```bash
# 创建站点配置
nano /etc/nginx/sites-available/ancient-script
```

**配置内容**：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    access_log /var/log/nginx/ancient-script-access.log;
    error_log /var/log/nginx/ancient-script-error.log;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
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
```

### 3. 启用配置

```bash
# 创建符号链接
ln -s /etc/nginx/sites-available/ancient-script /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

---

## HTTPS 配置

### 1. 安装 Certbot

```bash
apt install -y certbot python3-certbot-nginx
```

### 2. 获取证书

```bash
# 替换为您的域名和邮箱
certbot --nginx -d your-domain.com -m your-email@example.com --agree-tos --no-eff-email
```

### 3. 配置自动续期

```bash
# 测试续期
certbot renew --dry-run

# 配置定时任务
crontab -e

# 添加以下内容
0 0 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'
```

---

## 监控配置

### 1. 安装监控工具

```bash
# 安装监控工具
apt install -y htop iotop net-tools

# 创建监控目录
mkdir -p /opt/monitoring
```

### 2. 创建监控脚本

```bash
nano /opt/monitoring/monitor.sh
```

**监控脚本内容**：
```bash
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
```

**设置权限**：
```bash
chmod +x /opt/monitoring/monitor.sh
```

### 3. 配置定时监控

```bash
crontab -e

# 添加以下内容（每5分钟检查一次）
*/5 * * * * /opt/monitoring/monitor.sh
```

---

## 备份配置

### 1. 创建备份脚本

```bash
nano /opt/monitoring/backup.sh
```

**备份脚本内容**：
```bash
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
```

**设置权限**：
```bash
chmod +x /opt/monitoring/backup.sh
```

### 2. 配置定时备份

```bash
crontab -e

# 添加以下内容（每天凌晨2点备份）
0 2 * * * /opt/monitoring/backup.sh
```

---

## 安全加固

### 1. 配置防火墙

```bash
# 安装 UFW
apt install -y ufw

# 设置默认策略
ufw default deny incoming
ufw default allow outgoing

# 允许必要端口
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 启用防火墙
ufw enable

# 查看状态
ufw status
```

### 2. 配置 SSH

```bash
# 备份配置
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# 编辑配置
nano /etc/ssh/sshd_config
```

**安全配置**：
```
PermitRootLogin no
PasswordAuthentication no
```

**重启 SSH**：
```bash
systemctl restart sshd
```

### 3. 安装 fail2ban

```bash
apt install -y fail2ban

systemctl start fail2ban
systemctl enable fail2ban
```

---

## 故障排查

### 问题1：容器无法启动

```bash
# 查看容器日志
docker-compose logs -f

# 检查端口占用
netstat -tunlp | grep 8000

# 重启容器
docker-compose restart
```

### 问题2：Nginx 无法访问

```bash
# 检查 Nginx 状态
systemctl status nginx

# 查看 Nginx 日志
tail -f /var/log/nginx/error.log

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### 问题3：HTTPS 证书问题

```bash
# 检查证书状态
certbot certificates

# 手动续期
certbot renew

# 重新获取证书
certbot --nginx -d your-domain.com --force-renewal
```

### 问题4：内存不足

```bash
# 查看内存使用
free -h

# 查看容器资源使用
docker stats

# 限制容器内存（编辑 docker-compose.yml）
# services:
#   app:
#     deploy:
#       resources:
#         limits:
#           memory: 2G
```

---

## 维护手册

### 日常维护

| 任务 | 频率 | 命令 |
|------|------|------|
| 检查服务状态 | 每天 | `docker-compose ps` |
| 查看日志 | 每天 | `docker-compose logs --tail=100` |
| 检查磁盘空间 | 每天 | `df -h` |
| 检查内存使用 | 每天 | `free -h` |
| 更新系统 | 每周 | `apt update && apt upgrade -y` |
| 备份配置 | 每天 | 自动执行 |
| 更新SSL证书 | 自动 | 自动续期 |

### 更新应用

```bash
# 进入项目目录
cd /opt/ancient-script

# 拉取最新代码
git pull

# 重新构建
docker-compose build

# 重启服务
docker-compose down
docker-compose up -d

# 验证
curl http://localhost:8000/health
```

### 回滚应用

```bash
# 进入项目目录
cd /opt/ancient-script

# 查看提交历史
git log --oneline -10

# 回滚到指定版本
git checkout <commit-hash>

# 重启服务
docker-compose down
docker-compose up -d
```

### 扩容

```bash
# 如果使用 Kubernetes
kubectl scale deployment ancient-script --replicas=3

# 如果使用 Docker Swarm
docker service scale ancient-script=3
```

---

## 🎉 部署完成！

### 访问地址

- **API 文档**: https://your-domain.com/docs
- **前端界面**: https://your-domain.com/static/index.html
- **健康检查**: https://your-domain.com/health

### 后续任务

- [ ] 配置告警通知
- [ ] 设置日志分析
- [ ] 配置 CDN（可选）
- [ ] 配置负载均衡（可选）
- [ ] 配置数据库（可选）
- [ ] 配置 Redis（可选）

---

**文档版本**: v1.0  
**更新日期**: 2025-01-10
