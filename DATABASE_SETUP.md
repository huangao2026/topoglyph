# 数据库配置指南

古文字破译系统 - 完整的数据库配置和使用指南

---

## 📋 目录

1. [数据库架构](#数据库架构)
2. [环境变量配置](#环境变量配置)
3. [数据库初始化](#数据库初始化)
4. [数据库模型](#数据库模型)
5. [常用操作](#常用操作)
6. [备份与恢复](#备份与恢复)
7. [性能优化](#性能优化)
8. [故障排查](#故障排查)

---

## 数据库架构

### 数据库类型

本系统使用 **PostgreSQL 15** 作为主数据库，**Redis 7** 作为缓存。

### 服务架构

```
┌─────────────────┐
│   主应用服务    │
│  (FastAPI)      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼─────┐
│PostgreSQL│  Redis │
│  数据库  │  缓存  │
└────────┘ └────────┘
```

### 数据库信息

| 属性 | 值 |
|------|-----|
| **类型** | PostgreSQL 15 |
| **端口** | 5432 |
| **数据库名** | ancient_script |
| **用户名** | ancient_script |
| **密码** | ancient_script_password（默认，请修改） |

---

## 环境变量配置

### .env 文件配置

在项目根目录的 `.env` 文件中配置以下环境变量：

```bash
# ========================================
# 数据库配置（PostgreSQL）
# ========================================

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

# ========================================
# Redis 缓存配置
# ========================================

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

### 环境变量说明

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | - | 是 |
| `DB_HOST` | 数据库主机 | localhost | 否 |
| `DB_PORT` | 数据库端口 | 5432 | 否 |
| `DB_NAME` | 数据库名称 | ancient_script | 否 |
| `DB_USER` | 数据库用户名 | ancient_script | 否 |
| `DB_PASSWORD` | 数据库密码 | ancient_script_password | 否 |
| `DB_POOL_SIZE` | 连接池大小 | 20 | 否 |
| `DB_MAX_OVERFLOW` | 连接池溢出大小 | 10 | 否 |
| `REDIS_URL` | Redis 连接字符串 | - | 否 |
| `REDIS_HOST` | Redis 主机 | localhost | 否 |
| `REDIS_PORT` | Redis 端口 | 6379 | 否 |
| `REDIS_DB` | Redis 数据库编号 | 0 | 否 |

---

## 数据库初始化

### 方法1：使用快速启动脚本（推荐）

```bash
# 一键启动并初始化数据库
./start.sh start
```

### 方法2：使用 Docker Compose

```bash
# 启动数据库服务
docker-compose up -d db redis

# 等待数据库就绪
sleep 5

# 初始化数据库（创建表和默认数据）
docker-compose exec app python scripts/init_db.py
```

### 方法3：手动初始化

```bash
# 进入应用容器
docker-compose exec app bash

# 运行初始化脚本
python scripts/init_db.py

# 退出容器
exit
```

### 初始化脚本选项

运行 `python scripts/init_db.py` 后，会显示以下选项：

```
请选择操作：
1. 创建所有表
2. 删除所有表（危险！）
3. 初始化默认数据
4. 显示统计信息
5. 完整初始化（创建表 + 初始化数据）
0. 退出
```

**推荐操作**：选择 `5` 进行完整初始化

---

## 数据库模型

### 表结构概览

| 表名 | 说明 | 主要用途 |
|------|------|----------|
| `users` | 用户表 | 存储用户信息 |
| `sessions` | 会话表 | 存储对话会话 |
| `messages` | 消息表 | 存储对话消息 |
| `conversations` | 对话记录表 | 存储分析结果 |
| `analysis_history` | 分析历史表 | 存储历史分析记录 |
| `plugins` | 插件表 | 存储插件信息 |
| `tools` | 工具表 | 存储工具信息 |
| `system_logs` | 系统日志表 | 存储系统日志 |
| `system_metrics` | 系统指标表 | 存储系统指标 |

### 详细表结构

#### 1. users（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String(50) | 用户名（唯一） |
| email | String(100) | 邮箱（唯一） |
| hashed_password | String(255) | 密码哈希（可选） |
| full_name | String(100) | 全名 |
| is_active | Boolean | 是否激活 |
| is_superuser | Boolean | 是否超级用户 |
| api_key | String(100) | API 密钥 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| last_login | DateTime | 最后登录时间 |

#### 2. sessions（会话表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| session_id | String(100) | 会话ID（唯一） |
| user_id | Integer | 用户ID（外键，可选） |
| title | String(200) | 会话标题 |
| metadata | JSON | 元数据 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| is_active | Boolean | 是否激活 |

#### 3. messages（消息表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| session_id | String(100) | 会话ID（外键） |
| role | String(20) | 角色（user/assistant） |
| content | Text | 消息内容 |
| metadata | JSON | 元数据 |
| tokens | Integer | Token 数量 |
| model | String(50) | 使用的模型 |
| created_at | DateTime | 创建时间 |

#### 4. conversations（对话记录表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户ID（外键，可选） |
| session_id | String(100) | 会话ID（外键） |
| message_id | Integer | 消息ID（外键） |
| script_type | String(100) | 文字类型 |
| analysis_result | Text | 分析结果 |
| confidence_score | Float | 置信度评分 |
| image_url | String(500) | 图片 URL |
| tools_used | JSON | 使用的工具 |
| metadata | JSON | 元数据 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 5. analysis_history（分析历史表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户ID（外键，可选） |
| session_id | String(100) | 会话ID |
| input_type | String(20) | 输入类型（text/image） |
| input_content | Text | 输入内容 |
| image_url | String(500) | 图片 URL |
| output_content | Text | 输出内容 |
| script_type | String(100) | 文字类型 |
| confidence_score | Float | 置信度 |
| tools_used | JSON | 使用的工具 |
| model_used | String(50) | 使用的模型 |
| tokens_used | Integer | Token 使用量 |
| processing_time | Float | 处理时间（秒） |
| created_at | DateTime | 创建时间 |

#### 6. plugins（插件表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String(100) | 插件名称（唯一） |
| version | String(20) | 版本号 |
| description | Text | 描述 |
| author | String(100) | 作者 |
| config | JSON | 配置 |
| enabled | Boolean | 是否启用 |
| usage_count | Integer | 使用次数 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 7. tools（工具表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String(100) | 工具名称（唯一） |
| display_name | String(100) | 显示名称 |
| description | Text | 描述 |
| category | String(50) | 类别 |
| config | JSON | 配置 |
| enabled | Boolean | 是否启用 |
| api_endpoint | String(500) | API 端点 |
| api_key_required | Boolean | 是否需要 API Key |
| usage_count | Integer | 使用次数 |
| success_rate | Float | 成功率 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 8. system_logs（系统日志表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| level | String(20) | 日志级别 |
| message | Text | 消息 |
| module | String(100) | 模块 |
| function | String(100) | 函数 |
| user_id | Integer | 用户ID（外键，可选） |
| session_id | String(100) | 会话ID |
| metadata | JSON | 元数据 |
| created_at | DateTime | 创建时间 |

#### 9. system_metrics（系统指标表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| metric_name | String(100) | 指标名称 |
| metric_value | Float | 指标值 |
| metric_unit | String(20) | 指标单位 |
| metadata | JSON | 元数据 |
| created_at | DateTime | 创建时间 |

---

## 常用操作

### 连接到数据库

```bash
# 使用 docker-compose
docker-compose exec db psql -U ancient_script -d ancient_script

# 使用 psql
psql -h localhost -U ancient_script -d ancient_script
```

### 查看所有表

```sql
\dt
```

### 查看表结构

```sql
\d 表名
```

### 查看数据

```sql
-- 查看用户
SELECT * FROM users LIMIT 10;

-- 查看会话
SELECT * FROM sessions ORDER BY created_at DESC LIMIT 10;

-- 查看消息
SELECT * FROM messages ORDER BY created_at DESC LIMIT 10;

-- 查看分析历史
SELECT * FROM analysis_history ORDER BY created_at DESC LIMIT 10;
```

### 统计查询

```sql
-- 统计用户数
SELECT COUNT(*) FROM users;

-- 统计会话数
SELECT COUNT(*) FROM sessions;

-- 统计消息数
SELECT COUNT(*) FROM messages;

-- 按文字类型统计
SELECT script_type, COUNT(*) as count 
FROM analysis_history 
GROUP BY script_type 
ORDER BY count DESC;

-- 查看活跃用户
SELECT * FROM v_user_stats 
WHERE last_activity > NOW() - INTERVAL '7 days';

-- 查看今日统计
SELECT * FROM generate_daily_stats();
```

### 清理数据

```sql
-- 清理90天前的系统日志
SELECT cleanup_expired_data();

-- 手动删除过期数据
DELETE FROM system_logs WHERE created_at < NOW() - INTERVAL '90 days';

-- 删除未激活的会话
DELETE FROM sessions WHERE is_active = false AND updated_at < NOW() - INTERVAL '30 days';
```

---

## 备份与恢复

### 备份数据库

#### 方法1：使用 pg_dump

```bash
# 备份到文件
docker-compose exec db pg_dump -U ancient_script ancient_script > backup_$(date +%Y%m%d_%H%M%S).sql

# 备份到压缩文件
docker-compose exec db pg_dump -U ancient_script ancient_script | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### 方法2：使用 Docker Compose backup 服务

```bash
# 启动备份服务
docker-compose --profile with-backup up -d backup

# 查看备份
ls -lh backups/
```

### 恢复数据库

```bash
# 从备份文件恢复
docker-compose exec -T db psql -U ancient_script ancient_script < backup_20250110_120000.sql

# 从压缩备份恢复
gunzip -c backup_20250110_120000.sql.gz | docker-compose exec -T db psql -U ancient_script ancient_script
```

### 自动备份配置

在 `docker-compose.yml` 中配置自动备份：

```yaml
backup:
  image: prodrigestivill/postgres-backup-local:15
  environment:
    - SCHEDULE=@daily  # 每天备份一次
    - BACKUP_KEEP_DAYS=7  # 保留7天
```

---

## 性能优化

### 索引优化

数据库模型中已经定义了必要的索引。如需添加自定义索引：

```sql
-- 创建索引
CREATE INDEX idx_messages_session_created ON messages(session_id, created_at);

-- 删除索引
DROP INDEX idx_messages_session_created;
```

### 查询优化

```sql
-- 使用 EXPLAIN 分析查询计划
EXPLAIN ANALYZE SELECT * FROM messages WHERE session_id = 'xxx';

-- 使用 LIMIT 限制返回结果
SELECT * FROM messages WHERE session_id = 'xxx' ORDER BY created_at DESC LIMIT 10;

-- 使用 JOIN 优化多表查询
SELECT m.*, s.title 
FROM messages m 
JOIN sessions s ON m.session_id = s.session_id 
WHERE m.session_id = 'xxx';
```

### 连接池优化

在 `.env` 文件中调整连接池配置：

```bash
DB_POOL_SIZE=20          # 增加连接池大小
DB_MAX_OVERFLOW=10       # 增加溢出连接数
DB_POOL_TIMEOUT=30       # 增加超时时间
DB_POOL_RECYCLE=3600     # 减少回收时间
```

### 缓存优化

使用 Redis 缓存常用查询：

```python
# 缓存用户信息
def get_user(user_id):
    cache_key = f"user:{user_id}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    user = db.query(User).filter(User.id == user_id).first()
    redis.setex(cache_key, 3600, json.dumps(user.to_dict()))
    return user
```

---

## 故障排查

### 问题1：无法连接到数据库

**症状**：应用无法连接到数据库

**解决方案**：

```bash
# 检查数据库服务状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 检查端口占用
netstat -tunlp | grep 5432

# 检查网络连接
docker-compose exec app ping db
```

### 问题2：数据库连接池耗尽

**症状**：大量连接超时

**解决方案**：

```bash
# 查看当前连接数
docker-compose exec db psql -U ancient_script -d ancient_script -c "SELECT COUNT(*) FROM pg_stat_activity;"

# 增加连接池大小
# 编辑 .env 文件
DB_POOL_SIZE=30
DB_MAX_OVERFLOW=20

# 重启应用
docker-compose restart app
```

### 问题3：查询速度慢

**症状**：查询响应时间长

**解决方案**：

```sql
-- 查看慢查询
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- 分析查询计划
EXPLAIN ANALYZE SELECT * FROM messages WHERE session_id = 'xxx';

-- 添加缺失的索引
CREATE INDEX idx_messages_session_created ON messages(session_id, created_at);
```

### 问题4：Redis 连接失败

**症状**：缓存功能不可用

**解决方案**：

```bash
# 检查 Redis 服务状态
docker-compose ps redis

# 查看 Redis 日志
docker-compose logs redis

# 测试 Redis 连接
docker-compose exec app redis-cli -h redis ping
```

---

## 📚 相关文档

- [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) - 云服务器部署文档
- [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) - 部署快速开始指南
- [EGYPTIAN_HIEROGLYPHS_ENHANCEMENT.md](EGYPTIAN_HIEROGLYPHS_ENHANCEMENT.md) - 埃及古文字能力增强报告

---

**文档版本**: v1.0  
**更新日期**: 2025-01-10
