# 火山引擎知识库API集成指南

## 代码解析

这段代码展示了如何调用火山引擎（字节跳动）的知识库服务API。

### 主要组件

1. **认证系统**：使用SignerV4进行签名认证
2. **API端点**：`api-knowledgebase.mlp.cn-beijing.volces.com`
3. **接口路径**：`/api/knowledge/service/chat`
4. **查询类型**：支持纯文本和图文混合查询

---

## 配置说明

### 必需参数

```python
account_id = "your accountid"        # 火山引擎账号ID
apikey = "your apikey"               # API密钥
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"
service_resource_id = "kb-service-14ae584a2d80c3f9"  # 知识库服务ID
```

### 获取凭证

1. **访问火山引擎控制台**：https://console.volcengine.com/
2. **创建项目**：选择"知识库服务"
3. **获取凭证**：
   - Account ID
   - API Key
   - Service Resource ID（知识库服务ID）

---

## 集成到古文字破译系统

### 方案一：创建知识库工具

在 `src/tools/` 目录下创建新工具：

```python
# src/tools/volcengine_knowledge.py

import json
import os
import requests
from typing import Optional, Dict, Any, List
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context

class VolcengineKnowledgeConfig:
    """火山引擎知识库配置"""
    
    # 从环境变量读取配置
    ACCOUNT_ID = os.getenv("VOLCENGINE_ACCOUNT_ID", "")
    API_KEY = os.getenv("VOLCENGINE_API_KEY", "")
    DOMAIN = os.getenv("VOLCENGINE_KB_DOMAIN", "api-knowledgebase.mlp.cn-beijing.volces.com")
    SERVICE_RESOURCE_ID = os.getenv("VOLCENGINE_SERVICE_ID", "kb-service-14ae584a2d80c3f9")


def prepare_request(method: str, path: str, params: Optional[Dict] = None,
                   data: Optional[Dict] = None, doseq: bool = 0):
    """准备HTTP请求"""
    if params:
        for key in params:
            if isinstance(params[key], (int, float, bool)):
                params[key] = str(params[key])
            elif isinstance(params[key], list) and not doseq:
                params[key] = ",".join(params[key])
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": VolcengineKnowledgeConfig.DOMAIN,
        "Authorization": f'Bearer {VolcengineKnowledgeConfig.API_KEY}'
    }
    
    return {
        "method": method,
        "url": f"http://{VolcengineKnowledgeConfig.DOMAIN}{path}",
        "headers": headers,
        "params": params,
        "body": json.dumps(data) if data else None
    }


@tool
def search_volcengine_knowledge(
    query: str,
    image_url: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    搜索火山引擎知识库
    
    Args:
        query: 查询文本
        image_url: 图片URL（可选，用于图文查询）
        runtime: 工具运行时上下文
    
    Returns:
        搜索结果
    """
    try:
        # 准备查询内容
        if image_url:
            content = [
                {"text": query, "type": "text"},
                {"image_url": {"url": image_url}, "type": "image_url"}
            ]
        else:
            content = query
        
        # 准备请求
        request_data = {
            "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
            "messages": [
                {"role": "user", "content": content}
            ],
            "stream": False
        }
        
        # 发送请求
        req = prepare_request(
            method="POST",
            path="/api/knowledge/service/chat",
            data=request_data
        )
        
        response = requests.post(
            url=req["url"],
            headers=req["headers"],
            data=req["body"],
            timeout=30
        )
        
        response.encoding = "utf-8"
        result = response.json()
        
        # 解析结果
        if "answer" in result:
            return f"知识库回答: {result['answer']}"
        elif "message" in result:
            return f"知识库消息: {result['message']}"
        else:
            return f"知识库响应: {json.dumps(result, ensure_ascii=False, indent=2)}"
            
    except Exception as e:
        return f"搜索知识库时出错: {str(e)}"


@tool
def search_volcengine_knowledge_with_context(
    query: str,
    context: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    带上下文的知识库搜索
    
    Args:
        query: 查询文本
        context: 上下文信息（可选）
        runtime: 工具运行时上下文
    
    Returns:
        搜索结果
    """
    try:
        # 准备查询内容
        if context:
            full_query = f"上下文: {context}\n\n问题: {query}"
        else:
            full_query = query
        
        # 准备请求
        request_data = {
            "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
            "messages": [
                {
                    "role": "user",
                    "content": full_query
                }
            ],
            "stream": False
        }
        
        # 发送请求
        req = prepare_request(
            method="POST",
            path="/api/knowledge/service/chat",
            data=request_data
        )
        
        response = requests.post(
            url=req["url"],
            headers=req["headers"],
            data=req["body"],
            timeout=30
        )
        
        response.encoding = "utf-8"
        result = response.json()
        
        return f"知识库回答: {result.get('answer', json.dumps(result, ensure_ascii=False))}"
            
    except Exception as e:
        return f"搜索知识库时出错: {str(e)}"
```

### 方案二：配置环境变量

在 `.env` 文件中添加：

```bash
# ========================================
# 火山引擎知识库配置
# ========================================

# 火山引擎账号ID
VOLCENGINE_ACCOUNT_ID=your_account_id_here

# 火山引擎API密钥
VOLCENGINE_API_KEY=your_api_key_here

# 知识库服务域名
VOLCENGINE_KB_DOMAIN=api-knowledgebase.mlp.cn-beijing.volces.com

# 知识库服务ID
VOLCENGINE_SERVICE_ID=kb-service-14ae584a2d80c3f9
```

### 方案三：注册到Agent

修改 `src/agents/agent.py`：

```python
from tools import volcengine_knowledge

def build_agent(ctx=None):
    # ... 现有代码 ...
    
    # 导入火山引擎知识库工具
    from tools.volcengine_knowledge import (
        search_volcengine_knowledge,
        search_volcengine_knowledge_with_context
    )
    
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[
            search_volcengine_knowledge,
            search_volcengine_knowledge_with_context,
            # ... 其他工具 ...
        ],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
```

---

## 使用示例

### 示例1：纯文本查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

# 查询埃及象形文字
result = search_volcengine_knowledge(query="埃及象形文字荷鲁斯的含义")
print(result)
```

### 示例2：图文查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

# 查询图片中的古文字
result = search_volcengine_knowledge(
    query="这是什么古文字？请详细解释",
    image_url="https://example.com/ancient_text.jpg"
)
print(result)
```

### 示例3：带上下文的查询

```python
from tools.volcengine_knowledge import search_volcengine_knowledge_with_context

# 用户提供上下文后查询
result = search_volcengine_knowledge_with_context(
    query="这个符号代表什么？",
    context="用户正在研究古埃及象形文字，特别是关于神祇的符号"
)
print(result)
```

---

## 优缺点分析

### 优点

1. ✅ **专业级知识库**：火山引擎提供企业级知识库服务
2. ✅ **支持图文混合**：可以同时查询文本和图片
3. ✅ **高性能**：企业级服务，响应快速
4. ✅ **可扩展**：支持大规模知识库
5. ✅ **API接口**：便于集成

### 缺点

1. ❌ **需要账号**：需要注册火山引擎账号
2. ❌ **成本考虑**：可能有使用费用
3. ⚠️ **网络依赖**：依赖火山引擎服务可用性
4. ⚠️ **数据隐私**：查询数据发送到第三方服务

---

## 与现有知识库对比

| 特性 | 火山引擎知识库 | coze-coding-ai知识库 |
|------|--------------|-------------------|
| **部署方式** | 云服务 | 本地/云部署 |
| **图文支持** | ✅ 支持 | ⚠️ 有限支持 |
| **规模** | 企业级 | 中小型 |
| **成本** | 按使用收费 | 免费 |
| **数据隐私** | 云端 | 本地 |
| **可定制性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **易用性** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **响应速度** | 快 | 中等 |

---

## 推荐使用场景

### 适合使用火山引擎知识库

1. **企业级应用**：需要大规模知识库
2. **图文混合查询**：需要同时处理文本和图片
3. **高性能要求**：需要快速响应
4. **专业级服务**：需要SLA保障

### 适合使用coze-coding-ai知识库

1. **个人项目**：免费使用
2. **数据隐私**：敏感数据不外传
3. **高度定制**：需要完全控制
4. **学习研究**：了解知识库实现

---

## 快速集成步骤

### 1. 安装依赖

```bash
pip install requests volcengine-python-sdk
```

### 2. 配置环境变量

```bash
# 编辑 .env 文件
nano .env

# 添加以下配置
VOLCENGINE_ACCOUNT_ID=your_account_id
VOLCENGINE_API_KEY=your_api_key
VOLCENGINE_SERVICE_ID=kb-service-14ae584a2d80c3f9
```

### 3. 创建工具文件

```bash
# 复制上面提供的代码到
src/tools/volcengine_knowledge.py
```

### 4. 注册到Agent

修改 `src/agents/agent.py`，导入并注册工具

### 5. 测试

```python
from tools.volcengine_knowledge import search_volcengine_knowledge

result = search_volcengine_knowledge(query="测试查询")
print(result)
```

---

## 注意事项

### 1. 安全性

- ⚠️ 不要将API Key提交到Git仓库
- ⚠️ 使用环境变量存储敏感信息
- ⚠️ 定期轮换API Key

### 2. 错误处理

```python
try:
    result = search_volcengine_knowledge(query="测试")
    if "错误" in result:
        # 处理错误
        pass
except Exception as e:
    # 处理异常
    print(f"查询失败: {e}")
```

### 3. 性能优化

- 使用缓存减少重复查询
- 批量查询提高效率
- 异步调用提升性能

### 4. 成本控制

- 监控API调用次数
- 限制并发请求数
- 使用缓存降低成本

---

## 进阶功能

### 1. 流式响应

```python
# 设置stream=True获取流式响应
request_data = {
    "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
    "messages": [...],
    "stream": True  # 启用流式
}
```

### 2. 多轮对话

```python
# 保存对话历史
conversation_history = []

# 添加新消息
conversation_history.append({
    "role": "user",
    "content": query
})

# 发送对话
request_data = {
    "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
    "messages": conversation_history,
    "stream": False
}
```

### 3. 自定义参数

```python
request_data = {
    "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
    "messages": [...],
    "stream": False,
    "temperature": 0.7,      # 温度参数
    "top_k": 5,               # 返回Top K结果
    "max_tokens": 1000        # 最大token数
}
```

---

## 总结

火山引擎知识库API提供了专业级的知识库服务，支持图文混合查询，适合企业级应用。

**建议**：
- 如果需要企业级服务 → 使用火山引擎知识库
- 如果需要免费、隐私、定制 → 使用coze-coding-ai知识库
- 两者可以结合使用，互为补充

---

## 相关资源

- 火山引擎文档：https://www.volcengine.com/docs/
- Python SDK：https://github.com/volcengine/volcengine-python-sdk
- 知识库服务：https://www.volcengine.com/product/knowledgebase
