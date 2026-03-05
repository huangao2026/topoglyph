# 🗄️ 数据库快速配置

## ⚡ 3步快速配置

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 修改数据库密码

```bash
nano .env
```

**修改以下内容**：

```bash
# PostgreSQL 密码（必须修改！）
DB_PASSWORD=your_strong_password_here

# 自动生成的连接URL也会相应更新
DATABASE_URL=postgresql://ancienttext:your_strong_password_here@db:5432/ancienttext
```

**密码要求**：
- ⚠️ 必须修改默认密码
- 🔐 至少16位
- 🎲 包含大小写字母、数字、特殊字符

**生成强密码**：
```bash
openssl rand -base64 32
```

### 3. 启动服务

```bash
docker-compose up -d
```

---

## ✅ 验证配置

### 检查服务状态

```bash
docker-compose ps
```

应该看到所有服务都是 `Up` 状态：
- ✅ ancient-text-ai-web
- ✅ ancient-text-ai-db (PostgreSQL)
- ✅ ancient-text-ai-redis (Redis)

### 测试数据库连接

```bash
# 测试 PostgreSQL
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT version();"

# 测试 Redis
docker-compose exec redis redis-cli ping
```

应该返回：
- PostgreSQL：版本信息
- Redis：`PONG`

### 查看数据库表

```bash
docker-compose exec db psql -U ancienttext -d ancienttext -c "\dt"
```

应该看到以下表：
- users
- sessions
- ancient_text_analyses
- symbols
- tool_usage_logs
- system_configs
- feedback

---

## 📋 环境变量参考

### PostgreSQL 环境变量

| 变量名 | 说明 | 默认值 | 是否必需 |
|--------|------|--------|----------|
| `DB_USER` | 数据库用户名 | `ancienttext` | 是 |
| `DB_PASSWORD` | 数据库密码 | `your_strong_password_here` | **是（必须修改）** |
| `DB_NAME` | 数据库名称 | `ancienttext` | 是 |
| `DB_HOST` | 数据库主机 | `db` | 是（Docker内） |
| `DB_PORT` | 数据库端口 | `5432` | 是 |
| `DB_POOL_SIZE` | 连接池大小 | `10` | 否 |
| `DB_MAX_OVERFLOW` | 最大溢出连接 | `20` | 否 |
| `DB_TIMEOUT` | 连接超时（秒） | `30` | 否 |
| `DB_POOL_RECYCLE` | 连接回收时间（秒） | `3600` | 否 |

### Redis 环境变量

| 变量名 | 说明 | 默认值 | 是否必需 |
|--------|------|--------|----------|
| `REDIS_HOST` | Redis主机 | `redis` | 是（Docker内） |
| `REDIS_PORT` | Redis端口 | `6379` | 是 |
| `REDIS_DB` | Redis数据库编号 | `0` | 否 |
| `REDIS_PASSWORD` | Redis密码 | 空 | 否 |
| `REDIS_MAX_CONNECTIONS` | 最大连接数 | `50` | 否 |
| `REDIS_TIMEOUT` | 连接超时（秒） | `5` | 否 |
| `REDIS_CACHE_TTL` | 缓存过期时间（秒） | `3600` | 否 |

---

## 🔧 常用操作

### 查看日志

```bash
# PostgreSQL 日志
docker-compose logs -f db

# Redis 日志
docker-compose logs -f redis
```

### 备份数据

```bash
# 备份 PostgreSQL
docker-compose exec db pg_dump -U ancienttext ancienttext > backup_$(date +%Y%m%d_%H%M%S).sql

# 备份 Redis AOF
docker-compose exec redis redis-cli BGSAVE
docker cp ancient-text-ai-redis:/data/appendonly.aof redis_backup_$(date +%Y%m%d_%H%M%S).aof
```

### 恢复数据

```bash
# 恢复 PostgreSQL
docker-compose exec -T db psql -U ancienttext ancienttext < backup_20250110_120000.sql
```

### 重置数据库

```bash
# ⚠️ 警告：这将删除所有数据！

# 停止服务并删除数据卷
docker-compose down -v

# 重新启动
docker-compose up -d
```

---

## 🆘 常见问题

### Q1: 提示密码认证失败？

**A**: 检查 `.env` 文件中的 `DB_PASSWORD` 是否正确：

```bash
cat .env | grep DB_PASSWORD
```

确保密码与 `docker-compose.yml` 中的 `POSTGRES_PASSWORD` 一致。

### Q2: 提示表不存在？

**A**: 数据库可能未正确初始化，重新启动：

```bash
docker-compose down -v
docker-compose up -d
# 等待30秒让数据库初始化
```

### Q3: 端口冲突？

**A**: 修改 `docker-compose.yml` 中的端口映射：

```yaml
services:
  db:
    ports:
      - "5433:5432"  # 改为5433
  redis:
    ports:
      - "6380:6379"  # 改为6380
```

### Q4: 数据丢失？

**A**: 确保使用正确的命令停止服务：

```bash
# ✅ 正确：保留数据卷
docker-compose down

# ❌ 错误：删除数据卷（会丢失数据）
docker-compose down -v
```

---

## 📚 详细文档

- [完整数据库配置指南](DATABASE_SETUP.md) - 详细的配置说明
- [云服务器部署文档](CLOUD_DEPLOYMENT.md) - 生产环境部署
- [部署快速开始](DEPLOYMENT_QUICKSTART.md) - 快速部署指南

---

## 🎯 配置检查清单

- [ ] 已复制 `.env.example` 为 `.env`
- [ ] 已修改 `DB_PASSWORD` 为强密码
- [ ] 已启动所有服务（`docker-compose ps` 显示全部 Up）
- [ ] 已测试 PostgreSQL 连接（`SELECT version();`）
- [ ] 已测试 Redis 连接（`PING` 返回 `PONG`）
- [ ] 已验证数据库表已创建（`\dt` 显示所有表）
- [ ] 已配置自动备份（可选但推荐）

---

**配置完成后，系统即可正常使用！** 🎉

---

**快速命令参考**：

```bash
# 启动
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试数据库
docker-compose exec db psql -U ancienttext -d ancienttext -c "\dt"

# 停止
docker-compose down
```
