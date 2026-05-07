# 🚀 GitHub 快速启动指南

## 📋 5步快速发布

### 第1步：创建 GitHub 仓库

1. 访问 [github.com](https://github.com)
2. 点击 **"+"** → **"New repository"**
3. 填写信息：
   ```
   Repository name: tcd-origin
   Description: 跨文明古文字拓扑破译引擎
   Public ✓
   Initialize this repository: 不要勾选
   ```
4. 点击 **"Create repository"**

### 第2步：复制仓库地址

在创建后的页面，复制仓库的 HTTPS 或 SSH 地址：
```
https://github.com/YOUR_USERNAME/tcd-origin.git
```

### 第3步：添加远程仓库

```bash
cd /workspace/projects
git remote add origin https://github.com/YOUR_USERNAME/tcd-origin.git
```

### 第4步：推送代码

```bash
# 首次推送
git push -u origin main

# 后续推送
git push origin main
```

### 第5步：创建 Release

1. 在 GitHub 仓库页面，点击 **"Releases"**
2. 点击 **"Draft a new release"**
3. 填写信息：
   - Tag version: `v3.0.1`
   - Release title: `TCD Origin v3.0.1`
   - Description: 发布说明
4. 点击 **"Publish release"**

---

## 🔧 常用 Git 命令

### 基本操作

```bash
# 查看状态
git status

# 添加文件
git add .                    # 添加所有文件
git add README.md            # 添加单个文件

# 提交
git commit -m "提交信息"

# 推送
git push                     # 推送到远程
git pull                     # 拉取更新
```

### 分支操作

```bash
# 创建分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 查看分支
git branch

# 删除分支
git branch -d feature/new-feature
```

### 标签操作

```bash
# 创建标签
git tag -a v3.0.1 -m "版本说明"

# 推送标签
git push origin v3.0.1

# 查看标签
git tag
```

---

## 📊 发布后检查清单

### ✅ 代码审查

- [ ] 所有测试通过
- [ ] 没有敏感信息泄露
- [ ] 文档完整
- [ ] 示例可运行

### ✅ GitHub 设置

- [ ] 仓库描述已填写
- [ ] Topics 已添加
- [ ] Website 已链接（如果有）
- [ ] Collaborators 已添加（如果有）

### ✅ 文档完善

- [ ] README.md 完整
- [ ] LICENSE 文件存在
- [ ] CONTRIBUTING.md 存在
- [ ] CODE_OF_CONDUCT.md 存在

---

## 🌟 提升项目可见度

### 添加 Topics（标签）

在仓库页面右侧，点击 **"Add topics"**，添加：
```
python, artificial-intelligence, linguistics, archaeology, ancient-texts,
machine-learning, deep-learning, natural-language-processing,
cultural-heritage, historical-analysis
```

### 创建 GitHub Pages

1. **Settings** → **Pages**
2. Source: `main` branch, `/ (root)` folder
3. 点击 **Save**
4. 等待部署完成

网站将发布在：`https://YOUR_USERNAME.github.io/tcd-origin/`

---

## 📈 推广渠道

### 技术社区
- 🔵 [掘金](https://juejin.cn/)
- 🟢 [CSDN](https://blog.csdn.net/)
- 🟠 [SegmentFault](https://segmentfault.com/)
- 🔴 [Stack Overflow](https://stackoverflow.com/)

### 开源社区
- 🔵 [开源中国](https://www.oschina.net/)
- 🟢 [GitHub Explore](https://github.com/explore)
- 🟠 [Product Hunt](https://producthunt.com/)

### 学术社区
- 📚 [arXiv](https://arxiv.org/)
- 🎓 [ResearchGate](https://www.researchgate.net/)

---

## ❓ 常见问题

### Q: 如何重命名仓库？
A: Settings → Repository name → Rename

### Q: 如何删除仓库？
A: Settings → Danger Zone → Delete this repository

### Q: 如何添加协作者？
A: Settings → Collaborators → Add people

### Q: 如何查看贡献者？
A: Insights → Contributors

---

## 📞 资源链接

- [GitHub 官方文档](https://docs.github.com/)
- [Git 教程](https://git-scm.com/doc)
- [GitHub Actions](https://github.com/features/actions)
- [GitHub Pages](https://pages.github.com/)

---

**祝你的项目大火！🔥**

*需要帮助？查看 [GITHUB_RELEASE_GUIDE.md](./GITHUB_RELEASE_GUIDE.md)*
