# TCD Origin 公式使用指南

## 目录

1. [拓扑同源性距离公式](#1-拓扑同源性距离公式)
2. [欧拉示性数公式](#2-欧拉示性数公式)
3. [语义类型权重配置](#3-语义类型权重配置)
4. [文化传播检测公式](#4-文化传播检测公式)
5. [置信度坍缩公式](#5-置信度坍缩公式)
6. [实际应用示例](#6-实际应用示例)

---

## 1. 拓扑同源性距离公式

### 公式定义

**核心公式**：
```
D(S_a, S_b) = Σ ω_i × |T_i(a) - T_i(b)|
```

### 参数说明

| 参数 | 含义 | 取值范围 |
|------|------|---------|
| `D(S_a, S_b)` | 两个符号S_a和S_b之间的拓扑同源性距离 | [0, 1] |
| `ω_i` | 第i阶拓扑特征向量的权重系数 | [0, 1] |
| `T_i(a)` | 符号a的第i阶拓扑特征值 | 实数 |
| `T_i(b)` | 符号b的第i阶拓扑特征值 | 实数 |
| `Σ` | 对所有特征维度求和 | - |

### 相似度转换

```python
# 距离转相似度
similarity = 1 - (distance / max_possible_distance)

# 其中 max_possible_distance = Σ ω_i
```

### 判定标准

| 相似度范围 | 同源性等级 | 解释 |
|-----------|-----------|------|
| 0.8 - 1.0 | 高度同源 | 很可能存在文化关联 |
| 0.6 - 0.8 | 中等同源 | 可能存在同源性 |
| 0.4 - 0.6 | 低度同源 | 需要更多证据 |
| 0.0 - 0.4 | 非同源 | 独立起源 |

---

## 2. 欧拉示性数公式

### 公式定义

```
χ = β₀ - β₁ + β₂
```

### 参数说明

| 参数 | 含义 | 拓扑意义 |
|------|------|---------|
| `χ` (chi) | 欧拉示性数 | 表征连通性和环数 |
| `β₀` (beta-0) | 0维贝蒂数 | 连通分量数 |
| `β₁` (beta-1) | 1维贝蒂数 | 独立环数 |
| `β₂` (beta-2) | 2维贝蒂数 | 空洞数 |

### 物理意义

| 欧拉示性数 | 连通分量 | 环数 | 示例 |
|-----------|---------|------|------|
| 1 | 1 | 0 | 实心符号（如：人、目） |
| 0 | 1 | 1 | 单环符号（如：日、口） |
| -1 | 1 | 2 | 双环符号（如：吕、回） |
| 2-n | 1 | n-1 | 多环符号 |

### 代码实现

```python
# 计算欧拉示性数
euler_characteristic = betti_0 - betti_1 + betti_2

# 示例
betti_0, betti_1, betti_2 = 1, 1, 0
euler = betti_0 - betti_1 + betti_2  # = 0
```

---

## 3. 语义类型权重配置

### D1-D5层权重配置

**天体类**（太阳、月亮、星星等）：
```python
{
    "D1_visual": 0.15,
    "D2_topology": 0.30,    # 拓扑特征最重要
    "D3_evolution": 0.20,
    "D4_meaning": 0.20,
    "D5_collapse": 0.15
}
```

**自然类**（山、水、火等）：
```python
{
    "D1_visual": 0.20,
    "D2_topology": 0.25,
    "D3_evolution": 0.25,  # 演化特征重要
    "D4_meaning": 0.15,
    "D5_collapse": 0.15
}
```

**人体类**（人、目、口等）：
```python
{
    "D1_visual": 0.15,
    "D2_topology": 0.30,    # 拓扑+意义组合
    "D3_evolution": 0.15,
    "D4_meaning": 0.25,
    "D5_collapse": 0.15
}
```

**器物类**（田、皿、弓等）：
```python
{
    "D1_visual": 0.20,
    "D2_topology": 0.30,    # 拓扑+坍缩组合
    "D3_evolution": 0.15,
    "D4_meaning": 0.15,
    "D5_collapse": 0.20
}
```

### D2拓扑层子特征权重

```python
{
    "global": 0.40,   # 全局形态锚点（对称性、宽高比）
    "core": 0.35,      # 核心拓扑不变量（欧拉示性数、贝蒂数）
    "local": 0.25      # 局部结构指纹（环数分布）
}
```

---

## 4. 文化传播检测公式

### 核心指标

**环数比较**：
```
ring_diff = |rings_a - rings_b|
```

**对称性相似度**：
```
symmetry_sim = 1 - |symmetry_a - symmetry_b|
```

**综合判断**：

| 条件 | 信号强度 | 结论 |
|------|---------|------|
| `ring_diff == 0` 且 `symmetry_sim > 0.7` | strong | 强文化传播 |
| `ring_diff > 0` 且 `symmetry_sim > 0.8` | weak | 独立起源认知趋同 |
| 其他 | unknown | 无法判断 |

### 物理意义

**重要发现**：环数是区分独立起源与文化传播的最强指标

- **环数相同 + 拓扑相似** → 文化传播或符号借用
- **环数不同 + 拓扑相似** → 独立起源的认知趋同
- **环数不同 + 拓扑不同** → 很可能独立起源

---

## 5. 置信度坍缩公式

### D5逻辑坍缩层

**概率分布**：
```python
P(meaning_i) = softmax(scores_i)
```

**最终置信度**：
```python
confidence = max(P(meaning_i))
```

**交叉验证分数**：
```python
cross_val_score = (D1_match + D2_match + D3_match + D4_match) / 4
```

### 坍缩判定

| 置信度范围 | 坍缩状态 | 解释 |
|-----------|---------|------|
| 0.8 - 1.0 | 确定性坍缩 | 唯一解释 |
| 0.6 - 0.8 | 高置信度 | 主要解释明确 |
| 0.4 - 0.6 | 中等置信度 | 需更多信息 |
| 0.0 - 0.4 | 低置信度 | 解释模糊 |

---

## 6. 实际应用示例

### 示例1：计算两个符号的同源性距离

```python
from tools.tcd_origin_engine import TCDOriginEngine, SemanticType

engine = TCDOriginEngine()

# 提取符号特征
vector1 = engine.full_analysis("egypt_sun.jpg")
vector2 = engine.full_analysis("china_sun.jpg")

# 计算距离（天体类语义）
result = engine.calculate_homology_distance(
    vector1, vector2, SemanticType.CELESTIAL
)

print(f"距离: {result['distance']:.4f}")
print(f"相似度: {result['similarity']:.4f}")
print(f"解释: {result['interpretation']}")
```

### 示例2：检测文化传播信号

```python
from tools.tcd_origin_engine import CrossCivilizationAnalyzer

analyzer = CrossCivilizationAnalyzer()

# 创建两个符号
vector1 = engine.full_analysis("symbol1.jpg")
vector2 = engine.full_analysis("symbol2.jpg")

# 检测文化传播
result = analyzer.detect_cultural_transmission(
    vector1, vector2, SemanticType.CELESTIAL
)

print(f"传播信号: {result['transmission_signal']}")
print(f"环数差异: {result['ring_comparison']['difference']}")
print(f"解读: {result['interpretation']}")
```

### 示例3：完整分析流程

```python
from tools.tcd_origin_tools import tcd_full_analysis

# 执行D1-D5完整分析
result = tcd_full_analysis.invoke({
    "image_url": "ancient_symbol.jpg",
    "context": "祭祀场景",
    "origin_estimate": "甲骨文"
})

# 解析结果
import json
data = json.loads(result)
print(f"置信度: {data['layers']['D5_collapse']['confidence']}")
print(f"最终解释: {data['layers']['D5_collapse']['collapsed_meaning']}")
```

### 示例4：跨文明比较

```python
from tools.tcd_origin_tools import tcd_homology_distance

# 比较不同文明的符号
result = tcd_homology_distance.invoke({
    "symbol1_url": "https://example.com/mesopotamia.jpg",
    "symbol2_url": "https://example.com/china.jpg",
    "semantic_type": "器物类",
    "civilization1": "美索不达米亚",
    "civilization2": "中国"
})

data = json.loads(result)
print(f"同源性等级: {data['homology_level']}")
print(f"相似度: {data['similarity']:.4f}")
```

---

## 公式汇总表

| 公式名称 | 公式 | 用途 |
|---------|------|------|
| 拓扑同源性距离 | D(S_a, S_b) = Σ ω_i × \|T_i(a) - T_i(b)\| | 比较符号相似度 |
| 欧拉示性数 | χ = β₀ - β₁ + β₂ | 表征连通性 |
| 相似度转换 | similarity = 1 - distance | 距离转相似度 |
| 环数差异 | ring_diff = \|rings_a - rings_b\| | 文化传播检测 |
| 对称性相似度 | symmetry_sim = 1 - \|sym_a - sym_b\| | 结构比较 |
| 置信度计算 | confidence = max(softmax(scores)) | 最终解释 |
