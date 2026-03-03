"""
插件基类和接口定义
支持工具、模型、存储、监控等多种插件类型
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Callable


class PluginType(Enum):
    """插件类型"""
    TOOL = "tool"           # 工具插件
    MODEL = "model"         # 模型插件
    STORAGE = "storage"     # 存储插件
    MONITOR = "monitor"     # 监控插件
    ANALYSIS = "analysis"   # 分析插件


class PluginStatus(Enum):
    """插件状态"""
    LOADED = "loaded"               # 已加载
    UNLOADED = "unloaded"           # 已卸载
    ERROR = "error"                 # 错误
    LOADING = "loading"             # 加载中


@dataclass
class PluginInfo:
    """插件信息"""
    id: str                         # 插件唯一标识
    name: str                       # 插件名称
    version: str                    # 插件版本（语义化版本）
    author: str                     # 作者
    description: str                # 描述
    plugin_type: PluginType         # 插件类型
    dependencies: List[str] = field(default_factory=list)  # 依赖的插件ID
    config_schema: Dict[str, Any] = field(default_factory=dict)  # 配置模式
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class PluginContext:
    """插件上下文"""
    tool_manager: Any               # 工具管理器
    memory_manager: Any             # 记忆管理器
    config: Dict[str, Any]          # 插件配置
    event_bus: Any                  # 事件总线
    logger: Any                     # 日志器


class Plugin(ABC):
    """插件基类
    
    所有插件必须继承此类并实现相关方法。
    
    示例:
        class MyToolPlugin(Plugin):
            id = "my-tool"
            name = "我的工具"
            version = "1.0.0"
            plugin_type = PluginType.TOOL
            
            async def load(self, context: PluginContext):
                # 加载插件逻辑
                pass
                
            async def unload(self):
                # 卸载插件逻辑
                pass
    """
    
    # 必须在子类中定义的属性
    id: str = ""
    name: str = ""
    version: str = ""
    plugin_type: PluginType = PluginType.TOOL
    
    # 可选属性
    author: str = ""
    description: str = ""
    dependencies: List[str] = []
    config_schema: Dict[str, Any] = {}
    
    def __post_init__(self):
        """初始化后检查必要属性"""
        if not all([self.id, self.name, self.version]):
            raise ValueError(f"Plugin {self.__class__.__name__} must define id, name and version")
    
    @abstractmethod
    async def load(self, context: PluginContext) -> bool:
        """加载插件
        
        Args:
            context: 插件上下文，包含各种管理器和配置
            
        Returns:
            bool: 加载是否成功
        """
        pass
    
    @abstractmethod
    async def unload(self) -> bool:
        """卸载插件
        
        Returns:
            bool: 卸载是否成功
        """
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查
        
        Returns:
            Dict: 健康状态信息
                {
                    "status": "healthy" | "unhealthy" | "degraded",
                    "message": str,
                    "details": Dict
                }
        """
        return {
            "status": "healthy",
            "message": f"Plugin {self.id} is running",
            "details": {}
        }
    
    def get_info(self) -> PluginInfo:
        """获取插件信息"""
        return PluginInfo(
            id=self.id,
            name=self.name,
            version=self.version,
            author=self.author,
            description=self.description,
            plugin_type=self.plugin_type,
            dependencies=self.dependencies,
            config_schema=self.config_schema
        )
    
    async def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证插件配置
        
        Args:
            config: 配置字典
            
        Returns:
            bool: 配置是否有效
        """
        if not self.config_schema:
            return True
        # TODO: 实现基于 schema 的配置验证
        return True


class PluginRegistry:
    """插件注册表
    
    管理所有已注册的插件
    """
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._plugin_status: Dict[str, PluginStatus] = {}
    
    def register(self, plugin: Plugin) -> None:
        """注册插件
        
        Args:
            plugin: 插件实例
        """
        if plugin.id in self._plugins:
            raise ValueError(f"Plugin {plugin.id} already registered")
        
        self._plugins[plugin.id] = plugin
        self._plugin_status[plugin.id] = PluginStatus.UNLOADED
    
    def unregister(self, plugin_id: str) -> None:
        """注销插件
        
        Args:
            plugin_id: 插件ID
        """
        if plugin_id not in self._plugins:
            raise ValueError(f"Plugin {plugin_id} not found")
        
        del self._plugins[plugin_id]
        del self._plugin_status[plugin_id]
    
    def get(self, plugin_id: str) -> Optional[Plugin]:
        """获取插件"""
        return self._plugins.get(plugin_id)
    
    def get_status(self, plugin_id: str) -> Optional[PluginStatus]:
        """获取插件状态"""
        return self._plugin_status.get(plugin_id)
    
    def list_all(self) -> List[Plugin]:
        """列出所有插件"""
        return list(self._plugins.values())
    
    def list_by_type(self, plugin_type: PluginType) -> List[Plugin]:
        """按类型列出插件"""
        return [
            p for p in self._plugins.values()
            if p.plugin_type == plugin_type
        ]
    
    def set_status(self, plugin_id: str, status: PluginStatus) -> None:
        """设置插件状态"""
        if plugin_id not in self._plugin_status:
            raise ValueError(f"Plugin {plugin_id} not found")
        self._plugin_status[plugin_id] = status


class PluginLoadError(Exception):
    """插件加载错误"""
    pass


class PluginDependencyError(Exception):
    """插件依赖错误"""
    pass
