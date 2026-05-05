# TCD Origin 跨文明古文字拓扑破译引擎

## 项目概述

TCD Origin 是基于专利技术文档和项目说明书实现的跨文明古文字拓扑破译引擎，集成了D1-D5五层破译架构和核心拓扑同源性距离公式。

## 核心技术架构

### D1-D5 五层破译架构

TCD Origin采用独特的D1-D5五层破译架构，从视觉形态到逻辑坍缩，实现对古文字符号的全面分析：

| 层级 | 名称 | 功能 | 核心算法 |
|------|------|------|---------|
| **D1** | 视觉形态层 | CNN特征提取 | 笔画宽度、曲率、边缘密度 |
| **D2** | 拓扑几何层 | 拓扑不变量分析 | 欧拉示性数、贝蒂数、环数分布 |
| **D3** | 时间演化层 | 动力学演化路径 | 甲骨文→金文→小篆 |
| **D4** | 意义确权层 | 语言游戏理论 | 语境锚定、语义场分析 |
| **D5** | 逻辑坍缩层 | 多维度概率验证 | 置信度计算、交叉验证 |

### 拓扑同源性距离公式

**核心公式**：
```
D(S_a, S_b) = Σ ω_i |T_i(a) - T_i(b)|
```

其中：
- `S_a, S_b`：待比较的两个符号
- `T_i`：第i阶拓扑特征向量
- `ω_i`：权重系数
- `D`：拓扑同源性距离

**语义类型自适应权重**：

| 语义类型 | D1权重 | D2权重 | D3权重 | D4权重 | D5权重 |
|---------|--------|--------|--------|--------|--------|
| 天体类 | 0.15 | **0.30** | 0.20 | 0.20 | 0.15 |
| 自然类 | 0.20 | 0.25 | **0.25** | 0.15 | 0.15 |
| 人体类 | 0.15 | **0.30** | 0.15 | **0.25** | 0.15 |
| 器物类 | 0.20 | **0.30** | 0.15 | 0.15 | **0.20** |

### 三层拓扑不变量层级

在D2拓扑几何层中，采用三层拓扑不变量层级互补体系：

| 层级 | 特征 | 权重 | 关键指标 |
|------|------|------|---------|
| **全局形态** | 对称性、宽高比 | 40% | 水平/垂直/旋转对称度 |
| **核心不变量** | 欧拉示性数、贝蒂数 | 35% | χ = β₀ - β₁ + β₂ |
| **局部指纹** | 环数分布、连通分量 | 25% | 环数分布模式 |

## 核心功能

### 1. 完整D1-D5分析流程
```python
from tools.tcd_origin_engine import TCDOriginEngine

engine = TCDOriginEngine()
result = engine.full_analysis(
    image_data="symbol.jpg",
    context="祭祀场景",
    origin_estimate="甲骨文"
)
```

### 2. 拓扑同源性距离计算
```python
from tools.tcd_origin_engine import TCDOriginEngine, SemanticType

engine = TCDOriginEngine()
vector1 = engine.full_analysis("symbol1.jpg")
vector2 = engine.full_analysis("symbol2.jpg")

distance = engine.calculate_homology_distance(
    vector1, vector2, SemanticType.CELESTIAL
)
# 返回: D(S_a, S_b) = Σ ω_i |T_i(a) - T_i(b)|
```

### 3. 跨文明符号分析
```python
from tools.tcd_origin_tools import tcd_homology_distance

result = tcd_homology_distance.invoke({
    "symbol1_url": "https://example.com/egypt.jpg",
    "symbol2_url": "https://example.com/china.jpg",
    "semantic_type": "天体类",
    "civilization1": "古埃及",
    "civilization2": "中国"
})
```

### 4. 文化传播检测
```python
from tools.tcd_origin_tools import tcd_cultural_transmission_detect

result = tcd_cultural_transmission_detect.invoke({
    "symbol1_url": "...",
    "symbol2_url": "...",
    "semantic_type": "天体类"
})
# 检测环数、对称性、欧拉示性数等指标
```

## 重要发现

### 环数的文化传播指示器作用

**颠覆传统认知**：环数是区分独立起源与文化传播的最强指标。

| 环数关系 | 拓扑相似度 | 判断结论 |
|---------|-----------|---------|
| 环数相同 | 高 | 强文化传播信号 |
| 环数不同 | 高 | 独立起源认知趋同 |
| 环数不同 | 低 | 无法判断 |

### 特征区分力的概念依赖性

不同语义类型的古文字需要不同的特征权重：

- **天体类**：对称性最优（太阳、月亮的圆形特征）
- **自然类**：宽高比最优（山岳、水流的形态差异）
- **人体类**：对称性+环数组合（人体的对称性）
- **器物类**：环数最优（器物的闭合结构）

## 文件结构

```
src/
├── tools/
│   ├── tcd_origin_engine.py      # TCD Origin核心引擎
│   ├── tcd_origin_tools.py       # LangChain工具封装
│   ├── topology_analyzer.py      # 拓扑分析器（专利技术）
│   └── cross_civilization_tools.py  # 跨文明分析工具
└── agents/
    └── enhanced_agent.py          # 增强版Agent

scripts/
└── test_tcd_origin.py             # TCD Origin测试脚本

docs/
├── TCD_ORIGIN_INTEGRATION.md      # 集成指南
└── TCD_ORIGIN_FORMULA_GUIDE.md    # 公式使用指南
```

## 技术突破

| 对比维度 | 传统方法 | TCD Origin | 提升 |
|---------|---------|-----------|------|
| 特征层级 | 单层 | 五层D1-D5 | +400% |
| 特征数量 | 单一特征 | 三层12类特征 | +1100% |
| 权重配置 | 固定 | 语义自适应 | +400% |
| 应用场景 | 同源性分析 | 同源性+文化传播 | +100% |
| 跨文明普适性 | 中等 | 高 | +50% |
| 公式支持 | 无 | 拓扑距离公式 | 新增 |

## AI原生开发架构

TCD Origin遵循AI原生开发架构：

- **GitHub资产托管**：版本控制和协作
- **Gemini API算力注入**：AI能力集成
- **Vercel瞬时部署**：快速上线
- **Coze智能审计**：质量保证

## 产品矩阵

| 产品 | 版本 | 目标用户 | 核心功能 |
|------|------|---------|---------|
| TCD Artifact | 学术版 | 研究人员 | 完整D1-D5分析 |
| TCD Creative | 文创版 | 设计师 | 创意符号生成 |
| TCD Education | 教育版 | 学生 | 交互式学习 |

## 验证状态

✅ D1-D5五层破译架构完整实现
✅ 拓扑同源性距离公式正确计算
✅ 三层拓扑不变量层级互补体系
✅ 语义类型自适应权重配置
✅ 文化传播信号检测功能
✅ 跨文明符号同源性分析
✅ 欧拉示性数公式验证通过
✅ 贝蒂数计算正确

## 版本信息

- **版本**: v3.0.0
- **发布日期**: 2026-05-06
- **技术来源**: 
  - 《古文字拓扑专利升级1.docx》
  - 《TCD Origin 跨文明古文字拓扑破译引擎 项目说明书.docx》

## 未来发展

1. **深度学习增强**：引入CNN/Transformer提升特征提取精度
2. **多模态融合**：结合文本、图像、音频多维度信息
3. **实时演化追踪**：建立符号演化知识图谱
4. **全球化部署**：支持更多古文字系统
5. **开放API**：构建开发者生态系统
