# 🚀 TCD Origin 部署快速参考

## ⚡ 一键部署（本地）

```bash
# 方式1：使用部署脚本
./deploy.sh

# 方式2：使用 Docker Compose
docker-compose up -d
```

访问：
- 🌐 Web界面: http://localhost:7860
- 📚 API文档: http://localhost:8000/docs

---

## ☁️ 云平台部署

### 阿里云 ECS
```bash
# 1. 安装Docker
curl -fsSL https://get.docker.com | sudo sh

# 2. 克隆部署
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin
docker-compose up -d

# 3. 开放端口
sudo ufw allow 8000
sudo ufw allow 7860
```

### 腾讯云 CVM
```bash
# 1. SSH连接
ssh root@your-ip

# 2. 安装Docker
curl -fsSL https://get.docker.com | sudo sh

# 3. 部署
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin
docker-compose up -d
```

### AWS EC2
```bash
# 1. 启动EC2（Ubuntu 22.04）
# 2. SSH连接
ssh -i key.pem ubuntu@your-ip

# 3. 安装Docker
sudo apt update
sudo apt install docker.io -y

# 4. 部署
git clone https://github.com/YOUR_USERNAME/tcd-origin.git
cd tcd-origin
docker-compose up -d
```

---

## 🌟 免费平台

### Railway
1. 访问 https://railway.app
2. GitHub登录
3. New Project → Deploy from GitHub
4. 自动部署完成

### Render
1. 访问 https://render.com
2. GitHub登录
3. New → Web Service
4. 连接到仓库
5. 设置启动命令

### Fly.io
```bash
# 安装工具
curl -L https://fly.io/install.sh | sh

# 部署
fly launch
fly deploy
```

### Google Cloud Run
```bash
# 构建镜像
gcloud builds submit --tag gcr.io/PROJECT/tcd-origin

# 部署
gcloud run deploy tcd-origin \
  --image gcr.io/PROJECT/tcd-origin \
  --platform managed
```

---

## 🐳 Docker 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 重新构建
docker-compose build --no-cache

# 查看状态
docker-compose ps
```

---

## 📡 API 使用示例

### Python
```python
import requests

# 上传图片分析
url = "http://localhost:8000/api/v1/analyze"
files = {"image": open("oracle.jpg", "rb")}
data = {"symbol_name": "日"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('symbol_name', '日');

fetch('http://localhost:8000/api/v1/analyze', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "image=@oracle.jpg" \
  -F "symbol_name=日"
```

---

## 🔧 配置环境变量

编辑 `.env` 文件：

```bash
# API配置
HOST=0.0.0.0
PORT=8000

# 火山引擎（可选）
VOLCENGINE_API_KEY=your_key

# LLM（可选）
LLM_API_KEY=your_key
LLM_MODEL=gpt-4
```

---

## 🛡️ 安全配置

### 1. 设置API密钥
```bash
echo "API_KEY=your_secret_key" >> .env
```

### 2. 限制CORS
```python
# api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)
```

### 3. 启用HTTPS
```bash
# 使用 Nginx + Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

---

## 📊 监控

```bash
# 查看资源使用
docker stats

# 查看日志
docker-compose logs -f api

# 健康检查
curl http://localhost:8000/health
```

---

## 🎯 下一步

1. [详细部署指南](./ONLINE_DEPLOYMENT_GUIDE.md)
2. [API文档](./README.md#🚀-快速开始)
3. [GitHub发布](./GITHUB_PUBLISH_CHECKLIST.md)

---

**版本**: 3.0.1  
**更新时间**: 2026-05-06
