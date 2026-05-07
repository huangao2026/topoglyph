"""
TCD Origin API - 配置管理
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置"""
    
    # API配置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "TCD Origin API"
    
    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    
    # 知识库配置（可选）
    VOLCENGINE_API_KEY: Optional[str] = None
    VOLCENGINE_SERVICE_ID: Optional[str] = None
    
    # LLM配置（可选）
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4"
    
    # Redis缓存配置（可选）
    REDIS_URL: Optional[str] = None
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
