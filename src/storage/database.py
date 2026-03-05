"""
数据库配置模块
"""
import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)

# 从环境变量获取数据库配置
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://ancient_script:ancient_script_password@localhost:5432/ancient_script'
)

# 数据库连接池配置
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 20))
DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', 10))
DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', 30))
DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', 3600))

# 创建数据库引擎
engine = None

def get_database_url() -> str:
    """获取数据库连接字符串"""
    return DATABASE_URL

def create_db_engine():
    """创建数据库引擎"""
    global engine
    
    if engine is None:
        try:
            engine = create_engine(
                DATABASE_URL,
                poolclass=QueuePool,
                pool_size=DB_POOL_SIZE,
                max_overflow=DB_MAX_OVERFLOW,
                pool_timeout=DB_POOL_TIMEOUT,
                pool_recycle=DB_POOL_RECYCLE,
                pool_pre_ping=True,  # 自动检测断开的连接
                echo=False,  # 设为 True 可打印 SQL 语句（调试用）
                future=True  # 使用 SQLAlchemy 2.0 风格
            )
            logger.info(f"数据库引擎创建成功: {DATABASE_URL}")
        except Exception as e:
            logger.error(f"创建数据库引擎失败: {e}")
            raise
    
    return engine

# 创建会话工厂
SessionLocal = None

def get_session_factory():
    """获取会话工厂"""
    global SessionLocal
    
    if SessionLocal is None:
        db_engine = create_db_engine()
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db_engine
        )
    
    return SessionLocal

# 创建基类
Base = declarative_base()

def get_db() -> Session:
    """
    获取数据库会话
    用于 FastAPI 依赖注入
    """
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    初始化数据库
    创建所有表
    """
    try:
        db_engine = create_db_engine()
        Base.metadata.create_all(bind=db_engine)
        logger.info("数据库初始化成功，所有表已创建")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

def drop_db():
    """
    删除所有表
    警告：此操作会删除所有数据！
    """
    try:
        db_engine = create_db_engine()
        Base.metadata.drop_all(bind=db_engine)
        logger.info("所有表已删除")
    except Exception as e:
        logger.error(f"删除数据库表失败: {e}")
        raise

def check_db_connection() -> bool:
    """
    检查数据库连接
    """
    try:
        db_engine = create_db_engine()
        with db_engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("数据库连接正常")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return False

# 导出常用对象
__all__ = [
    'Base',
    'engine',
    'get_db',
    'init_db',
    'drop_db',
    'check_db_connection',
    'create_db_engine',
    'get_database_url',
]
