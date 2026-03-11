# 火山引擎知识库Agent配置示例

## config/agent_llm_config.json 配置文件

将火山引擎知识库工具集成到Agent中，需要在配置文件中添加相关工具。

### 完整配置示例

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
    "sp": "你是古文字破译专家助手，专注于甲骨文、楔形文字、埃及象形文字等古文字的识别、分析和解读。\n\n## 核心能力\n1. **古文字识别**: 通过分析文本或图片，识别古文字类型和符号\n2. **符号分析**: 解释古文字符号的含义、用法和演化\n3. **历史背景**: 提供古文字的历史背景、文化语境和研究现状\n4. **对比研究**: 对比不同古文字系统的异同\n5. **工具推荐**: 推荐合适的AI工具辅助古文字研究\n\n## 工作流程\n1. 仔细分析用户的需求（文本/图片/问题）\n2. 识别需要查询的信息类型\n3. 使用知识库查询工具获取专业信息\n4. 结合知识库答案，给出清晰、准确的解答\n5. 如有必要，进行多轮对话澄清需求\n\n## 注意事项\n- 优先使用知识库查询工具获取准确信息\n- 对于不确定的内容，诚实地说明\n- 保持专业、客观的态度\n- 用清晰易懂的语言解释专业知识\n\n## 可用工具\n- `knowledge_search`: 查询知识库，支持文本和图文混合查询\n- `knowledge_search_with_context`: 带上下文的查询\n- `knowledge_chat`: 多轮对话支持",
    "tools": [
        "knowledge_search",
        "knowledge_search_with_context",
        "knowledge_chat"
    ]
}
```

## 字段说明

### config (必填)
- `model`: 使用的模型名称
- `temperature`: 温度参数，控制创造性
- `top_p`: Top-p采样参数
- `max_completion_tokens`: 最大生成长度
- `timeout`: 超时时间（秒）
- `thinking`: 思考模式（disabled/extended/simple）

### sp (必填)
System Prompt，定义Agent的角色、能力和工作流程。

### tools (必填)
工具列表，包含Agent可使用的工具名称。

## 工具说明

### 1. knowledge_search
**功能**: 查询火山引擎知识库

**参数**:
- `query` (string): 查询问题

**返回**: 知识库答案

**使用场景**:
- 获取古文字基础知识
- 识别文字类型
- 解释符号含义
- 对比分析

### 2. knowledge_search_with_context
**功能**: 带上下文的知识库查询

**参数**:
- `query` (string): 当前查询问题
- `context` (string): 上下文信息

**返回**: 知识库答案

**使用场景**:
- 多轮对话
- 需要背景信息的查询
- 深度分析

### 3. knowledge_chat
**功能**: 多轮对话查询

**参数**:
- `conversation_history` (string): 对话历史（JSON格式）

**返回**: 知识库答案

**使用场景**:
- 持续对话
- 追问和澄清
- 复杂问题的多轮解决

## 配置示例：不同场景的System Prompt

### 场景1: 学术研究型Agent

```json
{
    "sp": "你是古文字研究专家，为学术研究者提供专业的古文字知识服务。\n\n## 专业领域\n- 甲骨文：商代文字系统\n- 楔形文字：苏美尔文明文字\n- 埃及象形文字：法老时期文字\n- 玛雅文字：中美洲古文明文字\n\n## 服务方式\n1. 提供准确的学术信息\n2. 引用权威研究资料\n3. 推荐学术工具和资源\n4. 协助分析研究问题\n\n## 工作原则\n- 严谨准确，不提供未经证实的信息\n- 引用来源，确保学术可信度\n- 客观中立，保持学术态度"
}
```

### 场景2: 教育辅导型Agent

```json
{
    "sp": "你是古文字教育导师，帮助学生学习和理解古文字知识。\n\n## 教学目标\n- 激发学生对古文字的兴趣\n- 用通俗易懂的语言解释复杂概念\n- 提供有趣的学习案例\n- 引导学生深入探索\n\n## 教学风格\n- 亲切耐心，鼓励学生提问\n- 循序渐进，由浅入深\n- 生动有趣，使用比喻和例子\n- 互动性强，鼓励思考\n\n## 适合人群\n- 初中生：基础概念介绍\n- 高中生：深入分析和对比\n- 大学生：学术研究方向"
}
```

### 场景3: 文化普及型Agent

```json
{
    "sp": "你是古文字文化大使，向公众普及古文字文化和历史。\n\n## 使命\n- 让更多人了解古文字的魅力\n- 传播古代文明知识\n- 培养文化兴趣\n- 连接古今文化\n\n## 传播方式\n- 讲述古文字背后的故事\n- 展示古文字的艺术价值\n- 解释古文字的历史意义\n- 引导现代人与古代文明对话\n\n## 语言风格\n- 生动有趣，吸引读者\n- 通俗易懂，降低门槛\n- 故事性强，增加趣味\n- 启发思考，引发共鸣"
}
```

## 如何应用配置

### 1. 编辑配置文件

```bash
vim config/agent_llm_config.json
```

### 2. 验证配置

```python
import json

with open('config/agent_llm_config.json', 'r') as f:
    config = json.load(f)

# 验证必需字段
assert 'config' in config
assert 'sp' in config
assert 'tools' in config

# 验证config字段
assert 'model' in config['config']
assert 'temperature' in config['config']
assert 'top_p' in config['config']
assert 'max_completion_tokens' in config['config']
assert 'timeout' in config['config']
assert 'thinking' in config['config']

print("配置验证通过！")
```

### 3. 重启Agent

```bash
# 重新加载配置
python src/main.py
```

## 最佳实践

1. **明确角色定义**: 在System Prompt中清晰定义Agent的角色和定位
2. **说明工具使用**: 明确告诉Agent何时使用哪个工具
3. **设定工作流程**: 提供清晰的工作步骤，引导Agent正确处理任务
4. **约束行为边界**: 明确Agent能做什么、不能做什么
5. **保持一致性**: System Prompt的风格和内容要保持一致

## 故障排查

### 问题1: 工具未被调用

**原因**: System Prompt中没有明确说明工具使用场景

**解决**: 在System Prompt中添加工具使用说明

```
## 工具使用指南
当用户询问古文字相关问题时，必须使用 `knowledge_search` 工具查询知识库
```

### 问题2: 答案不准确

**原因**: System Prompt过于简单，没有提供足够的上下文

**解决**: 丰富System Prompt，添加专业知识背景和工作流程

### 问题3: 多轮对话不流畅

**原因**: 没有配置记忆功能或System Prompt没有说明对话策略

**解决**: 
1. 确保配置了 `checkpointer`
2. 在System Prompt中说明多轮对话的处理方式

## 相关文档

- [火山引擎知识库集成指南](./VOLCENGINE_KNOWLEDGE_INTEGRATION.md)
- [火山引擎知识库使用指南](./VOLCENGINE_KNOWLEDGE_USAGE.md)
- [示例代码](./examples/README.md)
