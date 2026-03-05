# 🔧 401/404错误解决方案

## 问题描述

部署后访问系统时出现 **401** 或 **404** 错误。

---

## 🔍 问题诊断

### 1. 检查服务状态

```bash
# 检查服务是否运行
ps aux | grep -E "python|uvicorn"

# 输出示例：
# root   12  6.7  8.4 999880 170860 ?  Sl   20:26  uvicorn app.main:app --port 9000
# root   96  4.0  3.8 574692 78648 ?  Sl   20:26  python /workspace/projects/src/main.py -m http -p 5000
```

### 2. 检查健康端点

```bash
# 测试健康检查端点
curl http://localhost:5000/health

# 正常返回：
# {"status":"ok","message":"Service is running"}
```

### 3. 检查API文档端点

```bash
# 测试API文档
curl -I http://localhost:5000/docs

# 正常返回：
# HTTP/1.1 200 OK
```

### 4. 检查API端点

```bash
# 测试分析端点（可能返回404，这是正常的）
curl -I http://localhost:5000/api/analyze

# 可能返回：
# HTTP/1.1 404 Not Found
# 说明端点不存在，需要检查路由配置
```

---

## ✅ 解决方案

### 方案一：确认正确的访问端口

**问题**：服务运行在5000端口，但可能访问了8000端口。

**解决方法**：

```bash
# 查看服务运行的端口
netstat -tlnp | grep python
# 或
lsof -i :5000
lsof -i :8000
lsof -i :9000
```

**正确访问地址**：
- 如果服务在5000端口：http://localhost:5000/docs
- 如果服务在8000端口：http://localhost:8000/docs
- 如果服务在9000端口：http://localhost:9000/docs

---

### 方案二：检查环境变量配置

**问题**：`.env` 文件中的 API Key 未配置。

**解决方法**：

```bash
# 1. 检查 .env 文件
cat .env | grep API_KEY

# 2. 如果显示占位符，需要配置真实API Key
nano .env

# 3. 修改这一行：
COZE_WORKLOAD_IDENTITY_API_KEY=sk-your-moonshot-api-key-here
# 改为：
COZE_WORKLOAD_IDENTITY_API_KEY=sk-xxxxx  # 您的真实API Key

# 4. 获取API Key
# 访问：https://platform.moonshot.cn/console/api-keys
```

---

### 方案三：重启服务

**问题**：服务配置未生效。

**解决方法**：

```bash
# 1. 停止现有服务
pkill -f "uvicorn\|python.*main.py"

# 2. 重新启动服务
cd /workspace/projects

# 方式1：使用main.py
python src/main.py -m http -p 5000

# 方式2：使用uvicorn直接
uvicorn src.web_api_new:app --host 0.0.0.0 --port 5000 --reload

# 3. 等待服务启动（约10秒）

# 4. 测试服务
curl http://localhost:5000/health
```

---

### 方案四：检查API路由

**问题**：前端调用的API路径与后端实际路径不匹配。

**当前前端配置**（static/app.js）：
```javascript
const API_BASE_URL = window.location.origin;
// 调用：/api/analyze
// 调用：/api/analyze/image
```

**检查后端路由**（src/web_api_new.py）：
```python
# 需要确认是否有这些路由：
@app.post("/api/analyze")
@app.post("/api/analyze/image")
```

**解决方法**：

如果路由不存在，需要在 `src/web_api_new.py` 中添加：

```python
@app.post("/api/analyze")
async def analyze_text(request: AnalysisRequest):
    """文本分析API"""
    # 实现代码

@app.post("/api/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """图像分析API"""
    # 实现代码
```

---

### 方案五：使用API文档测试

**步骤**：

1. 访问：http://localhost:5000/docs
2. 查看可用的API端点
3. 在API文档中直接测试

**如果API文档可以访问，但前端401/404**：
- 问题在前端配置
- 检查前端JavaScript中的API路径

**如果API文档也无法访问**：
- 问题在服务启动
- 检查服务日志

---

## 📋 完整排查流程

```
1. 检查服务运行状态
   ps aux | grep python

2. 检查端口占用
   netstat -tlnp | grep python

3. 测试健康端点
   curl http://localhost:5000/health

4. 测试API文档
   curl http://localhost:5000/docs

5. 检查环境变量
   cat .env | grep API_KEY

6. 查看服务日志
   tail -f /app/work/logs/bypass/app.log

7. 重启服务
   pkill -f uvicorn
   python src/main.py -m http -p 5000

8. 测试具体API
   curl -X POST http://localhost:5000/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"text":"测试"}'
```

---

## 🚀 快速修复命令

### 一键修复脚本

```bash
#!/bin/bash

# 快速修复401/404错误

echo "======================================"
echo "古文字破译系统 - 错误修复脚本"
echo "======================================"

# 1. 停止现有服务
echo "步骤1: 停止现有服务..."
pkill -f "uvicorn\|python.*main.py" || true
sleep 2

# 2. 检查环境变量
echo "步骤2: 检查环境变量..."
if grep -q "sk-your-moonshot-api-key-here" .env; then
    echo "⚠️  警告：API Key未配置！"
    echo "请编辑 .env 文件，填入您的 Moonshot AI API Key"
    echo "访问：https://platform.moonshot.cn/console/api-keys"
    read -p "是否现在编辑 .env 文件？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        nano .env
    else
        echo "请稍后手动配置 .env 文件"
        exit 1
    fi
fi

# 3. 启动服务
echo "步骤3: 启动服务..."
python src/main.py -m http -p 5000 &

# 4. 等待服务启动
echo "步骤4: 等待服务启动..."
sleep 10

# 5. 测试服务
echo "步骤5: 测试服务..."
if curl -s http://localhost:5000/health | grep -q "ok"; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "访问地址："
    echo "  📡 API文档: http://localhost:5000/docs"
    echo "  🌐 前端界面: http://localhost:5000/static/index.html"
    echo "  ❤️  健康检查: http://localhost:5000/health"
else
    echo "❌ 服务启动失败！"
    echo "请查看日志：tail -f /app/work/logs/bypass/app.log"
    exit 1
fi

echo ""
echo "修复完成！🎉"
```

保存为 `fix-401-error.sh` 并运行：
```bash
chmod +x fix-401-error.sh
./fix-401-error.sh
```

---

## 🎯 常见错误及解决

### 错误1: 401 Unauthorized

**原因**：API Key未配置或无效

**解决**：
```bash
# 配置真实的API Key
nano .env
# 修改：COZE_WORKLOAD_IDENTITY_API_KEY=sk-xxxxx

# 重启服务
pkill -f uvicorn
python src/main.py -m http -p 5000
```

---

### 错误2: 404 Not Found

**原因**：访问了不存在的端点

**解决**：
1. 访问 http://localhost:5000/docs 查看所有可用端点
2. 使用正确的端点路径
3. 检查前端API路径配置

---

### 错误3: Connection Refused

**原因**：服务未运行或端口错误

**解决**：
```bash
# 检查服务是否运行
ps aux | grep python

# 检查端口
netstat -tlnp | grep 5000

# 启动服务
python src/main.py -m http -p 5000
```

---

### 错误4: 502 Bad Gateway

**原因**：后端服务未响应

**解决**：
1. 检查后端服务状态
2. 查看服务日志
3. 重启服务

---

## 📞 获取帮助

如果以上方法都无法解决问题，请：

1. **收集信息**：
   - 错误截图
   - 服务日志：`tail -100 /app/work/logs/bypass/app.log`
   - 访问的URL

2. **检查文档**：
   - [README.md](README.md)
   - [ONE_CLICK_DEPLOY.md](ONE_CLICK_DEPLOY.md)
   - [API_TOKEN_SETUP.md](API_TOKEN_SETUP.md)

3. **提交Issue**：
   - 提供详细的错误信息
   - 提供环境信息（操作系统、Python版本等）

---

## ✅ 验证修复

修复完成后，按以下步骤验证：

```bash
# 1. 健康检查
curl http://localhost:5000/health
# 应该返回：{"status":"ok","message":"Service is running"}

# 2. API文档
curl http://localhost:5000/docs
# 应该返回：HTML页面

# 3. 前端界面
curl http://localhost:5000/static/index.html
# 应该返回：HTML页面

# 4. 测试API（如果可用）
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"测试"}'
```

如果所有测试都通过，说明修复成功！🎉
