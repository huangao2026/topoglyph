"""
插件管理器
管理插件的生命周期、加载、卸载和依赖管理
"""
import importlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from core.plugin import (
    Plugin, PluginType, PluginStatus, PluginInfo,
    PluginContext, PluginRegistry, PluginLoadError, PluginDependencyError
)
from core.event import EventBus, Event, EventType
from core.version import VersionManager, VersionInfo, VersionComponent, SemanticVersion


class PluginManager:
    """插件管理器
    
    功能：
    - 插件发现和加载
    - 插件依赖管理
    - 插件生命周期管理
    - 插件健康检查
    """
    
    def __init__(
        self,
        plugin_dir: str = "plugins",
        event_bus: Optional[EventBus] = None,
        version_manager: Optional[VersionManager] = None
    ):
        self._plugin_dir = Path(plugin_dir)
        self._registry = PluginRegistry()
        self._event_bus = event_bus
        self._version_manager = version_manager
        self._loaded_plugins: Dict[str, Plugin] = {}
    
    async def discover_plugins(self) -> List[PluginInfo]:
        """发现插件
        
        扫描插件目录，发现所有可用的插件
        
        Returns:
            List[PluginInfo]: 发现的插件信息列表
        """
        plugins = []
        
        if not self._plugin_dir.exists():
            return plugins
        
        # 扫描插件目录
        for plugin_path in self._plugin_dir.iterdir():
            if plugin_path.is_dir():
                plugin_info = await self._scan_plugin_directory(plugin_path)
                if plugin_info:
                    plugins.append(plugin_info)
        
        return plugins
    
    async def _scan_plugin_directory(self, plugin_path: Path) -> Optional[PluginInfo]:
        """扫描插件目录
        
        Args:
            plugin_path: 插件目录路径
            
        Returns:
            Optional[PluginInfo]: 插件信息
        """
        # 查找插件入口文件
        plugin_file = plugin_path / "plugin.py"
        if not plugin_file.exists():
            return None
        
        # 动态加载插件模块
        try:
            spec = importlib.util.spec_from_file_location(
                f"plugin_{plugin_path.name}",
                plugin_file
            )
            if spec is None or spec.loader is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 查找插件类
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type) and
                    issubclass(attr, Plugin) and
                    attr != Plugin and
                    hasattr(attr, 'id') and attr.id
                ):
                    plugin_instance = attr()
                    plugin_info = plugin_instance.get_info()
                    return plugin_info
            
        except Exception as e:
            print(f"Error scanning plugin {plugin_path}: {e}")
        
        return None
    
    async def load_plugin(
        self,
        plugin_id: str,
        context: PluginContext
    ) -> bool:
        """加载插件
        
        Args:
            plugin_id: 插件ID
            context: 插件上下文
            
        Returns:
            bool: 是否加载成功
        """
        # 检查是否已加载
        if plugin_id in self._loaded_plugins:
            print(f"Plugin {plugin_id} already loaded")
            return False
        
        # 查找插件
        plugin = self._registry.get(plugin_id)
        if not plugin:
            # 尝试从文件系统加载
            plugin = await self._load_plugin_from_file(plugin_id)
            if not plugin:
                raise PluginLoadError(f"Plugin {plugin_id} not found")
        
        # 检查依赖
        dependencies = plugin.dependencies
        for dep_id in dependencies:
            if dep_id not in self._loaded_plugins:
                raise PluginDependencyError(f"Dependency {dep_id} not loaded")
        
        # 加载插件
        self._registry.set_status(plugin_id, PluginStatus.LOADING)
        
        try:
            success = await plugin.load(context)
            
            if success:
                self._loaded_plugins[plugin_id] = plugin
                self._registry.set_status(plugin_id, PluginStatus.LOADED)
                
                # 注册版本
                if self._version_manager:
                    version_info = VersionInfo(
                        component=VersionComponent.PLUGIN,
                        component_id=plugin_id,
                        version=SemanticVersion.parse(plugin.version)
                    )
                    self._version_manager.register_version(version_info)
                
                # 发布事件
                if self._event_bus:
                    await self._publish_plugin_loaded(plugin)
                
                return True
            else:
                self._registry.set_status(plugin_id, PluginStatus.ERROR)
                return False
        
        except Exception as e:
            self._registry.set_status(plugin_id, PluginStatus.ERROR)
            raise PluginLoadError(f"Failed to load plugin {plugin_id}: {e}")
    
    async def _load_plugin_from_file(self, plugin_id: str) -> Optional[Plugin]:
        """从文件系统加载插件
        
        Args:
            plugin_id: 插件ID
            
        Returns:
            Optional[Plugin]: 插件实例
        """
        if not self._plugin_dir.exists():
            return None
        
        # 扫描插件目录
        for plugin_path in self._plugin_dir.iterdir():
            if plugin_path.is_dir():
                plugin_info = await self._scan_plugin_directory(plugin_path)
                if plugin_info and plugin_info.id == plugin_id:
                    # 注册插件
                    plugin_file = plugin_path / "plugin.py"
                    spec = importlib.util.spec_from_file_location(
                        f"plugin_{plugin_path.name}",
                        plugin_file
                    )
                    if spec is None or spec.loader is None:
                        continue
                    
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 查找插件类
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type) and
                            issubclass(attr, Plugin) and
                            attr != Plugin and
                            hasattr(attr, 'id') and attr.id == plugin_id
                        ):
                            plugin_instance = attr()
                            self._registry.register(plugin_instance)
                            return plugin_instance
        
        return None
    
    async def unload_plugin(self, plugin_id: str) -> bool:
        """卸载插件
        
        Args:
            plugin_id: 插件ID
            
        Returns:
            bool: 是否卸载成功
        """
        plugin = self._loaded_plugins.get(plugin_id)
        if not plugin:
            return False
        
        try:
            success = await plugin.unload()
            
            if success:
                del self._loaded_plugins[plugin_id]
                self._registry.set_status(plugin_id, PluginStatus.UNLOADED)
                
                # 发布事件
                if self._event_bus:
                    await self._publish_plugin_unloaded(plugin)
                
                return True
            else:
                return False
        
        except Exception as e:
            print(f"Error unloading plugin {plugin_id}: {e}")
            return False
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """获取插件实例"""
        return self._loaded_plugins.get(plugin_id)
    
    def get_plugin_info(self, plugin_id: str) -> Optional[PluginInfo]:
        """获取插件信息"""
        plugin = self._registry.get(plugin_id)
        if plugin:
            return plugin.get_info()
        return None
    
    def list_plugins(
        self,
        plugin_type: Optional[PluginType] = None,
        status: Optional[PluginStatus] = None
    ) -> List[PluginInfo]:
        """列出插件
        
        Args:
            plugin_type: 插件类型过滤
            status: 插件状态过滤
            
        Returns:
            List[PluginInfo]: 插件信息列表
        """
        plugins = self._registry.list_all()
        
        if plugin_type:
            plugins = [p for p in plugins if p.get_info().plugin_type == plugin_type]
        
        if status:
            plugins = [
                p for p in plugins
                if self._registry.get_status(p.id) == status
            ]
        
        return [p.get_info() for p in plugins]
    
    async def reload_plugin(self, plugin_id: str, context: PluginContext) -> bool:
        """重新加载插件
        
        Args:
            plugin_id: 插件ID
            context: 插件上下文
            
        Returns:
            bool: 是否重载成功
        """
        # 先卸载
        await self.unload_plugin(plugin_id)
        
        # 再加载
        return await self.load_plugin(plugin_id, context)
    
    async def check_plugin_health(self, plugin_id: str) -> Dict[str, Any]:
        """检查插件健康状态
        
        Args:
            plugin_id: 插件ID
            
        Returns:
            Dict: 健康状态
        """
        plugin = self._loaded_plugins.get(plugin_id)
        if not plugin:
            return {
                "status": "unhealthy",
                "message": f"Plugin {plugin_id} not loaded"
            }
        
        try:
            return await plugin.health_check()
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Health check failed: {e}"
            }
    
    async def health_check_all(self) -> Dict[str, Any]:
        """检查所有插件的健康状态"""
        plugins = self.list_plugins()
        
        results = {
            "total_plugins": len(plugins),
            "healthy": 0,
            "unhealthy": 0,
            "details": {}
        }
        
        for plugin_info in plugins:
            health = await self.check_plugin_health(plugin_info.id)
            results["details"][plugin_info.id] = health
            
            if health.get("status") == "healthy":
                results["healthy"] += 1
            else:
                results["unhealthy"] += 1
        
        return results
    
    async def _publish_plugin_loaded(self, plugin: Plugin):
        """发布插件加载事件"""
        event = Event(
            type=EventType.PLUGIN_LOADED,
            data={
                "plugin_id": plugin.id,
                "plugin_name": plugin.name,
                "version": plugin.version,
                "plugin_type": plugin.plugin_type.value
            },
            source="PluginManager"
        )
        await self._event_bus.publish(event)
    
    async def _publish_plugin_unloaded(self, plugin: Plugin):
        """发布插件卸载事件"""
        event = Event(
            type=EventType.PLUGIN_UNLOADED,
            data={
                "plugin_id": plugin.id,
                "plugin_name": plugin.name
            },
            source="PluginManager"
        )
        await self._event_bus.publish(event)
    
    def get_plugin_dir(self) -> Path:
        """获取插件目录"""
        return self._plugin_dir
