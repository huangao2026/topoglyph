# 古代文字破解智能体 - 全球部署方案

> 🌍 让古文字知识服务全球学者和爱好者

---

## 📋 目录

- [部署架构](#部署架构)
- [方案选择](#方案选择)
- [快速部署（推荐）](#快速部署推荐)
- [专业部署](#专业部署)
- [前端开发](#前端开发)
- [安全与优化](#安全与优化)
- [成本估算](#成本估算)
- [运维监控](#运维监控)

---

## 🏗️ 部署架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户访问层                            │
│  Web浏览器  │  移动端App  │  API调用  │  第三方集成        │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS / CDN
┌──────────────────────▼──────────────────────────────────┐
│                    负载均衡层 (Nginx/Cloudflare)          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   Web应用层 (FastAPI)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Web服务  │  │ API服务  │  │ WebSocket│              │
│  │ (HTTP)   │  │ (REST)   │  │ (实时)   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   业务逻辑层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ LangChain│  │ Agent核心│  │ 工具调用 │              │
│  │ 框架     │  │ 逻辑     │  │ 模块     │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   AI模型层                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ LLM      │  │ 视觉模型 │  │ OCR模型  │              │
│  │ (Kimi)   │  │ (Vision) │  │ (可选)   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   数据存储层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ PostgreSQL│  │ Redis    │  │ S3/对象  │              │
│  │ (主数据库)│  │ (缓存)   │  │ 存储     │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 方案选择

根据需求选择合适的部署方案：

| 方案 | 适用场景 | 技术要求 | 月成本 | 部署时间 | 推荐指数 |
|:---|:---|:---|:---|:---|:---:|
| **方案A：H版云平台** | 快速上线，个人/小团队 | 低 | $20-50 | 30分钟 | ⭐⭐⭐⭐⭐ |
| **方案B：Docker + 云服务器** | 中小规模，灵活可控 | 中 | $50-150 | 2-4小时 | ⭐⭐⭐⭐ |
| **方案C：Kubernetes集群** | 大规模，高可用 | 高 | $200-500+ | 1-2天 | ⭐⭐⭐ |
| **方案D：混合云** | 企业级，多地部署 | 高 | $500+ | 3-5天 | ⭐⭐ |

---

## 🚀 方案A：一键部署（推荐新手）

### 适合人群
- 🎓 学生、研究者
- 👥 小型团队（1-5人）
- 💡 想快速体验的用户
- 📱 日访问量 < 1000

### 推荐平台
- **Render** (https://render.com) - 最简单，免费额度
- **Railway** (https://railway.app) - 开发者友好
- **Vercel** (https://vercel.com) - Web应用最佳
- **Hugging Face Spaces** - AI模型部署首选

### 详细步骤（Render示例）

#### 1. 准备代码
```bash
# 确保项目结构正确
/workspace/projects/
├── src/
│   ├── agents/
│   │   └── agent.py
│   └── main.py
├── config/
│   └── agent_llm_config.json
├── requirements.txt
└── .gitignore
```

#### 2. 创建GitHub仓库
```bash
cd /workspace/projects
git init
git add .
git commit -m "Initial commit: Ancient Text AI Agent"
git remote add origin https://github.com/yourusername/ancient-text-ai.git
git push -u origin main
```

#### 3. 配置环境变量

在 Render 中设置以下环境变量：

```bash
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url_here
COZE_WORKSPACE_PATH=/opt/render/project/src
PYTHON_VERSION=3.12
```

#### 4. 创建部署文件

创建 `render.yaml`：

```yaml
services:
  - type: web
    name: ancient-text-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: COZE_WORKLOAD_IDENTITY_API_KEY
        sync: false
      - key: COZE_INTEGRATION_MODEL_BASE_URL
        sync: false
    plan: free  # 免费版，或选择 starter ($7/月)
```

#### 5. 部署
```bash
# 在 Render 控制台
1. 点击 "New +"
2. 选择 "Web Service"
3. 连接你的 GitHub 仓库
4. 配置环境变量
5. 点击 "Deploy Web Service"
```

#### 6. 获取访问地址
部署完成后，Render 会提供：
- `https://ancient-text-ai.onrender.com`

### 优缺点
✅ **优点**：
- 零配置，自动扩容
- 自动 HTTPS
- 免费额度（750小时/月）
- Git 集成

❌ **缺点**：
- 免费版有休眠限制
- 自定义程度较低
- 高并发需升级套餐

---

## 💼 方案B：Docker + 云服务器（推荐专业）

### 适合人群
- 🔬 专业研究者
- 🏢 中小团队（5-50人）
- 📊 日访问量 1000-10000
- 🔧 需要自定义配置

### 推荐平台
- **阿里云 ECS**
- **腾讯云 CVM**
- **AWS EC2**
- **DigitalOcean** (最简单)

### 详细步骤（DigitalOcean示例）

#### 1. 准备Dockerfile

创建 `Dockerfile`：

```dockerfile
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - COZE_WORKLOAD_IDENTITY_API_KEY=${API_KEY}
      - COZE_INTEGRATION_MODEL_BASE_URL=${BASE_URL}
      - COZE_WORKSPACE_PATH=/app
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=ancienttext
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=ancienttext
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

#### 3. 创建.env文件

```bash
# API配置
API_KEY=your_api_key_here
BASE_URL=your_base_url_here

# 数据库配置
DB_PASSWORD=your_strong_password_here
DATABASE_URL=postgresql://ancienttext:${DB_PASSWORD}@db:5432/ancienttext
REDIS_URL=redis://redis:6379/0

# 应用配置
SECRET_KEY=your_secret_key_for_sessions
ALLOWED_ORIGINS=https://yourdomain.com
```

#### 4. 购买并配置服务器

```bash
# 在 DigitalOcean 控制台
1. 创建 Droplet
   - 规格：4GB RAM, 2 vCPU, 80GB SSD ($24/月)
   - 系统：Ubuntu 22.04 LTS
   - 地区：选择离用户最近的（如Singapore）

2. 等待服务器创建完成（约1分钟）

3. SSH登录
   ssh root@your_server_ip
```

#### 5. 安装Docker

```bash
# 在服务器上执行
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装 docker-compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

#### 6. 部署应用

```bash
# 克隆代码
git clone https://github.com/yourusername/ancient-text-ai.git
cd ancient-text-ai

# 创建.env文件
cp .env.example .env
nano .env  # 填入你的配置

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f web

# 访问服务
curl http://localhost:8000
```

#### 7. 配置Nginx反向代理

```bash
# 安装Nginx
apt update
apt install nginx -y

# 创建配置文件
nano /etc/nginx/sites-available/ancient-text-ai
```

Nginx配置内容：

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket支持
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

启用配置：

```bash
ln -s /etc/nginx/sites-available/ancient-text-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 8. 配置HTTPS（Let's Encrypt）

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx -y

# 获取SSL证书
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期
certbot renew --dry-run
```

#### 9. 配置防火墙

```bash
ufw allow ssh
ufw allow http
ufw allow https
ufw enable
```

### 优缺点
✅ **优点**：
- 完全控制
- 性能可预测
- 成本可控
- 可扩展性强

❌ **缺点**：
- 需要运维知识
- 需要手动维护
- 初始设置较复杂

---

## 🏛️ 方案C：Kubernetes集群（企业级）

### 适合人群
- 🏢 大型企业
- 🔬 研究机构
- 📈 高并发需求（日访问量 10,000+）
- 🔒 需要高可用性

### 推荐平台
- **AWS EKS**
- **Google Cloud GKE**
- **Azure AKS**
- **阿里云 ACK**

### 架构示例

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ancient-text-ai
spec:
  replicas: 3  # 3个副本保证高可用
  selector:
    matchLabels:
      app: ancient-text-ai
  template:
    metadata:
      labels:
        app: ancient-text-ai
    spec:
      containers:
      - name: ancient-text-ai
        image: yourregistry/ancient-text-ai:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secret
              key: api-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"

---
apiVersion: v1
kind: Service
metadata:
  name: ancient-text-ai
spec:
  selector:
    app: ancient-text-ai
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## 💰 成本估算

### 方案对比（月成本）

| 方案 | 免费额度 | 基础套餐 | 专业套餐 | 企业套餐 |
|:---|:---:|:---:|:---:|:---:|
| **Render** | $0 | $7 | $25 | $100 |
| **DigitalOcean** | $0 | $24 | $80 | $200 |
| **AWS** | $0 | $50 | $150 | $500 |
| **阿里云** | $0 | ¥150 | ¥600 | ¥2000 |

### 成本构成

| 项目 | 基础版 | 专业版 |
|:---|:---:|:---:|
| 云服务器 | $24 | $80 |
| 数据库 | $15 | $50 |
| 存储（S3） | $5 | $20 |
| 域名 | $12/年 | $12/年 |
| SSL证书 | $0 | $0 |
| CDN | $0 | $20 |
| 监控 | $0 | $10 |
| **月总计** | **$46** | **$180** |

---

## 🔒 安全配置

### 1. 环境变量保护
```bash
# 永远不要将.env文件提交到Git
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets/" >> .gitignore
```

### 2. API限流
```python
# 在 FastAPI 中添加限流
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/analyze")
@limiter.limit("10/minute")  # 每分钟最多10次
async def analyze_text(request: Request, data: AnalyzeRequest):
    # ...
```

### 3. 内容过滤
```python
# 防止恶意输入
def validate_input(text: str) -> bool:
    if len(text) > 10000:  # 限制输入长度
        return False
    if contains_malicious_content(text):
        return False
    return True
```

### 4. 访问日志
```python
# 记录所有请求
import logging

logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s - %(ip)s - %(method)s - %(path)s'
)
```

---

## 📊 监控与运维

### 1. 健康检查
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }
```

### 2. 性能监控
```python
# 使用 Prometheus + Grafana
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.post("/api/analyze")
async def analyze_text(request: Request):
    with request_duration.time():
        request_count.inc()
        # 处理逻辑
```

### 3. 自动重启
```yaml
# docker-compose.yml
restart: unless-stopped  # 自动重启
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

## 🌐 国际化支持

### 1. 多语言界面
```python
SUPPORTED_LANGUAGES = {
    'zh': '中文',
    'en': 'English',
    'ja': '日本語',
    'ko': '한국어',
    'es': 'Español',
    'fr': 'Français'
}

@app.get("/api/i18n/{lang}")
async def get_i18n_messages(lang: str):
    return get_translations(lang)
```

### 2. 多地区部署
- 亚太：新加坡、东京
- 北美：弗吉尼亚、加州
- 欧洲：法兰克福、伦敦

---

## 📱 移动端适配

### PWA支持
```html
<!-- manifest.json -->
{
  "name": "Ancient Text AI",
  "short_name": "AncientAI",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb"
}
```

---

## 🎓 教育版支持

### 学术机构折扣
- 🎓 提供学术机构专用套餐
- 📚 批量账号管理
- 🔒 数据安全保障
- 📊 使用报告

---

## 📞 技术支持

### 用户支持
- 📧 邮件：support@ancienttext.ai
- 💬 Discord 社区
- 📚 文档网站
- 🎥 视频教程

---

## 🚀 快速开始总结

### 10分钟部署（推荐）：
1. ✅ 创建 GitHub 仓库
2. ✅ 配置 Render.yaml
3. ✅ 设置环境变量
4. ✅ 一键部署

### 2小时部署（专业）：
1. ✅ 准备 Dockerfile
2. ✅ 购买云服务器
3. ✅ 配置 Nginx + SSL
4. ✅ 启动服务

---

需要我继续创建具体的代码文件吗？包括：
1. ✅ FastAPI 后端代码
2. ✅ Web 前端界面
3. ✅ Docker 配置
4. ✅ 数据库脚本
5. ✅ 部署脚本

请告诉我您选择哪个方案，我将为您生成完整的部署代码！ 🚀
