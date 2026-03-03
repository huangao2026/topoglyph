"""
古文字破译系统 - Web API
基于模块化架构的 FastAPI 应用
Copyright © 2025 专利申请
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from typing import Optional, List
import os
import json

# 导入核心服务
from services.tool_manager import ToolManager
from services.plugin_manager import PluginManager
from services.agent_engine import DeciphermentEngine
from services.monitor import SystemMonitor
from core.memory import ShortTermMemoryManager
from core.version import VersionManager
from core.event import EventBus, get_global_event_bus

# 初始化事件总线
event_bus = get_global_event_bus()

# 初始化管理器
version_manager = VersionManager()
tool_manager = ToolManager(event_bus=event_bus, version_manager=version_manager)
plugin_manager = PluginManager(event_bus=event_bus, version_manager=version_manager)
memory_manager = ShortTermMemoryManager(max_messages=40)
system_monitor = SystemMonitor(event_bus)

# 初始化 FastAPI
app = FastAPI(
    title="古文字破译系统 API",
    description="基于AI的古代文字识别、分析和破译智能体系统 - 专利申请",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置限流
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 初始化智能体引擎
engine: Optional[DeciphermentEngine] = None


# ========== 数据模型 ==========

class AnalysisRequest(BaseModel):
    """分析请求"""
    text: str
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    """对话请求"""
    message: str
    session_id: str


class ToolRecommendRequest(BaseModel):
    """工具推荐请求"""
    requirements: List[str]
    category: Optional[str] = None
    limit: int = 5


class AnalysisResponse(BaseModel):
    """分析响应"""
    success: bool
    session_id: str
    analysis_id: str
    response: Optional[str] = None
    error: Optional[str] = None
    timestamp: str


class ChatResponse(BaseModel):
    """对话响应"""
    success: bool
    session_id: str
    response: Optional[str] = None
    error: Optional[str] = None
    timestamp: str


# ========== 生命周期管理 ==========

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    global engine
    
    print("🚀 古文字破译系统启动中...")
    
    try:
        # 1. 加载 LLM 配置
        config_path = os.path.join(
            os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"),
            "config/agent_llm_config.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        
        # 2. 创建 LLM 实例
        from langchain_openai import ChatOpenAI
        from coze_coding_utils.runtime_ctx.context import default_headers
        
        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
        
        llm = ChatOpenAI(
            model=cfg['config'].get("model"),
            api_key=api_key,
            base_url=base_url,
            temperature=cfg['config'].get('temperature', 0.6),
            streaming=True,
            timeout=cfg['config'].get('timeout', 600),
            extra_body={
                "thinking": {
                    "type": cfg['config'].get('thinking', 'disabled')
                }
            },
            default_headers=default_headers()
        )
        
        # 3. 创建智能体引擎
        engine = DeciphermentEngine(
            llm=llm,
            tool_manager=tool_manager,
            plugin_manager=plugin_manager,
            event_bus=event_bus,
            memory_manager=memory_manager,
            version_manager=version_manager
        )
        
        await engine.initialize()
        
        # 4. 加载插件
        from core.plugin import PluginContext
        plugin_context = PluginContext(
            tool_manager=tool_manager,
            memory_manager=memory_manager,
            config={},
            event_bus=event_bus,
            logger=None
        )
        
        # 发现插件
        discovered_plugins = await plugin_manager.discover_plugins()
        print(f"📦 发现 {len(discovered_plugins)} 个插件")
        
        # 加载发现的插件
        for plugin_info in discovered_plugins:
            try:
                success = await plugin_manager.load_plugin(plugin_info.id, plugin_context)
                if success:
                    print(f"✅ 插件 {plugin_info.name} 加载成功")
                else:
                    print(f"❌ 插件 {plugin_info.name} 加载失败")
            except Exception as e:
                print(f"❌ 插件 {plugin_info.name} 加载出错: {e}")
        
        # 5. 注册系统监控
        system_monitor.get_health_checker().register_health_check(
            "engine",
            lambda: {"status": "healthy", "message": "Engine is running"}
        )
        
        print("✅ 古文字破译系统启动完成！")
        print(f"📊 已注册工具: {len(tool_manager.list_tools())} 个")
        print(f"🔌 已加载插件: {len(plugin_manager.list_plugins())} 个")
    
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("🛑 古文字破译系统正在关闭...")
    # TODO: 执行清理操作
    print("✅ 系统已关闭")


# ========== API 路由 ==========

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "古文字破译系统 API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    health_status = await system_monitor.get_health_checker().check_health()
    return health_status


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
@limiter.limit("60/minute")
async def analyze_text(request: AnalysisRequest):
    """分析古文字文本"""
    try:
        result = await engine.analyze_text(
            text=request.text,
            session_id=request.session_id
        )
        return AnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze/image")
@limiter.limit("30/minute")
async def analyze_image(
    file: UploadFile = File(...),
    session_id: Optional[str] = None
):
    """分析古文字图像"""
    try:
        # 读取图像数据
        image_data = await file.read()
        
        result = await engine.analyze_image(
            image_data=image_data,
            session_id=session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chat", response_model=ChatResponse)
@limiter.limit("120/minute")
async def chat(request: ChatRequest):
    """对话交互"""
    try:
        result = await engine.chat(
            message=request.message,
            session_id=request.session_id
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/sessions/{session_id}")
async def get_session(session_id: str):
    """获取会话信息"""
    try:
        history = await engine.get_session_history(session_id)
        return {
            "session_id": session_id,
            "history": history,
            "message_count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tools")
async def list_tools(category: Optional[str] = None):
    """获取工具列表"""
    try:
        from core.tool import ToolCategory
        
        tool_category = ToolCategory(category) if category else None
        tools = tool_manager.list_tools(category=tool_category)
        
        return {
            "total": len(tools),
            "tools": [tool.to_dict() for tool in tools]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/tools/recommend")
async def recommend_tools(request: ToolRecommendRequest):
    """推荐工具"""
    try:
        from core.tool import ToolCategory
        
        tool_category = ToolCategory(request.category) if request.category else None
        tools = tool_manager.recommend_tools(
            requirements=request.requirements,
            category=tool_category,
            limit=request.limit
        )
        
        return {
            "requirements": request.requirements,
            "recommended": [tool.to_dict() for tool in tools]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tools/{tool_id}")
async def get_tool_info(tool_id: str):
    """获取工具详情"""
    try:
        tool_info = tool_manager.get_tool_info(tool_id)
        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool {tool_id} not found")
        
        return tool_info.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/plugins")
async def list_plugins():
    """获取插件列表"""
    try:
        plugins = plugin_manager.list_plugins()
        
        return {
            "total": len(plugins),
            "plugins": [
                {
                    "id": p.id,
                    "name": p.name,
                    "version": p.version,
                    "plugin_type": p.plugin_type.value,
                    "author": p.author,
                    "description": p.description
                }
                for p in plugins
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/plugins/{plugin_id}/health")
async def check_plugin_health(plugin_id: str):
    """检查插件健康状态"""
    try:
        health = await plugin_manager.check_plugin_health(plugin_id)
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics")
async def get_metrics():
    """获取监控指标"""
    try:
        metrics_export = system_monitor.get_metrics_collector().export_metrics()
        status = await system_monitor.get_system_status()
        
        return {
            "metrics": metrics_export,
            "status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/version")
async def get_version_info():
    """获取版本信息"""
    try:
        version_report = version_manager.get_system_version_report()
        return version_report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== 运行入口 ==========

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "web_api_new:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
