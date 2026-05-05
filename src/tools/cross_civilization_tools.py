#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨文明符号分析工具 - LangChain工具封装
集成拓扑特征分析和跨文明同源性分析功能
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from langchain.tools import tool
from langchain_core.tools import Tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

from tools.topology_analyzer import (
    TopologyAnalyzer,
    CrossCivilizationAnalyzer,
    SemanticType,
    TopologyFeatureVector
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# LangChain工具定义
# ============================================================================

@tool
def extract_topology_features(image_url: str, symbol_name: Optional[str] = None) -> str:
    """
    提取古文字符号的拓扑特征向量。
    
    采用专利技术文档中的"三层拓扑不变量层级互补体系"，依次提取：
    1. 全局形态锚点特征（对称性指数、宽高比）
    2. 核心拓扑不变量（欧拉示性数、贝蒂数序列）
    3. 局部结构指纹特征（环数分布、连通分量数、像素密度）
    
    最终生成128维高维拓扑特征向量。
    
    Args:
        image_url: 古文字符号图片的URL
        symbol_name: 符号名称（可选），用于标识和记录
    
    Returns:
        JSON格式的拓扑特征分析结果，包含：
        - global_features: 全局形态特征
        - core_invariants: 核心拓扑不变量
        - local_fingerprint: 局部结构指纹
        - high_dim_vector: 128维特征向量摘要
        - semantic_type: 推测的语义类型
    """
    logger.info(f"提取拓扑特征: {symbol_name or image_url}")
    
    try:
        analyzer = TopologyAnalyzer()
        features = analyzer.extract_all_features(image_url)
        semantic_type = analyzer.analyze_semantic_type(features)
        
        result = {
            "status": "success",
            "symbol_name": symbol_name,
            "image_url": image_url,
            "semantic_type": semantic_type.value,
            "features": features.to_dict()
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"拓扑特征提取失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"拓扑特征提取失败: {str(e)}",
            "symbol_name": symbol_name
        }, ensure_ascii=False)


@tool
def analyze_cross_civilization_homology(
    symbol1_url: str,
    symbol2_url: str,
    semantic_type: Optional[str] = None,
    civilization1: Optional[str] = None,
    civilization2: Optional[str] = None
) -> str:
    """
    分析两个跨文明古文字符号的同源性。
    
    采用专利技术文档中的跨文明符号拓扑演化规律，包括：
    1. 特征区分力的概念依赖性：不同语义类型需要不同的特征权重
    2. 环数的文化传播指示器作用：区分独立起源与文化传播
    3. 三层特征互补机制：全局、核心、局部特征各有分工
    
    主要功能：
    - 计算两个符号的拓扑相似度
    - 判定同源性等级（高/中/低）
    - 检测文化传播信号
    - 提供语义类型自适应的权重调整
    
    Args:
        symbol1_url: 第一个符号的图片URL
        symbol2_url: 第二个符号的图片URL
        semantic_type: 语义类型（可选），可为"天体类"、"自然类"、"人体类"、"器物类"
        civilization1: 第一个符号所属文明（可选）
        civilization2: 第二个符号所属文明（可选）
    
    Returns:
        JSON格式的同源性分析结果，包含：
        - homology_level: 同源性等级
        - weighted_similarity: 加权相似度
        - semantic_type: 语义类型
        - transmission_analysis: 文化传播分析
        - interpretation: 结果解读
        - feature_weights: 使用的特征权重
    """
    logger.info(f"分析跨文明同源性: {civilization1 or '文明1'} vs {civilization2 or '文明2'}")
    
    try:
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
        logger.error(f"同源性分析失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"同源性分析失败: {str(e)}",
            "civilization1": civilization1,
            "civilization2": civilization2
        }, ensure_ascii=False)


@tool
def detect_cultural_transmission(
    symbol1_url: str,
    symbol2_url: str,
    semantic_type: Optional[str] = None
) -> str:
    """
    检测两个古文字符号间的文化传播信号。
    
    基于专利技术文档的重要发现：环数不是最强的同源性指标，
    而是最强的文化传播指示器。
    
    检测逻辑：
    1. 当两个独立起源文明的同一概念意外出现相同环数时 → 强文化传播信号
    2. 当环数差异大但整体拓扑相似时 → 独立发明但认知趋同
    3. 其他情况 → 无法判断
    
    Args:
        symbol1_url: 第一个符号的图片URL
        symbol2_url: 第二个符号的图片URL
        semantic_type: 语义类型（可选）
    
    Returns:
        JSON格式的文化传播分析结果，包含：
        - transmission_signal: 传播信号强度（strong/weak/unknown）
        - ring_comparison: 环数比较详情
        - symmetry_similarity: 对称性相似度
        - euler_match: 欧拉示性数是否匹配
        - interpretation: 结果解读
    """
    logger.info(f"检测文化传播信号")
    
    try:
        analyzer = CrossCivilizationAnalyzer()
        
        # 提取特征
        topology_analyzer = TopologyAnalyzer()
        features1 = topology_analyzer.extract_all_features(symbol1_url)
        features2 = topology_analyzer.extract_all_features(symbol2_url)
        
        # 确定语义类型
        sem_type = topology_analyzer.analyze_semantic_type(features1)
        if semantic_type:
            type_map = {
                "天体类": SemanticType.CELESTIAL,
                "自然类": SemanticType.NATURAL,
                "人体类": SemanticType.HUMAN,
                "器物类": SemanticType.ARTIFACT
            }
            sem_type = type_map.get(semantic_type, sem_type)
        
        # 检测文化传播
        result = analyzer.detect_cultural_transmission(
            features1, features2, sem_type
        )
        
        result["status"] = "success"
        result["symbol1"] = symbol1_url
        result["symbol2"] = symbol2_url
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"文化传播检测失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"文化传播检测失败: {str(e)}"
        }, ensure_ascii=False)


@tool
def analyze_semantic_type_from_features(topology_features_json: str) -> str:
    """
    根据拓扑特征分析古文字符号的语义类型。
    
    不同拓扑特征对不同语义类型的概念具有不同的区分力：
    - 天体类（日、月、星）：对称性最强
    - 自然类（山、水、火）：宽高比最强
    - 人体类（人、目、口）：对称性+环数共同
    - 器物类（田、皿、弓）：环数最强
    
    Args:
        topology_features_json: 拓扑特征向量的JSON字符串
                               （由extract_topology_features返回）
    
    Returns:
        JSON格式的语义类型分析结果，包含：
        - semantic_type: 语义类型
        - confidence: 分析置信度
        - reasoning: 推理过程
        - recommended_features: 推荐使用的特征
    """
    logger.info("分析语义类型")
    
    try:
        # 解析特征
        features_dict = json.loads(topology_features_json)
        
        if features_dict.get("status") == "error":
            return topology_features_json
        
        features_data = features_dict.get("features", {})
        global_features = features_data.get("global_features", {})
        local_fingerprint = features_data.get("local_fingerprint", {})
        
        # 简化版语义分析
        symmetry = global_features.get("rotational_symmetry", 0)
        aspect_ratio = global_features.get("aspect_ratio", 1)
        rings = sum(local_fingerprint.get("ring_distribution", []))
        
        # 分析逻辑
        if symmetry > 0.8 and rings > 0:
            semantic_type = "天体类"
            confidence = 0.85
            reasoning = "高旋转对称性和存在环状结构，符合天体类符号特征"
            recommended_features = ["对称性指数", "环数分布"]
        elif aspect_ratio > 1.5:
            semantic_type = "自然类"
            confidence = 0.80
            reasoning = "宽高比较大，符合自然类符号的形态特征"
            recommended_features = ["宽高比", "欧拉示性数"]
        elif symmetry > 0.6 and rings > 0:
            semantic_type = "人体类"
            confidence = 0.75
            reasoning = "中等对称性和环状结构，符合人体类符号特征"
            recommended_features = ["对称性指数", "环数分布", "贝蒂数"]
        elif rings > 0:
            semantic_type = "器物类"
            confidence = 0.70
            reasoning = "存在环状结构，符合器物类符号的设计特征"
            recommended_features = ["环数分布", "对称性指数"]
        else:
            semantic_type = "未知"
            confidence = 0.3
            reasoning = "特征不足以确定语义类型"
            recommended_features = ["全局形态锚点", "核心拓扑不变量"]
        
        result = {
            "status": "success",
            "semantic_type": semantic_type,
            "confidence": confidence,
            "reasoning": reasoning,
            "recommended_features": recommended_features,
            "original_features": features_data
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    except Exception as e:
        logger.error(f"语义类型分析失败: {e}")
        return json.dumps({
            "status": "error",
            "message": f"语义类型分析失败: {str(e)}"
        }, ensure_ascii=False)


# ============================================================================
# 工具列表导出
# ============================================================================

TOPOLOGY_TOOLS = [
    extract_topology_features,
    analyze_cross_civilization_homology,
    detect_cultural_transmission,
    analyze_semantic_type_from_features
]


def get_topology_tools() -> List[Tool]:
    """获取所有拓扑分析工具"""
    return TOPOLOGY_TOOLS


# ============================================================================
# 错误处理中间件
# ============================================================================

@wrap_tool_call
def handle_topology_tool_errors(request, handler):
    """处理拓扑分析工具执行错误"""
    try:
        return handler(request)
    except Exception as e:
        logger.error(f"拓扑工具执行错误: {e}")
        return ToolMessage(
            content=f"工具执行错误: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 测试工具
    print("测试拓扑特征提取工具...")
    
    # 示例拓扑特征
    sample_features = {
        "status": "success",
        "features": {
            "global_features": {
                "horizontal_symmetry": 0.85,
                "vertical_symmetry": 0.90,
                "rotational_symmetry": 0.75,
                "aspect_ratio": 1.2
            },
            "local_fingerprint": {
                "ring_distribution": [1, 0, 0],
                "connected_components": 1,
                "pixel_density": 0.45
            }
        }
    }
    
    # 测试语义类型分析
    result = analyze_semantic_type_from_features.invoke(
        json.dumps(sample_features)
    )
    print(f"语义类型分析结果:\n{result}\n")
    
    print("工具测试完成！")
