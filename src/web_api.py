#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古代文字破解智能体 - Web API服务
为全球用户提供古文字识别和破译服务
"""

import os
import json
import uuid
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Request, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 导入Agent
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/work/logs/bypass/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="古代文字破解智能体",
    description="AI-Powered Ancient Text Deciphering System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置限流
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 全局Agent实例（懒加载）
_agent = None

def get_agent():
    """获取或创建Agent实例"""
    global _agent
    if _agent is None:
        try:
            from agents.agent import build_agent
            _agent = build_agent()
            logger.info("Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise
    return _agent

# ===== 数据模型 =====

class AnalyzeRequest(BaseModel):
    """文本分析请求"""
    text: str = Field(..., description="待分析的古文字内容", min_length=1, max_length=10000)
    language: str = Field("zh", description="界面语言 (zh/en/ja/ko/es/fr)")
    context: Optional[str] = Field(None, description="上下文信息（可选）")

class ImageAnalysisRequest(BaseModel):
    """图像分析请求参数"""
    language: str = Field("zh", description="界面语言")
    context: Optional[str] = Field(None, description="上下文信息")

class AnalysisResponse(BaseModel):
    """分析响应"""
    request_id: str
    status: str
    message: str
    result: Optional[dict] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: datetime
    version: str
    agent_loaded: bool

# ===== 路由 =====

@app.get("/", response_model=dict)
async def root():
    """根路径"""
    return {
        "message": "古代文字破解智能体 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    try:
        agent = get_agent()
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version="1.0.0",
            agent_loaded=agent is not None
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.post("/api/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def analyze_text(request: Request, data: AnalyzeRequest):
    """分析文本"""
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Analyzing text: {data.text[:100]}...")
    
    try:
        agent = get_agent()
        
        # 调用Agent进行分析
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": data.text}]
        })
        
        # 提取结果
        content = result.get("messages", [])[-1].get("content", "") if result.get("messages") else ""
        
        logger.info(f"[{request_id}] Analysis completed successfully")
        
        return AnalysisResponse(
            request_id=request_id,
            status="success",
            message="分析完成",
            result={
                "content": content,
                "language": data.language
            }
        )
        
    except Exception as e:
        logger.error(f"[{request_id}] Analysis failed: {e}")
        return AnalysisResponse(
            request_id=request_id,
            status="error",
            message="分析失败",
            error=str(e)
        )

@app.post("/api/analyze/stream")
@limiter.limit("5/minute")
async def analyze_text_stream(request: Request, data: AnalyzeRequest):
    """流式分析文本（适合长文本）"""
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Streaming analysis: {data.text[:100]}...")
    
    async def generate():
        try:
            agent = get_agent()
            
            # 流式调用
            async for chunk in agent.astream({
                "messages": [{"role": "user", "content": data.text}]
            }):
                if chunk and "messages" in chunk:
                    content = chunk["messages"][-1].get("content", "")
                    if content:
                        yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
            
            logger.info(f"[{request_id}] Stream completed successfully")
            
        except Exception as e:
            logger.error(f"[{request_id}] Stream failed: {e}")
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/analyze/image", response_model=AnalysisResponse)
@limiter.limit("5/minute")
async def analyze_image(
    request: Request,
    image: UploadFile = File(..., description="古文字图片"),
    params: str = None  # JSON格式的额外参数
):
    """分析古文字图片"""
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Analyzing image: {image.filename}")
    
    try:
        # 保存上传的图片
        upload_dir = Path("/tmp/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / f"{request_id}_{image.filename}"
        with open(file_path, "wb") as f:
            content = await image.read()
            f.write(content)
        
        logger.info(f"[{request_id}] Image saved to {file_path}")
        
        # 解析参数
        if params:
            try:
                extra_params = json.loads(params)
                language = extra_params.get("language", "zh")
                context = extra_params.get("context")
            except:
                language = "zh"
                context = None
        else:
            language = "zh"
            context = None
        
        # 构建提示词
        prompt = f"""请分析这张古文字图片。

语言设置：{language}
{f'上下文信息：{context}' if context else ''}

请按照以下格式输出：
# 古代文字分析报告

## 基本信息
- 文字类型
- 大致年代
- 文化背景

## 图像识别
- 描述可见的符号和特征

## 破译内容
- 识别的文字
- 现代翻译
- 详细解析

## AI工具推荐
- 推荐使用的AI工具
- 使用建议

## 历史背景
- 相关的历史文化信息
"""
        
        # 调用Agent（注意：当前Agent需要支持多模态）
        agent = get_agent()
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": prompt}]
        })
        
        # 提取结果
        content = result.get("messages", [])[-1].get("content", "") if result.get("messages") else ""
        
        logger.info(f"[{request_id}] Image analysis completed")
        
        # 清理临时文件（异步）
        os.remove(file_path)
        
        return AnalysisResponse(
            request_id=request_id,
            status="success",
            message="图片分析完成",
            result={
                "content": content,
                "filename": image.filename,
                "language": language
            }
        )
        
    except Exception as e:
        logger.error(f"[{request_id}] Image analysis failed: {e}")
        return AnalysisResponse(
            request_id=request_id,
            status="error",
            message="图片分析失败",
            error=str(e)
        )

@app.get("/api/tools", response_model=dict)
async def get_available_tools():
    """获取可用的AI工具列表"""
    tools = {
        "oracle": {
            "name": "甲骨文工具",
            "tools": [
                {"name": "殷契文渊", "url": "http://www.jgwlbq.org.cn", "type": "web"},
                {"name": "殷契行止", "url": "微信小程序", "type": "mobile"},
                {"name": "JiaguCopilot", "url": "清华大学", "type": "academic"},
            ]
        },
        "bronze": {
            "name": "金文工具",
            "tools": [
                {"name": "商周金文智能镜", "url": "微信小程序", "type": "mobile"},
                {"name": "字鉴书法识别系统", "url": "http://api.shufashibie.com", "type": "web"},
            ]
        },
        "general": {
            "name": "综合工具",
            "tools": [
                {"name": "Transkribus", "url": "https://www.transkribus.org", "type": "web"},
                {"name": "HunyuanOCR", "url": "腾讯混元", "type": "api"},
            ]
        }
    }
    
    return {"tools": tools}

@app.get("/api/languages", response_model=dict)
async def get_supported_languages():
    """获取支持的语言"""
    return {
        "languages": {
            "zh": {"name": "中文", "native": "简体中文"},
            "en": {"name": "English", "native": "English"},
            "ja": {"name": "Japanese", "native": "日本語"},
            "ko": {"name": "Korean", "native": "한국어"},
            "es": {"name": "Spanish", "native": "Español"},
            "fr": {"name": "French", "native": "Français"}
        }
    }

@app.get("/api/stats", response_model=dict)
async def get_statistics():
    """获取系统统计信息"""
    return {
        "version": "1.0.0",
        "uptime": "运行中",
        "requests_today": 0,  # 需要从数据库获取
        "total_users": 0,  # 需要从数据库获取
        "languages_supported": 6
    }

# ===== 启动配置 =====

if __name__ == "__main__":
    import uvicorn
    
    # 从环境变量获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Starting Ancient Text AI Server on {host}:{port}")
    
    uvicorn.run(
        "web_api:app",
        host=host,
        port=port,
        reload=True,  # 开发模式
        log_level="info"
    )
