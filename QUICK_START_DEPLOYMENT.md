# 快速部署指南

古文字破译系统 - 智能体部署指南

## 📋 部署前准备

### 1. 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| 操作系统 | Linux / macOS / Windows | Ubuntu 22.04 LTS |
| Python | 3.10+ | 3.12 |
| 内存 | 2GB | 4GB+ |
| CPU | 2核 | 4核+ |
| 磁盘 | 10GB | 20GB+ |
| 网络 | 需要访问LLM API | 稳定的网络连接 |

### 2. 环境变量配置

创建 `.env` 文件：

```bash
# 必需的环境变量
COZE_WORKSPACE_PATH=/workspace/projects
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1

# 可选的环境变量
LOG_LEVEL=INFO
MAX_MESSAGES=40
PORT=8000
```

---

## 🚀 部署方式

### 方式一：本地部署（开发/测试）

适用于开发、测试和小规模使用。

#### 步骤 1: 安装依赖

```bash
# 确保使用 Python 3.12
python --version

# 安装依赖
pip install -r requirements.txt
```

#### 步骤 2: 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的 API Key
nano .env
```

#### 步骤 3: 启动服务

```bash
# 方式1: 使用 Python 直接运行
python -m src.web_api_new

# 方式2: 使用 uvicorn
uvicorn src.web_api_new:app --host 0.0.0.0 --port 8000 --reload

# 方式3: 使用旧版 API（兼容模式）
python -m src.web_api
```

#### 步骤 4: 验证部署

```bash
# 检查健康状态
curl http://localhost:8000/health

# 访问 API 文档
# 在浏览器中打开: http://localhost:8000/docs
```

#### 步骤 5: 使用前端界面

```bash
# 启动服务后，在浏览器中访问
http://localhost:8000/static/index.html
```

---

### 方式二：Docker 部署（推荐）

适用于生产环境和容器化部署。

#### 步骤 1: 构建 Docker 镜像

```bash
# 构建 Docker 镜像
docker build -t ancient-script-decipherment:latest .

# 或者使用 docker-compose
docker-compose build
```

#### 步骤 2: 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

#### 步骤 3: 启动容器

```bash
# 使用 docker-compose 启动（推荐）
docker-compose up -d

# 或者使用 docker 命令
docker run -d \
  --name ancient-script \
  -p 8000:8000 \
  --env-file .env \
  ancient-script-decipherment:latest
```

#### 步骤 4: 查看日志

```bash
# 查看容器日志
docker-compose logs -f

# 或者
docker logs -f ancient-script
```

#### 步骤 5: 验证部署

```bash
# 检查健康状态
curl http://localhost:8000/health
```

#### 步骤 6: 停止服务

```bash
# 停止容器
docker-compose down

# 或者
docker stop ancient-script
docker rm ancient-script
```

---

### 方式三：Render 一键部署（云端）

适用于快速部署到云端，无需服务器。

#### 步骤 1: 准备 GitHub 仓库

```bash
# 初始化 Git 仓库（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 推送到 GitHub
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

#### 步骤 2: 连接 Render

1. 访问 https://render.com
2. 注册/登录账号
3. 点击 "New+" → "Web Service"
4. 连接您的 GitHub 仓库
5. 选择分支（main）

#### 步骤 3: 配置部署

在 Render 配置页面：

```
Name: ancient-script-decipherment
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.web_api_new:app --host 0.0.0.0 --port $PORT
```

#### 步骤 4: 配置环境变量

在 Render 环境变量页面添加：

```
COZE_WORKSPACE_PATH=/opt/render/project/src
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1
LOG_LEVEL=INFO
MAX_MESSAGES=40
```

#### 步骤 5: 部署

点击 "Create Web Service"，Render 会自动构建和部署。

#### 步骤 6: 访问服务

部署完成后，Render 会提供一个 URL，例如：
```
https://your-app.onrender.com
```

访问 API 文档：
```
https://your-app.onrender.com/docs
```

---

### 方式四：云服务器部署（VPS）

适用于需要完全控制的生产环境。

#### 步骤 1: 购买服务器

推荐云服务商：
- 阿里云
- 腾讯云
- 华为云
- AWS
- Google Cloud

配置建议：
- CPU: 2核+
- 内存: 4GB+
- 系统: Ubuntu 22.04 LTS

#### 步骤 2: 连接服务器

```bash
# SSH 连接
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y
```

#### 步骤 3: 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装 Docker Compose
apt install docker-compose -y

# 启动 Docker
systemctl start docker
systemctl enable docker
```

#### 步骤 4: 部署应用

```bash
# 克隆代码
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 配置环境变量
cp .env.example .env
nano .env

# 启动服务
docker-compose up -d
```

#### 步骤 5: 配置 Nginx（可选）

```bash
# 安装 Nginx
apt install nginx -y

# 配置 Nginx
nano /etc/nginx/sites-available/ancient-script
```

Nginx 配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置：

```bash
ln -s /etc/nginx/sites-available/ancient-script /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 步骤 6: 配置 HTTPS（推荐）

```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 获取 SSL 证书
certbot --nginx -d your-domain.com

# 自动续期
certbot renew --dry-run
```

---

## 🔍 验证部署

### 1. 健康检查

```bash
curl http://your-domain.com/health
```

预期响应：

```json
{
  "status": "healthy",
  "timestamp": "2025-01-10T10:00:00Z",
  "checks": {
    "engine": {
      "status": "healthy",
      "message": "Engine is running"
    }
  }
}
```

### 2. API 测试

```bash
# 测试文本分析
curl -X POST http://your-domain.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "测试文本"}'

# 测试图像分析
curl -X POST http://your-domain.com/api/v1/analyze/image \
  -F "file=@test_image.jpg"

# 测试对话
curl -X POST http://your-domain.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "test-session"}'
```

### 3. 性能测试

```bash
# 安装 Apache Bench
apt install apache2-utils -y

# 测试并发性能
ab -n 1000 -c 10 http://your-domain.com/health
```

---

## 🛠️ 常见问题

### 1. 端口被占用

**问题**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或者使用其他端口
uvicorn src.web_api_new:app --port 8001
```

### 2. 权限错误

**问题**: `Permission denied`

**解决**:
```bash
# 赋予执行权限
chmod +x scripts/*.sh

# 或者使用 sudo
sudo python -m src.web_api_new
```

### 3. 依赖安装失败

**问题**: `pip install` 失败

**解决**:
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者升级 pip
pip install --upgrade pip
```

### 4. API Key 错误

**问题**: `Invalid API key`

**解决**:
```bash
# 检查环境变量
echo $COZE_WORKLOAD_IDENTITY_API_KEY

# 重新配置 .env 文件
nano .env

# 重启服务
docker-compose restart
```

### 5. 内存不足

**问题**: `Out of memory`

**解决**:
```bash
# 限制消息数量
export MAX_MESSAGES=20

# 或者增加交换空间
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## 📊 监控和日志

### 1. 查看日志

```bash
# Docker 日志
docker-compose logs -f

# 应用日志
tail -f /app/work/logs/bypass/app.log

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. 性能监控

访问监控端点：

```bash
curl http://your-domain.com/api/v1/metrics
```

### 3. 系统监控

```bash
# CPU 和内存
top

# 磁盘使用
df -h

# 网络连接
netstat -tunlp
```

---

## 🔒 安全建议

### 1. 启用认证（生产环境）

```python
# 在 web_api_new.py 中添加认证
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.get("/api/v1/analyze")
async def analyze_text(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # 验证 token
    pass
```

### 2. 配置防火墙

```bash
# 只允许必要的端口
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### 3. 定期更新

```bash
# 更新系统和依赖
apt update && apt upgrade -y
pip install --upgrade -r requirements.txt
```

### 4. 备份数据

```bash
# 定期备份数据库和配置
crontab -e

# 添加定时任务
0 2 * * * /path/to/backup.sh
```

---

## 📞 技术支持

如有问题，请联系：

- **文档**: `docs/DEPLOYMENT_GUIDE.md`
- **API文档**: `docs/API_DOCUMENTATION.md`
- **插件开发**: `docs/PLUGIN_DEVELOPMENT.md`
- **GitHub Issues**: https://github.com/your-username/your-repo/issues

---

## 🎉 部署完成

恭喜！您的古文字破译智能体已成功部署！

**下一步**:
1. 访问 API 文档: `http://your-domain.com/docs`
2. 测试核心功能
3. 配置监控和告警
4. 根据需要添加插件

---

**文档版本**: v2.0  
**更新日期**: 2025-01-10
