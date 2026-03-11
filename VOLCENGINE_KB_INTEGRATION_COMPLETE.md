# 火山引擎知识库集成完成指南

## ✅ 集成完成

火山引擎知识库已成功集成到古文字破译智能体项目中！

## 📦 已创建的文件

### 1. 核心代码
- `src/tools/volcengine_knowledge.py` - 火山引擎知识库工具实现
- `src/agents/agent_with_volcengine_kb.py` - 集成知识库的Agent代码
- `scripts/test_volcengine_kb.py` - 测试脚本

### 2. 示例代码
- `examples/quick_start_volcengine.py` - 快速开始示例
- `examples/volcengine_kb_examples.py` - 完整示例集（10个示例）
- `examples/ancient_text_agent_scenarios.py` - 实际应用场景

### 3. 文档
- `VOLCENGINE_KNOWLEDGE_INTEGRATION.md` - 集成指南
- `VOLCENGINE_KNOWLEDGE_USAGE.md` - 使用指南
- `AGENT_CONFIG_WITH_VOLCENGINE_KB.md` - Agent配置示例
- `examples/README.md` - 示例文档

### 4. 配置更新
- `.env.example` - 添加了火山引擎知识库配置项
- `src/tools/__init__.py` - 导出火山引擎知识库工具

## 🚀 快速开始

### 步骤1: 配置环境变量

```bash
# 编辑.env文件
vim .env

# 添加以下配置
VOLCENGINE_API_KEY=your_api_key_here
VOLCENGINE_SERVICE_ID=your_service_id_here
```

### 步骤2: 运行测试

```bash
# 测试火山引擎知识库连接
python scripts/test_volcengine_kb.py
```

### 步骤3: 运行示例

```bash
# 快速开始
python examples/quick_start_volcengine.py

# 完整示例集
python examples/volcengine_kb_examples.py

# 实际应用场景
python examples/ancient_text_agent_scenarios.py
```

### 步骤4: 配置Agent

编辑 `config/agent_llm_config.json`:

```json
{
    "config": {
        "model": "doubao-pro-32k-241215",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 10000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "你是古文字破译专家助手，拥有专业的知识库...",
    "tools": [
        "knowledge_search",
        "knowledge_search_with_context",
        "knowledge_chat"
    ]
}
```

## 🎯 主要功能

### 1. 知识库查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

# 简单查询
result = search_volcengine_knowledge("什么是甲骨文？")
print(result)
```

### 2. 图文混合查询

```python
# 图文查询
result = search_volcengine_knowledge(
    query="图片中是什么古文字？",
    image_url="https://example.com/hieroglyphs.jpg"
)
print(result)
```

### 3. 带上下文查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge_with_context

# 带上下文查询
result = search_volcengine_knowledge_with_context(
    query="如何判断书写方向？",
    context="用户正在研究古埃及象形文字..."
)
print(result)
```

### 4. 多轮对话

```python
from tools.volcengine_knowledge import multi_round_knowledge_chat

# 多轮对话
messages = [
    {"role": "user", "content": "什么是楔形文字？"},
    {"role": "assistant", "content": "楔形文字是..."}
]

result = multi_round_knowledge_chat(messages)
print(result)
```

## 📚 文档导航

- [集成指南](./VOLCENGINE_KNOWLEDGE_INTEGRATION.md) - 如何集成火山引擎知识库
- [使用指南](./VOLCENGINE_KNOWLEDGE_USAGE.md) - 详细使用说明
- [配置示例](./AGENT_CONFIG_WITH_VOLCENGINE_KB.md) - Agent配置详解
- [示例文档](./examples/README.md) - 示例代码说明

## 🎨 应用场景

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

### 修改API参数

```python
from tools.volcengine_knowledge import VolcengineKnowledgeConfig

# 修改超时时间
VolcengineKnowledgeConfig.TIMEOUT = 60

# 修改最大返回字符数
VolcengineKnowledgeConfig.MAX_CHAR_COUNT = 3000

# 修改API版本
VolcengineKnowledgeConfig.API_VERSION = "2024-08-01"
```

## ⚠️ 注意事项

1. **环境变量**: 必须正确配置 `VOLCENGINE_API_KEY` 和 `VOLCENGINE_SERVICE_ID`
2. **网络访问**: 确保服务器可以访问火山引擎API
3. **错误处理**: 代码已包含完整的错误处理，遇到问题会返回友好提示
4. **API限制**: 注意火山引擎API的调用频率限制

## 🐛 常见问题

### 问题1: 配置未找到

**错误**: `错误: 火山引擎知识库未配置`

**解决**: 检查环境变量配置

```bash
echo $VOLCENGINE_API_KEY
echo $VOLCENGINE_SERVICE_ID
```

### 问题2: API调用失败

**错误**: `错误: 调用火山引擎知识库失败`

**解决**:
- 检查API Key是否正确
- 检查Service ID是否有效
- 检查网络连接

### 问题3: 查询超时

**错误**: 查询时间过长

**解决**: 增加超时时间配置

```python
VolcengineKnowledgeConfig.TIMEOUT = 60
```

## 📞 获取帮助

如果遇到问题：

1. 查看文档:
   - [集成指南](./VOLCENGINE_KNOWLEDGE_INTEGRATION.md)
   - [使用指南](./VOLCENGINE_KNOWLEDGE_USAGE.md)
   - [FAQ](#常见问题)

2. 查看示例:
   - [快速开始](./examples/quick_start_volcengine.py)
   - [完整示例集](./examples/volcengine_kb_examples.py)

3. 运行测试:
   ```bash
   python scripts/test_volcengine_kb.py
   ```

## 🎉 开始使用

现在您已经了解了火山引擎知识库的集成情况，可以开始使用了！

推荐的学习路径：

1. **快速入门**: 运行 `examples/quick_start_volcengine.py`
2. **深入学习**: 阅读 `VOLCENGINE_KNOWLEDGE_USAGE.md`
3. **实践应用**: 查看 `examples/volcengine_kb_examples.py`
4. **场景应用**: 运行 `examples/ancient_text_agent_scenarios.py`

祝您使用愉快！🚀
