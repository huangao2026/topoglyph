# 拓扑分析使用指南

本文档详细介绍如何使用古文字破译智能体中的拓扑特征分析功能。

---

## 📖 目录

1. [快速开始](#快速开始)
2. [核心概念](#核心概念)
3. [工具详解](#工具详解)
4. [使用示例](#使用示例)
5. [最佳实践](#最佳实践)
6. [常见问题](#常见问题)

---

## 🚀 快速开始

### 1. 基本查询

```python
from tools.cross_civilization_tools import extract_topology_features

# 分析单个符号
result = extract_topology_features.invoke({
    "image_url": "https://example.com/ancient_symbol.jpg",
    "symbol_name": "太阳符号"
})

print(result)
```

### 2. 同源性分析

```python
from tools.cross_civilization_tools import analyze_cross_civilization_homology

# 比较两个符号
result = analyze_cross_civilization_homology.invoke({
    "symbol1_url": "https://example.com/chinese_sun.jpg",
    "symbol2_url": "https://example.com/egypt_sun.jpg",
    "semantic_type": "天体类",
    "civilization1": "中国",
    "civilization2": "古埃及"
})

print(result)
```

---

## 🔬 核心概念

### 1. 三层拓扑不变量体系

#### 第一层：全局形态锚点特征（权重40%）

**对称性指数**：
- 水平对称度：符号左右对称程度
- 垂直对称度：符号上下对称程度
- 旋转对称度：符号旋转后的重合程度

**宽高比**：
- 符号外接矩形的宽度与高度之比
- 描述整体形态（横扁/竖长/方正）

#### 第二层：核心拓扑不变量（权重35%）

**欧拉示性数**：
```
χ = 连通分量数 - 环数
```

**贝蒂数序列**：
- β₀：连通分支数
- β₁：独立环数
- β₂：空腔数

#### 第三层：局部结构指纹（权重25%）

**环数分布**：
- 不同大小、位置的封闭区域
- 捕捉局部细节特征

**连通分量数**：
- 独立连通区域的数量
- 描述笔画离散程度

**像素密度**：
- 笔画像素占总像素的比例
- 反映符号繁简程度

### 2. 语义类型

|类型|代表概念|最优特征|特点|
|---|---|---|---|
|天体类|日、月、星|对称性|天然对称|
|自然类|山、水、火|宽高比|形态稳定|
|人体类|人、目、口|对称性+环数|既有对称又有器官|
|器物类|田、皿、弓|环数|封闭结构是核心|

### 3. 特征向量

**128维高维向量**：
```
T = [对称性指数×3, 宽高比, 欧拉示性数, 贝蒂数×3, 环数, 连通分量数, 像素密度, ...]
```

---

## 🛠️ 工具详解

### extract_topology_features

**功能**：提取古文字符号的完整拓扑特征

**参数**：
- `image_url`（必填）：符号图片URL
- `symbol_name`（可选）：符号名称

**返回**：
```json
{
  "status": "success",
  "symbol_name": "符号名称",
  "semantic_type": "语义类型",
  "features": {
    "global_features": {
      "horizontal_symmetry": 0.85,
      "vertical_symmetry": 0.90,
      "rotational_symmetry": 0.75,
      "aspect_ratio": 1.2
    },
    "core_invariants": {
      "euler_characteristic": 0,
      "betti_0": 1,
      "betti_1": 1,
      "betti_2": 0
    },
    "local_fingerprint": {
      "ring_distribution": [1, 0, 0],
      "connected_components": 1,
      "pixel_density": 0.45
    },
    "high_dim_vector": [0.85, 0.90, 0.75, 1.2, 0, 1, 1, 1, 1, 0.45, 0, ...]
  }
}
```

### analyze_cross_civilization_homology

**功能**：分析跨文明符号的同源性

**参数**：
- `symbol1_url`（必填）：第一个符号图片URL
- `symbol2_url`（必填）：第二个符号图片URL
- `semantic_type`（可选）：语义类型
- `civilization1`（可选）：第一个符号所属文明
- `civilization2`（可选）：第二个符号所属文明

**返回**：
```json
{
  "status": "success",
  "homology_level": "high",
  "weighted_similarity": 0.85,
  "semantic_type": "天体类",
  "base_similarity": 0.82,
  "interpretation": "拓扑相似度高，可能存在同源性",
  "transmission_analysis": {
    "ring_comparison": {
      "symbol1_rings": 1,
      "symbol2_rings": 1,
      "difference": 0
    },
    "symmetry_similarity": 0.85,
    "euler_match": true,
    "transmission_signal": "weak",
    "interpretation": "拓扑结构相似但环数相同..."
  },
  "feature_weights": {
    "primary": "symmetry",
    "secondary": "rings",
    "weights": {
      "symmetry": 1.0,
      "euler": 0.4,
      "rings": 0.6,
      "aspect_ratio": 0.3
    }
  }
}
```

### detect_cultural_transmission

**功能**：检测文化传播信号

**参数**：
- `symbol1_url`（必填）：第一个符号图片URL
- `symbol2_url`（必填）：第二个符号图片URL
- `semantic_type`（可选）：语义类型

**返回**：
```json
{
  "status": "success",
  "transmission_signal": "strong",
  "ring_comparison": {
    "symbol1_rings": 1,
    "symbol2_rings": 1,
    "difference": 0
  },
  "symmetry_similarity": 0.85,
  "euler_match": true,
  "interpretation": "环数一致性强，可能存在文化传播或符号借用"
}
```

### analyze_semantic_type_from_features

**功能**：根据已有特征分析语义类型

**参数**：
- `topology_features_json`（必填）：拓扑特征JSON字符串

**返回**：
```json
{
  "status": "success",
  "semantic_type": "天体类",
  "confidence": 0.85,
  "reasoning": "高旋转对称性和存在环状结构，符合天体类符号特征",
  "recommended_features": ["对称性指数", "环数分布"]
}
```

---

## 💡 使用示例

### 示例1：分析单个符号

```python
from tools.cross_civilization_tools import extract_topology_features

# 分析古埃及太阳神符号
result = extract_topology_features.invoke({
    "image_url": "https://example.com/ra.jpg",
    "symbol_name": "拉神符号"
})

# 解析结果
import json
data = json.loads(result)
print(f"语义类型: {data['semantic_type']}")
print(f"对称性: {data['features']['global_features']['rotational_symmetry']}")
```

### 示例2：比较两个符号

```python
from tools.cross_civilization_tools import analyze_cross_civilization_homology

# 比较中国和埃及的太阳符号
result = analyze_cross_civilization_homology.invoke({
    "symbol1_url": "https://example.com/chinese_sun.jpg",
    "symbol2_url": "https://example.com/egypt_sun.jpg",
    "semantic_type": "天体类",
    "civilization1": "中国",
    "civilization2": "古埃及"
})

# 解析结果
data = json.loads(result)
print(f"同源性等级: {data['homology_level']}")
print(f"相似度: {data['weighted_similarity']}")
print(f"文化传播信号: {data['transmission_analysis']['transmission_signal']}")
```

### 示例3：批量分析

```python
from tools.cross_civilization_tools import extract_topology_features

symbols = [
    {"url": "https://example.com/symbol1.jpg", "name": "符号1"},
    {"url": "https://example.com/symbol2.jpg", "name": "符号2"},
    {"url": "https://example.com/symbol3.jpg", "name": "符号3"},
]

results = []
for symbol in symbols:
    result = extract_topology_features.invoke({
        "image_url": symbol["url"],
        "symbol_name": symbol["name"]
    })
    results.append(result)
    print(f"✓ {symbol['name']} 分析完成")

print(f"\n总计分析了 {len(results)} 个符号")
```

---

## 🎯 最佳实践

### 1. 特征提取

- ✅ 使用清晰的符号图片（高分辨率、对比度好）
- ✅ 确保符号完整，不要截断
- ✅ 尽量使用PNG或JPG格式
- ❌ 不要使用过于模糊或变形的图片

### 2. 同源性分析

- ✅ 先确定语义类型，提高分析准确性
- ✅ 提供符号所属文明信息
- ✅ 结合知识库信息综合判断
- ❌ 不要仅凭单一特征下结论

### 3. 文化传播检测

- ✅ 关注环数的文化传播指示器作用
- ✅ 结合拓扑相似度综合判断
- ✅ 考虑历史背景和考古证据
- ❌ 不要将文化传播与同源性混淆

### 4. 结果解读

- ✅ 理解不同同源性等级的含义
- ✅ 参考置信度和权重配置
- ✅ 结合专业知识进行解读
- ❌ 不要过度解读统计结果

---

## ❓ 常见问题

### Q1: 特征提取失败怎么办？

**A**: 检查图片URL是否可访问，确保图片格式正确（PNG/JPG），尝试提高图片清晰度。

### Q2: 同源性分析结果不理想？

**A**: 
1. 确认语义类型是否正确
2. 检查特征提取是否完整
3. 参考特征权重配置调整
4. 结合历史背景综合判断

### Q3: 如何提高分析准确性？

**A**:
1. 使用高质量的图片
2. 正确指定语义类型
3. 提供充分的历史背景
4. 结合多个分析结果综合判断

### Q4: 128维特征向量有什么作用？

**A**: 128维高维特征向量用于：
1. 精确表示符号的完整拓扑特征
2. 支持向量相似度计算
3. 便于机器学习模型处理
4. 支持大规模符号数据库构建

### Q5: 环数的文化传播指示器作用是什么？

**A**: 环数是区分"独立起源"和"文化传播"的关键指标：
- 环数相同 + 拓扑相似 → 文化传播信号
- 环数不同 + 拓扑相似 → 独立起源认知趋同

---

## 📚 相关文档

- [专利技术升级文档](./PATENT_TECH_UPGRADE.md)
- [跨文明分析指南](./CROSS_CIVILIZATION_ANALYSIS.md)
- [增强版Agent代码](./src/agents/enhanced_agent.py)

---

## 🤝 反馈

如有问题或建议，请联系项目维护者。
