"""
事件总线
支持发布-订阅模式，实现模块间解耦通信
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import asyncio
import json


class EventType(Enum):
    """事件类型"""
    # 工具相关事件
    TOOL_REGISTERED = "tool_registered"
    TOOL_UNREGISTERED = "tool_unregistered"
    TOOL_CALLED = "tool_called"
    TOOL_ERROR = "tool_error"
    
    # 插件相关事件
    PLUGIN_LOADED = "plugin_loaded"
    PLUGIN_UNLOADED = "plugin_unloaded"
    PLUGIN_ERROR = "plugin_error"
    
    # 记忆相关事件
    MEMORY_ADDED = "memory_added"
    MEMORY_RETRIEVED = "memory_retrieved"
    MEMORY_DELETED = "memory_deleted"
    
    # 会话相关事件
    SESSION_CREATED = "session_created"
    SESSION_UPDATED = "session_updated"
    SESSION_DELETED = "session_deleted"
    
    # 分析相关事件
    ANALYSIS_STARTED = "analysis_started"
    ANALYSIS_COMPLETED = "analysis_completed"
    ANALYSIS_FAILED = "analysis_failed"
    
    # 系统相关事件
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    SYSTEM_ERROR = "system_error"
    
    # 自定义事件
    CUSTOM = "custom"


@dataclass
class Event:
    """事件"""
    type: EventType                 # 事件类型
    data: Dict[str, Any] = field(default_factory=dict)  # 事件数据
    timestamp: datetime = field(default_factory=datetime.now)  # 时间戳
    source: Optional[str] = None    # 事件源
    event_id: Optional[str] = None  # 事件ID
    
    def __post_init__(self):
        """初始化后生成事件ID"""
        if not self.event_id:
            import uuid
            self.event_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_id": self.event_id,
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """从字典创建"""
        return cls(
            event_id=data.get("event_id"),
            type=EventType(data["type"]),
            data=data.get("data", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            source=data.get("source")
        )


@dataclass
class EventHandler:
    """事件处理器"""
    callback: Callable[[Event], None]  # 回调函数
    filter_func: Optional[Callable[[Event], bool]] = None  # 过滤函数
    async_handler: bool = False        # 是否为异步处理器
    priority: int = 0                  # 优先级（数值越大优先级越高）


class EventBus:
    """事件总线
    
    实现发布-订阅模式，支持同步和异步事件处理
    """
    
    def __init__(self):
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._event_history: List[Event] = []  # 事件历史
        self._max_history_size: int = 1000     # 最大历史记录数
        self._lock = asyncio.Lock()
    
    def subscribe(
        self,
        event_type: EventType,
        handler: Callable[[Event], None],
        async_handler: bool = False,
        priority: int = 0,
        filter_func: Optional[Callable[[Event], bool]] = None
    ):
        """订阅事件
        
        Args:
            event_type: 事件类型
            handler: 处理函数
            async_handler: 是否为异步处理函数
            priority: 优先级
            filter_func: 过滤函数，返回True则处理该事件
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        event_handler = EventHandler(
            callback=handler,
            async_handler=async_handler,
            priority=priority,
            filter_func=filter_func
        )
        
        self._handlers[event_type].append(event_handler)
        
        # 按优先级排序
        self._handlers[event_type].sort(key=lambda h: h.priority, reverse=True)
    
    def unsubscribe(
        self,
        event_type: EventType,
        handler: Callable[[Event], None]
    ):
        """取消订阅
        
        Args:
            event_type: 事件类型
            handler: 处理函数
        """
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type]
                if h.callback != handler
            ]
    
    async def publish(self, event: Event) -> int:
        """发布事件（异步）
        
        Args:
            event: 事件对象
            
        Returns:
            int: 处理器数量
        """
        async with self._lock:
            # 添加到历史记录
            self._event_history.append(event)
            
            # 限制历史记录大小
            if len(self._event_history) > self._max_history_size:
                self._event_history = self._event_history[-self._max_history_size:]
        
        # 获取该事件类型的所有处理器
        handlers = self._handlers.get(event.type, [])
        
        if not handlers:
            return 0
        
        # 执行处理器
        count = 0
        for handler in handlers:
            # 应用过滤函数
            if handler.filter_func and not handler.filter_func(event):
                continue
            
            try:
                if handler.async_handler:
                    await handler.callback(event)
                else:
                    handler.callback(event)
                count += 1
            except Exception as e:
                # 打印错误日志，但不影响其他处理器
                print(f"Error in event handler: {e}")
        
        return count
    
    def publish_sync(self, event: Event) -> int:
        """发布事件（同步）
        
        Args:
            event: 事件对象
            
        Returns:
            int: 处理器数量
        """
        # 获取该事件类型的所有处理器
        handlers = self._handlers.get(event.type, [])
        
        if not handlers:
            return 0
        
        # 执行处理器
        count = 0
        for handler in handlers:
            # 应用过滤函数
            if handler.filter_func and not handler.filter_func(event):
                continue
            
            try:
                handler.callback(event)
                count += 1
            except Exception as e:
                # 打印错误日志，但不影响其他处理器
                print(f"Error in event handler: {e}")
        
        return count
    
    def get_event_history(
        self,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[Event]:
        """获取事件历史
        
        Args:
            event_type: 事件类型过滤
            limit: 返回数量限制
            
        Returns:
            List[Event]: 事件列表
        """
        history = self._event_history
        
        # 过滤事件类型
        if event_type:
            history = [e for e in history if e.type == event_type]
        
        # 返回最近的N条记录
        return history[-limit:]
    
    def clear_history(self):
        """清空事件历史"""
        self._event_history = []
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            "total_handlers": sum(len(handlers) for handlers in self._handlers.values()),
            "handlers_by_type": {
                event_type.value: len(handlers)
                for event_type, handlers in self._handlers.items()
            },
            "total_events": len(self._event_history),
            "event_types_count": len(self._handlers)
        }
        return stats


class EventPublisher:
    """事件发布器辅助类
    
    提供便捷的事件发布方法
    """
    
    def __init__(self, event_bus: EventBus, source: Optional[str] = None):
        self._event_bus = event_bus
        self._source = source
    
    async def publish_tool_registered(self, tool_id: str, tool_name: str):
        """发布工具注册事件"""
        event = Event(
            type=EventType.TOOL_REGISTERED,
            data={"tool_id": tool_id, "tool_name": tool_name},
            source=self._source
        )
        await self._event_bus.publish(event)
    
    async def publish_tool_called(self, tool_id: str, success: bool, response_time: float):
        """发布工具调用事件"""
        event = Event(
            type=EventType.TOOL_CALLED,
            data={
                "tool_id": tool_id,
                "success": success,
                "response_time": response_time
            },
            source=self._source
        )
        await self._event_bus.publish(event)
    
    async def publish_plugin_loaded(self, plugin_id: str, plugin_name: str):
        """发布插件加载事件"""
        event = Event(
            type=EventType.PLUGIN_LOADED,
            data={"plugin_id": plugin_id, "plugin_name": plugin_name},
            source=self._source
        )
        await self._event_bus.publish(event)
    
    async def publish_analysis_started(self, analysis_id: str, input_type: str):
        """发布分析开始事件"""
        event = Event(
            type=EventType.ANALYSIS_STARTED,
            data={"analysis_id": analysis_id, "input_type": input_type},
            source=self._source
        )
        await self._event_bus.publish(event)
    
    async def publish_analysis_completed(self, analysis_id: str, result: Dict[str, Any]):
        """发布分析完成事件"""
        event = Event(
            type=EventType.ANALYSIS_COMPLETED,
            data={"analysis_id": analysis_id, "result": result},
            source=self._source
        )
        await self._event_bus.publish(event)
    
    async def publish_custom(self, event_type: str, data: Dict[str, Any]):
        """发布自定义事件"""
        event = Event(
            type=EventType.CUSTOM,
            data={"custom_type": event_type, **data},
            source=self._source
        )
        await self._event_bus.publish(event)


# 全局事件总线实例
_global_event_bus: Optional[EventBus] = None


def get_global_event_bus() -> EventBus:
    """获取全局事件总线实例"""
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def set_global_event_bus(event_bus: EventBus):
    """设置全局事件总线实例"""
    global _global_event_bus
    _global_event_bus = event_bus
