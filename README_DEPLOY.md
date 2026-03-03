# 古代文字破解智能体 - 部署指南

> 🌍 让古文字知识服务全球学者和爱好者

---

## 📋 快速开始

### 方案一：Render一键部署（推荐新手，5分钟）

1. **Fork本仓库到你的GitHub**
   ```bash
   # 访问 GitHub 并点击 Fork 按钮
   ```

2. **注册Render账号**
   - 访问 https://render.com
   - 使用GitHub账号登录

3. **创建Web Service**
   - 点击 "New +"
   - 选择 "Web Service"
   - 连接你Fork的仓库
   - 使用 `render.yaml` 配置

4. **设置环境变量**
   在Render控制台设置：
   - `COZE_WORKLOAD_IDENTITY_API_KEY`: 你的API密钥
   - `COZE_INTEGRATION_MODEL_BASE_URL`: 你的Base URL

5. **部署**
   - 点击 "Deploy Web Service"
   - 等待约2-3分钟
   - 访问生成的URL（如 `https://ancient-text-ai.onrender.com`）

### 方案二：Docker本地运行（推荐开发者）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/ancient-text-ai.git
cd ancient-text-ai

# 2. 配置环境变量
cp .env.example .env
nano .env  # 填入你的配置

# 3. 构建并启动
docker-compose up -d

# 4. 访问服务
open http://localhost:8000

# 5. 查看日志
docker-compose logs -f web
```

### 方案三：云服务器部署（推荐生产环境）

详细步骤请参考：[DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)

---

## 🔧 配置说明

### 必需的环境变量

| 变量名 | 说明 | 示例 |
|:---|:---|:---|
| `COZE_WORKLOAD_IDENTITY_API_KEY` | Coze API密钥 | `your_api_key` |
| `COZE_INTEGRATION_MODEL_BASE_URL` | Coze Base URL | `https://api.coze.com` |

### 可选的环境变量

| 变量名 | 说明 | 默认值 |
|:---|:---|:---|
| `SECRET_KEY` | 会话密钥 | 自动生成 |
| `ALLOWED_ORIGINS` | 跨域允许的源 | `*` |
| `RATE_LIMIT_PER_MINUTE` | 每分钟请求限制 | `10` |
| `MAX_UPLOAD_SIZE` | 最大上传大小（字节） | `10485760` |

---

## 📁 项目结构

```
ancient-text-ai/
├── src/
│   ├── agents/
│   │   └── agent.py              # Agent核心逻辑
│   ├── main.py                    # 原有主入口
│   └── web_api.py                 # Web API服务
├── config/
│   └── agent_llm_config.json      # Agent配置
├── static/
│   ├── index.html                 # 前端页面
│   ├── styles.css                 # 样式文件
│   └── app.js                     # 前端脚本
├── docs/
│   └── DEPLOYMENT_GUIDE.md        # 详细部署指南
├── tests/
│   └── test_api.py                # API测试
├── Dockerfile                     # Docker镜像
├── docker-compose.yml             # Docker编排
├── render.yaml                    # Render配置
├── requirements.txt               # Python依赖
└── README.md                      # 本文档
```

---

## 🚀 本地开发

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 运行开发服务器

```bash
# 设置环境变量
export COZE_WORKLOAD_IDENTITY_API_KEY=your_key
export COZE_INTEGRATION_MODEL_BASE_URL=your_url

# 启动服务
uvicorn src.web_api:app --reload --host 0.0.0.0 --port 8000
```

### 访问应用

- Web界面: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行API测试
pytest tests/test_api.py

# 带覆盖率报告
pytest --cov=src --cov-report=html
```

---

## 📊 API端点

### 健康检查
```http
GET /health
```

### 文本分析
```http
POST /api/analyze
Content-Type: application/json

{
  "text": "请分析这段古文字...",
  "language": "zh"
}
```

### 图像识别
```http
POST /api/analyze/image
Content-Type: multipart/form-data

image: [文件]
params: {"language": "zh"}
```

### 获取工具列表
```http
GET /api/tools
```

### 获取支持的语言
```http
GET /api/languages
```

---

## 🔒 安全配置

### 1. 环境变量保护
```bash
# 永远不要将 .env 文件提交到 Git
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
```

### 2. 限流配置
已在应用中启用，默认每分钟10次请求。

### 3. HTTPS配置
生产环境建议使用Nginx + Let's Encrypt自动配置HTTPS。

---

## 📈 监控与日志

### 查看日志
```bash
# Docker部署
docker-compose logs -f web

# Render部署
# 在Render控制台查看实时日志

# 本地部署
tail -f logs/app.log
```

### 性能监控
- 响应时间
- 请求成功率
- 错误率
- 资源使用率

---

## 🌍 多语言支持

当前支持的语言：
- 中文 (zh)
- English (en)
- 日本語 (ja)
- 한국어 (ko)
- Español (es)
- Français (fr)

---

## 💡 常见问题

### 1. 部署失败
- 检查环境变量是否正确设置
- 查看日志获取详细错误信息
- 确保所有依赖都已安装

### 2. API调用失败
- 验证API密钥是否有效
- 检查网络连接
- 查看限流是否触发

### 3. 图片上传失败
- 确保图片格式正确（JPG/PNG/TIFF）
- 检查文件大小是否超过限制（10MB）
- 验证上传目录权限

---

## 📞 技术支持

- 📧 Email: support@ancienttext.ai
- 💬 GitHub Issues: https://github.com/yourusername/ancient-text-ai/issues
- 📚 文档: https://docs.ancienttext.ai

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢所有为古文字研究做出贡献的学者和开发者！

---

**立即部署，让全球古文字爱好者受益！** 🌍🚀
