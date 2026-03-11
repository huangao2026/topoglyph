# 火山引擎知识库使用示例

本目录包含火山引擎知识库API的完整使用示例，帮助您快速上手。

## 📁 文件说明

### 1. `quick_start_volcengine.py` - 快速开始
最简单的使用方式，3步上手火山引擎知识库。

```bash
python examples/quick_start_volcengine.py
```

**功能**：
- 配置检查
- 单次查询示例

### 2. `volcengine_kb_examples.py` - 完整示例集
包含10个详细的使用示例，覆盖所有API功能。

```bash
python examples/volcengine_kb_examples.py
```

**示例内容**：
1. 简单的文本查询
2. 图文混合查询
3. 带上下文的查询
4. 多轮对话
5. 对比分析查询
6. 研究助手模式
7. 教育辅导模式
8. 错误处理
9. 批量处理
10. 自定义参数

### 3. `ancient_text_agent_scenarios.py` - 实际应用场景
展示如何在古文字破译系统中使用火山引擎知识库。

```bash
python examples/ancient_text_agent_scenarios.py
```

**场景内容**：
1. 文本分析
2. 图片分析
3. 研究助手
4. AI工具推荐
5. 综合分析

## 🚀 快速开始

### 步骤1: 配置环境变量

在运行示例前，需要先配置火山引擎知识库的环境变量：

```bash
# Linux/Mac
export VOLCENGINE_API_KEY='your_api_key_here'
export VOLCENGINE_SERVICE_ID='your_service_id_here'

# Windows (PowerShell)
$env:VOLCENGINE_API_KEY='your_api_key_here'
$env:VOLCENGINE_SERVICE_ID='your_service_id_here'
```

或者在 `.env` 文件中添加：

```env
VOLCENGINE_API_KEY=your_api_key_here
VOLCENGINE_SERVICE_ID=your_service_id_here
```

### 步骤2: 选择示例

选择一个示例运行：

```bash
# 快速开始（推荐新手）
python examples/quick_start_volcengine.py

# 完整示例集
python examples/volcengine_kb_examples.py

# 实际应用场景
python examples/ancient_text_agent_scenarios.py
```

## 💡 使用提示

### 基础查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

# 简单查询
result = search_volcengine_knowledge("什么是甲骨文？")
print(result)
```

### 图文混合查询

```python
# 图文查询
result = search_volcengine_knowledge(
    query="图片中是什么古文字？",
    image_url="https://example.com/ancient-text.jpg"
)
print(result)
```

### 多轮对话

```python
from tools.volcengine_knowledge import multi_round_knowledge_chat

# 对话历史
messages = [
    {"role": "user", "content": "什么是楔形文字？"},
    {"role": "assistant", "content": "楔形文字是..."}
]

# 追问
result = multi_round_knowledge_chat(messages)
print(result)
```

### 带上下文的查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge_with_context

# 上下文
context = "用户正在研究古埃及象形文字..."

# 查询
result = search_volcengine_knowledge_with_context(
    query="如何判断书写方向？",
    context=context
)
print(result)
```

## 🎯 应用场景

### 场景1: 学术研究

```python
# 查询学术信息
result = search_volcengine_knowledge("""
请对比分析甲骨文和楔形文字的：
1. 起源时间和地点
2. 载体材料
3. 符号系统特点
4. 破译历史
""")
```

### 场景2: 教育辅导

```python
# 适合初中生的解释
result = search_volcengine_knowledge(
    "用通俗易懂的语言介绍什么是甲骨文，适合初中生理解"
)
```

### 场景3: 图片识别

```python
# 识别图片中的古文字
result = search_volcengine_knowledge(
    query="请详细分析图片中的古文字",
    image_url="https://example.com/hieroglyphs.png"
)
```

### 场景4: 工具推荐

```python
# 获取AI工具推荐
result = search_volcengine_knowledge("""
用户需要识别甲骨文图片，要求：
1. 学术级精度
2. 免费使用
3. 支持批量处理

请推荐合适的AI工具
""")
```

## 🔧 自定义配置

您可以通过修改 `src/tools/volcengine_knowledge.py` 中的配置来自定义API行为：

```python
class VolcengineKnowledgeConfig:
    # API域名
    DOMAIN = "ark.cn-beijing.volces.com"
    
    # 请求超时时间（秒）
    TIMEOUT = 30
    
    # 每次返回的最大字符数
    MAX_CHAR_COUNT = 2000
    
    # API版本
    API_VERSION = "2024-07-01"
```

## ❓ 常见问题

### 1. 配置未找到

**问题**：`错误: 火山引擎知识库未配置`

**解决**：检查环境变量是否正确配置

```bash
echo $VOLCENGINE_API_KEY
echo $VOLCENGINE_SERVICE_ID
```

### 2. API调用失败

**问题**：`错误: 调用火山引擎知识库失败`

**解决**：
- 检查API Key是否正确
- 检查网络连接
- 检查Service ID是否有效

### 3. 查询超时

**问题**：查询时间过长

**解决**：增加超时时间配置

```python
VolcengineKnowledgeConfig.TIMEOUT = 60  # 60秒
```

## 📚 相关文档

- [火山引擎知识库集成指南](./VOLCENGINE_KNOWLEDGE_INTEGRATION.md)
- [火山引擎知识库使用指南](./VOLCENGINE_KNOWLEDGE_USAGE.md)
- [项目README](./README.md)

## 🤝 反馈

如有问题或建议，请联系项目维护者。
