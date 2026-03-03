"""
智能体引擎
古文字破译系统的核心，整合所有功能模块
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers

from core.tool import Tool, ToolInput, ToolOutput, ToolCategory
from core.memory import Memory, MemoryType, Session, DialogueMessage, MemoryQuery
from core.event import EventBus, Event, EventType
from services.tool_manager import ToolManager
from services.plugin_manager import PluginManager
from core.memory import ShortTermMemoryManager, LongTermMemoryManager
from core.version import VersionManager
import json
import os
from typing import Annotated


class DeciphermentEngine:
    """古文字破译引擎
    
    核心功能：
    - 文本分析和破译
    - 图像识别和符号分析
    - 多模态推理
    - 工具调用和协调
    - 对话管理
    """
    
    def __init__(
        self,
        llm: ChatOpenAI,
        tool_manager: ToolManager,
        plugin_manager: PluginManager,
        event_bus: EventBus,
        memory_manager: Any,
        version_manager: Optional[VersionManager] = None
    ):
        self._llm = llm
        self._tool_manager = tool_manager
        self._plugin_manager = plugin_manager
        self._event_bus = event_bus
        self._memory_manager = memory_manager
        self._version_manager = version_manager
        
        # 初始化 LangChain Agent
        self._agent = None
        self._checkpointer = None
    
    async def initialize(self):
        """初始化引擎"""
        # 加载配置
        config_path = os.path.join(
            os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"),
            "config/agent_llm_config.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        
        # 创建 Agent
        from storage.memory.memory_saver import get_memory_saver
        
        MAX_MESSAGES = 40
        
        def _windowed_messages(old, new):
            """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
            return add_messages(old, new)[-MAX_MESSAGES:]
        
        class AgentState(MessagesState):
            messages: Annotated[list[AnyMessage], _windowed_messages]
        
        self._checkpointer = get_memory_saver()
        
        # 获取所有工具
        tools = []
        tool_infos = self._tool_manager.list_tools()
        for tool_info in tool_infos:
            tool_instance = self._tool_manager.get_tool(tool_info.id)
            if tool_instance:
                # 将 Tool 转换为 LangChain Tool
                from langchain.tools import tool as langchain_tool
                
                @langchain_tool
                async def execute_tool_wrapper(input_data: str, runtime=None) -> str:
                    """执行破译工具"""
                    # 解析输入
                    import json
                    try:
                        data = json.loads(input_data)
                        tool_input = ToolInput(
                            text=data.get("text"),
                            parameters=data.get("parameters", {})
                        )
                        result = await tool_instance.execute(tool_input)
                        return result.to_dict()
                    except Exception as e:
                        return json.dumps({"success": False, "error": str(e)})
                
                execute_tool_wrapper.name = tool_info.id
                execute_tool_wrapper.description = tool_info.description
                tools.append(execute_tool_wrapper)
        
        # 创建 Agent
        self._agent = create_agent(
            model=self._llm,
            system_prompt=cfg.get("sp", "You are an ancient script decipherment expert."),
            tools=tools,
            checkpointer=self._checkpointer,
            state_schema=AgentState,
        )
    
    async def analyze_text(
        self,
        text: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """分析文本
        
        Args:
            text: 古文字文本
            session_id: 会话ID
            
        Returns:
            Dict: 分析结果
        """
        # 创建或获取会话
        if session_id:
            session = await self._memory_manager.get_session(session_id)
            if not session:
                session = await self._memory_manager.create_session(session_id)
        else:
            session_id = str(uuid.uuid4())
            session = await self._memory_manager.create_session(session_id)
        
        # 添加用户消息
        await self._memory_manager.add_message(
            session_id,
            "user",
            f"请分析这段古文字：{text}"
        )
        
        # 发布分析开始事件
        analysis_id = str(uuid.uuid4())
        await self._event_bus.publish(Event(
            type=EventType.ANALYSIS_STARTED,
            data={"analysis_id": analysis_id, "input_type": "text"},
            source="DeciphermentEngine"
        ))
        
        try:
            # 获取最近的消息历史
            history = await self._memory_manager.get_recent_messages(session_id, 20)
            
            # 构造消息列表
            messages = []
            for msg in history:
                if msg.role == "user":
                    messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    messages.append({"role": "assistant", "content": msg.content})
            
            # 调用 Agent
            config = {"configurable": {"thread_id": session_id}}
            result = await self._agent.ainvoke(
                {"messages": messages[-1:]},
                config=config
            )
            
            # 提取响应
            response_text = result["messages"][-1].content if result["messages"] else ""
            
            # 添加助手消息
            await self._memory_manager.add_message(
                session_id,
                "assistant",
                response_text
            )
            
            # 发布分析完成事件
            await self._event_bus.publish(Event(
                type=EventType.ANALYSIS_COMPLETED,
                data={
                    "analysis_id": analysis_id,
                    "result": {"response": response_text}
                },
                source="DeciphermentEngine"
            ))
            
            return {
                "success": True,
                "session_id": session_id,
                "analysis_id": analysis_id,
                "response": response_text,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            # 发布分析失败事件
            await self._event_bus.publish(Event(
                type=EventType.ANALYSIS_FAILED,
                data={
                    "analysis_id": analysis_id,
                    "error": str(e)
                },
                source="DeciphermentEngine"
            ))
            
            return {
                "success": False,
                "session_id": session_id,
                "analysis_id": analysis_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def analyze_image(
        self,
        image_data: bytes,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """分析图像
        
        Args:
            image_data: 图像数据
            session_id: 会话ID
            
        Returns:
            Dict: 分析结果
        """
        # 创建或获取会话
        if session_id:
            session = await self._memory_manager.get_session(session_id)
            if not session:
                session = await self._memory_manager.create_session(session_id)
        else:
            session_id = str(uuid.uuid4())
            session = await self._memory_manager.create_session(session_id)
        
        # 添加用户消息
        await self._memory_manager.add_message(
            session_id,
            "user",
            f"[上传了一张图片]请识别和分析这张图片中的古文字"
        )
        
        # 发布分析开始事件
        analysis_id = str(uuid.uuid4())
        await self._event_bus.publish(Event(
            type=EventType.ANALYSIS_STARTED,
            data={"analysis_id": analysis_id, "input_type": "image"},
            source="DeciphermentEngine"
        ))
        
        try:
            # 查找图像识别工具
            tools = self._tool_manager.list_tools(category=ToolCategory.RECOGNITION)
            
            if tools:
                # 使用第一个可用的识别工具
                tool_id = tools[0].id
                tool_instance = self._tool_manager.get_tool(tool_id)
                
                if tool_instance:
                    # 执行识别
                    tool_input = ToolInput(image=image_data)
                    recognition_result = await tool_instance.execute(tool_input)
                    
                    if recognition_result.success:
                        # 将识别结果传递给 Agent 进行分析
                        recognition_text = recognition_result.result or ""
                        
                        await self._memory_manager.add_message(
                            session_id,
                            "system",
                            f"图像识别结果：{recognition_text}"
                        )
        
            # 获取最近的消息历史
            history = await self._memory_manager.get_recent_messages(session_id, 20)
            
            # 构造消息列表
            messages = []
            for msg in history:
                if msg.role == "user":
                    messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    messages.append({"role": "assistant", "content": msg.content})
                elif msg.role == "system":
                    messages.append({"role": "system", "content": msg.content})
            
            # 调用 Agent
            config = {"configurable": {"thread_id": session_id}}
            result = await self._agent.ainvoke(
                {"messages": messages[-1:]},
                config=config
            )
            
            # 提取响应
            response_text = result["messages"][-1].content if result["messages"] else ""
            
            # 添加助手消息
            await self._memory_manager.add_message(
                session_id,
                "assistant",
                response_text
            )
            
            # 发布分析完成事件
            await self._event_bus.publish(Event(
                type=EventType.ANALYSIS_COMPLETED,
                data={
                    "analysis_id": analysis_id,
                    "result": {"response": response_text}
                },
                source="DeciphermentEngine"
            ))
            
            return {
                "success": True,
                "session_id": session_id,
                "analysis_id": analysis_id,
                "response": response_text,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            # 发布分析失败事件
            await self._event_bus.publish(Event(
                type=EventType.ANALYSIS_FAILED,
                data={
                    "analysis_id": analysis_id,
                    "error": str(e)
                },
                source="DeciphermentEngine"
            ))
            
            return {
                "success": False,
                "session_id": session_id,
                "analysis_id": analysis_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def chat(
        self,
        message: str,
        session_id: str
    ) -> Dict[str, Any]:
        """对话交互
        
        Args:
            message: 用户消息
            session_id: 会话ID
            
        Returns:
            Dict: 响应结果
        """
        # 添加用户消息
        await self._memory_manager.add_message(
            session_id,
            "user",
            message
        )
        
        try:
            # 获取最近的消息历史
            history = await self._memory_manager.get_recent_messages(session_id, 20)
            
            # 构造消息列表
            messages = []
            for msg in history:
                if msg.role == "user":
                    messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    messages.append({"role": "assistant", "content": msg.content})
            
            # 调用 Agent
            config = {"configurable": {"thread_id": session_id}}
            result = await self._agent.ainvoke(
                {"messages": messages[-1:]},
                config=config
            )
            
            # 提取响应
            response_text = result["messages"][-1].content if result["messages"] else ""
            
            # 添加助手消息
            await self._memory_manager.add_message(
                session_id,
                "assistant",
                response_text
            )
            
            return {
                "success": True,
                "session_id": session_id,
                "response": response_text,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_session_history(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        """获取会话历史"""
        session = await self._memory_manager.get_session(session_id)
        if not session:
            return []
        
        return [msg.to_dict() for msg in session.messages]
