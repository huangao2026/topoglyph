# 系统功能测试指南

## 🧪 自动化测试

### 快速测试（推荐）

使用自动化测试脚本，一键测试所有功能：

```bash
# 运行完整测试
./test_system.sh
```

测试脚本会自动验证：
- ✅ 系统健康状态
- ✅ API基础功能
- ✅ 工具管理功能
- ✅ 插件管理功能
- ✅ 文本分析功能
- ✅ 对话交互功能
- ✅ 会话管理功能

测试结果示例：
```
==================================
测试总结
==================================
总测试数: 15
通过: 15
失败: 0

🎉 所有测试通过！系统运行正常！
```

---

## 📝 手动测试用例

### 1️⃣ 健康检查测试

#### 测试目标
验证系统是否正常运行。

#### 测试步骤
```bash
curl http://localhost:8000/health
```

#### 预期结果
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

#### 判定标准
- ✅ 返回 `status: "healthy"`
- ✅ HTTP 状态码为 200
- ✅ 响应时间 < 1秒

---

### 2️⃣ 文本分析测试

#### 测试用例 1：基础问答

**输入**:
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "什么是甲骨文？"
  }'
```

**预期输出**:
```json
{
  "success": true,
  "session_id": "...",
  "analysis_id": "...",
  "response": "甲骨文是中国古代最早的成熟文字系统...",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

#### 测试用例 2：甲骨文破译

**输入**:
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "王贞卜，旬亡祸？在十月又二。请分析这段甲骨文的含义。"
  }'
```

**预期输出**:
```json
{
  "success": true,
  "response": "# 古代文字分析报告\n\n## 基本信息\n- **文字类型**: 甲骨文（商代）\n- **大致年代**: 约公元前14-11世纪\n\n## 符号识别\n- \"王\" - 商王\n- \"贞\" - 占卜\n..."
}
```

**判定标准**:
- ✅ 正确识别文字类型（甲骨文）
- ✅ 提供年代信息
- ✅ 识别关键符号
- ✅ 给出翻译和解释

#### 测试用例 3：金文分析

**输入**:
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "请介绍西周金文的特点和用途。"
  }'
```

**预期输出**:
应包含金文的特征、历史背景、用途等信息。

---

### 3️⃣ 图像识别测试

#### 准备测试图片

创建或下载一张古文字图片，保存为 `test_image.jpg`。

#### 测试步骤

```bash
# 上传图像进行分析
curl -X POST http://localhost:8000/api/v1/analyze/image \
  -F "file=@test_image.jpg"
```

#### 预期输出
```json
{
  "success": true,
  "session_id": "...",
  "analysis_id": "...",
  "response": "# 古代文字分析报告\n\n## 图像识别\n识别到以下古文字符号：\n\n1. 符号A - 可能是\"日\"或\"天\"\n2. 符号B - 可能是\"山\"或\"地\"\n...",
  "timestamp": "2025-01-10T10:00:00Z"
}
```

#### 判定标准
- ✅ 成功接收图像文件
- ✅ 调用OCR工具进行识别
- ✅ 返回结构化的分析报告
- ✅ 响应时间 < 10秒

---

### 4️⃣ 对话交互测试

#### 测试用例 1：单轮对话

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是楔形文字？",
    "session_id": "test-001"
  }'
```

#### 测试用例 2：多轮对话（保持上下文）

**第一轮**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "介绍一下2026年古文字破解的最新进展。",
    "session_id": "test-002"
  }'
```

**第二轮**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "这些新技术有什么优势？",
    "session_id": "test-002"
  }'
```

**第三轮**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "推荐的工具中哪个最适合初学者？",
    "session_id": "test-002"
  }'
```

**判定标准**:
- ✅ 每轮对话都能正确响应
- ✅ 后续对话能够理解前文的上下文
- ✅ 不会重复之前已回答的内容
- ✅ 能够根据上下文进行推理

---

### 5️⃣ 工具管理测试

#### 测试用例 1：获取工具列表

```bash
curl http://localhost:8000/api/v1/tools
```

**预期输出**:
```json
{
  "total": 2,
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
        "success_rate": 1.0,
        "call_count": 0,
        "error_count": 0
      }
    }
  ]
}
```

#### 测试用例 2：按分类获取工具

```bash
curl http://localhost:8000/api/v1/tools?category=ocr
```

#### 测试用例 3：工具推荐

```bash
curl -X POST http://localhost:8000/api/v1/tools/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "requirements": ["识别甲骨文", "图像处理"],
    "category": "ocr",
    "limit": 5
  }'
```

**判定标准**:
- ✅ 返回的工具符合需求
- ✅ 工具按匹配度排序
- ✅ 包含工具的详细信息

---

### 6️⃣ 插件管理测试

#### 测试用例 1：获取插件列表

```bash
curl http://localhost:8000/api/v1/plugins
```

**预期输出**:
```json
{
  "total": 1,
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

#### 测试用例 2：检查插件健康状态

```bash
curl http://localhost:8000/api/v1/plugins/ocr-tool-plugin/health
```

**预期输出**:
```json
{
  "status": "healthy",
  "plugin_id": "ocr-tool-plugin",
  "tool_id": "ocr-recognition",
  "message": "OCR tool is ready"
}
```

---

### 7️⃣ 性能测试

#### 测试用例 1：并发请求测试

```bash
# 安装 Apache Bench（如果没有）
# sudo apt install apache2-utils

# 测试并发性能
ab -n 100 -c 10 http://localhost:8000/health
```

**判定标准**:
- ✅ 成功率 > 99%
- ✅ 平均响应时间 < 500ms
- ✅ 无超时错误

#### 测试用例 2：响应时间测试

```bash
# 测试文本分析响应时间
time curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "测试文本"}' \
  -o /dev/null -s -w "HTTP Status: %{http_code}\nTime: %{time_total}s\n"
```

**判定标准**:
- ✅ HTTP 状态码为 200
- ✅ 响应时间 < 10秒

---

### 8️⃣ 错误处理测试

#### 测试用例 1：无效输入

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

**预期**: 返回适当的错误信息

#### 测试用例 2：不存在的端点

```bash
curl http://localhost:8000/api/v1/nonexistent
```

**预期**: 返回 404 错误

#### 测试用例 3：限流测试

```bash
# 快速发送多个请求（超过限流限制）
for i in {1..70}; do
  curl http://localhost:8000/health &
done
wait
```

**预期**: 超过限流后返回 429 错误

---

### 9️⃣ 会话管理测试

#### 测试用例 1：创建会话

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "开始对话", "session_id": "test-session-001"}'
```

#### 测试用例 2：获取会话历史

```bash
curl http://localhost:8000/api/v1/sessions/test-session-001
```

**预期输出**:
```json
{
  "session_id": "test-session-001",
  "history": [
    {
      "role": "user",
      "content": "开始对话",
      "timestamp": "2025-01-10T10:00:00Z",
      "metadata": {}
    },
    {
      "role": "assistant",
      "content": "...",
      "timestamp": "2025-01-10T10:00:00Z",
      "metadata": {}
    }
  ],
  "message_count": 2
}
```

---

### 🔟 综合场景测试

#### 场景 1：完整的破译流程

```bash
# 1. 分析古文字文本
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "王贞卜，旬亡祸？"}'

# 2. 基于分析结果进行对话
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "这段文字的历史背景是什么？",
    "session_id": "xxx"  # 使用上面的 session_id
  }'

# 3. 请求工具推荐
curl -X POST http://localhost:8000/api/v1/tools/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "requirements": ["甲骨文", "破译", "图像识别"],
    "limit": 3
  }'
```

#### 场景 2：用户咨询流程

```bash
# 用户咨询：如何识别甲骨文？
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "如何识别甲骨文？",
    "session_id": "consult-001"
  }'

# 用户追问：有什么工具推荐？
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "有什么AI工具可以帮助识别甲骨文？",
    "session_id": "consult-001"
  }'

# 用户最后问：这些工具哪里可以获取？
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "这些工具哪里可以获取？",
    "session_id": "consult-001"
  }'
```

**判定标准**:
- ✅ 整个流程流畅无卡顿
- ✅ 上下文保持连贯
- ✅ 回答准确且有用

---

## 📊 测试报告模板

### 测试执行记录

| 测试项 | 测试时间 | 测试人员 | 结果 | 备注 |
|--------|----------|----------|------|------|
| 健康检查 | | | ☐ | |
| 文本分析 | | | ☐ | |
| 图像识别 | | | ☐ | |
| 对话交互 | | | ☐ | |
| 工具管理 | | | ☐ | |
| 插件管理 | | | ☐ | |
| 性能测试 | | | ☐ | |
| 错误处理 | | | ☐ | |
| 综合场景 | | | ☐ | |

### 测试结果统计

- **总测试数**: ___
- **通过**: ___
- **失败**: ___
- **通过率**: ___%

### 问题记录

| 序号 | 问题描述 | 严重程度 | 状态 |
|------|----------|----------|------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## ✅ 测试通过标准

所有测试满足以下条件视为通过：

1. **功能完整性**
   - ✅ 所有核心功能正常运行
   - ✅ API 响应符合预期格式
   - ✅ 错误处理正确

2. **性能指标**
   - ✅ 响应时间 < 10秒（复杂分析）
   - ✅ 响应时间 < 3秒（简单查询）
   - ✅ 并发支持 > 10 QPS

3. **稳定性**
   - ✅ 连续运行无崩溃
   - ✅ 内存使用稳定
   - ✅ 错误率 < 1%

4. **可用性**
   - ✅ API 文档可访问
   - ✅ 前端界面可用
   - ✅ 日志记录完整

---

## 🚀 下一步

测试通过后，您可以：

1. ✅ **开始使用系统** - 进行实际的古文字分析工作
2. 🔧 **开发插件** - 扩展系统功能
3. 🌐 **部署到生产** - 配置Nginx、HTTPS等
4. 📊 **配置监控** - 设置告警和性能监控
5. 📖 **编写文档** - 为团队使用提供指南

---

**祝测试顺利！** 🎉
