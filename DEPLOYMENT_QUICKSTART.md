# 🚀 部署快速开始

古文字破译系统 - 快速部署指南（5分钟上手）

---

## 📋 前置要求

- 一台云服务器（Ubuntu 22.04 LTS）
- 服务器配置：2核4G 或以上
- 已购买域名（可选，用于 HTTPS）
- Moonshot AI API Key

---

## ⚡ 一键部署（推荐）

### 1. 连接服务器

```bash
ssh root@your-server-ip
```

### 2. 下载部署脚本

```bash
# 方法1：使用 curl
curl -O https://raw.githubusercontent.com/your-username/your-repo/main/deploy.sh
chmod +x deploy.sh

# 方法2：使用 wget
wget https://raw.githubusercontent.com/your-username/your-repo/main/deploy.sh
chmod +x deploy.sh
```

### 3. 运行部署脚本

```bash
./deploy.sh
```

### 4. 填写配置信息

脚本会询问以下信息：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| **域名** | 您的域名 | `example.com` |
| **API Key** | Moonshot AI API Key | `sk-xxxxx...` |
| **邮箱** | 用于 SSL 证书 | `your-email@example.com` |

### 5. 等待部署完成

脚本会自动完成以下操作：

- ✅ 更新系统
- ✅ 安装 Docker 和 Docker Compose
- ✅ 克隆代码
- ✅ 配置环境变量
- ✅ 构建并启动服务
- ✅ 配置 Nginx
- ✅ 配置 HTTPS（如果提供了域名）
- ✅ 配置监控和备份

**预计耗时**：5-10分钟

### 6. 访问系统

部署完成后，通过浏览器访问：

```
https://your-domain.com/static/index.html
```

---

## 📝 详细部署步骤

如果您想手动部署，请按照以下步骤操作：

### 步骤1：更新系统

```bash
apt update && apt upgrade -y
apt install -y git curl wget vim htop
```

### 步骤2：安装 Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl start docker
systemctl enable docker
```

### 步骤3：安装 Docker Compose

```bash
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

### 步骤4：克隆代码

```bash
cd /opt
git clone https://github.com/your-username/your-repo.git ancient-script
cd ancient-script
```

### 步骤5：配置环境变量

```bash
cp .env.example .env
nano .env
```

**重要配置**：
```bash
COZE_WORKSPACE_PATH=/opt/ancient-script
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-api-key-here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1
PORT=8000
HOST=0.0.0.0
```

### 步骤6：启动服务

```bash
docker-compose build
docker-compose up -d
```

### 步骤7：配置 Nginx（可选）

```bash
# 安装 Nginx
apt install -y nginx
systemctl start nginx
systemctl enable nginx

# 创建站点配置
nano /etc/nginx/sites-available/ancient-script
```

**Nginx 配置**：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /static/ {
        alias /opt/ancient-script/static/;
    }
}
```

**启用配置**：
```bash
ln -s /etc/nginx/sites-available/ancient-script /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 步骤8：配置 HTTPS（可选）

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com -m your-email@example.com --agree-tos --no-eff-email

# 配置自动续期
echo "0 0 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'" | crontab -
```

---

## ✅ 验证部署

### 1. 检查服务状态

```bash
# 检查容器
cd /opt/ancient-script
docker-compose ps

# 检查 API
curl http://localhost:8000/health

# 检查 Nginx
systemctl status nginx
```

### 2. 访问系统

在浏览器打开：

- **API 文档**: `https://your-domain.com/docs`
- **前端界面**: `https://your-domain.com/static/index.html`
- **健康检查**: `https://your-domain.com/health`

---

## 🛠️ 常用操作

### 查看日志

```bash
# 查看应用日志
cd /opt/ancient-script
docker-compose logs -f

# 查看 Nginx 日志
tail -f /var/log/nginx/error.log
```

### 重启服务

```bash
# 重启应用
cd /opt/ancient-script
docker-compose restart

# 重启 Nginx
systemctl restart nginx
```

### 更新应用

```bash
cd /opt/ancient-script
git pull
docker-compose build
docker-compose down
docker-compose up -d
```

### 查看监控

```bash
# 查看监控日志
tail -f /var/log/ancient-script-monitor.log

# 查看备份
ls -lh /opt/backups/ancient-script/
```

---

## 🔧 故障排查

### 问题1：容器无法启动

```bash
# 查看详细日志
docker-compose logs -f

# 检查端口占用
netstat -tunlp | grep 8000
```

### 问题2：Nginx 无法访问

```bash
# 检查 Nginx 状态
systemctl status nginx

# 检查配置
nginx -t

# 查看 Nginx 日志
tail -f /var/log/nginx/error.log
```

### 问题3：API 无法访问

```bash
# 检查容器状态
docker-compose ps

# 检查 API 健康状态
curl http://localhost:8000/health

# 检查环境变量
cat .env
```

---

## 📊 性能优化

### 1. 增加内存限制

编辑 `docker-compose.yml`：
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
```

### 2. 配置缓存

如果需要，可以添加 Redis 缓存：
```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

### 3. 使用 CDN

配置 CDN 加速静态资源：
```nginx
location /static/ {
    proxy_pass https://your-cdn-domain.com/;
}
```

---

## 🔒 安全建议

1. **配置防火墙**
   ```bash
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

2. **禁用 root 登录**
   ```bash
   nano /etc/ssh/sshd_config
   # 修改为：PermitRootLogin no
   ```

3. **使用 SSH 密钥**
   ```bash
   ssh-copy-id user@your-server-ip
   ```

4. **定期更新**
   ```bash
   apt update && apt upgrade -y
   ```

---

## 📚 相关文档

- [完整部署文档](CLOUD_DEPLOYMENT.md)
- [快速启动指南](SIMPLE_START.md)
- [API 文档](docs/API_DOCUMENTATION.md)
- [架构设计](docs/ARCHITECTURE_DESIGN.md)

---

## 💬 获取帮助

如果遇到问题：

1. 查看日志：`docker-compose logs -f`
2. 查看文档：[CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md)
3. 提交 Issue：[GitHub Issues](https://github.com/your-username/your-repo/issues)

---

## 🎉 开始使用

部署完成后，您可以：

1. ✅ 使用前端界面进行古文字分析
2. ✅ 调用 API 进行集成开发
3. ✅ 开发自定义插件扩展功能
4. ✅ 配置监控和告警

**祝您使用愉快！** 🚀

---

**更新日期**: 2025-01-10
