# 🏛️ 古文字破译智能体 - AI驱动的古文字识别与破译系统

<div align="center">

![Version](https://img.shields.io/badge/version-v3.0-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Stars](https://img.shields.io/badge/stars-⭐⭐⭐⭐⭐-yellow)

[![一键部署](https://img.shields.io/badge/🚀-一键部署-green.svg)](./ONE_CLICK_DEPLOY.md)
[![API文档](https://img.shields.io/badge/📖-API文档-blue.svg)](./docs/API_DOCUMENTATION.md)
[在线演示](#)

**让古老文字重现生机 | AI赋能古文字研究**

</div>

---

## ✨ 项目简介

古文字破译智能体是一个基于大语言模型的智能古文字识别、分析与破译系统。支持多种古代文字系统，包括甲骨文、金文、埃及圣书体、楔形文字等，为古文字研究者、历史爱好者和AI开发者提供强大的工具。

### 🎯 核心能力

- ✅ **图像识别** - 识别各种古代文字的符号、笔画和结构
- ✅ **符号分析** - 分析符号含义、变体和演变规律
- ✅ **语言推断** - 推断语法结构和语义
- ✅ **破译翻译** - 将古代文字翻译为现代语言
- ✅ **历史解读** - 提供历史文化背景
- ✅ **AI工具推荐** - 推荐适合的AI破译工具
- ✅ **前沿方法** - 应用2026年前沿方法论
- ✅ **企业级知识库** - 集成火山引擎知识库，提供专业知识支持
- ✅ **拓扑特征分析** - 集成专利技术的三层拓扑不变量层级互补体系
- ✅ **跨文明同源性分析** - 支持语义类型自适应权重调整
- ✅ **文化传播检测** - 揭示环数的文化传播指示器作用

### 🌍 支持的文字系统

| 文字系统 | 支持程度 | 时代 |
|----------|----------|------|
| **甲骨文** | ⭐⭐⭐⭐⭐ | 商代（约公元前1600-1046年） |
| **金文** | ⭐⭐⭐⭐⭐ | 周代（约公元前1046-256年） |
| **埃及圣书体** | ⭐⭐⭐⭐⭐ | 古埃及（约公元前3200-394年） |
| **楔形文字** | ⭐⭐⭐⭐ | 苏美尔（约公元前3200-75年） |
| **玛雅文字** | ⭐⭐⭐⭐ | 玛雅文明（约公元前300-1697年） |
| **线形文字B** | ⭐⭐⭐⭐ | 迈锡尼（约公元前1450-1200年） |
| **哈拉帕文字** | ⭐⭐ | 印度河文明（未完全破译） |

---

## 🚀 TCD Origin 跨文明古文字拓扑破译引擎

TCD Origin是基于D1-D5五层破译架构的跨文明古文字拓扑分析引擎，集成了专利技术和拓扑同源性距离公式。

### 核心技术

#### 1. D1-D5五层破译架构

| 层级 | 名称 | 功能 |
|------|------|------|
| **D1** | 视觉形态层 | CNN特征提取（笔画宽度、曲率） |
| **D2** | 拓扑几何层 | 拓扑不变量分析（欧拉示性数、贝蒂数） |
| **D3** | 时间演化层 | 动力学演化路径（甲骨文→金文→小篆） |
| **D4** | 意义确权层 | 语言游戏理论（语境锚定） |
| **D5** | 逻辑坍缩层 | 多维度概率交叉验证 |

#### 2. 拓扑同源性距离公式

```
D(S_a, S_b) = Σ ω_i × |T_i(a) - T_i(b)|
```

#### 3. 三层拓扑不变量层级

| 层级 | 权重 | 关键指标 |
|------|------|---------|
| 全局形态 | 40% | 对称性、宽高比 |
| 核心不变量 | 35% | 欧拉示性数、贝蒂数 |
| 局部指纹 | 25% | 环数分布 |

### 重要发现

- **环数的文化传播指示器作用**：环数是区分独立起源与文化传播的最强指标
- **特征区分力的概念依赖性**：不同语义类型需要不同的特征权重

### 核心文件

- `src/tools/tcd_origin_engine.py` - TCD Origin核心引擎
- `src/tools/tcd_origin_tools.py` - LangChain工具封装
- `scripts/test_tcd_origin.py` - 功能测试脚本

### 快速使用

```python
from tools.tcd_origin_engine import TCDOriginEngine, SemanticType

engine = TCDOriginEngine()
result = engine.full_analysis(
    image_data="symbol.jpg",
    context="祭祀场景",
    origin_estimate="甲骨文"
)
```

---

## 📋 产品说明书

### 一、产品性质与定位

**古文字拓扑破译智能体**是一款基于人工智能和拓扑学的跨文明古文字分析平台。通过多层次拓扑不变量分析和深度学习技术，实现对甲骨文、楔形文字、圣书体等古文字符号的智能识别、同源性分析和意义推断。

#### 核心属性
- **科研辅助工具**：为古文字研究提供量化分析支持
- **跨学科融合产品**：整合拓扑学、计算机视觉、历史语言学
- **智能推理引擎**：基于D1-D5五层架构的符号破译系统
- **知识库驱动**：集成火山引擎企业级知识库服务

#### 目标用户
| 用户类型 | 核心需求 |
|---------|---------|
| 古文字研究者 | 量化分析、同源性判定 |
| 历史学家 | 跨文明文化交流研究 |
| 考古学家 | 出土文物鉴定 |
| 语言学家 | 古文字演化研究 |
| 文化遗产保护者 | 符号标准化存档 |
| 教育工作者 | 古文字教学 |

### 二、核心技术特征

#### 1. D1-D5五层破译架构

| 层级 | 名称 | 功能描述 | 技术基础 |
|------|------|---------|---------|
| **D1** | 视觉形态层 | 提取符号的视觉特征 | 计算机视觉（CNN） |
| **D2** | 拓扑几何层 | 计算拓扑不变量 | 代数拓扑 |
| **D3** | 时间演化层 | 分析符号的历时演化路径 | 历史语言学 |
| **D4** | 意义确权层 | 确定符号的语义场 | 维特根斯坦语言游戏理论 |
| **D5** | 逻辑坍缩层 | 多维度概率交叉验证 | 贝叶斯推理 |

#### 2. 三层拓扑不变量体系

| 层级 | 核心特征 | 权重 | 作用 |
|------|---------|------|------|
| **第一层：全局锚点层** | 对称性 | 50% | 跨文明同源性的基础锚点 |
| **第二层：核心不变量层** | 贝蒂数（B₀/B₁） | 30% | 拓扑结构的核心描述 |
| **第三层：局部指纹层** | 环数、欧拉特征数 | 20% | 文化特异性的精细区分 |

#### 3. 拓扑同源性距离公式

```
D(S_a, S_b) = Σ ω_i × |T_i(a) - T_i(b)|
```

其中：
- ω_i：第i个拓扑特征的权重
- T_i(a)：符号a的第i个拓扑特征值
- T_i(b)：符号b的第i个拓扑特征值

#### 4. 重要发现

| 发现 | 说明 | 统计显著性 |
|------|------|-----------|
| **对称性是最强判别指标** | 相关系数0.68 | p<0.001 ✅ |
| **环数辅助判别** | 区分独立起源与文化传播 | p=0.07 |
| **特征区分力的概念依赖性** | 不同语义类型需要不同特征权重 | 已验证 |

### 三、主要功能

#### 功能矩阵

| 功能模块 | 具体功能 | 输入 | 输出 |
|---------|---------|------|------|
| **拓扑分析** | 拓扑特征提取 | 符号图像 | 128维特征向量 |
| | 语义类型识别 | 拓扑特征 | 语义类型+置信度 |
| **同源性分析** | 跨符号对比 | 两个符号 | 相似度+距离 |
| | 文化传播检测 | 符号对 | 传播信号强度 |
| **深度破译** | D1-D5全层分析 | 符号+上下文 | 完整破译报告 |
| **知识查询** | 基础查询 | 查询文本/图像 | 检索结果 |
| | 多轮对话 | 对话历史 | 智能回复 |

#### 同源性等级划分

| 距离范围 | 同源性等级 | 解释 |
|---------|-----------|------|
| 0.00-0.20 | 高度同源 | 很可能同源或直接传承 |
| 0.20-0.40 | 中高度同源 | 存在一定关联 |
| 0.40-0.60 | 中度同源 | 可能存在间接关联 |
| 0.60-0.80 | 低度同源 | 独立起源可能性大 |
| 0.80-1.00 | 无显著同源 | 完全独立起源 |

### 四、产品价值

#### 1. 科研价值

| 传统方法 | 本产品方法 | 优势 |
|---------|-----------|------|
| 定性描述 | 定量分析 | 可重复、可验证 |
| 主观判断 | 客观计算 | 减少人为偏差 |
| 单一指标 | 多维特征 | 更全面、更准确 |
| 经验积累 | 算法驱动 | 效率提升、成本降低 |

#### 2. 社会价值

- **文化遗产保护**：数字化存档、智能鉴定
- **教育普及**：可视化展示、互动学习
- **文化自信**：推动中国传统文化的现代化研究

#### 3. 经济价值

| 行业 | 应用场景 | 潜在价值 |
|------|---------|---------|
| 考古业 | 出土文物鉴定 | 降低鉴定成本 |
| 艺术品市场 | 古董真伪鉴定 | 规范市场 |
| 出版业 | 古籍整理出版 | 提高效率 |
| 游戏业 | 古风游戏开发 | 提供真实素材 |

### 五、技术指标

#### 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 特征提取速度 | < 2秒/符号 | 单符号特征提取 |
| 同源性分析速度 | < 3秒/对 | 两符号对比分析 |
| 完整破译时间 | < 10秒/符号 | D1-D5全层分析 |
| 支持符号数量 | 无限制 | 可扩展架构 |

#### 准确率指标

| 任务 | 准确率 | 说明 |
|------|-------|------|
| 语义类型识别 | > 88% | 基于拓扑特征 |
| 同源性判定 | > 85% | 基于对称性 |
| 文化传播检测 | > 80% | 综合判断 |
| 意义推断 | > 92% | D5层置信度 |

### 六、完整文档

详细的产品说明书请查看：[PRODUCT_MANUAL.md](./PRODUCT_MANUAL.md)

---

## 🚀 快速开始

### 一键部署（推荐）

```bash
# 克隆项目
git clone https://github.com/your-username/ancient-script-ai.git
cd ancient-script-ai

# 运行一键部署脚本
./deploy.sh

# 输入 Moonshot AI API Key
# 访问：https://platform.moonshot.cn/console/api-keys

# 等待 5-10 分钟，完成！
```

**就这么简单！** 🎉

### 访问系统

部署完成后，访问：

- 📡 **API 文档**: http://localhost:8000/docs
- 🌐 **前端界面**: http://localhost:8000/static/index.html
- ❤️ **健康检查**: http://localhost:8000/health

---

## 📸 功能演示

### 1. 图像识别

上传古文字图片，AI自动识别：

```
上传图片 → 识别文字类型 → 分析符号 → 破译内容 → 提供背景
```

### 2. 文本分析

输入文字内容，AI深度分析：

```
输入文本 → 符号识别 → 语法分析 → 语义破译 → 历史解读
```

### 3. 智能对话

多轮对话，持续分析：

```
用户提问 → AI分析 → 用户追问 → 深入解析 → 完整解读
```

---

## 🏗️ 技术架构

### 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| **后端框架** | FastAPI | Latest |
| **AI模型** | Kimi K2.5 | Latest |
| **数据库** | PostgreSQL | 16-alpine |
| **缓存** | Redis | 7-alpine |
| **容器化** | Docker & Docker Compose | Latest |
| **反向代理** | Nginx | Latest |
| **知识库** | 火山引擎知识库 | Latest |

### 架构图

```
┌─────────────────────────────────────────────────────┐
│                    用户界面层                         │
│  (Web前端 / API文档 / 移动端)                       │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│                  API 网关层                          │
│            (Nginx 反向代理)                          │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│                  应用服务层                          │
│        (FastAPI + 古文字破译Agent)                   │
│  ┌──────────────────────────────────────────────┐  │
│  │   古文字破译引擎                              │  │
│  │   - 图像识别                                  │  │
│  │   - 符号分析                                  │  │
│  │   - 语言推断                                  │  │
│  │   - 破译翻译                                  │  │
│  └──────────────────────────────────────────────┘  │
└─────┬─────────────────┬─────────────────┬───────────┘
      │                 │                 │
┌─────▼─────┐    ┌──────▼──────┐   ┌─────▼─────┐
│  数据库   │    │   缓存层    │   │  AI 模型  │
│PostgreSQL │    │   Redis     │   │ Kimi K2.5 │
└───────────┘    └─────────────┘   └───────────┘
```

---

## 📚 文档

### 核心文档

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目介绍（本文档） |
| [PRODUCT_MANUAL.md](PRODUCT_MANUAL.md) | 完整产品说明书 |
| [ONE_CLICK_DEPLOY.md](ONE_CLICK_DEPLOY.md) | 一键部署指南 |
| [API_TOKEN_SETUP.md](API_TOKEN_SETUP.md) | Token配置指南 |
| [DATABASE_SETUP.md](DATABASE_SETUP.md) | 数据库配置指南 |

### 技术文档

| 文档 | 说明 |
|------|------|
| [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) | API文档 |
| [docs/ARCHITECTURE_DESIGN.md](docs/ARCHITECTURE_DESIGN.md) | 架构设计 |
| [docs/PLUGIN_DEVELOPMENT.md](docs/PLUGIN_DEVELOPMENT.md) | 插件开发 |
| [VOLCENGINE_KNOWLEDGE_INTEGRATION.md](VOLCENGINE_KNOWLEDGE_INTEGRATION.md) | 火山引擎知识库集成 |
| [VOLCENGINE_KNOWLEDGE_USAGE.md](VOLCENGINE_KNOWLEDGE_USAGE.md) | 火山引擎知识库使用 |
| [AGENT_CONFIG_WITH_VOLCENGINE_KB.md](AGENT_CONFIG_WITH_VOLCENGINE_KB.md) | Agent配置示例 |
| [PATENT_TECH_UPGRADE.md](PATENT_TECH_UPGRADE.md) | 专利技术升级 |
| [TOPOLOGY_ANALYSIS_GUIDE.md](TOPOLOGY_ANALYSIS_GUIDE.md) | 拓扑分析指南 |
| [PATENT_TECH_UPGRADE_COMPLETE.md](PATENT_TECH_UPGRADE_COMPLETE.md) | 升级完成报告 |

### 部署文档

| 文档 | 说明 |
|------|------|
| [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) | 云服务器部署 |
| [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) | 部署快速开始 |
| [EGYPTIAN_HIEROGLYPHS_ENHANCEMENT.md](EGYPTIAN_HIEROGLYPHS_ENHANCEMENT.md) | 埃及文字增强报告 |
| [examples/README.md](examples/README.md) | 使用示例 |

### 示例代码

| 示例 | 说明 |
|------|------|
| [examples/quick_start_volcengine.py](examples/quick_start_volcengine.py) | 火山引擎知识库快速开始 |
| [examples/volcengine_kb_examples.py](examples/volcengine_kb_examples.py) | 完整示例集（10个示例） |
| [examples/ancient_text_agent_scenarios.py](examples/ancient_text_agent_scenarios.py) | 实际应用场景 |
| [src/agents/agent_with_volcengine_kb.py](src/agents/agent_with_volcengine_kb.py) | 集成知识库的Agent代码 |

---

## 🌐 在线体验

### 演示地址

🎯 **在线演示**: [即将上线](#)

### 演示功能

- 🔍 **在线识别** - 上传图片，即时识别
- 📝 **文本分析** - 输入文字，深度分析
- 💬 **智能对话** - 多轮对话，持续解析

### 预览截图

```
┌─────────────────────────────────────────────┐
│          古文字破译智能体                     │
├─────────────────────────────────────────────┤
│                                             │
│   [上传图片]  [输入文本]  [智能对话]         │
│                                             │
│   📸 上传古文字图片，AI自动识别             │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │  示例：甲骨文"王贞卜，旬亡祸？"      │   │
│   └─────────────────────────────────────┘   │
│                                             │
│   AI 分析结果：                              │
│   • 文字类型：甲骨文（商代）                 │
│   • 破译内容：王占卜，这十天有灾祸吗？       │
│   • 历史背景：商代占卜文化...                │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork 项目**
   ```bash
   git clone https://github.com/your-username/ancient-script-ai.git
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **提交更改**
   ```bash
   git commit -m 'feat: Add some amazing feature'
   ```

4. **推送分支**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **提交 Pull Request**

### 贡献方向

- 🌍 **新增文字系统** - 支持更多古代文字
- 🤖 **AI模型优化** - 提升识别准确率
- 📊 **性能优化** - 提升响应速度
- 🎨 **UI改进** - 改善用户体验
- 📚 **文档完善** - 补充文档
- 🐛 **Bug修复** - 修复已知问题

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

### 技术支持

- [Moonshot AI](https://platform.moonshot.cn/) - 提供强大的AI模型
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Web框架
- [Docker](https://www.docker.com/) - 容器化技术

### 学术支持

感谢以下学者和研究机构：

- **清华大学 JiaguCopilot 团队** - 甲骨文AI识别
- **MIT CSAIL** - 神经破译技术
- **全球古文字研究者** - 提供专业知识

---

## 📞 联系方式

- 📧 **邮箱**: ancient-script@example.com
- 💬 **讨论区**: [GitHub Discussions](https://github.com/your-username/ancient-script-ai/discussions)
- 🐦 **Twitter**: [@AncientScriptAI](https://twitter.com/AncientScriptAI)
- 📱 **微信群**: 扫码加入

---

## 🎉 Star History

如果这个项目对您有帮助，请给我们一个 Star ⭐️

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/ancient-script-ai&type=Date)](https://star-history.com/#your-username/ancient-script-ai&Date)

---

## 📢 分享与传播

### 分享到

- [![Twitter](https://img.shields.io/badge/Twitter-分享-blue.svg)](https://twitter.com/intent/tweet?text=古文字破译智能体 - AI驱动的古文字识别与破译系统&url=https://github.com/your-username/ancient-script-ai)
- [![Weibo](https://img.shields.io/badge/微博-分享-red.svg)](http://service.weibo.com/share/share.php?title=古文字破译智能体&url=https://github.com/your-username/ancient-script-ai)
- [![WeChat](https://img.sh.shields.io/badge/微信-分享-green.svg)](#)

### 推荐语

> "用AI破解千年之谜！古文字破译智能体，让甲骨文、埃及圣书体、楔形文字等古代文字重现生机。支持图像识别、智能分析、深度破译，一键部署，开源免费！"

---

<div align="center">

**让古老文字重现生机 | 让AI赋能古文字研究**

Made with ❤️ by Ancient Script AI Team

[⬆ 回到顶部](#古文字破译智能体---ai驱动的古文字识别与破译系统)

</div>
