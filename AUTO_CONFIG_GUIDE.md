# 🚀 自动配置脚本使用指南

## ⚡ 一键配置所有 Token

### 使用方法

```bash
# 1. 进入项目根目录
cd /path/to/ancient-script

# 2. 运行配置脚本
./setup-config.sh

# 3. 按照提示输入信息
#    - Moonshot AI API Key
#    - 数据库密码（可自动生成）
#    - 其他配置（可选）
```

### 脚本功能

✅ **自动完成的任务**：
1. 检查 `.env` 文件是否存在
2. 配置 Moonshot AI API Key
3. 配置数据库密码（可自动生成强密码）
4. 配置应用密钥（SECRET_KEY）
5. 配置 Redis 密码（可选）
6. 配置 JWT 密钥（可选）
7. 配置外部 API Key（可选）
8. 设置文件权限（600）
9. 验证配置
10. 显示配置摘要

### 交互式配置流程

```
======================================
古文字破译系统 - 自动配置脚本
======================================

此脚本将帮助您配置所有必要的 API Token 和敏感信息

是否开始配置？(y/n): y

======================================
步骤 1: 检查配置文件
======================================

[INFO] .env 文件不存在，从 .env.example 复制...
[SUCCESS] .env 文件已创建

======================================
步骤 2: 配置 Moonshot AI API Key
======================================

获取 Moonshot AI API Key：
  1. 访问 https://platform.moonshot.cn/console/api-keys
  2. 登录或注册账号
  3. 点击"创建 API Key"
  4. 复制生成的 API Key（格式：sk-xxxxx...）

请输入您的 Moonshot AI API Key: sk-abc123...
[SUCCESS] Moonshot AI API Key 已配置

======================================
步骤 3: 配置数据库密码
======================================

数据库密码用于保护您的数据安全
建议使用强密码（至少16位）

是否自动生成强密码？(y/n，推荐 y): y
[INFO] 已生成数据库密码: Xk9$mN2#p***（仅显示前8位）
[SUCCESS] 数据库密码已配置

======================================
步骤 4: 配置应用密钥（SECRET_KEY）
======================================

应用密钥用于加密用户会话和数据
正在生成强密钥...
[SUCCESS] 应用密钥已配置

======================================
步骤 5: 配置 Redis 密码（可选）
======================================

是否配置 Redis 密码？(y/n，推荐 y): y
[SUCCESS] Redis 密码已配置

======================================
步骤 6: 配置 JWT 密钥（可选）
======================================

是否配置 JWT 密钥？(y/n，推荐 y): y
[SUCCESS] JWT 密钥已配置

======================================
步骤 7: 配置外部 API Key（可选）
======================================

是否配置外部 API Key？(y/n): n
[INFO] 跳过外部 API Key 配置

======================================
步骤 8: 设置文件权限
======================================

[SUCCESS] 文件权限已设置（600）

======================================
步骤 9: 验证配置
======================================

[INFO] 检查配置文件...
[SUCCESS] 配置验证通过

======================================
配置完成
======================================

✅ 所有 Token 已配置完成！

已配置的项目：
  ✅ Moonshot AI API Key
  ✅ 数据库密码
  ✅ 应用密钥（SECRET_KEY）
  ✅ Redis 密码（如配置）
  ✅ JWT 密钥（如配置）
  ✅ 外部 API Key（如配置）

安全措施：
  ✅ .env 文件权限已设置为 600
  ⚠️  请确保 .env 已添加到 .gitignore
  ⚠️  请妥善保存配置信息

下一步操作：
  1. 启动服务: docker-compose up -d
  2. 查看日志: docker-compose logs -f
  3. 测试 API: curl http://localhost:8000/health

⚠️  重要提示：
  • 请将配置信息保存到安全的地方
  • 不要将 .env 文件提交到 Git 仓库
  • 定期更换 Token（建议每3-6个月）

配置脚本执行完成！
```

---

## 📋 配置前准备

### 1. 获取 Moonshot AI API Key

访问 [Moonshot AI 控制台](https://platform.moonshot.cn/console/api-keys)

1. 登录或注册账号
2. 点击"创建 API Key"
3. 复制生成的 API Key（格式：`sk-xxxxx...`）

### 2. 准备安装依赖

```bash
# 检查 openssl 是否安装
which openssl

# 如果未安装，请安装：
# Ubuntu/Debian: sudo apt install openssl
# CentOS/RHEL: sudo yum install openssl
# macOS: brew install openssl
```

---

## 🔧 手动配置（如脚本无法运行）

如果脚本无法运行，请参考 [API_TOKEN_SETUP.md](API_TOKEN_SETUP.md) 进行手动配置。

---

## ✅ 配置验证

配置完成后，验证配置是否正确：

```bash
# 1. 检查 .env 文件权限
ls -la .env
# 应该显示：-rw-------

# 2. 检查是否有默认值
cat .env | grep -E "your_|change_this"
# 应该没有任何输出

# 3. 启动服务测试
docker-compose up -d

# 4. 查看日志
docker-compose logs -f web

# 5. 测试 API
curl http://localhost:8000/health
```

---

## 🆘 常见问题

### Q1: 脚本无法执行

**A**: 添加执行权限

```bash
chmod +x setup-config.sh
./setup-config.sh
```

### Q2: 提示权限被拒绝

**A**: 使用 sudo 或检查文件权限

```bash
# 使用 sudo
sudo ./setup-config.sh

# 或者修改 .env.example 权限
chmod 644 .env.example
```

### Q3: API Key 格式错误

**A**: 确保格式正确

- ✅ 正确：`sk-abc123def456...`
- ❌ 错误：`sk abc123`（空格）
- ❌ 错误：`abc123`（缺少 sk- 前缀）

### Q4: 数据库密码未生效

**A**: 确保 `DB_PASSWORD` 和 `DATABASE_URL` 中的密码一致

```bash
# 检查配置
cat .env | grep -E "DB_PASSWORD|DATABASE_URL"

# 应该看到：
# DB_PASSWORD=MyPass@123
# DATABASE_URL=postgresql://ancienttext:MyPass@123@db:5432/ancienttext
```

---

## 📚 相关文档

- [API_TOKEN_SETUP.md](API_TOKEN_SETUP.md) - 详细的 Token 配置指南
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - 数据库配置指南
- [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) - 部署快速开始

---

## 🎯 配置检查清单

使用脚本后，检查以下项目：

- [x] `.env` 文件已创建
- [x] Moonshot AI API Key 已配置
- [x] 数据库密码已配置
- [x] 应用密钥已配置
- [x] 文件权限已设置为 600
- [x] 配置验证通过
- [ ] 服务启动成功
- [ ] API 测试通过

---

## 🎉 完成！

配置完成后，启动服务：

```bash
# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试 API
curl http://localhost:8000/health
```

**系统即可正常使用！** 🚀
