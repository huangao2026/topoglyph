# 环境变量配置说明

古文字破译系统 - 完整的环境变量配置指南

---

## 📋 目录

1. [环境变量文件](#环境变量文件)
2. [必需配置](#必需配置)
3. [可选配置](#可选配置)
4. [数据库配置](#数据库配置)
5. [Redis配置](#Redis配置)
6. [安全配置](#安全配置)
7. [监控配置](#监控配置)
8. [开发配置](#开发配置)
9. [部署配置](#部署配置)

---

## 环境变量文件

### 文件位置

```
ancient-script/
├── .env.example      # 环境变量模板
└── .env              # 实际配置文件（不提交到 Git）
```

### 创建配置文件

```bash
# 复制模板
cp .env.example .env

# 编辑配置
nano .env
```

---

## 必需配置

这些配置项**必须**填写，否则系统无法正常运行。

### 1. Moonshot AI API Key

```bash
# Moonshot AI API Key（用于调用 Kimi K2.5 模型）
# 获取方式：https://platform.moonshot.cn/console/api-keys
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-moonshot-api-key-here
```

**说明**：
- 这是调用 Kimi K2.5 模型的凭证
- 请替换为您的实际 API Key
- 不要泄露 API Key，不要提交到版本控制系统

**获取 API Key**：
1. 访问：https://platform.moonshot.cn/console/api-keys
2. 登录或注册账号
3. 创建新的 API Key
4. 复制 API Key 并粘贴到配置文件

### 2. 工作空间路径

```bash
# 工作空间路径
COZE_WORKSPACE_PATH=/workspace/projects
```

**说明**：
- 项目根目录的绝对路径
- 通常不需要修改
- Docker 环境中使用默认值即可

### 3. API 基础 URL

```bash
# Moonshot AI API 基础 URL
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1
```

**说明**：
- Moonshot AI API 的基础 URL
- 通常不需要修改
- 如果使用自定义 API 端点，请修改此配置

---

## 可选配置

这些配置项有默认值，可以根据需要修改。

### 服务配置

```bash
# 服务端口
PORT=8000

# 服务主机地址
HOST=0.0.0.0

# 日志级别（DEBUG, INFO, WARNING, ERROR）
LOG_LEVEL=INFO

# 最大消息数量（滑动窗口大小）
MAX_MESSAGES=40

# 模型温度参数（0-1，越高越随机）
MODEL_TEMPERATURE=0.6

# 模型最大输出 Token 数
MAX_TOKENS=32768

# 请求超时时间（秒）
REQUEST_TIMEOUT=600
```

**说明**：
- `PORT`：服务监听端口，默认 8000
- `HOST`：服务监听地址，0.0.0.0 表示监听所有网卡
- `LOG_LEVEL`：日志级别，开发环境可用 DEBUG，生产环境建议 INFO
- `MAX_MESSAGES`：保留的对话消息数量
- `MODEL_TEMPERATURE`：模型生成随机性，0.0 最确定，1.0 最随机
- `MAX_TOKENS`：模型最大输出 Token 数
- `REQUEST_TIMEOUT`：API 请求超时时间（秒）

---

## 数据库配置

### PostgreSQL 配置

```bash
# PostgreSQL 数据库连接字符串
DATABASE_URL=postgresql://ancient_script:ancient_script_password@localhost:5432/ancient_script

# 数据库详细配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ancient_script
DB_USER=ancient_script
DB_PASSWORD=ancient_script_password

# 数据库连接池配置
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

**说明**：
- `DATABASE_URL`：完整的数据库连接字符串
- `DB_HOST`：数据库主机地址
- `DB_PORT`：数据库端口
- `DB_NAME`：数据库名称
- `DB_USER`：数据库用户名
- `DB_PASSWORD`：数据库密码（生产环境请修改）
- `DB_POOL_SIZE`：连接池大小
- `DB_MAX_OVERFLOW`：连接池溢出大小
- `DB_POOL_TIMEOUT`：连接池超时时间（秒）
- `DB_POOL_RECYCLE`：连接回收时间（秒）

**生产环境建议**：
- 修改默认密码
- 增加连接池大小
- 根据负载调整参数

---

## Redis配置

```bash
# Redis 连接字符串
REDIS_URL=redis://localhost:6379/0

# Redis 详细配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_MAX_CONNECTIONS=50

# 缓存过期时间（秒）
CACHE_TTL=3600
```

**说明**：
- `REDIS_URL`：Redis 连接字符串
- `REDIS_HOST`：Redis 主机地址
- `REDIS_PORT`：Redis 端口
- `REDIS_DB`：Redis 数据库编号（0-15）
- `REDIS_PASSWORD`：Redis 密码（可选）
- `REDIS_MAX_CONNECTIONS`：最大连接数
- `CACHE_TTL`：缓存过期时间（秒）

**生产环境建议**：
- 设置密码
- 增加连接数
- 根据 TTL 调整缓存策略

---

## 安全配置

### JWT 和 API Key

```bash
# JWT Secret（用于 API 认证）
JWT_SECRET=your_jwt_secret_key_here_change_this_in_production

# API Key（用于外部 API 访问）
API_KEY=your_api_key_here
```

**说明**：
- `JWT_SECRET`：JWT 签名密钥，生产环境必须修改为强随机字符串
- `API_KEY`：外部 API 访问密钥

**生成强密钥**：
```bash
# 生成 JWT Secret
openssl rand -hex 32

# 生成 API Key
openssl rand -hex 16
```

### CORS 配置

```bash
# CORS 允许的源（多个用逗号分隔）
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# 允许的 HTTP 方法
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS

# 允许的 HTTP 头
CORS_HEADERS=Content-Type,Authorization,X-API-Key
```

**说明**：
- `CORS_ORIGINS`：允许跨域访问的源列表
- `CORS_METHODS`：允许的 HTTP 方法
- `CORS_HEADERS`：允许的 HTTP 头

### API 限流配置

```bash
# 每分钟最大请求数
RATE_LIMIT_PER_MINUTE=60

# 每小时最大请求数
RATE_LIMIT_PER_HOUR=1000

# 每天最大请求数
RATE_LIMIT_PER_DAY=10000
```

**说明**：
- 用于防止 API 滥用
- 根据业务需求调整限制

---

## 监控配置

```bash
# 启用 Prometheus 监控
ENABLE_PROMETHEUS=false

# Prometheus 端口
PROMETHEUS_PORT=9090

# 启用健康检查
ENABLE_HEALTH_CHECK=true

# 健康检查端点路径
HEALTH_CHECK_PATH=/health
```

**说明**：
- `ENABLE_PROMETHEUS`：是否启用 Prometheus 监控
- `PROMETHEUS_PORT`：Prometheus 端口
- `ENABLE_HEALTH_CHECK`：是否启用健康检查
- `HEALTH_CHECK_PATH`：健康检查端点路径

---

## 对象存储配置

```bash
# S3 兼容存储配置
S3_ENDPOINT=https://s3.amazonaws.com
S3_ACCESS_KEY=your_access_key_here
S3_SECRET_KEY=your_secret_key_here
S3_BUCKET=ancient-script-bucket
S3_REGION=us-east-1

# 本地文件存储路径
LOCAL_STORAGE_PATH=/workspace/projects/assets/uploads

# 最大文件大小（MB）
MAX_FILE_SIZE=50
```

**说明**：
- `S3_ENDPOINT`：S3 兼容存储端点
- `S3_ACCESS_KEY`：访问密钥
- `S3_SECRET_KEY`：密钥
- `S3_BUCKET`：存储桶名称
- `S3_REGION`：存储区域
- `LOCAL_STORAGE_PATH`：本地文件存储路径
- `MAX_FILE_SIZE`：最大文件大小（MB）

---

## 邮件通知配置

```bash
# 启用邮件通知
ENABLE_EMAIL_NOTIFICATIONS=false

# SMTP 配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password
SMTP_FROM=your_email@gmail.com
SMTP_FROM_NAME=古文字破译系统
```

**说明**：
- 用于发送系统通知邮件
- 支持标准 SMTP 协议
- `SMTP_USE_TLS`：是否使用 TLS 加密

---

## 日志配置

```bash
# 日志文件路径
LOG_FILE_PATH=/workspace/projects/logs

# 日志文件最大大小（MB）
LOG_FILE_MAX_SIZE=100

# 日志文件保留数量
LOG_FILE_BACKUP_COUNT=10

# 启用日志轮转
ENABLE_LOG_ROTATION=true
```

**说明**：
- `LOG_FILE_PATH`：日志文件存储路径
- `LOG_FILE_MAX_SIZE`：单个日志文件最大大小（MB）
- `LOG_FILE_BACKUP_COUNT`：保留的日志文件数量
- `ENABLE_LOG_ROTATION`：是否启用日志轮转

---

## 开发配置

```bash
# 开发模式（启用调试和自动重载）
DEVELOPMENT_MODE=false

# 启用 API 文档
ENABLE_DOCS=true

# 启用 CORS 调试
CORS_DEBUG=false

# 启用详细错误信息
ENABLE_VERBOSE_ERRORS=false
```

**说明**：
- `DEVELOPMENT_MODE`：开发模式，启用调试和自动重载
- `ENABLE_DOCS`：启用 API 文档（Swagger UI）
- `CORS_DEBUG`：CORS 调试模式
- `ENABLE_VERBOSE_ERRORS`：显示详细错误信息

---

## 功能开关

```bash
# 启用用户认证
ENABLE_AUTH=false

# 启用会话管理
ENABLE_SESSION_MANAGEMENT=true

# 启用文件上传
ENABLE_FILE_UPLOAD=true

# 启用图像识别
ENABLE_IMAGE_RECOGNITION=true

# 启用对话功能
ENABLE_CHAT=true

# 启用文本分析
ENABLE_TEXT_ANALYSIS=true
```

**说明**：
- 用于控制功能模块的启用/禁用
- 根据需求调整

---

## 部署配置

```bash
# 部署环境（development, staging, production）
DEPLOYMENT_ENV=development

# 应用版本
APP_VERSION=2.1.0

# 应用名称
APP_NAME=Ancient Script Decipherment System
```

**说明**：
- `DEPLOYMENT_ENV`：部署环境
- `APP_VERSION`：应用版本
- `APP_NAME`：应用名称

---

## 数据备份配置

```bash
# 启用自动备份
ENABLE_AUTO_BACKUP=false

# 备份路径
BACKUP_PATH=/workspace/projects/backups

# 备份保留天数
BACKUP_RETENTION_DAYS=7

# 备份时间（Cron 表达式）
BACKUP_SCHEDULE=0 2 * * *
```

**说明**：
- `ENABLE_AUTO_BACKUP`：是否启用自动备份
- `BACKUP_PATH`：备份文件存储路径
- `BACKUP_RETENTION_DAYS`：备份保留天数
- `BACKUP_SCHEDULE`：备份时间（Cron 表达式）

---

## 联系信息

```bash
# 管理员邮箱
ADMIN_EMAIL=admin@example.com

# 技术支持邮箱
SUPPORT_EMAIL=support@example.com

# 项目主页
PROJECT_URL=https://github.com/your-username/ancient-script
```

**说明**：
- 用于系统通知和支持

---

## 许可证信息

```bash
# 许可证类型
LICENSE_TYPE=MIT

# 版权信息
COPYRIGHT=Copyright (c) 2025 Ancient Script Project. All rights reserved.
```

---

## 🚀 快速配置指南

### 最小配置（必需）

```bash
COZE_WORKSPACE_PATH=/workspace/projects
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-moonshot-api-key-here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1
```

### 标准配置（推荐）

```bash
# 必需配置
COZE_WORKSPACE_PATH=/workspace/projects
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-moonshot-api-key-here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1

# 服务配置
PORT=8000
LOG_LEVEL=INFO
MAX_MESSAGES=40
MODEL_TEMPERATURE=0.6

# 数据库配置
DATABASE_URL=postgresql://ancient_script:ancient_script_password@localhost:5432/ancient_script
DB_POOL_SIZE=20

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# 安全配置
JWT_SECRET=your_jwt_secret_key_here
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 生产环境配置

```bash
# 必需配置
COZE_WORKSPACE_PATH=/workspace/projects
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-moonshot-api-key-here
COZE_INTEGRATION_MODEL_BASE_URL=https://api.moonshot.cn/v1

# 服务配置
PORT=8000
LOG_LEVEL=INFO
MAX_MESSAGES=40
MODEL_TEMPERATURE=0.6
REQUEST_TIMEOUT=600

# 数据库配置（修改密码）
DATABASE_URL=postgresql://ancient_script:strong_password_here@localhost:5432/ancient_script
DB_POOL_SIZE=50
DB_MAX_OVERFLOW=20

# Redis 配置（设置密码）
REDIS_URL=redis://:strong_password@localhost:6379/0
REDIS_MAX_CONNECTIONS=100

# 安全配置（使用强密钥）
JWT_SECRET=<生成的强密钥>
API_KEY=<生成的API密钥>
CORS_ORIGINS=https://your-domain.com

# 限流配置
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_DAY=10000

# 部署配置
DEPLOYMENT_ENV=production
DEVELOPMENT_MODE=false
ENABLE_VERBOSE_ERRORS=false

# 备份配置
ENABLE_AUTO_BACKUP=true
BACKUP_RETENTION_DAYS=30
```

---

## 📝 配置检查清单

部署前请检查以下配置项：

- [ ] `COZE_WORKLOAD_IDENTITY_API_KEY` 已填写实际的 API Key
- [ ] `DATABASE_PASSWORD` 已修改为强密码（生产环境）
- [ ] `JWT_SECRET` 已设置为强随机字符串（生产环境）
- [ ] `REDIS_PASSWORD` 已设置（生产环境）
- [ ] `CORS_ORIGINS` 已配置正确的域名（生产环境）
- [ ] `LOG_LEVEL` 设置为 INFO 或 WARNING（生产环境）
- [ ] `DEVELOPMENT_MODE` 设置为 false（生产环境）
- [ ] `ENABLE_AUTO_BACKUP` 已启用（生产环境）

---

## 📚 相关文档

- [DATABASE_SETUP.md](DATABASE_SETUP.md) - 数据库配置指南
- [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) - 云服务器部署文档
- [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) - 部署快速开始指南

---

**文档版本**: v1.0  
**更新日期**: 2025-01-10
