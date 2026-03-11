# 火山引擎知识库工具使用指南

## 概述

本工具集提供了与火山引擎知识库服务集成的功能，支持纯文本查询、图文混合查询、多轮对话等功能。

---

## 快速开始

### 1. 配置环境变量

编辑 `.env` 文件，添加以下配置：

```bash
# 火山引擎知识库配置
VOLCENGINE_ACCOUNT_ID=your_account_id_here
VOLCENGINE_API_KEY=your_volcengine_api_key_here
VOLCENGINE_KB_DOMAIN=api-knowledgebase.mlp.cn-beijing.volces.com
VOLCENGINE_SERVICE_ID=kb-service-14ae584a2d80c3f9
```

### 2. 获取凭证

1. 访问火山引擎控制台：https://console.volcengine.com/
2. 创建知识库服务
3. 获取：
   - Account ID
   - API Key
   - Service Resource ID

### 3. 测试配置

```bash
# 运行测试脚本
python scripts/test_volcengine_kb.py
```

---

## 工具列表

### 1. search_volcengine_knowledge

**功能**: 纯文本或图文混合查询

**参数**:
- `query` (str): 查询文本
- `image_url` (str, optional): 图片URL

**返回**: 知识库搜索结果

**示例**:
```python
from tools.volcengine_knowledge import search_volcengine_knowledge

# 纯文本查询
result = search_volcengine_knowledge("埃及象形文字荷鲁斯的含义")
print(result)

# 图文查询
result = search_volcengine_knowledge(
    query="这是什么古文字？",
    image_url="https://example.com/ancient_text.jpg"
)
print(result)
```

---

### 2. search_volcengine_knowledge_with_context

**功能**: 带上下文的查询

**参数**:
- `query` (str): 查询文本
- `context` (str, optional): 上下文信息

**返回**: 知识库搜索结果

**示例**:
```python
from tools.volcengine_knowledge import search_volcengine_knowledge_with_context

result = search_volcengine_knowledge_with_context(
    query="这个符号代表什么？",
    context="用户正在研究古埃及象形文字，特别是关于神祇的符号"
)
print(result)
```

---

### 3. multi_round_knowledge_chat

**功能**: 多轮对话

**参数**:
- `messages` (List[Dict]): 对话消息列表

**返回**: 知识库回答

**示例**:
```python
from tools.volcengine_knowledge import multi_round_knowledge_chat

messages = [
    {"role": "user", "content": "什么是甲骨文？"},
    {"role": "assistant", "content": "甲骨文是中国商代的文字..."},
    {"role": "user", "content": "它有什么特点？"}
]

result = multi_round_knowledge_chat(messages)
print(result)
```

---

## 集成到Agent

### 步骤1: 注册工具

编辑 `src/agents/agent.py`:

```python
from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat
)

def build_agent(ctx=None):
    # ... 现有代码 ...
    
    tools = [
        search_volcengine_knowledge,
        search_volcengine_knowledge_with_context,
        multi_round_knowledge_chat,
        # ... 其他工具 ...
    ]
    
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
```

### 步骤2: 更新配置

编辑 `config/agent_llm_config.json`:

```json
{
  "config": {
    "model": "kimi-k2-5-260127",
    "temperature": 0.6,
    "top_p": 0.9,
    "max_completion_tokens": 32768,
    "timeout": 600,
    "thinking": "disabled"
  },
  "sp": "# 角色定义\n你是古代文字破解专家...\n\n# 工具说明\n你有以下工具可用：\n- search_volcengine_knowledge: 搜索火山引擎知识库\n- search_volcengine_knowledge_with_context: 带上下文的搜索\n- multi_round_knowledge_chat: 多轮对话\n\n# 使用指南\n当用户询问古文字相关知识时，优先使用火山引擎知识库工具查询...",
  "tools": [
    "search_volcengine_knowledge",
    "search_volcengine_knowledge_with_context",
    "multi_round_knowledge_chat"
  ]
}
```

---

## 使用场景

### 场景1: 用户提问

```
用户: 什么是甲骨文？

Agent调用: search_volcengine_knowledge("什么是甲骨文？")

知识库返回: 甲骨文是中国商代晚期（约公元前1600-1046年）的文字...
```

### 场景2: 图文识别

```
用户上传图片: [古文字图片.jpg]

用户: 这是什么古文字？

Agent调用: search_volcengine_knowledge(
    query="这是什么古文字？",
    image_url="https://.../image.jpg"
)

知识库返回: 这是古埃及象形文字，符号表示...
```

### 场景3: 多轮对话

```
用户: 什么是甲骨文？

Agent: [调用知识库] 甲骨文是...

用户: 它有什么特点？

Agent: [调用多轮对话] 甲骨文有以下特点...
```

---

## 错误处理

### 常见错误

1. **未配置错误**
   ```
   火山引擎知识库未配置，请设置环境变量
   ```
   解决：配置 `.env` 文件中的环境变量

2. **连接超时**
   ```
   知识库查询超时，请稍后重试
   ```
   解决：检查网络连接，增加超时时间

3. **连接错误**
   ```
   无法连接到知识库服务，请检查网络连接
   ```
   解决：检查网络和域名配置

### 错误处理示例

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

try:
    result = search_volcengine_knowledge("测试查询")
    if "错误" in result or "未配置" in result:
        # 处理错误
        print("查询失败")
    else:
        # 处理成功结果
        print(result)
except Exception as e:
    print(f"异常: {e}")
```

---

## 性能优化

### 1. 缓存

```python
from functools import lru_cache
from tools.volcengine_knowledge import search_volcengine_knowledge

@lru_cache(maxsize=100)
def cached_search(query):
    """带缓存的搜索"""
    return search_volcengine_knowledge(query)
```

### 2. 异步调用

```python
import asyncio
from tools.volcengine_knowledge import search_volcengine_knowledge

async def async_search(query):
    """异步搜索"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, search_volcengine_knowledge, query)
    return result
```

### 3. 批量查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

def batch_search(queries):
    """批量查询"""
    results = []
    for query in queries:
        result = search_volcengine_knowledge(query)
        results.append(result)
    return results

# 使用
queries = ["甲骨文", "楔形文字", "埃及象形文字"]
results = batch_search(queries)
```

---

## 监控和日志

### 监控指标

- API调用次数
- 响应时间
- 错误率
- 成功率

### 日志记录

```python
import logging
from tools.volcengine_knowledge import search_volcengine_knowledge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    result = search_volcengine_knowledge("测试")
    logger.info(f"查询成功: {len(result)} 字符")
except Exception as e:
    logger.error(f"查询失败: {e}")
```

---

## 成本控制

### 1. 监控用量

```python
import time
from collections import defaultdict

class VolcengineKBMetrics:
    def __init__(self):
        self.call_count = 0
        self.total_time = 0
        self.errors = 0
    
    def record_call(self, duration, success):
        self.call_count += 1
        self.total_time += duration
        if not success:
            self.errors += 1
    
    def get_stats(self):
        return {
            "call_count": self.call_count,
            "avg_time": self.total_time / self.call_count if self.call_count > 0 else 0,
            "error_rate": self.errors / self.call_count if self.call_count > 0 else 0
        }

# 使用
metrics = VolcengineKBMetrics()
start = time.time()
result = search_volcengine_knowledge("测试")
duration = time.time() - start
metrics.record_call(duration, "错误" not in result)
print(metrics.get_stats())
```

### 2. 限流

```python
from functools import wraps
import time

def rate_limit(calls_per_minute=60):
    """限流装饰器"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 移除1分钟前的调用记录
            calls[:] = [c for c in calls if now - c < 60]
            
            if len(calls) >= calls_per_minute:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# 使用
@rate_limit(calls_per_minute=60)
def limited_search(query):
    return search_volcengine_knowledge(query)
```

---

## 故障排查

### 问题1: 配置未生效

**检查**:
```bash
# 检查环境变量
env | grep VOLCENGINE

# 检查.env文件
cat .env | grep VOLCENGINE
```

**解决**: 确保环境变量正确设置

### 问题2: 无法连接

**检查**:
```bash
# 测试网络连接
ping api-knowledgebase.mlp.cn-beijing.volces.com

# 测试API
curl -X POST http://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/service/chat
```

**解决**: 检查网络和防火墙设置

### 问题3: 返回错误

**检查**:
```bash
# 查看详细日志
tail -f /app/work/logs/bypass/app.log

# 查看API返回
python -c "from tools.volcengine_knowledge import search_volcengine_knowledge; print(search_volcengine_knowledge('测试'))"
```

**解决**: 查看错误信息，检查配置

---

## 相关文档

- [火山引擎知识库API文档](https://www.volcengine.com/docs/82379)
- [集成指南](VOLCENGINE_KNOWLEDGE_INTEGRATION.md)
- [工具测试](scripts/test_volcengine_kb.py)
- [配置示例](.env.example)

---

## 联系支持

如需帮助，请访问：
- 火山引擎控制台：https://console.volcengine.com/
- 技术支持：https://www.volcengine.com/docs/
- 问题反馈：提交Issue

---

**最后更新**: 2026年3月5日
