# 🚀 最简单的部署方式（3分钟上手）

## 方式一：使用快速启动脚本（推荐新手）

### 第一步：获取 API Key

1. 访问 [Moonshot AI 控制台](https://platform.moonshot.cn/console/api-keys)
2. 注册/登录账号
3. 创建 API Key
4. 复制 API Key（类似：`sk-xxxxx...`）

### 第二步：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的 API Key
nano .env
```

找到这一行：
```
COZE_WORKLOAD_IDENTITY_API_KEY=your_moonshot_api_key_here
```

替换为：
```
COZE_WORKLOAD_IDENTITY_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

保存并退出（按 `Ctrl+X`，然后 `Y`，然后 `Enter`）

### 第三步：启动服务

```bash
# 使用快速启动脚本
./quick_start.sh
```

选择 `1`（开发模式）或 `2`（生产模式）

### 第四步：验证部署

打开浏览器，访问：
```
http://localhost:8000/docs
```

你应该能看到 API 文档界面。

---

## 方式二：一行命令启动（最快速）

如果您已经配置好 `.env` 文件：

```bash
# 开发模式（支持热重载）
uvicorn src.web_api_new:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn src.web_api_new:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 方式三：Docker 部署（最稳定）

```bash
# 一键启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 🎯 快速测试

### 测试 1：健康检查

```bash
curl http://localhost:8000/health
```

预期输出：
```json
{
  "status": "healthy",
  "timestamp": "2025-01-10T10:00:00Z",
  "checks": {}
}
```

### 测试 2：文本分析

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，请介绍一下甲骨文"}'
```

### 测试 3：对话

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "什么是甲骨文？", "session_id": "test-123"}'
```

---

## 🌐 访问前端界面

启动服务后，在浏览器中访问：

```
http://localhost:8000/static/index.html
```

你将看到一个现代化的古文字破译界面！

---

## 🔧 常见问题

### Q: 提示 "Invalid API key"

**A**: 检查 `.env` 文件中的 API Key 是否正确，确保没有多余的空格。

### Q: 端口 8000 被占用

**A**: 修改 `.env` 文件中的 `PORT=8000` 为其他端口，如 `PORT=8001`

### Q: 如何停止服务？

**A**: 
- 开发模式：按 `Ctrl+C`
- Docker 模式：`docker-compose down`

### Q: 如何查看日志？

**A**:
```bash
# Docker 模式
docker-compose logs -f

# 本地模式
# 日志会直接输出到终端
```

---

## 📚 下一步

1. **阅读文档**
   - [完整部署指南](QUICK_START_DEPLOYMENT.md)
   - [API 文档](docs/API_DOCUMENTATION.md)
   - [插件开发指南](docs/PLUGIN_DEVELOPMENT.md)

2. **开发插件**
   - 参考 `plugins/ocr_tool/` 示例
   - 按照插件开发指南创建自己的插件

3. **生产部署**
   - 使用 Docker 或 Render
   - 配置 Nginx 和 HTTPS
   - 设置监控和告警

---

## 🆘 需要帮助？

- 查看日志：`docker-compose logs -f`
- 检查配置：`cat .env`
- 测试 API：访问 `http://localhost:8000/docs`

---

**祝您使用愉快！** 🎉
