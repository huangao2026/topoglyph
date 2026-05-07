# 🔑 GitHub Token 获取指南

## 为什么需要 Token？

因为 GitHub 已不再支持密码认证，需要使用 Personal Access Token 来推送代码。

---

## 🚀 快速获取 Token（2分钟）

### 第一步：访问 Token 设置

👉 **https://github.com/settings/tokens**

点击 **"Generate new token"** → **"Generate new token (classic)"**

---

### 第二步：创建 Token

填写信息：

```
Note: TCD Origin 部署
Expiration: 30 days（30天有效期）

Select scopes（勾选）:
✓ repo (Full control of private repositories)
```

点击 **"Generate token"**

---

### 第三步：复制 Token

**重要！** 页面会显示一个 Token，格式类似：

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**立即复制保存！** 刷新页面后无法再次查看。

---

## 🔧 在终端使用 Token

获取 Token 后，请将 Token 发给我，我帮您完成推送：

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

或者您也可以直接在终端输入：

```bash
cd /workspace/projects

# 设置远程仓库
git remote set-url origin https://github.com/huangao2026/topoglyph.git

# 推送代码（会提示输入用户名和密码）
git push -u origin main

# Username: huangao2026
# Password: 粘贴您的 Token
```

---

## ✅ 推送成功后

访问 👉 **https://github.com/huangao2026/topoglyph**

确认看到所有代码文件！

---

## 🎯 下一步：Railway 部署

代码推送成功后：
1. 访问 👉 **https://railway.app**
2. Login with GitHub
3. Deploy from GitHub
4. 获取链接 ✅

---

**请提供您的 Token，我立即帮您推送代码！🔑**
