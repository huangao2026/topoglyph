# 插件开发文档

古文字破译系统 - 插件开发指南

## 概述

本系统采用插件化架构，允许开发者通过插件扩展系统功能。插件可以添加新工具、新模型、新存储后端等。

## 插件类型

系统支持以下插件类型：

1. **工具插件** - 添加新的破译工具
2. **模型插件** - 添加新的LLM模型
3. **存储插件** - 添加新的存储后端
4. **监控插件** - 添加新的监控指标

## 插件目录结构

```
plugins/
└── your_plugin/
    ├── __init__.py
    ├── plugin.py           # 插件主文件
    ├── tools/              # 工具目录（可选）
    │   └── your_tool.py
    ├── config/             # 配置文件（可选）
    │   └── config.json
    └── README.md           # 插件说明（可选）
```

## 开发工具插件

### 步骤 1: 创建插件目录

```bash
mkdir -p plugins/my_custom_tool
touch plugins/my_custom_tool/__init__.py
```

### 步骤 2: 实现工具类

创建 `plugins/my_custom_tool/tools/my_tool.py`:

```python
from core.tool import Tool, ToolCategory, ToolInput, ToolOutput

class MyCustomTool(Tool):
    """自定义工具示例"""
    
    # 必填属性
    id = "my-custom-tool"
    name = "我的自定义工具"
    category = ToolCategory.CUSTOM
    
    # 可选属性
    version = "1.0.0"
    description = "这是一个自定义工具的示例"
    capabilities = ["功能1", "功能2"]
    
    async def execute(self, input_data: ToolInput) -> ToolOutput:
        """执行工具功能"""
        try:
            # 1. 验证输入
            if not input_data.text:
                return ToolOutput(
                    success=False,
                    error="缺少输入文本"
                )
            
            # 2. 执行业务逻辑
            result = await self._process(input_data.text)
            
            # 3. 返回结果
            return ToolOutput(
                success=True,
                result=result,
                metadata={
                    "tool_version": self.version
                }
            )
        
        except Exception as e:
            return ToolOutput(
                success=False,
                error=f"执行失败: {str(e)}"
            )
    
    async def _process(self, text: str) -> str:
        """处理逻辑"""
        # TODO: 实现具体的处理逻辑
        return f"处理结果: {text}"
```

### 步骤 3: 实现插件类

创建 `plugins/my_custom_tool/plugin.py`:

```python
from core.plugin import Plugin, PluginContext, PluginType, PluginInfo
from core.tool import Tool
from tools.my_tool import MyCustomTool

class MyCustomToolPlugin(Plugin):
    """自定义工具插件"""
    
    # 必填属性
    id = "my-custom-tool-plugin"
    name = "我的工具插件"
    version = "1.0.0"
    plugin_type = PluginType.TOOL
    
    # 可选属性
    author = "Your Name"
    description = "提供自定义工具功能的插件"
    dependencies = []  # 依赖的其他插件ID
    
    def __init__(self):
        self._tool_instance = None
    
    async def load(self, context: PluginContext) -> bool:
        """加载插件"""
        try:
            # 1. 创建工具实例
            self._tool_instance = MyCustomTool()
            
            # 2. 注册工具到工具管理器
            context.tool_manager.register_tool(self._tool_instance)
            
            # 3. 记录日志
            if hasattr(context, 'logger'):
                context.logger.info(f"插件 {self.id} 加载成功")
            
            return True
        
        except Exception as e:
            if hasattr(context, 'logger'):
                context.logger.error(f"插件 {self.id} 加载失败: {e}")
            return False
    
    async def unload(self) -> bool:
        """卸载插件"""
        try:
            # 执行清理操作
            self._tool_instance = None
            return True
        
        except Exception as e:
            return False
    
    async def health_check(self):
        """健康检查"""
        if self._tool_instance:
            return {
                "status": "healthy",
                "plugin_id": self.id,
                "tool_id": self._tool_instance.id,
                "message": "工具运行正常"
            }
        else:
            return {
                "status": "unhealthy",
                "plugin_id": self.id,
                "message": "工具未初始化"
            }
```

### 步骤 4: 插件配置（可选）

创建 `plugins/my_custom_tool/config/config.json`:

```json
{
  "enabled": true,
  "settings": {
    "api_endpoint": "https://api.example.com",
    "timeout": 30,
    "max_retries": 3
  }
}
```

## 插件生命周期

### 1. 加载

系统启动时，`PluginManager` 会自动发现并加载所有插件：

```python
# 发现插件
discovered_plugins = await plugin_manager.discover_plugins()

# 加载插件
for plugin_info in discovered_plugins:
    success = await plugin_manager.load_plugin(plugin_info.id, context)
```

### 2. 运行

插件加载后，可以通过 API 调用工具：

```python
# 使用工具
tool = tool_manager.get_tool("my-custom-tool")
input_data = ToolInput(text="输入文本")
result = await tool.execute(input_data)
```

### 3. 卸载

系统关闭时，插件会被自动卸载：

```python
# 卸载插件
await plugin_manager.unload_plugin(plugin_id)
```

## 依赖管理

插件可以声明对其他插件的依赖：

```python
class MyPlugin(Plugin):
    dependencies = ["plugin-1", "plugin-2"]
```

系统会确保依赖的插件先被加载，否则会抛出 `PluginDependencyError`。

## 事件处理

插件可以监听和响应系统事件：

```python
from core.event import EventType

async def load(self, context: PluginContext) -> bool:
    # 订阅事件
    context.event_bus.subscribe(
        EventType.TOOL_CALLED,
        self.on_tool_called
    )
    return True

async def on_tool_called(self, event):
    """处理工具调用事件"""
    tool_id = event.data.get("tool_id")
    print(f"工具 {tool_id} 被调用")
```

## 性能监控

工具的性能会被自动记录：

```python
# 工具的性能指标会自动更新
tool_info = tool_manager.get_tool_info("my-custom-tool")
print(tool_info.performance.to_dict())
# {
#   "avg_response_time": 500.5,
#   "success_rate": 0.98,
#   "call_count": 1000,
#   "error_count": 20
# }
```

## 版本管理

插件版本遵循语义化版本规范：

```
MAJOR.MINOR.PATCH

MAJOR: 不兼容的API修改
MINOR: 向下兼容的功能性新增
PATCH: 向下兼容的问题修正
```

示例：

- `1.0.0` - 初始版本
- `1.1.0` - 新增功能
- `1.1.1` - 修复bug
- `2.0.0` - 破坏性更新

## 错误处理

工具应该正确处理错误：

```python
async def execute(self, input_data: ToolInput) -> ToolOutput:
    try:
        # 业务逻辑
        pass
    except ValidationError as e:
        return ToolOutput(
            success=False,
            error=f"输入验证失败: {e}"
        )
    except APIError as e:
        return ToolOutput(
            success=False,
            error=f"API调用失败: {e}"
        )
    except Exception as e:
        return ToolOutput(
            success=False,
            error=f"未知错误: {e}"
        )
```

## 最佳实践

### 1. 输入验证

始终验证输入数据：

```python
async def validate_input(self, input_data: ToolInput) -> bool:
    if not input_data.text:
        return False
    if len(input_data.text) > 10000:
        return False
    return True
```

### 2. 超时处理

为外部调用设置超时：

```python
import asyncio

async def execute(self, input_data: ToolInput) -> ToolOutput:
    try:
        result = await asyncio.wait_for(
            self._call_external_api(),
            timeout=30.0
        )
        return ToolOutput(success=True, result=result)
    except asyncio.TimeoutError:
        return ToolOutput(success=False, error="请求超时")
```

### 3. 日志记录

记录重要操作：

```python
async def load(self, context: PluginContext) -> bool:
    if hasattr(context, 'logger'):
        context.logger.info("插件正在加载")
    
    # ... 加载逻辑
    
    if hasattr(context, 'logger'):
        context.logger.info("插件加载完成")
    
    return True
```

### 4. 配置管理

使用配置文件管理参数：

```python
async def load(self, context: PluginContext) -> bool:
    # 读取配置
    config = context.config.get("settings", {})
    timeout = config.get("timeout", 30)
    
    # 使用配置
    self._timeout = timeout
    
    return True
```

### 5. 健康检查

实现健康检查：

```python
async def health_check(self):
    try:
        # 检查外部服务
        await self._check_external_service()
        
        return {
            "status": "healthy",
            "message": "服务正常运行"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"服务异常: {e}"
        }
```

## 测试

### 单元测试

```python
import pytest

@pytest.mark.asyncio
async def test_my_custom_tool():
    tool = MyCustomTool()
    input_data = ToolInput(text="测试文本")
    
    result = await tool.execute(input_data)
    
    assert result.success is True
    assert "处理结果" in result.result
```

### 集成测试

```python
@pytest.mark.asyncio
async def test_plugin_loading():
    plugin = MyCustomToolPlugin()
    context = create_mock_context()
    
    success = await plugin.load(context)
    
    assert success is True
    assert plugin._tool_instance is not None
```

## 发布

### 1. 打包

```bash
cd plugins/my_custom_tool
zip -r my_custom_tool.zip *
```

### 2. 文档

创建 `README.md`：

```markdown
# My Custom Tool Plugin

## 简介

这是一个自定义工具插件。

## 功能

- 功能1
- 功能2

## 安装

1. 将插件文件解压到 `plugins/` 目录
2. 重启系统

## 使用

通过API调用工具：

```python
POST /api/v1/tools/my-custom-tool/execute
{
  "text": "输入文本"
}
```

## 配置

编辑 `config/config.json` 文件。

## 作者

Your Name

## 许可

MIT
```

### 3. 分享

将插件分享给其他开发者：

- GitHub仓库
- 插件市场（即将推出）

## 示例插件

系统提供了以下示例插件：

1. **OCR工具插件** (`plugins/ocr_tool/`)
   - 演示如何创建工具插件
   - 演示如何注册工具

参考这些示例来学习如何开发自己的插件。

## 支持

如有问题，请联系：

- 邮箱: support@example.com
- 文档: https://docs.example.com
- 社区: https://community.example.com

## 更新日志

### 1.0.0 (2025-01-10)
- 初始版本
- 支持工具插件
- 支持依赖管理
- 支持事件处理
