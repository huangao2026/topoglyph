"""
示例插件：OCR文字识别工具
展示如何创建和注册插件
"""
from core.plugin import Plugin, PluginContext, PluginType, PluginInfo
from core.tool import Tool, ToolCategory, ToolInput, ToolOutput, ToolStatus


class OCRRecognitionTool(Tool):
    """OCR文字识别工具示例"""
    
    id = "ocr-recognition"
    name = "OCR文字识别"
    category = ToolCategory.OCR
    version = "1.0.0"
    description = "使用OCR技术识别古文字图像中的文字内容"
    capabilities = ["图像识别", "文字提取", "古文字识别"]
    
    async def execute(self, input_data: ToolInput) -> ToolOutput:
        """执行OCR识别
        
        Args:
            input_data: 输入数据，包含图像
            
        Returns:
            ToolOutput: 识别结果
        """
        try:
            # 验证输入
            if not input_data.image:
                return ToolOutput(
                    success=False,
                    error="No image data provided"
                )
            
            # TODO: 这里应该调用实际的OCR API
            # 目前返回模拟数据
            result_text = """
识别到以下古文字符号：

1. 符号A - 可能是"日"或"天"
2. 符号B - 可能是"山"或"地"
3. 符号C - 可能是"人"或"王"

注意：这是示例插件的模拟输出，实际部署时需要集成真实的OCR服务。
            """
            
            return ToolOutput(
                success=True,
                result=result_text.strip(),
                metadata={
                    "tool_version": self.version,
                    "recognition_confidence": 0.85
                }
            )
        
        except Exception as e:
            return ToolOutput(
                success=False,
                error=f"OCR recognition failed: {str(e)}"
            )


class OCRToolPlugin(Plugin):
    """OCR工具插件
    
    这是一个示例插件，展示了如何：
    1. 创建自定义工具
    2. 注册工具到工具管理器
    3. 实现插件的生命周期管理
    """
    
    id = "ocr-tool-plugin"
    name = "OCR工具插件"
    version = "1.0.0"
    plugin_type = PluginType.TOOL
    author = "专利系统开发团队"
    description = "提供OCR文字识别功能的示例插件"
    dependencies = []  # 无依赖
    
    def __init__(self):
        self._tool_instance = None
    
    async def load(self, context: PluginContext) -> bool:
        """加载插件
        
        Args:
            context: 插件上下文
            
        Returns:
            bool: 是否加载成功
        """
        try:
            # 创建工具实例
            self._tool_instance = OCRRecognitionTool()
            
            # 注册工具到工具管理器
            context.tool_manager.register_tool(self._tool_instance)
            
            # 记录日志
            if hasattr(context, 'logger'):
                context.logger.info(f"Plugin {self.id} loaded successfully")
            
            return True
        
        except Exception as e:
            if hasattr(context, 'logger'):
                context.logger.error(f"Failed to load plugin {self.id}: {e}")
            return False
    
    async def unload(self) -> bool:
        """卸载插件
        
        Returns:
            bool: 是否卸载成功
        """
        try:
            # 如果需要，可以执行清理操作
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
                "message": "OCR tool is ready"
            }
        else:
            return {
                "status": "unhealthy",
                "plugin_id": self.id,
                "message": "OCR tool not initialized"
            }
