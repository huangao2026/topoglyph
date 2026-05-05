#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCD Origin 破译引擎 - LangChain工具封装
集成D1-D5破译架构和拓扑同源性距离公式
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from langchain.tools import tool

from tools.tcd_origin_engine import (
    TCDOriginEngine,
    CrossCivilizationAnalyzer,
    DecodingLayer,
    SemanticType,
    TCDHighDimVector
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# LangChain工具定义
# ============================================================================

@tool
def tcd_full_analysis(image_url: str, 
                      context: Optional[str] = None,
                      origin_estimate: Optional[str] = None) -> str:
    """
    TCD Origin 全链路分析 - 执行完整的D1-D5破译流程。
    
    D1-D5五层破译架构：
    - D1: 视觉形态层 - CNN提取笔画宽度、曲率等基础视觉特征
    - D2: 拓扑几何层 - 拓扑不变量分析（连通性、闭合环、节点关系）
    - D3: 时间演化层 - 动力学演化路径，反向推导原始态
    - D4: 意义确权层 - 语言游戏理论，语境关联锁定社会学意义
    - D5: 逻辑坍缩层 - 多维度概率交叉验证，坍缩为确定性解释
    
    Args:
        image_url: 古文字符号图片的URL
        context: 语境信息（可选），用于D4意义确权
        origin_estimate: 原始态估计（可选），用于D3演化分析
    
    Returns:
        JSON格式的完整分析结果，包含：
        - D1视觉特征
        - D2拓扑特征（欧拉示性数、贝蒂数等）
        - D3演化特征
        - D4意义特征
        - D5坍缩结果（置信度、概率分布）
        - TCD Origin高维特征向量
    """
    logger.info(f"TCD Origin全链路分析: {image_url}")
    
    try:
        engine = TCDOriginEngine()
        result = engine.full_analysis(
            image_data=image_url,
            context=context,
            origin_estimate=origin_estimate
        )
        
        output = {
            "status": "success",
            "image_url": image_url,
            "layers": {
                "D1_visual": result.d1_features.to_dict(),
                "D2_topology": result.d2_features.to_dict(),
                "D3_evolution": result.d3_features.to_dict(),
                "D4_meaning": result.d4_features.to_dict(),
                "D5_collapse": result.d5_result.to_dict()
            },
            "high_dim_vector": result.to_vector(),
            "formula_used": "D1-D5 Hierarchical Decoding Architecture"
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"TCD全链路分析失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"TCD全链路分析失败: {str(e)}",
            "image_url": image_url
        }, ensure_ascii=False)


@tool
def tcd_homology_distance(symbol1_url: str,
                          symbol2_url: str,
                          semantic_type: Optional[str] = None,
                          civilization1: Optional[str] = None,
                          civilization2: Optional[str] = None) -> str:
    """
    TCD Origin 拓扑同源性距离分析 - 核心公式实现。
    
    核心公式：D(S_a, S_b) = Σ ω_i |T_i(a) - T_i(b)|
    
    其中：
    - S_a, S_b: 两个待比较的符号
    - T_i: 第i阶拓扑特征向量
    - ω_i: 权重系数
    - D: 拓扑同源性距离
    
    Args:
        symbol1_url: 第一个符号的图片URL
        symbol2_url: 第二个符号的图片URL
        semantic_type: 语义类型（可选），可为"天体类"、"自然类"、"人体类"、"器物类"
        civilization1: 第一个符号所属文明（可选）
        civilization2: 第二个符号所属文明（可选）
    
    Returns:
        JSON格式的距离分析结果，包含：
        - distance: 拓扑同源性距离
        - similarity: 相似度 (0-1)
        - layer_distances: 各层距离分析
        - layer_weights: 使用的权重配置
        - formula: 使用的公式
        - interpretation: 结果解读
    """
    logger.info(f"计算拓扑同源性距离: {civilization1 or '符号1'} vs {civilization2 or '符号2'}")
    
    try:
        engine = TCDOriginEngine()
        analyzer = CrossCivilizationAnalyzer()
        
        # 转换语义类型
        sem_type = None
        if semantic_type:
            type_map = {
                "天体类": SemanticType.CELESTIAL,
                "自然类": SemanticType.NATURAL,
                "人体类": SemanticType.HUMAN,
                "器物类": SemanticType.ARTIFACT
            }
            sem_type = type_map.get(semantic_type)
        
        # 执行分析
        result = analyzer.analyze_homology(
            symbol1_url, 
            symbol2_url, 
            sem_type
        )
        
        # 添加文明信息
        result["civilization1"] = civilization1 or "未知"
        result["civilization2"] = civilization2 or "未知"
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"拓扑同源性距离计算失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"拓扑同源性距离计算失败: {str(e)}",
            "civilization1": civilization1,
            "civilization2": civilization2
        }, ensure_ascii=False)


@tool
def tcd_layer_analysis(image_url: str, 
                      target_layer: str) -> str:
    """
    TCD Origin 单层深度分析 - 分析指定层级的特征。
    
    支持的分析层级：
    - D1: 视觉形态层 - CNN特征提取
    - D2: 拓扑几何层 - 拓扑不变量分析
    - D3: 时间演化层 - 动力学演化
    - D4: 意义确权层 - 语言游戏理论
    - D5: 逻辑坍缩层 - 概率交叉验证
    
    Args:
        image_url: 古文字符号图片的URL
        target_layer: 目标分析层级 ("D1", "D2", "D3", "D4", "D5")
    
    Returns:
        JSON格式的指定层级分析结果
    """
    logger.info(f"TCD Origin单层分析: {target_layer}")
    
    try:
        engine = TCDOriginEngine()
        
        # 提取完整特征
        vector = engine.full_analysis(image_data=image_url)
        
        # 根据目标层级返回对应结果
        layer_map = {
            "D1": ("D1_visual", vector.d1_features.to_dict(), "视觉形态层"),
            "D2": ("D2_topology", vector.d2_features.to_dict(), "拓扑几何层"),
            "D3": ("D3_evolution", vector.d3_features.to_dict(), "时间演化层"),
            "D4": ("D4_meaning", vector.d4_features.to_dict(), "意义确权层"),
            "D5": ("D5_collapse", vector.d5_result.to_dict(), "逻辑坍缩层")
        }
        
        if target_layer not in layer_map:
            return json.dumps({
                "status": "error",
                "message": f"不支持的分析层级: {target_layer}",
                "supported_layers": ["D1", "D2", "D3", "D4", "D5"]
            }, ensure_ascii=False)
        
        layer_key, layer_data, layer_desc = layer_map[target_layer]
        
        output = {
            "status": "success",
            "image_url": image_url,
            "target_layer": target_layer,
            "layer_name": layer_desc,
            "layer_data": layer_data,
            "formula": f"TCD {target_layer} Analysis"
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"TCD单层分析失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"TCD单层分析失败: {str(e)}",
            "image_url": image_url,
            "target_layer": target_layer
        }, ensure_ascii=False)


@tool
def tcd_cultural_transmission_detect(symbol1_url: str,
                                    symbol2_url: str,
                                    semantic_type: Optional[str] = None) -> str:
    """
    TCD Origin 文化传播检测 - 检测跨文明符号传播信号。
    
    基于重要发现：环数是最强的文化传播指示器
    - 环数相同 + 拓扑相似 → 强文化传播信号
    - 环数不同 + 拓扑相似 → 独立起源认知趋同
    - 其他情况 → 无法判断
    
    Args:
        symbol1_url: 第一个符号的图片URL
        symbol2_url: 第二个符号的图片URL
        semantic_type: 语义类型（可选）
    
    Returns:
        JSON格式的文化传播分析结果，包含：
        - transmission_signal: 传播信号强度
        - ring_comparison: 环数比较
        - symmetry_similarity: 对称性相似度
        - euler_match: 欧拉示性数匹配
        - interpretation: 结果解读
    """
    logger.info("TCD Origin文化传播检测")
    
    try:
        analyzer = CrossCivilizationAnalyzer()
        engine = TCDOriginEngine()
        
        # 转换语义类型
        sem_type = None
        if semantic_type:
            type_map = {
                "天体类": SemanticType.CELESTIAL,
                "自然类": SemanticType.NATURAL,
                "人体类": SemanticType.HUMAN,
                "器物类": SemanticType.ARTIFACT
            }
            sem_type = type_map.get(semantic_type, SemanticType.UNKNOWN)
        else:
            # 自动检测
            vector1 = engine.full_analysis(symbol1_url)
            vector2 = engine.full_analysis(symbol2_url)
            sem_type = analyzer._detect_semantic_type(vector1)
        
        # 提取特征
        vector1 = engine.full_analysis(symbol1_url)
        vector2 = engine.full_analysis(symbol2_url)
        
        # 检测文化传播
        result = analyzer.detect_cultural_transmission(
            vector1, vector2, sem_type
        )
        
        result["status"] = "success"
        result["symbol1"] = symbol1_url
        result["symbol2"] = symbol2_url
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"TCD文化传播检测失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"TCD文化传播检测失败: {str(e)}"
        }, ensure_ascii=False)


# ============================================================================
# 工具列表导出
# ============================================================================

TCD_ORIGIN_TOOLS = [
    tcd_full_analysis,
    tcd_homology_distance,
    tcd_layer_analysis,
    tcd_cultural_transmission_detect
]


def get_tcd_origin_tools() -> List:
    """获取所有TCD Origin工具"""
    return TCD_ORIGIN_TOOLS


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("TCD Origin 破译引擎工具测试")
    
    # 测试D1-D5全链路分析
    print("\n1. 测试D1-D5全链路分析:")
    result = tcd_full_analysis.invoke({
        "image_url": "https://example.com/test.jpg",
        "context": "祭祀场景",
        "origin_estimate": "甲骨文"
    })
    data = json.loads(result)
    print(f"状态: {data['status']}")
    print(f"层级数: {len(data['layers'])}")
    
    # 测试拓扑同源性距离
    print("\n2. 测试拓扑同源性距离:")
    result = tcd_homology_distance.invoke({
        "symbol1_url": "https://example.com/symbol1.jpg",
        "symbol2_url": "https://example.com/symbol2.jpg",
        "semantic_type": "天体类",
        "civilization1": "中国",
        "civilization2": "古埃及"
    })
    data = json.loads(result)
    print(f"相似度: {data.get('similarity')}")
    print(f"距离: {data.get('distance')}")
    print(f"公式: {data.get('formula')}")
    
    print("\n工具测试完成！")
