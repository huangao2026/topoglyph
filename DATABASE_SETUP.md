# 🗄️ 数据库配置指南

古文字破译系统 - 数据库环境变量配置说明

---

## 📋 目录

1. [数据库概述](#数据库概述)
2. [环境变量配置](#环境变量配置)
3. [数据库初始化](#数据库初始化)
4. [连接测试](#连接测试)
5. [数据备份](#数据备份)
6. [常见问题](#常见问题)

---

## 数据库概述

系统使用以下数据库服务：

| 数据库 | 用途 | 版本 | 端口 |
|--------|------|------|------|
| **PostgreSQL** | 主数据库，存储用户数据、分析记录、符号库等 | 16-alpine | 5432 |
| **Redis** | 缓存层，加速查询、会话管理 | 7-alpine | 6379 |

---

## 环境变量配置

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 编辑 .env 文件

```bash
nano .env
```

### 3. 配置数据库环境变量

#### PostgreSQL 配置

```bash
# ========================================
# 数据库配置（PostgreSQL）
# ========================================

# PostgreSQL 数据库用户名
DB_USER=ancienttext

# PostgreSQL 数据库密码（请修改为强密码！）
DB_PASSWORD=your_strong_password_here

# PostgreSQL 数据库名称
DB_NAME=ancienttext

# PostgreSQL 数据库主机（Docker内部网络使用服务名）
DB_HOST=db

# PostgreSQL 数据库端口
DB_PORT=5432

# PostgreSQL 数据库连接URL（自动生成）
DATABASE_URL=postgresql://ancienttext:your_strong_password_here@db:5432/ancienttext

# 数据库连接池大小
DB_POOL_SIZE=10

# 数据池最大溢出连接数
DB_MAX_OVERFLOW=20

# 数据库连接超时时间（秒）
DB_TIMEOUT=30

# 数据库连接回收时间（秒）
DB_POOL_RECYCLE=3600
```

#### Redis 配置

```bash
# ========================================
# Redis 缓存配置
# ========================================

# Redis 主机（Docker内部网络使用服务名）
REDIS_HOST=redis

# Redis 端口
REDIS_PORT=6379

# Redis 数据库编号
REDIS_DB=0

# Redis 密码（如需密码认证）
REDIS_PASSWORD=

# Redis 连接URL（自动生成）
REDIS_URL=redis://redis:6379/0

# Redis 最大连接数
REDIS_MAX_CONNECTIONS=50

# Redis 连接超时时间（秒）
REDIS_TIMEOUT=5

# Redis 缓存过期时间（秒，默认1小时）
REDIS_CACHE_TTL=3600
```

### 4. 必需的环境变量

| 变量名 | 说明 | 默认值 | 是否必需 |
|--------|------|--------|----------|
| **DB_USER** | PostgreSQL用户名 | ancienttext | 是 |
| **DB_PASSWORD** | PostgreSQL密码 | - | **是（必须修改）** |
| **DB_NAME** | PostgreSQL数据库名 | ancienttext | 是 |
| **DB_HOST** | PostgreSQL主机 | db | 是（Docker内） |
| **DB_PORT** | PostgreSQL端口 | 5432 | 是 |
| **REDIS_HOST** | Redis主机 | redis | 是（Docker内） |
| **REDIS_PORT** | Redis端口 | 6379 | 是 |
| **REDIS_PASSWORD** | Redis密码 | - | 否 |

### 5. 密码安全建议

⚠️ **重要提示**：

1. **修改默认密码**：不要使用 `your_strong_password_here`
2. **使用强密码**：至少16位，包含大小写字母、数字、特殊字符
3. **定期更换**：建议每3-6个月更换一次
4. **不要提交到版本控制**：确保 `.env` 文件不被 Git 跟踪

**生成强密码示例**：

```bash
# 方法1：使用 openssl
openssl rand -base64 32

# 方法2：使用 /dev/urandom
cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%^&*' | fold -w 32 | head -n 1

# 方法3：使用密码管理器（推荐）
# 使用 LastPass、1Password、Bitwarden 等生成
```

---

## 数据库初始化

### 自动初始化

数据库初始化脚本位于 `scripts/init-db.sql`，会在以下情况自动执行：

1. 首次启动 PostgreSQL 容器
2. `postgres_data` 卷为空时

### 初始化脚本包含的内容

#### 数据表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| `users` | 用户表 | id, username, email, password_hash |
| `sessions` | 会话表 | id, user_id, session_id, expires_at |
| `ancient_text_analyses` | 古文字分析记录表 | id, text_type, analysis_result, translation |
| `symbols` | 符号库表 | id, script_type, symbol_code, meaning |
| `tool_usage_logs` | 工具使用记录表 | id, tool_name, input_data, output_data |
| `system_configs` | 系统配置表 | config_key, config_value |
| `feedback` | 反馈表 | id, user_id, rating, comment |

#### 视图

| 视图名 | 说明 |
|--------|------|
| `user_analysis_stats` | 用户分析统计视图 |
| `tool_usage_stats` | 工具使用统计视图 |

#### 函数

| 函数名 | 说明 |
|--------|------|
| `cleanup_expired_sessions()` | 清理过期会话 |
| `get_user_recent_analyses()` | 获取用户最近分析 |

#### 示例数据

- 埃及象形文字示例符号（A19、G5、N5）
- 甲骨文示例符号（日、月、人）
- 默认系统配置

---

## 连接测试

### 1. 启动服务

```bash
docker-compose up -d
```

### 2. 检查数据库状态

```bash
# 检查 PostgreSQL 容器
docker-compose ps db

# 检查 Redis 容器
docker-compose ps redis
```

### 3. 测试 PostgreSQL 连接

```bash
# 方法1：使用 docker exec
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT version();"

# 方法2：使用 docker exec（完整SQL）
docker-compose exec db psql -U ancienttext -d ancienttext <<EOF
-- 查看所有表
\dt

-- 查看示例数据
SELECT * FROM symbols LIMIT 5;
EOF
```

### 4. 测试 Redis 连接

```bash
# 测试 Redis
docker-compose exec redis redis-cli ping

# 应该返回：PONG

# 查看所有键
docker-compose exec redis redis-cli KEYS "*"
```

### 5. 查看日志

```bash
# 查看 PostgreSQL 日志
docker-compose logs -f db

# 查看 Redis 日志
docker-compose logs -f redis
```

---

## 数据备份

### 1. PostgreSQL 备份

```bash
# 备份数据库
docker-compose exec db pg_dump -U ancienttext ancienttext > backup_$(date +%Y%m%d_%H%M%S).sql

# 备份到指定目录
mkdir -p backups
docker-compose exec db pg_dump -U ancienttext ancienttext > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# 仅备份数据（不包含结构）
docker-compose exec db pg_dump -U ancienttext --data-only ancienttext > backup_data_$(date +%Y%m%d_%H%M%S).sql
```

### 2. PostgreSQL 恢复

```bash
# 恢复数据库
docker-compose exec -T db psql -U ancienttext ancienttext < backup_20250110_120000.sql
```

### 3. Redis 备份

```bash
# Redis 使用 AOF 持久化，数据自动保存在卷中
# 手动触发备份
docker-compose exec redis redis-cli BGSAVE

# 复制 AOF 文件
docker cp ancient-text-ai-redis:/data/appendonly.aof backups/redis_backup_$(date +%Y%m%d_%H%M%S).aof
```

### 4. 自动备份脚本

创建自动备份脚本 `scripts/backup.sh`：

```bash
#!/bin/bash

# 古文字破译系统 - 数据库备份脚本

BACKUP_DIR="/opt/backups/ancient-script"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份 PostgreSQL
echo "[$(date)] 备份 PostgreSQL..."
docker-compose exec -T db pg_dump -U ancienttext ancienttext > "$BACKUP_DIR/postgres_$DATE.sql"

# 备份 Redis AOF
echo "[$(date)] 备份 Redis..."
docker cp ancient-text-ai-redis:/data/appendonly.aof "$BACKUP_DIR/redis_$DATE.aof"

# 清理旧备份
echo "[$(date)] 清理旧备份..."
find "$BACKUP_DIR" -name "postgres_*.sql" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "redis_*.aof" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] 备份完成！"
```

添加执行权限：

```bash
chmod +x scripts/backup.sh
```

配置定时任务：

```bash
crontab -e

# 添加以下内容（每天凌晨2点备份）
0 2 * * * /path/to/ancient-script/scripts/backup.sh
```

---

## 常见问题

### 问题1：数据库连接失败

**症状**：启动服务时提示无法连接数据库

**解决方案**：

```bash
# 1. 检查数据库容器是否运行
docker-compose ps db

# 2. 检查数据库日志
docker-compose logs db

# 3. 测试数据库连接
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT 1;"

# 4. 检查环境变量
cat .env | grep DB_

# 5. 重新创建数据库容器
docker-compose down -v
docker-compose up -d
```

### 问题2：密码错误

**症状**：提示密码认证失败

**解决方案**：

```bash
# 1. 检查 .env 文件中的 DB_PASSWORD
cat .env | grep DB_PASSWORD

# 2. 确保密码与 docker-compose.yml 中的 POSTGRES_PASSWORD 一致
grep POSTGRES_PASSWORD docker-compose.yml

# 3. 如果不一致，修改 .env 文件
nano .env

# 4. 重启服务
docker-compose down
docker-compose up -d
```

### 问题3：表不存在

**症状**：提示表不存在（如 `relation "users" does not exist`）

**解决方案**：

```bash
# 1. 检查初始化脚本是否存在
ls -la scripts/init-db.sql

# 2. 删除数据库卷并重新初始化
docker-compose down -v
docker-compose up -d

# 3. 等待数据库初始化（约30秒）
sleep 30

# 4. 验证表已创建
docker-compose exec db psql -U ancienttext -d ancienttext -c "\dt"
```

### 问题4：端口冲突

**症状**：提示端口已被占用

**解决方案**：

```bash
# 1. 查看端口占用
netstat -tunlp | grep 5432
netstat -tunlp | grep 6379

# 2. 修改 docker-compose.yml 中的端口映射
# 例如将 5432:5432 改为 5433:5432

# 3. 重启服务
docker-compose down
docker-compose up -d
```

### 问题5：数据丢失

**症状**：重启后数据不见了

**解决方案**：

```bash
# 1. 检查 Docker 卷是否正确挂载
docker volume ls

# 2. 检查卷的挂载点
docker volume inspect ancient-script_postgres_data
docker volume inspect ancient-script_redis_data

# 3. 检查 docker-compose.yml 中的 volumes 配置
grep -A 5 "postgres_data:" docker-compose.yml
grep -A 5 "redis_data:" docker-compose.yml

# 4. 确保使用 -v 参数时不要删除卷
# 正确的命令：docker-compose down
# 错误的命令：docker-compose down -v（会删除卷）
```

---

## 数据库优化

### 1. PostgreSQL 优化

编辑 `docker-compose.yml`，添加 PostgreSQL 配置：

```yaml
db:
  image: postgres:16-alpine
  command:
    - "postgres"
    - "-c"
    - "shared_buffers=256MB"
    - "-c"
    - "max_connections=200"
    - "-c"
    - "work_mem=4MB"
```

### 2. Redis 优化

编辑 `docker-compose.yml`，添加 Redis 配置：

```yaml
redis:
  image: redis:7-alpine
  command: >
    redis-server
    --appendonly yes
    --maxmemory 256mb
    --maxmemory-policy allkeys-lru
```

### 3. 连接池优化

编辑 `.env` 文件：

```bash
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_TIMEOUT=60
```

---

## 监控和维护

### 1. 数据库性能监控

```bash
# 查看数据库连接数
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT count(*) FROM pg_stat_activity;"

# 查看数据库大小
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT pg_size_pretty(pg_database_size('ancienttext'));"

# 查看表大小
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;"
```

### 2. Redis 性能监控

```bash
# 查看 Redis 信息
docker-compose exec redis redis-cli INFO

# 查看内存使用
docker-compose exec redis redis-cli INFO memory

# 查看键的过期时间
docker-compose exec redis redis-cli TTL "key_name"
```

### 3. 定期维护

```bash
# PostgreSQL VACUUM（清理死元组）
docker-compose exec db psql -U ancienttext -d ancienttext -c "VACUUM ANALYZE;"

# Redis 内存碎片整理
docker-compose exec redis redis-cli MEMORY PURGE
```

---

## 总结

### 配置清单

- [ ] 复制 `.env.example` 为 `.env`
- [ ] 修改 `DB_PASSWORD` 为强密码
- [ ] 检查其他数据库环境变量
- [ ] 启动服务并测试连接
- [ ] 配置自动备份
- [ ] 配置监控

### 快速命令

```bash
# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f db
docker-compose logs -f redis

# 测试连接
docker-compose exec db psql -U ancienttext -d ancienttext -c "SELECT version();"
docker-compose exec redis redis-cli ping

# 备份数据
docker-compose exec db pg_dump -U ancienttext ancienttext > backup.sql

# 停止服务
docker-compose down

# 完全清理（包括数据）
docker-compose down -v  # ⚠️ 会删除所有数据！
```

---

**文档版本**: v1.0
**更新日期**: 2025-01-10
