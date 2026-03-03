"""
工具管理器
管理所有破译工具的生命周期、调用、性能监控和推荐
"""
import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from core.tool import (
    Tool, ToolCategory, ToolStatus, ToolInfo,
    ToolInput, ToolOutput, ToolRegistry, ToolError
)
from core.event import EventBus, Event, EventType
from core.version import VersionManager, VersionInfo, VersionComponent, SemanticVersion


class ToolManager:
    """工具管理器
    
    功能：
    - 工具注册和发现
    - 工具调用和监控
    - 工具性能评估
    - 工具推荐
    - 工具版本管理
    """
    
    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
        version_manager: Optional[VersionManager] = None
    ):
        self._registry = ToolRegistry()
        self._event_bus = event_bus
        self._version_manager = version_manager
        self._tool_instances: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> ToolInfo:
        """注册工具
        
        Args:
            tool: 工具实例
            
        Returns:
            ToolInfo: 工具信息
        """
        self._registry.register(tool)
        self._tool_instances[tool.id] = tool
        
        # 注册版本
        if self._version_manager:
            version_info = VersionInfo(
                component=VersionComponent.TOOL,
                component_id=tool.id,
                version=SemanticVersion.parse(tool.version)
            )
            self._version_manager.register_version(version_info)
        
        # 发布事件
        if self._event_bus:
            asyncio.create_task(self._publish_tool_registered(tool))
        
        return tool.get_info()
    
    def unregister_tool(self, tool_id: str):
        """注销工具"""
        if tool_id in self._tool_instances:
            del self._tool_instances[tool_id]
            self._registry.unregister(tool_id)
    
    def get_tool(self, tool_id: str) -> Optional[Tool]:
        """获取工具实例"""
        return self._tool_instances.get(tool_id)
    
    def get_tool_info(self, tool_id: str) -> Optional[ToolInfo]:
        """获取工具信息"""
        return self._registry.get_info(tool_id)
    
    def list_tools(
        self,
        category: Optional[ToolCategory] = None,
        status: Optional[ToolStatus] = None
    ) -> List[ToolInfo]:
        """列出工具
        
        Args:
            category: 工具分类过滤
            status: 工具状态过滤
            
        Returns:
            List[ToolInfo]: 工具信息列表
        """
        tools = self._registry.list_all()
        
        if category:
            tools = [t for t in tools if t.category == category]
        
        if status:
            tools = [t for t in tools if t.status == status]
        
        return tools
    
    async def execute_tool(
        self,
        tool_id: str,
        input_data: ToolInput
    ) -> ToolOutput:
        """执行工具
        
        Args:
            tool_id: 工具ID
            input_data: 输入数据
            
        Returns:
            ToolOutput: 输出结果
        """
        tool = self.get_tool(tool_id)
        if not tool:
            return ToolOutput(
                success=False,
                error=f"Tool {tool_id} not found"
            )
        
        start_time = time.time()
        
        try:
            # 验证输入
            if not await tool.validate_input(input_data):
                return ToolOutput(
                    success=False,
                    error="Invalid input data"
                )
            
            # 执行工具
            result = await tool.execute(input_data)
            
            # 更新性能指标
            response_time = (time.time() - start_time) * 1000  # 转换为毫秒
            self._registry.update_performance(tool_id, response_time, result.success)
            
            # 发布事件
            if self._event_bus:
                await self._publish_tool_called(tool_id, result.success, response_time)
            
            return result
        
        except Exception as e:
            # 记录错误
            response_time = (time.time() - start_time) * 1000
            self._registry.update_performance(tool_id, response_time, False)
            
            # 发布错误事件
            if self._event_bus:
                await self._publish_tool_error(tool_id, str(e))
            
            return ToolOutput(
                success=False,
                error=f"Tool execution error: {str(e)}"
            )
    
    async def batch_execute(
        self,
        tool_id: str,
        inputs: List[ToolInput]
    ) -> List[ToolOutput]:
        """批量执行工具
        
        Args:
            tool_id: 工具ID
            inputs: 输入数据列表
            
        Returns:
            List[ToolOutput]: 输出结果列表
        """
        tasks = [self.execute_tool(tool_id, inp) for inp in inputs]
        return await asyncio.gather(*tasks)
    
    def recommend_tools(
        self,
        requirements: List[str],
        category: Optional[ToolCategory] = None,
        limit: int = 5
    ) -> List[ToolInfo]:
        """推荐工具
        
        根据需求和能力匹配推荐合适的工具
        
        Args:
            requirements: 需求列表
            category: 工具分类
            limit: 返回数量限制
            
        Returns:
            List[ToolInfo]: 推荐的工具列表
        """
        tools = self.list_tools(category, ToolStatus.ACTIVE)
        
        # 计算匹配分数
        scored_tools = []
        for tool in tools:
            score = self._calculate_match_score(tool, requirements)
            if score > 0:
                scored_tools.append((tool, score))
        
        # 按分数排序
        scored_tools.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前N个
        return [tool for tool, score in scored_tools[:limit]]
    
    def _calculate_match_score(self, tool: ToolInfo, requirements: List[str]) -> float:
        """计算工具匹配分数
        
        Args:
            tool: 工具信息
            requirements: 需求列表
            
        Returns:
            float: 匹配分数 (0-1)
        """
        score = 0.0
        requirements_lower = [r.lower() for r in requirements]
        
        # 检查能力匹配
        for capability in tool.capabilities:
            capability_lower = capability.lower()
            for requirement in requirements_lower:
                if requirement in capability_lower or capability_lower in requirement:
                    score += 0.3
        
        # 检查描述匹配
        description_lower = tool.description.lower()
        for requirement in requirements_lower:
            if requirement in description_lower:
                score += 0.2
        
        # 检查名称匹配
        name_lower = tool.name.lower()
        for requirement in requirements_lower:
            if requirement in name_lower:
                score += 0.5
        
        # 归一化分数到 [0, 1]
        return min(score, 1.0)
    
    def get_tool_stats(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """获取工具统计信息"""
        tool_info = self.get_tool_info(tool_id)
        if not tool_info:
            return None
        
        return {
            "tool_id": tool_id,
            "name": tool_info.name,
            "version": tool_info.version,
            "category": tool_info.category.value,
            "status": tool_info.status.value,
            "performance": tool_info.performance.to_dict(),
            "capabilities": tool_info.capabilities
        }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """获取所有工具的统计信息"""
        tools = self.list_tools()
        
        stats = {
            "total_tools": len(tools),
            "by_category": {},
            "by_status": {},
            "tools": []
        }
        
        for tool in tools:
            # 按分类统计
            category = tool.category.value
            if category not in stats["by_category"]:
                stats["by_category"][category] = 0
            stats["by_category"][category] += 1
            
            # 按状态统计
            status = tool.status.value
            if status not in stats["by_status"]:
                stats["by_status"][status] = 0
            stats["by_status"][status] += 1
            
            # 添加工具统计
            stats["tools"].append(self.get_tool_stats(tool.id))
        
        return stats
    
    async def _publish_tool_registered(self, tool: Tool):
        """发布工具注册事件"""
        event = Event(
            type=EventType.TOOL_REGISTERED,
            data={
                "tool_id": tool.id,
                "tool_name": tool.name,
                "version": tool.version,
                "category": tool.category.value
            },
            source="ToolManager"
        )
        await self._event_bus.publish(event)
    
    async def _publish_tool_called(self, tool_id: str, success: bool, response_time: float):
        """发布工具调用事件"""
        event = Event(
            type=EventType.TOOL_CALLED,
            data={
                "tool_id": tool_id,
                "success": success,
                "response_time": response_time
            },
            source="ToolManager"
        )
        await self._event_bus.publish(event)
    
    async def _publish_tool_error(self, tool_id: str, error_msg: str):
        """发布工具错误事件"""
        event = Event(
            type=EventType.TOOL_ERROR,
            data={
                "tool_id": tool_id,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            },
            source="ToolManager"
        )
        await self._event_bus.publish(event)
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        tools = self.list_tools()
        
        healthy_count = 0
        unhealthy_count = 0
        
        for tool in tools:
            try:
                health = await self.get_tool(tool.id).health_check()
                if health.get("status") == "healthy":
                    healthy_count += 1
                else:
                    unhealthy_count += 1
            except Exception:
                unhealthy_count += 1
        
        return {
            "status": "healthy" if unhealthy_count == 0 else "degraded",
            "total_tools": len(tools),
            "healthy_tools": healthy_count,
            "unhealthy_tools": unhealthy_count,
            "timestamp": datetime.now().isoformat()
        }
