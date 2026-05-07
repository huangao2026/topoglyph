"""
TCD Origin API - 数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class SemanticType(str, Enum):
    """语义类型枚举"""
    CELESTIAL = "天体类"      # 太阳、月亮、星星
    NATURAL = "自然类"        # 山、水、风、雨
    HUMAN = "人体类"          # 人、目、口、手
    UTENSIL = "器物类"        # 刀、弓、鼎、爵

class HomologyLevel(str, Enum):
    """同源性等级"""
    HIGH = "高度同源"         # 综合距离 < 0.2
    MEDIUM = "中度同源"       # 0.2 <= 综合距离 < 0.4
    LOW = "低度同源"          # 0.4 <= 综合距离 < 0.6
    NONE = "非同源"           # 综合距离 >= 0.6

# ============ 请求模型 ============

class AnalysisRequest(BaseModel):
    """分析请求（Base64图片）"""
    image_base64: str = Field(..., description="Base64编码的图片数据")
    symbol_name: str = Field(..., description="符号名称")
    context: Optional[str] = Field(None, description="分析上下文")
    origin_estimate: Optional[str] = Field(None, description="起源估计")

class SymbolInfo(BaseModel):
    """符号信息"""
    name: str = Field(..., description="符号名称")
    meaning: str = Field(..., description="符号含义")
    origin: str = Field(..., description="文明起源")
    topology_features: Optional[Dict[str, Any]] = Field(None, description="拓扑特征")

class HomologyRequest(BaseModel):
    """同源性分析请求"""
    symbol1: SymbolInfo = Field(..., description="第一个符号")
    symbol2: SymbolInfo = Field(..., description="第二个符号")
    semantic_type: Optional[SemanticType] = Field(None, description="语义类型")

# ============ 响应模型 ============

class D1VisualFeatures(BaseModel):
    """D1视觉形态特征"""
    symmetry_score: float
    aspect_ratio: float
    stroke_uniformity: float

class D2TopologyFeatures(BaseModel):
    """D2拓扑几何特征"""
    euler_characteristic: int
    betti_numbers: List[int]
    ring_count: int
    symmetry_score: float

class D3EvolutionFeatures(BaseModel):
    """D3时间演化特征"""
    stability_score: float
    variation_rate: float
    evolutionary_pressure: str

class D4MeaningFeatures(BaseModel):
    """D4意义确权特征"""
    semantic_field: str
    semantic_stability: float
    meaning_evolution: str

class D5LogicFeatures(BaseModel):
    """D5逻辑坍缩特征"""
    final_semantic: str
    confidence: float
    alternative_semantics: List[str]

class AnalysisResult(BaseModel):
    """分析结果"""
    d1_visual: D1VisualFeatures
    d2_topology: D2TopologyFeatures
    d3_evolution: D3EvolutionFeatures
    d4_meaning: D4MeaningFeatures
    d5_logic: D5LogicFeatures
    semantic_type: str
    semantic_confidence: float

class HomologyResult(BaseModel):
    """同源性分析结果"""
    homology_level: str
    comprehensive_distance: float
    cultural_transmission_signal: str
    explanation: str

class AnalysisResponse(BaseModel):
    """分析响应"""
    success: bool
    symbol_name: str
    result: AnalysisResult

class HomologyResponse(BaseModel):
    """同源性分析响应"""
    success: bool
    homology_result: HomologyResult

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    service: str
    version: str
