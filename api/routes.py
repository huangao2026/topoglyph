"""
TCD Origin API - 路由定义
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json
import base64
import logging

from api.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    HomologyRequest,
    HomologyResponse,
    HealthResponse
)
from api.analyzer import TCDAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()

# 初始化分析器
analyzer = TCDAnalyzer()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_ancient_text(
    image: UploadFile = File(..., description="古文字图片"),
    symbol_name: str = Form(..., description="符号名称（如：日、月、山）"),
    context: Optional[str] = Form(None, description="分析上下文（可选）"),
    origin_estimate: Optional[str] = Form(None, description="起源估计（可选）")
):
    """
    分析古文字符号
    
    支持上传图片文件进行分析，返回完整的D1-D5五层破译结果。
    """
    try:
        # 验证文件类型
        if not image.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
            raise HTTPException(
                status_code=400,
                detail="不支持的文件格式。请上传 JPG、PNG、GIF、BMP 或 WebP 格式的图片。"
            )
        
        # 读取图片数据
        image_data = await image.read()
        
        # 执行分析
        result = await analyzer.full_analysis(
            image_data=image_data,
            symbol_name=symbol_name,
            context=context,
            origin_estimate=origin_estimate
        )
        
        logger.info(f"分析完成: {symbol_name}")
        
        return AnalysisResponse(
            success=True,
            symbol_name=symbol_name,
            result=result
        )
        
    except Exception as e:
        logger.error(f"分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-base64", response_model=AnalysisResponse)
async def analyze_base64(request: AnalysisRequest):
    """
    分析古文字符号（Base64图片）
    
    接收Base64编码的图片数据进行分析。
    """
    try:
        # 解码Base64图片
        image_data = base64.b64decode(request.image_base64)
        
        # 执行分析
        result = await analyzer.full_analysis(
            image_data=image_data,
            symbol_name=request.symbol_name,
            context=request.context,
            origin_estimate=request.origin_estimate
        )
        
        logger.info(f"Base64分析完成: {request.symbol_name}")
        
        return AnalysisResponse(
            success=True,
            symbol_name=request.symbol_name,
            result=result
        )
        
    except Exception as e:
        logger.error(f"Base64分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/homology", response_model=HomologyResponse)
async def analyze_homology(homology_request: HomologyRequest):
    """
    跨文明同源性分析
    
    比较两个古文字符号的同源性关系。
    """
    try:
        result = await analyzer.homology_analysis(
            symbol1=homology_request.symbol1,
            symbol2=homology_request.symbol2,
            semantic_type=homology_request.semantic_type
        )
        
        logger.info(f"同源性分析完成: {homology_request.symbol1.name} vs {homology_request.symbol2.name}")
        
        return HomologyResponse(
            success=True,
            homology_result=result
        )
        
    except Exception as e:
        logger.error(f"同源性分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        service="TCD Origin API",
        version="3.0.1"
    )

@router.get("/capabilities")
async def get_capabilities():
    """获取API能力列表"""
    return {
        "capabilities": [
            {
                "name": "古文字分析",
                "endpoint": "/api/v1/analyze",
                "method": "POST",
                "description": "上传图片分析古文字符号"
            },
            {
                "name": "Base64图片分析",
                "endpoint": "/api/v1/analyze-base64",
                "method": "POST",
                "description": "使用Base64编码的图片进行分析"
            },
            {
                "name": "同源性分析",
                "endpoint": "/api/v1/homology",
                "method": "POST",
                "description": "比较两个符号的跨文明同源性"
            }
        ],
        "supported_formats": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "max_file_size": "10MB"
    }
