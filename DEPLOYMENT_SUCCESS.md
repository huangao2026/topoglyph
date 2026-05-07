# 🎉 TCD Origin 免费部署指南（Render）

## ✅ 代码已成功推送到 GitHub

```
🔗 https://github.com/huangao2026/topoglyph
```

---

## 🚀 免费部署方案：Render

### 为什么选择 Render？

| 平台 | 免费额度 | 需要信用卡 | 推荐度 |
|------|---------|-----------|--------|
| **Render** | 750小时/月 | ❌ 不需要 | ⭐⭐⭐⭐⭐ |
| Railway | 500小时/月 | ✅ 需要 | ⭐⭐⭐ |
| Fly.io | 3200小时/月 | ❌ 不需要 | ⭐⭐⭐⭐ |

**Render 最适合**：无需信用卡，完全免费，支持 Docker！

---

## 📋 Render 部署步骤（6分钟）

### 第一步：访问 Render

👉 **https://render.com**

### 第二步：注册/登录

1. 点击 **"Get Started Free"**
2. 选择 **"GitHub"** 登录
3. 授权 Render 访问您的 GitHub

### 第三步：创建 Web Service

1. 点击 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 点击 **"Configure Account"**
4. 选择 **"topoglyph"** 仓库
5. 点击 **"Connect"**

### 第四步：配置服务

在配置页面填写：

```
🏷️ Name: tcd-origin
🌍 Region: Singapore（亚太最快）
📦 Branch: main
🗂️ Root Directory: (留空)
🐳 Runtime: Docker
📝 Dockerfile Path: ./Dockerfile
⚡ Instance Type: Free
🚀 Build Command: (留空)
🎯 Start Command: (留空)
```

### 第五步：添加环境变量

点击 **"Advanced"** → **"Add Environment Variable"**：

```
🔑 Key: PORT
🔐 Value: 7860

🔑 Key: ENVIRONMENT
🔐 Value: production
```

### 第六步：创建并等待

1. 点击 **"Create Web Service"**
2. ⏱️ 等待 **3-5分钟** 构建和部署
3. 看到绿色 ✓ 表示成功！

---

## 🌐 获取您的免费链接

部署成功后，Render 会显示：

```
🌐 您的在线地址: https://tcd-origin.onrender.com
```

**这就是您的对外分享链接！** 🎉

---

## 📝 快速检查清单

```
部署前检查：
[✓] GitHub 代码已推送
[✓] 仓库：topoglyph
[✓] 包含 web_app.py
[✓] 包含 Dockerfile

Render 配置：
[ ] Name: tcd-origin
[ ] Region: Singapore
[ ] Runtime: Docker
[ ] Instance: Free
[ ] Dockerfile Path: ./Dockerfile
[ ] Environment: PORT=7860, ENVIRONMENT=production
```

---

## 🔧 如果部署失败

### 错误：Build Failed

检查：
1. Dockerfile 是否在根目录
2. 环境变量是否添加了 PORT=7860
3. 点击 "Manual Deploy" → "Clear build cache & deploy"

### 错误：服务启动失败

查看日志排查问题，或联系技术支持

### 成功但链接打不开

等待 1-2 分钟，服务需要预热

---

## 📱 分享给朋友

部署成功后，复制以下内容分享：

```
🎉 古文字破译智能体上线啦！

🔗 在线体验：https://tcd-origin.onrender.com

✨ 功能：
- 📷 上传古文字图片，自动识别分析
- 🔍 跨文明符号同源性比较
- 📊 D1-D5五层破译架构
- 🌍 支持甲骨文、楔形文字、圣书体等

快来试试吧！🔮
```

---

## 💡 Render 免费版限制

- 每月 **750小时** 免费
- 闲置 **15分钟** 后自动休眠
- 下次访问时自动唤醒
- 适合个人/学习使用

**如果需要7x24小时运行，可以升级付费版（约$7/月）**

---

## 🆘 常见问题

### Q: 链接显示 "Service Unavailable"？
A: 免费版休眠了，访问后会自动唤醒，等待30秒即可

### Q: 如何保持服务活跃？
A: 使用 UptimeRobot 等免费监控服务定时ping

### Q: 如何升级为付费版？
A: Render 控制台 → 你的服务 → Plan → 选择付费方案

### Q: 能用自定义域名吗？
A: 可以，在 Settings → Custom Domains 添加

---

## 🎯 完成后的效果

```
🌐 在线体验: https://tcd-origin.onrender.com
🔗 GitHub: https://github.com/huangao2026/topoglyph
📖 文档: 项目内的 README.md
```

---

## 📚 更多资源

| 资源 | 链接 |
|------|------|
| 🌐 Render 官网 | https://render.com |
| 📖 Render 文档 | https://render.com/docs |
| 🔗 GitHub 仓库 | https://github.com/huangao2026/topoglyph |

---

**🎊 恭喜！您的 TCD Origin 即将免费上线！**

立即部署 👉 **https://render.com** 🚀

有任何问题随时告诉我！
