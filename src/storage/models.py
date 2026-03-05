"""
数据库模型定义
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, JSON, Float, Index
)
from sqlalchemy.orm import relationship
from src.storage.database import Base

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # 可选，支持第三方登录
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    api_key = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # 关系
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Session(Base):
    """会话表"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 可选，支持匿名会话
    title = Column(String(200), default="新对话")
    metadata = Column(JSON, default={})  # 存储额外信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # 关系
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.id}, session_id='{self.session_id}')>"

class Message(Base):
    """消息表"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("sessions.session_id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' 或 'assistant'
    content = Column(Text, nullable=False)
    metadata = Column(JSON, default={})  # 存储额外信息（如图片URL、工具调用等）
    tokens = Column(Integer, default=0)  # Token 使用量
    model = Column(String(50))  # 使用的模型
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    session = relationship("Session", back_populates="messages")
    
    # 索引
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', content='{self.content[:50]}...')>"

class Conversation(Base):
    """对话记录表（扩展 Message 的功能）"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), ForeignKey("sessions.session_id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"))
    
    # 分析结果
    script_type = Column(String(100))  # 文字类型（甲骨文、埃及圣书体等）
    analysis_result = Column(Text)  # 分析结果（JSON 格式）
    confidence_score = Column(Float)  # 置信度评分
    image_url = Column(String(500))  # 图片 URL
    tools_used = Column(JSON, default=[])  # 使用的工具
    
    # 元数据
    metadata = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="conversations")
    session = relationship("Session", back_populates="conversations")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, script_type='{self.script_type}')>"

class AnalysisHistory(Base):
    """分析历史表"""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100))
    
    # 输入
    input_type = Column(String(20))  # 'text' 或 'image'
    input_content = Column(Text)  # 文本内容
    image_url = Column(String(500))  # 图片 URL
    
    # 输出
    output_content = Column(Text)  # 输出内容
    script_type = Column(String(100))  # 识别的文字类型
    confidence_score = Column(Float)  # 置信度
    
    # 工具使用
    tools_used = Column(JSON, default=[])
    model_used = Column(String(50))
    tokens_used = Column(Integer, default=0)
    
    # 性能指标
    processing_time = Column(Float)  # 处理时间（秒）
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AnalysisHistory(id={self.id}, script_type='{self.script_type}')>"

class Plugin(Base):
    """插件表"""
    __tablename__ = "plugins"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    version = Column(String(20))
    description = Column(Text)
    author = Column(String(100))
    
    # 配置
    config = Column(JSON, default={})
    enabled = Column(Boolean, default=True)
    
    # 统计
    usage_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Plugin(id={self.id}, name='{self.name}', enabled={self.enabled})>"

class Tool(Base):
    """工具表"""
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(100))
    description = Column(Text)
    category = Column(String(50))  # 类别（如：ocr、translation、analysis等）
    
    # 配置
    config = Column(JSON, default={})
    enabled = Column(Boolean, default=True)
    
    # API 配置
    api_endpoint = Column(String(500))
    api_key_required = Column(Boolean, default=False)
    
    # 统计
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Tool(id={self.id}, name='{self.name}', enabled={self.enabled})>"

class SystemLog(Base):
    """系统日志表"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), index=True)  # DEBUG, INFO, WARNING, ERROR
    message = Column(Text)
    module = Column(String(100))
    function = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100))
    
    # 额外信息
    metadata = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 索引
    __table_args__ = (
        Index('idx_level_created', 'level', 'created_at'),
    )
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}', message='{self.message[:50]}...')>"

class SystemMetrics(Base):
    """系统指标表"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), index=True, nullable=False)
    metric_value = Column(Float)
    metric_unit = Column(String(20))  # 单位
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<SystemMetrics(id={self.id}, name='{self.metric_name}', value={self.metric_value})>"
