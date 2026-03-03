# API 文档

古文字破译系统 - RESTful API 文档

## 基本信息

- **基础URL**: `http://your-domain/api/v1`
- **版本**: v2.0.0
- **认证**: 暂未启用（生产环境建议启用）
- **限流**: 见各接口说明

## 通用响应格式

所有API响应遵循以下格式：

```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

错误响应格式：

```json
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

## API 端点

### 1. 系统管理

#### 1.1 健康检查

检查系统健康状态。

**请求:**
```http
GET /health
```

**响应:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-10T10:00:00Z",
  "checks": {
    "engine": {
      "status": "healthy",
      "message": "Engine is running"
    }
  }
}
```

#### 1.2 获取系统状态

获取系统运行状态和监控指标。

**请求:**
```http
GET /api/v1/metrics
```

**响应:**
```json
{
  "metrics": "Prometheus 格式指标",
  "status": {
    "health": {},
    "alerts": []
  }
}
```

#### 1.3 获取版本信息

获取系统各组件版本信息。

**请求:**
```http
GET /api/v1/version
```

**响应:**
```json
{
  "components": {
    "tool:ocr-recognition": {
      "component": "tool",
      "component_id": "ocr-recognition",
      "version": "1.0.0",
      "deployed_at": "2025-01-10T10:00:00Z"
    }
  },
  "timestamp": "2025-01-10T10:00:00Z"
}
```

### 2. 古文字分析

#### 2.1 文本分析

分析古文字文本内容。

**请求:**
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "甲骨文字符串",
  "session_id": "optional-session-id"
}
```

**参数说明:**
- `text` (string, 必需): 要分析的古文字文本
- `session_id` (string, 可选): 会话ID，用于多轮对话

**限流:** 60次/分钟

**响应:**
```json
{
  "success": true,
  "session_id": "session-uuid",
  "analysis_id": "analysis-uuid",
  "response": "分析结果",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

#### 2.2 图像分析

分析古文字图像。

**请求:**
```http
POST /api/v1/analyze/image
Content-Type: multipart/form-data

file: <图像文件>
session_id: optional-session-id
```

**参数说明:**
- `file` (file, 必需): 图像文件，支持 jpg, png 格式
- `session_id` (string, 可选): 会话ID

**限流:** 30次/分钟

**响应:**
```json
{
  "success": true,
  "session_id": "session-uuid",
  "analysis_id": "analysis-uuid",
  "response": "图像分析结果",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

### 3. 对话交互

#### 3.1 发送消息

与智能体进行对话。

**请求:**
```http
POST /api/v1/chat
Content-Type: application/json

{
  "message": "用户消息",
  "session_id": "session-uuid"
}
```

**参数说明:**
- `message` (string, 必需): 用户消息内容
- `session_id` (string, 必需): 会话ID

**限流:** 120次/分钟

**响应:**
```json
{
  "success": true,
  "session_id": "session-uuid",
  "response": "智能体回复",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

#### 3.2 获取会话历史

获取会话的历史消息。

**请求:**
```http
GET /api/v1/sessions/{session_id}
```

**参数说明:**
- `session_id` (string, 必需): 会话ID

**响应:**
```json
{
  "session_id": "session-uuid",
  "history": [
    {
      "role": "user",
      "content": "用户消息",
      "timestamp": "2025-01-10T10:00:00Z",
      "metadata": {}
    },
    {
      "role": "assistant",
      "content": "智能体回复",
      "timestamp": "2025-01-10T10:00:00Z",
      "metadata": {}
    }
  ],
  "message_count": 2
}
```

### 4. 工具管理

#### 4.1 获取工具列表

获取所有可用工具。

**请求:**
```http
GET /api/v1/tools?category=ocr
```

**参数说明:**
- `category` (string, 可选): 工具分类，可选值: `ocr`, `translation`, `analysis`, `recognition`, `comparison`, `repair`, `search`, `database`, `custom`

**响应:**
```json
{
  "total": 5,
  "tools": [
    {
      "id": "ocr-recognition",
      "name": "OCR文字识别",
      "version": "1.0.0",
      "category": "ocr",
      "description": "使用OCR技术识别古文字图像中的文字内容",
      "capabilities": ["图像识别", "文字提取", "古文字识别"],
      "status": "active",
      "performance": {
        "avg_response_time": 500.5,
        "success_rate": 0.98,
        "call_count": 1000,
        "error_count": 20
      }
    }
  ]
}
```

#### 4.2 获取工具详情

获取指定工具的详细信息。

**请求:**
```http
GET /api/v1/tools/{tool_id}
```

**参数说明:**
- `tool_id` (string, 必需): 工具ID

**响应:**
```json
{
  "id": "ocr-recognition",
  "name": "OCR文字识别",
  "version": "1.0.0",
  "category": "ocr",
  "description": "使用OCR技术识别古文字图像中的文字内容",
  "capabilities": ["图像识别", "文字提取", "古文字识别"],
  "status": "active",
  "performance": {
    "avg_response_time": 500.5,
    "success_rate": 0.98,
    "call_count": 1000,
    "error_count": 20,
    "last_called": "2025-01-10T09:59:00Z"
  },
  "created_at": "2025-01-10T08:00:00Z",
  "updated_at": "2025-01-10T08:00:00Z"
}
```

#### 4.3 推荐工具

根据需求推荐合适的工具。

**请求:**
```http
POST /api/v1/tools/recommend
Content-Type: application/json

{
  "requirements": ["识别甲骨文", "图像处理"],
  "category": "ocr",
  "limit": 5
}
```

**参数说明:**
- `requirements` (array, 必需): 需求列表
- `category` (string, 可选): 工具分类
- `limit` (integer, 可选): 返回数量限制，默认 5

**响应:**
```json
{
  "requirements": ["识别甲骨文", "图像处理"],
  "recommended": [
    {
      "id": "ocr-recognition",
      "name": "OCR文字识别",
      "match_score": 0.85
    }
  ]
}
```

### 5. 插件管理

#### 5.1 获取插件列表

获取所有已加载的插件。

**请求:**
```http
GET /api/v1/plugins
```

**响应:**
```json
{
  "total": 3,
  "plugins": [
    {
      "id": "ocr-tool-plugin",
      "name": "OCR工具插件",
      "version": "1.0.0",
      "plugin_type": "tool",
      "author": "专利系统开发团队",
      "description": "提供OCR文字识别功能的示例插件"
    }
  ]
}
```

#### 5.2 检查插件健康状态

检查指定插件的健康状态。

**请求:**
```http
GET /api/v1/plugins/{plugin_id}/health
```

**参数说明:**
- `plugin_id` (string, 必需): 插件ID

**响应:**
```json
{
  "status": "healthy",
  "plugin_id": "ocr-tool-plugin",
  "tool_id": "ocr-recognition",
  "message": "OCR tool is ready"
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

## SDK 示例

### Python 示例

```python
import requests

BASE_URL = "http://your-domain/api/v1"

# 文本分析
response = requests.post(
    f"{BASE_URL}/analyze",
    json={"text": "甲骨文字符串"}
)
print(response.json())

# 图像分析
with open("image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        f"{BASE_URL}/analyze/image",
        files=files
    )
    print(response.json())

# 对话
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "message": "这段文字是什么意思？",
        "session_id": "session-uuid"
    }
)
print(response.json())
```

### JavaScript 示例

```javascript
const BASE_URL = "http://your-domain/api/v1";

// 文本分析
async function analyzeText(text) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return await response.json();
}

// 图像分析
async function analyzeImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${BASE_URL}/analyze/image`, {
    method: 'POST',
    body: formData
  });
  return await response.json();
}

// 对话
async function chat(message, sessionId) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId })
  });
  return await response.json();
}
```

## 更新日志

### v2.0.0 (2025-01-10)
- 重构架构，实现模块化设计
- 新增插件系统
- 新增版本管理系统
- 新增性能监控
- 新增长期记忆功能
- 优化API限流机制

### v1.0.0 (2025-01-08)
- 初始版本
- 基础文本分析功能
- 图像识别功能
- 对话功能
- 工具推荐功能
