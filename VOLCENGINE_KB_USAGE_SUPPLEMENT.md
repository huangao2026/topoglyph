# 火山引擎知识库集成 - 使用调用补充

## ✨ 新增内容

为了更好地展示火山引擎知识库的完整调用方式，我补充了以下内容：

## 📁 新增文件

### 1. 完整示例代码

#### `examples/volcengine_kb_examples.py` - 10个详细示例
- 示例1: 简单的文本查询
- 示例2: 图文混合查询
- 示例3: 带上下文的查询
- 示例4: 多轮对话
- 示例5: 对比分析查询
- 示例6: 研究助手模式
- 示例7: 教育辅导模式
- 示例8: 错误处理
- 示例9: 批量处理
- 示例10: 自定义参数

#### `examples/quick_start_volcengine.py` - 快速开始
- 最简单的3步上手示例
- 适合新手快速入门

#### `examples/ancient_text_agent_scenarios.py` - 实际应用场景
- 场景1: 文本分析
- 场景2: 图片分析
- 场景3: 研究助手
- 场景4: AI工具推荐
- 场景5: 综合分析

#### `src/agents/agent_with_volcengine_kb.py` - Agent集成示例
- 完整的Agent构建代码
- 工具包装示例
- 配置文件示例
- 使用说明

### 2. 文档

#### `examples/README.md` - 示例文档
- 快速开始指南
- 使用提示
- 应用场景说明
- 常见问题

#### `AGENT_CONFIG_WITH_VOLCENGINE_KB.md` - Agent配置示例
- 配置文件详解
- 不同场景的System Prompt
- 工具说明
- 最佳实践

#### `VOLCENGINE_KB_INTEGRATION_COMPLETE.md` - 集成完成指南
- 快速开始
- 主要功能
- 应用场景
- 常见问题

#### `VOLCENGINE_KB_CHANGES_SUMMARY.md` - 变更总结
- 集成概述
- 已完成工作
- 代码统计
- 功能特性

## 🚀 快速开始

### 1. 配置环境变量

```bash
# 编辑.env文件
vim .env

# 添加以下配置
VOLCENGINE_API_KEY=your_api_key_here
VOLCENGINE_SERVICE_ID=your_service_id_here
```

### 2. 运行快速开始示例

```bash
python examples/quick_start_volcengine.py
```

### 3. 运行完整示例集

```bash
python examples/volcengine_kb_examples.py
```

### 4. 运行应用场景

```bash
python examples/ancient_text_agent_scenarios.py
```

## 💡 使用示例

### 示例1: 简单查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

result = search_volcengine_knowledge("什么是甲骨文？")
print(result)
```

### 示例2: 图文查询

```python
result = search_volcengine_knowledge(
    query="图片中是什么古文字？",
    image_url="https://example.com/hieroglyphs.jpg"
)
print(result)
```

### 示例3: 带上下文查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge_with_context

result = search_volcengine_knowledge_with_context(
    query="如何判断书写方向？",
    context="用户正在研究古埃及象形文字..."
)
print(result)
```

### 示例4: 多轮对话

```python
from tools.volcengine_knowledge import multi_round_knowledge_chat

messages = [
    {"role": "user", "content": "什么是楔形文字？"},
    {"role": "assistant", "content": "楔形文字是..."}
]

result = multi_round_knowledge_chat(messages)
print(result)
```

## 🎯 应用场景

### 场景1: 学术研究

```python
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
result = search_volcengine_knowledge(
    "用通俗易懂的语言介绍什么是甲骨文，适合初中生理解"
)
```

### 场景3: 图片识别

```python
result = search_volcengine_knowledge(
    query="请详细分析图片中的古文字",
    image_url="https://example.com/hieroglyphs.png"
)
```

### 场景4: 工具推荐

```python
result = search_volcengine_knowledge("""
用户需要识别甲骨文图片，要求：
1. 学术级精度
2. 免费使用
3. 支持批量处理

请推荐合适的AI工具
""")
```

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| [集成指南](./VOLCENGINE_KNOWLEDGE_INTEGRATION.md) | 如何集成火山引擎知识库 |
| [使用指南](./VOLCENGINE_KNOWLEDGE_USAGE.md) | 详细使用说明 |
| [配置示例](./AGENT_CONFIG_WITH_VOLCENGINE_KB.md) | Agent配置详解 |
| [完成指南](./VOLCENGINE_KB_INTEGRATION_COMPLETE.md) | 集成完成后的使用指南 |
| [变更总结](./VOLCENGINE_KB_CHANGES_SUMMARY.md) | 本次集成的详细变更 |
| [示例文档](./examples/README.md) | 示例代码说明 |

## 🔗 相关文件

### 核心代码
- `src/tools/volcengine_knowledge.py` - 工具实现
- `src/agents/agent_with_volcengine_kb.py` - Agent集成
- `scripts/test_volcengine_kb.py` - 测试脚本

### 示例代码
- `examples/quick_start_volcengine.py` - 快速开始
- `examples/volcengine_kb_examples.py` - 完整示例集
- `examples/ancient_text_agent_scenarios.py` - 应用场景

## ⚡ 特性亮点

### 1. 完整的错误处理
- 配置检查
- API调用错误处理
- 超时处理
- 友好的错误提示

### 2. 详细的类型提示
- 完整的类型注解
- 类型安全

### 3. 丰富的示例
- 10个详细示例
- 5个应用场景
- 快速开始示例

### 4. 完善的文档
- 集成指南
- 使用指南
- 配置示例
- FAQ

### 5. 灵活的配置
- 环境变量配置
- 可自定义参数
- 支持多种查询方式

## 🎉 开始使用

现在您已经有了完整的调用示例，可以开始使用火山引擎知识库了！

推荐的学习路径：

1. **快速入门**: 运行 `examples/quick_start_volcengine.py`
2. **深入学习**: 阅读 `VOLCENGINE_KNOWLEDGE_USAGE.md`
3. **实践应用**: 查看 `examples/volcengine_kb_examples.py`
4. **场景应用**: 运行 `examples/ancient_text_agent_scenarios.py`

祝您使用愉快！🚀
