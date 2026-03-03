"""
记忆管理系统
支持短期记忆（对话历史）和长期记忆（知识库、用户偏好）
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import json


class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"       # 短期记忆（对话历史）
    LONG_TERM = "long_term"         # 长期记忆（知识库）
    PREFERENCE = "preference"       # 偏好记忆
    HISTORY = "history"             # 历史记录


@dataclass
class Memory:
    """记忆基类"""
    id: str                         # 记忆ID
    type: MemoryType                # 记忆类型
    content: str                    # 记忆内容
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    embedding: Optional[List[float]] = None  # 向量嵌入（用于检索）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class DialogueMessage:
    """对话消息"""
    role: str                       # role: "user" | "assistant" | "system"
    content: str                    # 消息内容
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogueMessage':
        """从字典创建"""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


@dataclass
class Session:
    """会话"""
    id: str                         # 会话ID
    user_id: Optional[str] = None   # 用户ID
    messages: List[DialogueMessage] = field(default_factory=list)  # 消息列表
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_message(self, message: DialogueMessage):
        """添加消息"""
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def get_recent_messages(self, count: int = 10) -> List[DialogueMessage]:
        """获取最近的消息"""
        return self.messages[-count:] if len(self.messages) > count else self.messages
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """从字典创建"""
        return cls(
            id=data["id"],
            user_id=data.get("user_id"),
            messages=[DialogueMessage.from_dict(msg) for msg in data.get("messages", [])],
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )


@dataclass
class MemoryQuery:
    """记忆查询"""
    query_text: str                 # 查询文本
    memory_type: Optional[MemoryType] = None  # 记忆类型过滤
    limit: int = 10                 # 返回数量限制
    threshold: float = 0.7          # 相似度阈值
    filters: Dict[str, Any] = field(default_factory=dict)  # 其他过滤条件


@dataclass
class MemoryStats:
    """记忆统计"""
    total_memories: int = 0         # 总记忆数
    short_term_count: int = 0       # 短期记忆数
    long_term_count: int = 0        # 长期记忆数
    preference_count: int = 0       # 偏好记忆数
    history_count: int = 0          # 历史记录数
    total_sessions: int = 0         # 总会话数
    active_sessions: int = 0        # 活跃会话数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_memories": self.total_memories,
            "short_term_count": self.short_term_count,
            "long_term_count": self.long_term_count,
            "preference_count": self.preference_count,
            "history_count": self.history_count,
            "total_sessions": self.total_sessions,
            "active_sessions": self.active_sessions
        }


class MemoryStore:
    """记忆存储基类
    
    提供记忆的存储、检索、更新和删除功能
    """
    
    def __init__(self):
        self._memories: Dict[str, Memory] = {}
        self._sessions: Dict[str, Session] = {}
    
    async def add_memory(self, memory: Memory) -> str:
        """添加记忆
        
        Args:
            memory: 记忆对象
            
        Returns:
            str: 记忆ID
        """
        self._memories[memory.id] = memory
        return memory.id
    
    async def get_memory(self, memory_id: str) -> Optional[Memory]:
        """获取记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            Optional[Memory]: 记忆对象
        """
        return self._memories.get(memory_id)
    
    async def update_memory(self, memory_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """更新记忆
        
        Args:
            memory_id: 记忆ID
            content: 新内容
            metadata: 新元数据
        """
        if memory_id in self._memories:
            memory = self._memories[memory_id]
            memory.content = content
            memory.updated_at = datetime.now()
            if metadata:
                memory.metadata.update(metadata)
    
    async def delete_memory(self, memory_id: str):
        """删除记忆
        
        Args:
            memory_id: 记忆ID
        """
        if memory_id in self._memories:
            del self._memories[memory_id]
    
    async def search_memories(self, query: MemoryQuery) -> List[Memory]:
        """搜索记忆
        
        Args:
            query: 查询条件
            
        Returns:
            List[Memory]: 匹配的记忆列表
        """
        # 简单实现：基于文本匹配
        results = []
        for memory in self._memories.values():
            # 类型过滤
            if query.memory_type and memory.type != query.memory_type:
                continue
            
            # 文本匹配
            if query.query_text.lower() in memory.content.lower():
                results.append(memory)
            
            # 数量限制
            if len(results) >= query.limit:
                break
        
        return results
    
    async def get_stats(self) -> MemoryStats:
        """获取统计信息"""
        stats = MemoryStats()
        stats.total_memories = len(self._memories)
        
        for memory in self._memories.values():
            if memory.type == MemoryType.SHORT_TERM:
                stats.short_term_count += 1
            elif memory.type == MemoryType.LONG_TERM:
                stats.long_term_count += 1
            elif memory.type == MemoryType.PREFERENCE:
                stats.preference_count += 1
            elif memory.type == MemoryType.HISTORY:
                stats.history_count += 1
        
        stats.total_sessions = len(self._sessions)
        # TODO: 计算活跃会话数
        
        return stats


class ShortTermMemoryManager:
    """短期记忆管理器
    
    管理对话历史，支持滑动窗口和上下文压缩
    """
    
    def __init__(self, max_messages: int = 40):
        self.max_messages = max_messages
        self.store = MemoryStore()
    
    async def create_session(self, session_id: str, user_id: Optional[str] = None) -> Session:
        """创建会话
        
        Args:
            session_id: 会话ID
            user_id: 用户ID
            
        Returns:
            Session: 会话对象
        """
        session = Session(id=session_id, user_id=user_id)
        self.store._sessions[session_id] = session
        return session
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        return self.store._sessions.get(session_id)
    
    async def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """添加消息到会话
        
        Args:
            session_id: 会话ID
            role: 角色
            content: 内容
            metadata: 元数据
        """
        session = await self.get_session(session_id)
        if session:
            message = DialogueMessage(role=role, content=content, metadata=metadata or {})
            session.add_message(message)
            
            # 滑动窗口：保持最近 max_messages 条消息
            if len(session.messages) > self.max_messages:
                session.messages = session.messages[-self.max_messages:]
    
    async def get_recent_messages(self, session_id: str, count: int = 10) -> List[DialogueMessage]:
        """获取最近的消息"""
        session = await self.get_session(session_id)
        if session:
            return session.get_recent_messages(count)
        return []
    
    async def compress_session(self, session_id: str) -> str:
        """压缩会话历史
        
        Args:
            session_id: 会话ID
            
        Returns:
            str: 压缩后的摘要
        """
        session = await self.get_session(session_id)
        if not session:
            return ""
        
        # 简单实现：生成摘要
        # TODO: 使用LLM生成更好的摘要
        messages = session.get_recent_messages(20)
        summary_parts = [f"{msg.role}: {msg.content[:100]}..." for msg in messages[-5:]]
        return "\n".join(summary_parts)


class LongTermMemoryManager:
    """长期记忆管理器
    
    管理知识库、用户偏好和历史记录
    """
    
    def __init__(self):
        self.store = MemoryStore()
    
    async def add_knowledge(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """添加知识
        
        Args:
            content: 知识内容
            metadata: 元数据
            
        Returns:
            str: 记忆ID
        """
        import uuid
        memory_id = str(uuid.uuid4())
        memory = Memory(
            id=memory_id,
            type=MemoryType.LONG_TERM,
            content=content,
            metadata=metadata or {}
        )
        return await self.store.add_memory(memory)
    
    async def search_knowledge(self, query: str, limit: int = 10) -> List[Memory]:
        """搜索知识
        
        Args:
            query: 查询文本
            limit: 返回数量限制
            
        Returns:
            List[Memory]: 匹配的知识列表
        """
        memory_query = MemoryQuery(
            query_text=query,
            memory_type=MemoryType.LONG_TERM,
            limit=limit
        )
        return await self.store.search_memories(memory_query)
    
    async def save_preference(self, user_id: str, preference_type: str, value: Any):
        """保存用户偏好
        
        Args:
            user_id: 用户ID
            preference_type: 偏好类型
            value: 偏好值
        """
        import uuid
        memory_id = str(uuid.uuid4())
        memory = Memory(
            id=memory_id,
            type=MemoryType.PREFERENCE,
            content=json.dumps(value),
            metadata={
                "user_id": user_id,
                "preference_type": preference_type
            }
        )
        await self.store.add_memory(memory)
    
    async def get_preference(self, user_id: str, preference_type: str) -> Optional[Any]:
        """获取用户偏好"""
        query = MemoryQuery(
            query_text="",
            memory_type=MemoryType.PREFERENCE,
            filters={
                "user_id": user_id,
                "preference_type": preference_type
            },
            limit=1
        )
        results = await self.store.search_memories(query)
        if results:
            return json.loads(results[0].content)
        return None
