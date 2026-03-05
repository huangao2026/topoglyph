# 🚀 一键部署指南

## ⚡ 真正的一键部署

**是的！现在您只需要运行一个命令，就能完成配置和部署！**

---

## 📝 使用方法

### 3步完成部署

```bash
# 1. 进入项目目录
cd /path/to/ancient-script

# 2. 运行一键部署脚本
./deploy.sh

# 3. 输入 Moonshot AI API Key
#    访问：https://platform.moonshot.cn/console/api-keys

# 完成！
```

---

## 🎯 一键部署脚本做什么

**自动完成以下操作**：

1. ✅ **检查依赖** - Docker、Docker Compose
2. ✅ **配置环境变量** - 自动生成所有密码和密钥
3. ✅ **拉取镜像** - PostgreSQL、Redis、Nginx
4. ✅ **构建应用** - 编译应用镜像
5. ✅ **启动服务** - 启动所有容器
6. ✅ **等待就绪** - 等待数据库初始化
7. ✅ **验证部署** - 测试所有服务

**用户只需要**：
- 输入 Moonshot AI API Key
- 等待完成

---

## 📋 部署流程

```
======================================
古文字破译系统 - 一键部署脚本
======================================

此脚本将自动完成以下操作：
  1. 检查依赖（Docker、Docker Compose）
  2. 配置环境变量（API Token、密码等）
  3. 拉取 Docker 镜像
  4. 构建应用镜像
  5. 启动所有服务
  6. 等待服务就绪
  7. 验证部署

是否开始部署？(y/n): y

======================================
步骤 1: 检查依赖
======================================

[SUCCESS] Docker 已安装: Docker version 24.0.0
[SUCCESS] Docker Compose 已安装: Docker Compose version 2.20.0
[SUCCESS] openssl 已安装

======================================
步骤 2: 配置环境变量
======================================

[INFO] 开始配置环境变量...
[INFO] 配置 Moonshot AI API Key
  访问: https://platform.moonshot.cn/console/api-keys
  请输入您的 Moonshot AI API Key: sk-abc123...
[INFO] 生成数据库密码...
[INFO] 生成应用密钥...
[INFO] 生成 Redis 密码...
[INFO] 生成 JWT 密钥...
[SUCCESS] 环境变量配置完成

======================================
步骤 3: 拉取 Docker 镜像
======================================

[INFO] 拉取 PostgreSQL 镜像...
[INFO] 拉取 Redis 镜像...
[INFO] 拉取 Nginx 镜像...
[SUCCESS] 镜像拉取完成

======================================
步骤 4: 构建应用镜像
======================================

[INFO] 构建应用镜像（这可能需要几分钟）...
...
[SUCCESS] 应用镜像构建完成

======================================
步骤 5: 启动服务
======================================

[INFO] 启动所有服务...
Creating network "ancient-network" ...
Creating volume "ancient-script_postgres_data" ...
Creating volume "ancient-script_redis_data" ...
Creating ancient-text-ai-db ...
Creating ancient-text-ai-redis ...
Creating ancient-text-ai-web ...
Creating ancient-text-ai-nginx ...
[SUCCESS] 服务已启动

======================================
步骤 6: 等待服务就绪
======================================

[INFO] 等待数据库初始化（约30秒）...
[INFO] 检查数据库状态...
[SUCCESS] 数据库已就绪
[INFO] 检查 Redis 状态...
[SUCCESS] Redis 已就绪
[INFO] 检查应用状态...
[SUCCESS] 应用已就绪
[SUCCESS] 所有服务已就绪

======================================
步骤 7: 验证部署
======================================

[INFO] 检查服务状态...
NAME                    COMMAND             STATUS         PORTS
ancient-text-ai-db      ...                 Up 2 minutes   5432->5432
ancient-text-ai-redis   ...                 Up 2 minutes   6379->6379
ancient-text-ai-web     ...                 Up 1 minute    0.0.0.0:8000->8000
ancient-text-ai-nginx   ...                 Up 1 minute    80->80, 443->443

[INFO] 测试数据库连接...
[SUCCESS] 数据库连接正常
[INFO] 测试 Redis 连接...
[SUCCESS] Redis 连接正常
[INFO] 测试应用健康检查...
[SUCCESS] 应用健康检查通过
[SUCCESS] 部署验证完成

======================================
部署完成
======================================

🎉 古文字破译系统部署成功！

服务访问地址：
  📡 API 文档: http://localhost:8000/docs
  🌐 前端界面: http://localhost:8000/static/index.html
  ❤️  健康检查: http://localhost:8000/health

常用命令：
  📋 查看状态: docker-compose ps
  📜 查看日志: docker-compose logs -f
  🔄 重启服务: docker-compose restart
  ⏹️  停止服务: docker-compose down

服务信息：
  🗄️  数据库: localhost:5432
  🔴 Redis: localhost:6379
  🌐 Web 应用: localhost:8000

⚠️  重要提示：
  • 请妥善保存配置信息（.env 文件）
  • 不要将 .env 文件提交到 Git 仓库
  • 定期更换 Token（建议每3-6个月）
  • 定期备份数据（./scripts/backup.sh）

部署已完成，系统可以正常使用！
```

---

## 🎯 部署前准备

### 1. 安装 Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# macOS
brew install --cask docker

# Windows
# 下载 Docker Desktop: https://www.docker.com/products/docker-desktop
```

### 2. 安装 Docker Compose

```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# macOS/Windows
# Docker Desktop 已包含 Docker Compose
```

### 3. 获取 Moonshot AI API Key

1. 访问 [Moonshot AI 控制台](https://platform.moonshot.cn/console/api-keys)
2. 登录或注册账号
3. 点击"创建 API Key"
4. 复制生成的 API Key（格式：`sk-xxxxx...`）

---

## ✅ 部署验证

部署完成后，验证系统是否正常：

```bash
# 1. 查看服务状态
docker-compose ps

# 应该看到所有服务都是 "Up" 状态

# 2. 测试健康检查
curl http://localhost:8000/health

# 应该返回：{"status": "healthy"}

# 3. 访问前端界面
# 浏览器打开：http://localhost:8000/static/index.html

# 4. 访问 API 文档
# 浏览器打开：http://localhost:8000/docs
```

---

## 🆘 常见问题

### Q1: 脚本无法执行

**A**: 添加执行权限

```bash
chmod +x deploy.sh
./deploy.sh
```

### Q2: Docker 未安装

**A**: 安装 Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Q3: API Key 格式错误

**A**: 确保格式正确

- ✅ 正确：`sk-abc123def456...`
- ❌ 错误：`sk abc123`（空格）
- ❌ 错误：`abc123`（缺少 sk- 前缀）

### Q4: 部署失败

**A**: 查看日志

```bash
docker-compose logs -f
```

---

## 📚 相关文档

- [API_TOKEN_SETUP.md](API_TOKEN_SETUP.md) - Token 配置详情
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - 数据库配置详情
- [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) - 云服务器部署

---

## 🎉 总结

### 配置 vs 部署

| 操作 | 说明 | 脚本 |
|------|------|------|
| **配置** | 替换 API Token、生成密码等 | `setup-config.sh` |
| **部署** | 启动服务、构建镜像等 | `deploy.sh` |

### 一键部署

**✅ `deploy.sh` = 配置 + 部署**

**是的！现在您只需要运行一个命令：**

```bash
./deploy.sh
```

**就能完成所有配置和部署！** 🚀

---

**从输入命令到系统可用，大约需要 5-10 分钟！** ⏱️

**现在就开始吧！** 🎯
