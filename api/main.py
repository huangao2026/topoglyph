"""
TCD Origin API - 跨文明古文字拓扑破译引擎
FastAPI 核心配置
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import logging

from api.routes import router as api_router
from api.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="TCD Origin API",
    description="跨文明古文字拓扑破译引擎 - API服务",
    version="3.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 添加中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1", tags=["古文字分析"])

# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "TCD Origin API",
        "version": "3.0.1"
    }

# 根路径
@app.get("/", tags=["系统"])
async def root():
    """API根路径"""
    return {
        "message": "TCD Origin API - 跨文明古文字拓扑破译引擎",
        "version": "3.0.1",
        "docs": "/docs",
        "health": "/health"
    }

logger.info("TCD Origin API 服务已启动")
