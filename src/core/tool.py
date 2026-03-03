"""
工具基类和数据模型
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
import json


class ToolCategory(Enum):
    """工具分类"""
    OCR = "ocr"                     # 文字识别
    TRANSLATION = "translation"     # 翻译
    ANALYSIS = "analysis"           # 分析
    RECOGNITION = "recognition"     # 识别
    COMPARISON = "comparison"       # 对比
    REPAIR = "repair"               # 修复
    SEARCH = "search"               # 搜索
    DATABASE = "database"           # 数据库
    CUSTOM = "custom"               # 自定义


class ToolStatus(Enum):
    """工具状态"""
    ACTIVE = "active"               # 活跃
    DEPRECATED = "deprecated"       # 已弃用
    EXPERIMENTAL = "experimental"   # 实验性
    MAINTENANCE = "maintenance"     # 维护中


@dataclass
class ToolPerformance:
    """工具性能指标"""
    avg_response_time: float = 0.0          # 平均响应时间（毫秒）
    success_rate: float = 1.0               # 成功率 (0-1)
    last_called: Optional[datetime] = None  # 最后调用时间
    call_count: int = 0                     # 调用次数
    error_count: int = 0                    # 错误次数
    
    def update(self, response_time: float, success: bool):
        """更新性能指标"""
        # 更新平均响应时间
        if self.call_count == 0:
            self.avg_response_time = response_time
        else:
            self.avg_response_time = (
                self.avg_response_time * self.call_count + response_time
            ) / (self.call_count + 1)
        
        # 更新调用次数
        self.call_count += 1
        
        # 更新成功率
        if success:
            # 之前全部成功，保持1.0
            if self.success_rate == 1.0:
                pass
            else:
                # 重新计算成功率
                success_count = int(self.success_rate * (self.call_count - 1)) + 1
                self.success_rate = success_count / self.call_count
        else:
            self.error_count += 1
            success_count = int(self.success_rate * (self.call_count - 1))
            self.success_rate = success_count / self.call_count
        
        # 更新最后调用时间
        self.last_called = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "avg_response_time": self.avg_response_time,
            "success_rate": self.success_rate,
            "last_called": self.last_called.isoformat() if self.last_called else None,
            "call_count": self.call_count,
            "error_count": self.error_count
        }


@dataclass
class ToolConfig:
    """工具配置"""
    api_endpoint: Optional[str] = None      # API端点
    api_key: Optional[str] = None           # API密钥
    timeout: int = 30                       # 超时时间（秒）
    max_retries: int = 3                    # 最大重试次数
    custom_params: Dict[str, Any] = field(default_factory=dict)  # 自定义参数


@dataclass
class ToolInfo:
    """工具信息"""
    id: str                                 # 工具唯一标识
    name: str                               # 工具名称
    version: str                            # 工具版本
    category: ToolCategory                  # 工具分类
    description: str                        # 工具描述
    capabilities: List[str] = field(default_factory=list)        # 能力列表
    config: ToolConfig = field(default_factory=ToolConfig)        # 配置
    performance: ToolPerformance = field(default_factory=ToolPerformance)  # 性能指标
    status: ToolStatus = ToolStatus.ACTIVE  # 状态
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "category": self.category.value,
            "description": self.description,
            "capabilities": self.capabilities,
            "config": {
                "api_endpoint": self.config.api_endpoint,
                "timeout": self.config.timeout,
                "max_retries": self.config.max_retries
            },
            "performance": self.performance.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ToolInput:
    """工具输入"""
    text: Optional[str] = None              # 文本输入
    image: Optional[bytes] = None           # 图像输入
    image_url: Optional[str] = None         # 图像URL
    parameters: Dict[str, Any] = field(default_factory=dict)     # 其他参数
    
    def validate(self) -> bool:
        """验证输入"""
        return True


@dataclass
class ToolOutput:
    """工具输出"""
    success: bool                           # 是否成功
    result: Optional[str] = None            # 结果文本
    data: Optional[Dict[str, Any]] = None   # 结构化数据
    error: Optional[str] = None             # 错误信息
    metadata: Dict[str, Any] = field(default_factory=dict)       # 元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "result": self.result,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata
        }


class Tool(ABC):
    """工具基类
    
    所有破译工具必须继承此类并实现相关方法。
    
    示例:
        class OCRTool(Tool):
            id = "ocr-basic"
            name = "基础OCR识别"
            category = ToolCategory.OCR
            
            async def execute(self, input_data: ToolInput) -> ToolOutput:
                # 执行识别逻辑
                return ToolOutput(success=True, result="识别结果")
    """
    
    # 必须在子类中定义的属性
    id: str = ""
    name: str = ""
    category: ToolCategory = ToolCategory.CUSTOM
    
    # 可选属性
    version: str = "1.0.0"
    description: str = ""
    capabilities: List[str] = []
    config: ToolConfig = ToolConfig()
    
    def __post_init__(self):
        """初始化后检查必要属性"""
        if not all([self.id, self.name]):
            raise ValueError(f"Tool {self.__class__.__name__} must define id and name")
    
    @abstractmethod
    async def execute(self, input_data: ToolInput) -> ToolOutput:
        """执行工具功能
        
        Args:
            input_data: 工具输入数据
            
        Returns:
            ToolOutput: 工具输出结果
        """
        pass
    
    def get_info(self) -> ToolInfo:
        """获取工具信息"""
        return ToolInfo(
            id=self.id,
            name=self.name,
            version=self.version,
            category=self.category,
            description=self.description,
            capabilities=self.capabilities,
            config=self.config
        )
    
    async def validate_input(self, input_data: ToolInput) -> bool:
        """验证输入数据
        
        Args:
            input_data: 输入数据
            
        Returns:
            bool: 输入是否有效
        """
        return input_data.validate()
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查
        
        Returns:
            Dict: 健康状态
        """
        return {
            "status": "healthy",
            "tool_id": self.id,
            "message": f"Tool {self.name} is ready"
        }


class ToolRegistry:
    """工具注册表
    
    管理所有已注册的工具
    """
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._tool_info: Dict[str, ToolInfo] = {}
    
    def register(self, tool: Tool) -> None:
        """注册工具
        
        Args:
            tool: 工具实例
        """
        if tool.id in self._tools:
            raise ValueError(f"Tool {tool.id} already registered")
        
        self._tools[tool.id] = tool
        self._tool_info[tool.id] = tool.get_info()
    
    def unregister(self, tool_id: str) -> None:
        """注销工具
        
        Args:
            tool_id: 工具ID
        """
        if tool_id not in self._tools:
            raise ValueError(f"Tool {tool_id} not found")
        
        del self._tools[tool_id]
        del self._tool_info[tool_id]
    
    def get(self, tool_id: str) -> Optional[Tool]:
        """获取工具实例"""
        return self._tools.get(tool_id)
    
    def get_info(self, tool_id: str) -> Optional[ToolInfo]:
        """获取工具信息"""
        return self._tool_info.get(tool_id)
    
    def list_all(self) -> List[ToolInfo]:
        """列出所有工具信息"""
        return list(self._tool_info.values())
    
    def list_by_category(self, category: ToolCategory) -> List[ToolInfo]:
        """按分类列出工具"""
        return [
            info for info in self._tool_info.values()
            if info.category == category
        ]
    
    def update_performance(self, tool_id: str, response_time: float, success: bool):
        """更新工具性能指标
        
        Args:
            tool_id: 工具ID
            response_time: 响应时间（毫秒）
            success: 是否成功
        """
        if tool_id in self._tool_info:
            self._tool_info[tool_id].performance.update(response_time, success)


class ToolError(Exception):
    """工具错误"""
    pass


class ToolExecutionError(ToolError):
    """工具执行错误"""
    pass


class ToolConfigError(ToolError):
    """工具配置错误"""
    pass
