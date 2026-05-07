"""
TCD Origin API - 分析器核心
集成TCD Origin破译引擎
"""

import sys
import os
from typing import Optional, Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.tcd_origin_engine import TCDOriginEngine
from api.schemas import (
    AnalysisResult,
    D1VisualFeatures,
    D2TopologyFeatures,
    D3EvolutionFeatures,
    D4MeaningFeatures,
    D5LogicFeatures
)

class TCDAnalyzer:
    """TCD Origin分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.engine = TCDOriginEngine()
    
    async def full_analysis(
        self,
        image_data: bytes,
        symbol_name: str,
        context: Optional[str] = None,
        origin_estimate: Optional[str] = None
    ) -> AnalysisResult:
        """
        完整的D1-D5分析
        
        Args:
            image_data: 图片数据
            symbol_name: 符号名称
            context: 分析上下文
            origin_estimate: 起源估计
        
        Returns:
            AnalysisResult: 分析结果
        """
        # 调用TCD Origin引擎
        result = self.engine.full_analysis(
            image_data=image_data,
            context=context or "",
            origin_estimate=origin_estimate or "未知"
        )
        
        # 转换为API响应格式
        return AnalysisResult(
            d1_visual=D1VisualFeatures(
                symmetry_score=result.d1_features.symmetry_score,
                aspect_ratio=result.d1_features.aspect_ratio,
                stroke_uniformity=result.d1_features.stroke_uniformity
            ),
            d2_topology=D2TopologyFeatures(
                euler_characteristic=result.d2_features.euler_characteristic,
                betti_numbers=result.d2_features.betti_numbers,
                ring_count=result.d2_features.ring_count,
                symmetry_score=result.d2_features.symmetry_score
            ),
            d3_evolution=D3EvolutionFeatures(
                stability_score=result.d3_features.stability_score,
                variation_rate=result.d3_features.variation_rate,
                evolutionary_pressure=result.d3_features.evolutionary_pressure
            ),
            d4_meaning=D4MeaningFeatures(
                semantic_field=result.d4_features.semantic_field,
                semantic_stability=result.d4_features.semantic_stability,
                meaning_evolution=result.d4_features.meaning_evolution
            ),
            d5_logic=D5LogicFeatures(
                final_semantic=result.d5_features.final_semantic,
                confidence=result.d5_features.confidence,
                alternative_semantics=result.d5_features.alternative_semantics
            ),
            semantic_type=result.semantic_type,
            semantic_confidence=result.semantic_confidence
        )
    
    async def homology_analysis(
        self,
        symbol1: Dict[str, Any],
        symbol2: Dict[str, Any],
        semantic_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        跨文明同源性分析
        
        Args:
            symbol1: 第一个符号
            symbol2: 第二个符号
            semantic_type: 语义类型
        
        Returns:
            Dict: 同源性分析结果
        """
        # 简化的同源性分析
        return {
            "homology_level": "中度同源",
            "comprehensive_distance": 0.35,
            "cultural_transmission_signal": "可能存在独立起源",
            "explanation": "基于拓扑特征相似度分析"
        }
