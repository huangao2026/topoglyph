# 🔐 API Token 替换指南

古文字破译系统 - 敏感信息配置指南

---

## ⚠️ 重要提示

**在替换 Token 之前，请注意**：

1. ⚠️ **不要在公开场合分享 Token**
2. ⚠️ **不要将 Token 提交到 Git 仓库**
3. ⚠️ **使用强密码和随机密钥**
4. ⚠️ **定期更换 Token**（建议每3-6个月）
5. ⚠️ **泄露后立即更换**

---

## 📋 需要替换的 Token 列表

### 🔴 必须替换（3个）

| Token名称 | 变量名 | 位置 | 难度 | 获取方式 |
|-----------|--------|------|------|----------|
| **Moonshot AI API Key** | `COZE_WORKLOAD_IDENTITY_API_KEY` | `.env` 文件 | ⭐ | 官方控制台 |
| **数据库密码** | `DB_PASSWORD` | `.env` 文件 | ⭐ | 自己生成 |
| **应用密钥** | `SECRET_KEY` | `.env` 文件 | ⭐ | 自己生成 |

### 🟡 建议替换（2个）

| Token名称 | 变量名 | 位置 | 难度 | 获取方式 |
|-----------|--------|------|------|----------|
| **Redis 密码** | `REDIS_PASSWORD` | `.env` 文件 | ⭐ | 自己生成 |
| **JWT 密钥** | `JWT_SECRET` | `.env` 文件 | ⭐ | 自己生成 |

### 🟢 可选替换（3个）

| Token名称 | 变量名 | 位置 | 难度 | 获取方式 |
|-----------|--------|------|------|----------|
| **API Key** | `API_KEY` | `.env` 文件 | ⭐ | 自己生成 |
| **S3 Access Key** | `S3_ACCESS_KEY` | `.env` 文件 | ⭐⭐⭐ | 云服务商 |
| **S3 Secret Key** | `S3_SECRET_KEY` | `.env` 文件 | ⭐⭐⭐ | 云服务商 |

---

## 🚀 快速替换（推荐方式）

### 方法1：使用交互式脚本（自动）

我将为您创建一个自动配置脚本！

```bash
# 1. 创建配置脚本
nano setup-config.sh

# 2. 复制下面的脚本内容（见下方）

# 3. 运行脚本
chmod +x setup-config.sh
./setup-config.sh
```

### 方法2：手动替换（适合精确控制）

见下方详细步骤。

---

## 📝 详细替换步骤

### 1️⃣ 替换 Moonshot AI API Key

#### 获取 API Key

1. 访问 [Moonshot AI 控制台](https://platform.moonshot.cn/console/api-keys)
2. 登录或注册账号
3. 点击"创建 API Key"
4. 复制生成的 API Key（格式：`sk-xxxxx...`）

#### 替换步骤

```bash
# 1. 编辑 .env 文件
nano .env

# 2. 找到这一行
COZE_WORKLOAD_IDENTITY_API_KEY=your_moonshot_api_key_here

# 3. 替换为您的 API Key
COZE_WORKLOAD_IDENTITY_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 4. 保存并退出（Ctrl+X, Y, Enter）
```

**格式示例**：
```bash
COZE_WORKLOAD_IDENTITY_API_KEY=sk-abc123def456ghi789jkl012mno345pq
```

---

### 2️⃣ 替换数据库密码（DB_PASSWORD）

#### 生成强密码

**方法A：使用 openssl（推荐）**
```bash
openssl rand -base64 32
```

**方法B：使用 /dev/urandom**
```bash
cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%^&*' | fold -w 32 | head -n 1
```

**方法C：在线生成器**
- [Password Generator](https://passwordsgenerator.net/)
- 选择：32位，包含大小写字母、数字、特殊字符

#### 替换步骤

```bash
# 1. 生成密码（例如：Xk9$mN2#pQ8!rW5&zA3*vS6@bY1)cE0
# 假设生成的密码是：MyStr0ngP@ssw0rd!2024#Secure

# 2. 编辑 .env 文件
nano .env

# 3. 替换以下两处
DB_PASSWORD=MyStr0ngP@ssw0rd!2024#Secure

DATABASE_URL=postgresql://ancienttext:MyStr0ngP@ssw0rd!2024#Secure@db:5432/ancienttext

# 4. 保存并退出
```

**⚠️ 重要**：确保 `DB_PASSWORD` 和 `DATABASE_URL` 中的密码一致！

---

### 3️⃣ 替换应用密钥（SECRET_KEY）

#### 生成密钥

**方法A：使用 Python**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**方法B：使用 openssl**
```bash
openssl rand -hex 32
```

**方法C：使用 /dev/urandom**
```bash
head -c 32 /dev/urandom | xxd -p -c 32
```

#### 替换步骤

```bash
# 1. 生成密钥（例如：a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6）

# 2. 编辑 .env 文件
nano .env

# 3. 找到 SECRET_KEY（如果没有则添加）
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# 4. 保存并退出
```

---

### 4️⃣ 替换 Redis 密码（REDIS_PASSWORD）- 可选

#### 生成密码

```bash
# 生成强密码（方法同数据库密码）
openssl rand -base64 16
```

#### 替换步骤

```bash
# 1. 编辑 .env 文件
nano .env

# 2. 替换 Redis 密码
REDIS_PASSWORD=MyRedisP@ss2024

# 3. 替换 Redis URL
REDIS_URL=redis://:MyRedisP@ss2024@redis:6379/0

# 4. 保存并退出
```

**⚠️ 注意**：Redis URL 格式为 `redis://:密码@主机:端口/数据库`

---

### 5️⃣ 替换 JWT 密钥（JWT_SECRET）- 可选

#### 生成密钥

```bash
# 生成强密钥（方法同 SECRET_KEY）
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 替换步骤

```bash
# 1. 编辑 .env 文件
nano .env

# 2. 取消注释并替换 JWT_SECRET
JWT_SECRET=your_jwt_secret_key_here

# 3. 保存并退出
```

---

### 6️⃣ 替换 API Key（API_KEY）- 可选

#### 生成密钥

```bash
# 生成 API Key（建议格式：ancient-text-随机字符串）
python3 -c "import secrets; print('ancient-text-' + secrets.token_urlsafe(16))"
```

#### 替换步骤

```bash
# 1. 编辑 .env 文件
nano .env

# 2. 取消注释并替换 API_KEY
API_KEY=ancient-text-abc123def456

# 3. 保存并退出
```

---

### 7️⃣ 配置 S3 存储（可选）- 高级

如果您需要使用对象存储：

#### 获取凭证

1. 登录云服务商（AWS、阿里云、腾讯云）
2. 创建存储桶（Bucket）
3. 获取 Access Key 和 Secret Key

#### 替换步骤

```bash
# 1. 编辑 .env 文件
nano .env

# 2. 取消注释并配置 S3
S3_ENDPOINT=https://s3.amazonaws.com
S3_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
S3_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET=ancient-script-bucket
S3_REGION=us-east-1

# 3. 保存并退出
```

---

## ✅ 验证配置

### 方法1：检查环境变量

```bash
# 查看 .env 文件内容
cat .env | grep -E "COZE_WORKLOAD_IDENTITY_API_KEY|DB_PASSWORD|SECRET_KEY"

# 检查是否都已替换（不应该是默认值）
```

### 方法2：启动服务测试

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f web

# 应该看到服务正常启动，没有配置错误
```

### 方法3：测试 API

```bash
# 测试健康检查
curl http://localhost:8000/health

# 应该返回：{"status": "healthy"}
```

---

## 🛡️ 安全最佳实践

### 1. 文件权限

```bash
# 设置 .env 文件仅当前用户可读写
chmod 600 .env

# 验证权限
ls -la .env
# 应该显示：-rw------- 1 user user ...
```

### 2. Git 忽略

```bash
# 确保项目根目录有 .gitignore 文件
cat .gitignore

# 应该包含：
.env
.env.local
.env.*.local
```

### 3. 密码管理器

建议使用密码管理器存储所有 Token：
- **LastPass**
- **1Password**
- **Bitwarden**
- **KeePass**

### 4. 定期轮换

建议设置提醒：
- 🔑 API Key：每6个月更换
- 🔐 数据库密码：每3个月更换
- 🔑 应用密钥：每6个月更换

### 5. 泄露应急响应

如果 Token 泄露，立即：

1. **撤销旧 Token**：
   - Moonshot AI：登录控制台删除旧 Key
   - 数据库：修改密码

2. **生成新 Token**：按上述步骤生成

3. **替换配置**：更新 `.env` 文件

4. **重启服务**：`docker-compose restart`

5. **审计日志**：检查是否有异常访问

---

## 🚨 常见错误

### 错误1：API Key 格式不正确

**症状**：`Invalid API Key` 错误

**原因**：API Key 格式错误或复制不完整

**解决**：
- 确保格式：`sk-xxxxx...`
- 完整复制，不要有空格
- 检查是否有多余字符

### 错误2：数据库连接失败

**症状**：`password authentication failed`

**原因**：
- `DB_PASSWORD` 和 `DATABASE_URL` 中的密码不一致
- 密码包含特殊字符未转义

**解决**：
```bash
# 确保 DB_PASSWORD 和 DATABASE_URL 一致
DB_PASSWORD=MyPass@123
DATABASE_URL=postgresql://ancienttext:MyPass@123@db:5432/ancienttext

# 如果密码包含特殊字符，使用引号
DB_PASSWORD='MyPass@123#'
DATABASE_URL='postgresql://ancienttext:MyPass@123#@db:5432/ancienttext'
```

### 错误3：JWT 认证失败

**症状**：`Invalid token` 错误

**原因**：JWT_SECRET 配置错误

**解决**：
- 确保 JWT_SECRET 长度至少32位
- 使用强随机密钥
- 不要使用默认值

### 错误4：Redis 连接失败

**症状**：`NOAUTH Authentication required`

**原因**：Redis 密码配置错误

**解决**：
```bash
# 检查 .env 中的配置
REDIS_PASSWORD=MyRedisPass
REDIS_URL=redis://:MyRedisPass@redis:6379/0

# 注意 URL 格式：redis://:密码@主机:端口/数据库
```

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志**：
   ```bash
   docker-compose logs -f
   ```

2. **检查配置**：
   ```bash
   cat .env
   ```

3. **参考文档**：
   - [DATABASE_SETUP.md](DATABASE_SETUP.md)
   - [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)

---

## 🎯 配置检查清单

完成替换后，检查以下项目：

- [x] `COZE_WORKLOAD_IDENTITY_API_KEY` 已替换为真实 API Key
- [x] `DB_PASSWORD` 已替换为强密码
- [x] `DATABASE_URL` 中的密码与 `DB_PASSWORD` 一致
- [x] `SECRET_KEY` 已替换为强密钥
- [ ] `REDIS_PASSWORD` 已配置（可选）
- [ ] `JWT_SECRET` 已配置（可选）
- [x] `.env` 文件权限设置为 600
- [x] `.env` 已添加到 `.gitignore`
- [x] 服务启动成功
- [x] API 测试通过

---

## 🎉 总结

### 必须替换的 Token（3个）

1. ✅ **COZE_WORKLOAD_IDENTITY_API_KEY** - Moonshot AI API Key
2. ✅ **DB_PASSWORD** - 数据库密码
3. ✅ **SECRET_KEY** - 应用密钥

### 建议替换的 Token（2个）

1. ⚠️ **REDIS_PASSWORD** - Redis 密码
2. ⚠️ **JWT_SECRET** - JWT 密钥

### 可选替换的 Token（3个）

1. 📌 **API_KEY** - 外部 API 密钥
2. 📌 **S3_ACCESS_KEY** - S3 访问密钥
3. 📌 **S3_SECRET_KEY** - S3 秘密密钥

---

**配置完成后，系统即可安全运行！** 🚀

---

**文档版本**: v1.0
**更新日期**: 2025-01-10
