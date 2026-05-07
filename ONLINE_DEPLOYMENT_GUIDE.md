# 🌍 TCD Origin 在线部署完整指南

## 📋 概述

本文档提供将 TCD Origin 智能体部署到线上供大家使用的完整指南。支持多种部署方式，从简单到专业，满足不同用户需求。

### 🎯 部署架构

```
┌─────────────────────────────────────────────────────┐
│                    用户访问                          │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                 Nginx 反向代理                        │
│         (可选，端口80/443)                           │
└─────────────────────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
┌───────────────────────┐   ┌───────────────────────┐
│    API 服务            │   │    Web 界面           │
│  (FastAPI)            │   │  (Gradio)             │
│  端口: 8000           │   │  端口: 7860           │
└───────────────────────┘   └───────────────────────┘
```

---

## 🚀 快速开始（本地测试）

### 方式1：Docker 一键部署（推荐⭐）

```bash
# 1. 克隆项目
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin

# 2. 一键启动
docker-compose up -d

# 3. 访问服务
# API文档: http://localhost:8000/docs
# Web界面: http://localhost:7860
```

### 方式2：本地开发模式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 API 服务
uvicorn api.main:app --reload --port 8000

# 3. 启动 Web 界面（新终端）
python web_app.py
```

---

## ☁️ 云平台部署

### 1️⃣ 阿里云 ECS

#### 步骤1：购买云服务器

```
产品: 云服务器 ECS
配置: 2核4G (最低)
系统: Ubuntu 22.04 LTS
带宽: 5Mbps (最低)
```

#### 步骤2：安装 Docker

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sudo sh

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER
```

#### 步骤3：部署应用

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin

# 启动服务
docker-compose up -d

# 配置防火墙
sudo ufw allow 8000  # API
sudo ufw allow 7860  # Web
```

#### 步骤4：访问服务

```
API文档: http://你的服务器IP:8000/docs
Web界面: http://你的服务器IP:7860
```

---

### 2️⃣ 腾讯云 CVM

#### 步骤1：创建云服务器

```
平台: 腾讯云 CVM
配置: 2核4G S2 SA2
系统: Ubuntu 22.04 LTS
带宽: 5Mbps
```

#### 步骤2：部署应用

```bash
# SSH 连接到服务器
ssh root@你的服务器IP

# 安装 Docker
curl -fsSL https://get.docker.com | sudo sh

# 克隆并部署
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin
docker-compose up -d

# 配置安全组（控制台）
# 入口规则: 8000, 7860 端口
```

#### 步骤3：域名配置（可选）

```bash
# 安装 Nginx
sudo apt install nginx -y

# 配置反向代理
sudo nano /etc/nginx/sites-available/tcd-origin
```

配置内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
    }

    location / {
        proxy_pass http://127.0.0.1:7860/;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/tcd-origin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### 3️⃣ AWS EC2

#### 步骤1：启动实例

```
Instance Type: t3.medium (2vCPU, 4GB)
AMI: Ubuntu 22.04 LTS
Storage: 20GB
Security Group: 开放 8000, 7860 端口
```

#### 步骤2：部署应用

```bash
# SSH 连接
ssh -i your-key.pem ubuntu@your-instance-ip

# 安装 Docker
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker

# 克隆部署
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin
docker-compose up -d
```

#### 步骤3：配置域名（可选）

使用 Route 53 或其他 DNS 服务指向 EC2 实例IP。

---

### 4️⃣ 阿里云函数计算（Serverless）

#### 步骤1：准备代码

```bash
# 创建函数计算项目
mkdir tcd-origin-fc && cd tcd-origin-fc

# 复制必要文件
cp -r ../api ./src
cp ../requirements.txt .
```

#### 步骤2：编写函数

```python
# index.py
import sys
sys.path.insert(0, '/code')

from api.main import app

def handler(environ, start_response):
    return app(environ, start_response)
```

#### 步骤3：部署

```bash
# 安装 fun 工具
npm install @alicloud/fun -g

# 配置凭证
fun config

# 部署
fun deploy
```

---

### 5️⃣ Docker Hub 自动部署

#### 步骤1：创建 Dockerfile

项目已包含 `Dockerfile`，直接使用。

#### 步骤2：构建镜像

```bash
# 登录 Docker Hub
docker login

# 构建镜像
docker build -t your-dockerhub-username/tcd-origin:latest .

# 推送镜像
docker push your-dockerhub-username/tcd-origin:latest
```

#### 步骤3：在云平台使用镜像

```bash
# 在云服务器拉取镜像
docker pull your-dockerhub-username/tcd-origin:latest

# 运行容器
docker run -d -p 8000:8000 -p 7860:7860 your-dockerhub-username/tcd-origin:latest
```

---

## 🌐 免费部署平台

### 1️⃣ Railway（推荐⭐）

#### 优点
- ✅ 免费额度充足
- ✅ 支持 Docker
- ✅ 自动 HTTPS
- ✅ 简单易用

#### 部署步骤

1. 访问 [railway.app](https://railway.app)
2. GitHub 登录
3. New Project → Deploy from GitHub repo
4. 选择仓库
5. Railway 自动检测并部署

#### 配置环境变量

```
VOLCENGINE_API_KEY = your_key
LLM_API_KEY = your_key
```

---

### 2️⃣ Render

#### 优点
- ✅ 免费套餐
- ✅ 支持 Docker
- ✅ 自动 HTTPS
- ✅ 简单部署

#### 部署步骤

1. 访问 [render.com](https://render.com)
2. GitHub 登录
3. New → Web Service
4. 连接到 GitHub 仓库
5. 设置：
   - Build Command: `docker-compose build`
   - Start Command: `docker-compose up -d`

---

### 3️⃣ Fly.io

#### 优点
- ✅ 免费额度
- ✅ 全球部署
- ✅ 自动 HTTPS
- ✅ 支持 Docker

#### 部署步骤

```bash
# 安装 flyctl
curl -L https://fly.io/install.sh | sh

# 登录
fly auth login

# 部署
fly launch
fly deploy
```

---

### 4️⃣ Google Cloud Run

#### 优点
- ✅ 每次请求计费（免费额度内免费）
- ✅ 自动扩缩容
- ✅ 全托管服务
- ✅ 自动 HTTPS

#### 部署步骤

```bash
# 安装 gcloud
curl https://sdk.cloud.google.com | bash
gcloud init

# 构建并推送镜像
gcloud builds submit --tag gcr.io/PROJECT_ID/tcd-origin

# 部署
gcloud run deploy tcd-origin \
  --image gcr.io/PROJECT_ID/tcd-origin \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🐳 Docker 高级配置

### 1️⃣ 使用 GPU 加速

```yaml
# docker-compose.gpu.yml
version: '3.8'

services:
  api:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - CUDA_VISIBLE_DEVICES=0
```

启动：
```bash
docker-compose -f docker-compose.gpu.yml up -d
```

---

### 2️⃣ 配置 Redis 缓存

```yaml
# docker-compose.with-redis.yml
services:
  api:
    depends_on:
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

---

### 3️⃣ 配置 HTTPS（Let's Encrypt）

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 📊 监控与日志

### 1️⃣ 使用 Prometheus

```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

### 2️⃣ 日志管理

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务
docker-compose logs -f api

# 保存日志到文件
docker-compose logs > app.log

# 配置日志轮转
# /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

---

## 🔒 安全配置

### 1️⃣ 设置环境变量

```bash
# .env 文件（不要提交到Git）
VOLCENGINE_API_KEY=your_secret_key
LLM_API_KEY=your_secret_key
```

### 2️⃣ 限制 API 访问

```python
# api/middleware.py
from fastapi import Request, HTTPException

async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
```

### 3️⃣ 配置 CORS

```python
# api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # 只允许你的域名
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 🚀 性能优化

### 1️⃣ 使用 uWSGI

```python
# wsgi.py
from api.main import app

application = app
```

```ini
; uwsgi.ini
[uwsgi]
http = :8000
wsgi-file = wsgi.py
processes = 4
threads = 2
```

### 2️⃣ 配置 Gunicorn

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  api.main:app
```

### 3️⃣ 使用 CDN

```nginx
# Nginx 配置
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 📞 获取帮助

- 📖 详细文档: [README.md](./README.md)
- 🐛 问题反馈: [GitHub Issues](https://github.com/YOUR_USERNAME/tcd-origin/issues)
- 💬 讨论组: [GitHub Discussions](https://github.com/YOUR_USERNAME/tcd-origin/discussions)
- 📧 邮箱: support@tcd-origin.com

---

## ✅ 部署检查清单

在部署前，请确认以下内容：

- [ ] GitHub 仓库已创建
- [ ] 代码已推送到仓库
- [ ] Docker 已安装
- [ ] 云服务器已购买（或使用免费平台）
- [ ] 域名已配置（可选）
- [ ] 环境变量已设置
- [ ] 防火墙端口已开放
- [ ] 服务已启动
- [ ] 健康检查通过
- [ ] 用户测试通过

---

**🎉 恭喜！您的 TCD Origin 智能体已成功部署到线上！**

*现在用户可以通过 API 或 Web 界面使用您的智能体了！*
