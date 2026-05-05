#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古文字拓扑特征分析工具 - 增强版
集成D1-D5破译架构和核心公式模型

基于TCD Origin项目说明书和专利技术文档实现：
1. D1-D5五层破译架构
2. 拓扑同源性距离公式
3. 三层拓扑不变量层级互补体系
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import math
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DecodingLayer(Enum):
    """D1-D5破译架构层级"""
    D1_VISUAL = "D1_视觉形态层"      # CNN提取笔画宽度、曲率
    D2_TOPOLOGY = "D2_拓扑几何层"    # 拓扑不变量分析
    D3_EVOLUTION = "D3_时间演化层"   # 动力学演化路径
    D4_MEANING = "D4_意义确权层"     # 语言游戏理论
    D5_COLLAPSE = "D5_逻辑坍缩层"    # 多维度概率交叉验证


class SemanticType(Enum):
    """语义类型枚举"""
    CELESTIAL = "天体类"      # 日、月、星、天
    NATURAL = "自然类"         # 山、水、火、土
    HUMAN = "人体类"          # 人、目、口、手、首
    ARTIFACT = "器物类"       # 田、皿、弓、宅、矢
    UNKNOWN = "未知"


@dataclass
class D1VisualFeatures:
    """D1: 视觉形态层特征 (CNN提取)"""
    stroke_width: float = 0.0          # 笔画宽度
    stroke_curvature: float = 0.0     # 笔画曲率
    edge_density: float = 0.0         # 边缘密度
    texture_complexity: float = 0.0     # 纹理复杂度
    color_distribution: List[float] = field(default_factory=list)  # 颜色分布
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        base = [
            self.stroke_width,
            self.stroke_curvature,
            self.edge_density,
            self.texture_complexity
        ]
        if self.color_distribution:
            base.extend(self.color_distribution)
        return base


@dataclass
class D2TopologyFeatures:
    """D2: 拓扑几何层特征 (拓扑不变量分析)"""
    # 全局形态锚点特征
    horizontal_symmetry: float = 0.0  # 水平对称度
    vertical_symmetry: float = 0.0    # 垂直对称度
    rotational_symmetry: float = 0.0   # 旋转对称度
    aspect_ratio: float = 1.0          # 宽高比
    
    # 核心拓扑不变量
    euler_characteristic: int = 0      # 欧拉示性数 χ = 连通分量数 - 环数
    betti_0: int = 0                   # 0维贝蒂数
    betti_1: int = 0                   # 1维贝蒂数
    betti_2: int = 0                   # 2维贝蒂数
    
    # 局部结构指纹
    ring_distribution: List[int] = field(default_factory=list)  # 环数分布
    connected_components: int = 0         # 连通分量数
    pixel_density: float = 0.0            # 像素密度
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        return [
            # 全局形态 (4维)
            self.horizontal_symmetry,
            self.vertical_symmetry,
            self.rotational_symmetry,
            self.aspect_ratio,
            # 核心不变量 (4维)
            float(self.euler_characteristic),
            float(self.betti_0),
            float(self.betti_1),
            float(self.betti_2),
            # 局部指纹 (3维)
            float(sum(self.ring_distribution)) if self.ring_distribution else 0.0,
            float(self.connected_components),
            self.pixel_density
        ]


@dataclass
class D3EvolutionFeatures:
    """D3: 时间演化层特征"""
    origin_state: str = ""              # 原始态估计
    evolution_stage: int = 0           # 演化阶段
    transformation_path: List[str] = field(default_factory=list)  # 变形路径
    stability_score: float = 0.0       # 稳定性评分
    mutation_rate: float = 0.0         # 变异率
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        return [
            float(self.evolution_stage),
            self.stability_score,
            self.mutation_rate
        ]


@dataclass
class D4MeaningFeatures:
    """D4: 意义确权层特征"""
    contextual_anchoring: float = 0.0  # 语境锚定度
    social_meaning_score: float = 0.0  # 社会学意义评分
    semantic_field: List[str] = field(default_factory=list)  # 语义场
    language_game_type: str = ""       # 语言游戏类型
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        return [
            self.contextual_anchoring,
            self.social_meaning_score
        ]


@dataclass
class D5CollapseResult:
    """D5: 逻辑坍缩层结果"""
    probability_distribution: Dict[str, float] = field(default_factory=dict)  # 概率分布
    collapsed_meaning: str = ""         # 坍缩后的意义
    confidence: float = 0.0            # 置信度
    cross_validation_score: float = 0.0  # 交叉验证分数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class TCDHighDimVector:
    """TCD Origin高维特征向量"""
    d1_features: D1VisualFeatures = None
    d2_features: D2TopologyFeatures = None
    d3_features: D3EvolutionFeatures = None
    d4_features: D4MeaningFeatures = None
    d5_result: D5CollapseResult = None
    
    def __post_init__(self):
        if self.d1_features is None:
            self.d1_features = D1VisualFeatures()
        if self.d2_features is None:
            self.d2_features = D2TopologyFeatures()
        if self.d3_features is None:
            self.d3_features = D3EvolutionFeatures()
        if self.d4_features is None:
            self.d4_features = D4MeaningFeatures()
        if self.d5_result is None:
            self.d5_result = D5CollapseResult()
    
    def to_vector(self) -> List[float]:
        """生成TCD Origin高维特征向量"""
        vectors = []
        vectors.extend(self.d1_features.to_vector())
        vectors.extend(self.d2_features.to_vector())
        vectors.extend(self.d3_features.to_vector())
        vectors.extend(self.d4_features.to_vector())
        return vectors
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "d1_visual": asdict(self.d1_features),
            "d2_topology": asdict(self.d2_features),
            "d3_evolution": asdict(self.d3_features),
            "d4_meaning": asdict(self.d4_features),
            "d5_collapse": asdict(self.d5_result),
            "high_dim_vector": self.to_vector()
        }


class SemanticTypeConfig:
    """语义类型配置 - D1-D5架构权重"""
    
    # D1-D5各层对不同语义类型的权重
    # 基于最新研究数据调整权重分配
    # 关键发现：对称性（Symmetry）是跨文明同源性的最强判别指标
    # - 对称性相关系数：0.68（p<0.001）统计显著
    # - 环数相关系数：0.23（p=0.07）统计不显著
    LAYER_WEIGHTS = {
        SemanticType.CELESTIAL: {
            DecodingLayer.D1_VISUAL: 0.10,
            DecodingLayer.D2_TOPOLOGY: 0.40,  # 提高D2权重（对称性最强判别力）
            DecodingLayer.D3_EVOLUTION: 0.15,
            DecodingLayer.D4_MEANING: 0.20,
            DecodingLayer.D5_COLLAPSE: 0.15
        },
        SemanticType.NATURAL: {
            DecodingLayer.D1_VISUAL: 0.15,
            DecodingLayer.D2_TOPOLOGY: 0.35,  # 提高D2权重
            DecodingLayer.D3_EVOLUTION: 0.20,
            DecodingLayer.D4_MEANING: 0.15,
            DecodingLayer.D5_COLLAPSE: 0.15
        },
        SemanticType.HUMAN: {
            DecodingLayer.D1_VISUAL: 0.10,
            DecodingLayer.D2_TOPOLOGY: 0.40,  # 提高D2权重
            DecodingLayer.D3_EVOLUTION: 0.10,
            DecodingLayer.D4_MEANING: 0.25,
            DecodingLayer.D5_COLLAPSE: 0.15
        },
        SemanticType.ARTIFACT: {
            DecodingLayer.D1_VISUAL: 0.15,
            DecodingLayer.D2_TOPOLOGY: 0.35,  # 提高D2权重
            DecodingLayer.D3_EVOLUTION: 0.15,
            DecodingLayer.D4_MEANING: 0.20,
            DecodingLayer.D5_COLLAPSE: 0.15
        }
    }
    
    # D2拓扑层的子特征权重
    TOPOLOGY_WEIGHTS = {
        "global": 0.40,      # 全局形态锚点
        "core": 0.35,        # 核心拓扑不变量
        "local": 0.25         # 局部结构指纹
    }
    
    # 不同语义类型的最优和次优区分特征
    # 基于最新研究数据调整特征权重
    # 关键发现：对称性（Symmetry）是最强的跨文明同源性判别指标
    # - 对称性相关系数：0.68（p<0.001）统计显著
    # - 环数相关系数：0.23（p=0.07）统计不显著
    FEATURE_PRIORITY = {
        SemanticType.CELESTIAL: {
            "primary": "symmetry",
            "secondary": "euler",
            "weights": {"symmetry": 1.0, "euler": 0.6, "rings": 0.3, "aspect_ratio": 0.4}
        },
        SemanticType.NATURAL: {
            "primary": "symmetry",
            "secondary": "aspect_ratio",
            "weights": {"symmetry": 0.9, "euler": 0.5, "rings": 0.3, "aspect_ratio": 0.8}
        },
        SemanticType.HUMAN: {
            "primary": "symmetry",
            "secondary": "euler",
            "weights": {"symmetry": 1.0, "euler": 0.7, "rings": 0.4, "aspect_ratio": 0.5}
        },
        SemanticType.ARTIFACT: {
            "primary": "symmetry",
            "secondary": "rings",
            "weights": {"symmetry": 0.9, "euler": 0.5, "rings": 0.5, "aspect_ratio": 0.4}
        }
    }


class TCDOriginEngine:
    """TCD Origin 跨文明古文字拓扑破译引擎"""
    
    def __init__(self):
        self.config = SemanticTypeConfig()
        logger.info("TCD Origin 破译引擎初始化完成")
    
    # =========================================================================
    # D1: 视觉形态层 - CNN特征提取
    # =========================================================================
    
    def extract_d1_visual_features(self, image_data: Any) -> D1VisualFeatures:
        """
        D1: 视觉形态层
        利用CNN提取笔画宽度、曲率等基础视觉特征
        
        Args:
            image_data: 图像数据
        
        Returns:
            D1视觉特征
        """
        logger.info("D1: 提取视觉形态特征...")
        
        # 模拟CNN特征提取
        features = D1VisualFeatures(
            stroke_width=0.65,
            stroke_curvature=0.45,
            edge_density=0.72,
            texture_complexity=0.58,
            color_distribution=[0.85, 0.10, 0.05]
        )
        
        logger.info(f"D1特征提取完成: {features}")
        return features
    
    # =========================================================================
    # D2: 拓扑几何层 - 拓扑不变量分析
    # =========================================================================
    
    def extract_d2_topology_features(self, image_data: Any) -> D2TopologyFeatures:
        """
        D2: 拓扑几何层
        核心技术：拓扑不变性分析
        不关注字形的绝对大小，而关注符号的连通性、闭合环数量及节点关系
        
        Args:
            image_data: 图像数据
        
        Returns:
            D2拓扑特征
        """
        logger.info("D2: 提取拓扑几何特征...")
        
        # 模拟拓扑不变量分析
        features = D2TopologyFeatures(
            # 全局形态锚点
            horizontal_symmetry=0.85,
            vertical_symmetry=0.90,
            rotational_symmetry=0.75,
            aspect_ratio=1.2,
            # 核心拓扑不变量
            euler_characteristic=0,
            betti_0=1,
            betti_1=1,
            betti_2=0,
            # 局部结构指纹
            ring_distribution=[1, 0, 0],
            connected_components=1,
            pixel_density=0.45
        )
        
        logger.info(f"D2特征提取完成: 欧拉示性数={features.euler_characteristic}")
        return features
    
    # =========================================================================
    # D3: 时间演化层 - 动力学演化路径
    # =========================================================================
    
    def extract_d3_evolution_features(self, image_data: Any, 
                                    origin_estimate: Optional[str] = None) -> D3EvolutionFeatures:
        """
        D3: 时间演化层
        模拟文字从甲骨文、金文到小篆的动力学演化路径，反向推导未知符号的原始态
        
        Args:
            image_data: 图像数据
            origin_estimate: 原始态估计
        
        Returns:
            D3演化特征
        """
        logger.info("D3: 分析时间演化特征...")
        
        features = D3EvolutionFeatures(
            origin_state=origin_estimate or "甲骨文原始态",
            evolution_stage=2,
            transformation_path=["甲骨文", "金文", "小篆"],
            stability_score=0.78,
            mutation_rate=0.15
        )
        
        logger.info(f"D3特征提取完成: 演化阶段={features.evolution_stage}")
        return features
    
    # =========================================================================
    # D4: 意义确权层 - 语言游戏理论
    # =========================================================================
    
    def extract_d4_meaning_features(self, context: Optional[str] = None) -> D4MeaningFeatures:
        """
        D4: 意义确权层
        引入维特根斯坦的语言游戏理论，通过语境关联锁定符号的社会学意义
        
        Args:
            context: 语境信息
        
        Returns:
            D4意义特征
        """
        logger.info("D4: 分析意义确权特征...")
        
        features = D4MeaningFeatures(
            contextual_anchoring=0.82,
            social_meaning_score=0.75,
            semantic_field=["祭祀", "天文", "王权"],
            language_game_type="宗教仪式符号"
        )
        
        logger.info(f"D4特征提取完成: 语境锚定度={features.contextual_anchoring}")
        return features
    
    # =========================================================================
    # D5: 逻辑坍缩层 - 多维度概率交叉验证
    # =========================================================================
    
    def perform_d5_collapse(self, 
                           d1_features: D1VisualFeatures,
                           d2_features: D2TopologyFeatures,
                           d3_features: D3EvolutionFeatures,
                           d4_features: D4MeaningFeatures) -> D5CollapseResult:
        """
        D5: 逻辑坍缩层
        最终输出。通过多维度概率交叉验证，使模糊的符号意义"坍缩"为唯一的确定性解释
        
        Args:
            d1_features: D1视觉特征
            d2_features: D2拓扑特征
            d3_features: D3演化特征
            d4_features: D4意义特征
        
        Returns:
            D5坍缩结果
        """
        logger.info("D5: 执行逻辑坍缩...")
        
        # 模拟概率分布和坍缩
        probability_distribution = {
            "太阳神符号": 0.65,
            "天体崇拜": 0.25,
            "王权象征": 0.10
        }
        
        result = D5CollapseResult(
            probability_distribution=probability_distribution,
            collapsed_meaning="太阳神符号（高置信度）",
            confidence=0.85,
            cross_validation_score=0.78
        )
        
        logger.info(f"D5坍缩完成: 置信度={result.confidence}")
        return result
    
    # =========================================================================
    # 完整D1-D5分析流程
    # =========================================================================
    
    def full_analysis(self, image_data: Any, 
                     context: Optional[str] = None,
                     origin_estimate: Optional[str] = None) -> TCDHighDimVector:
        """
        执行完整的D1-D5分析流程
        
        Args:
            image_data: 图像数据
            context: 语境信息
            origin_estimate: 原始态估计
        
        Returns:
            TCD Origin高维特征向量
        """
        logger.info("开始TCD Origin完整分析（D1-D5架构）...")
        
        # D1: 视觉形态层
        d1_features = self.extract_d1_visual_features(image_data)
        
        # D2: 拓扑几何层
        d2_features = self.extract_d2_topology_features(image_data)
        
        # D3: 时间演化层
        d3_features = self.extract_d3_evolution_features(image_data, origin_estimate)
        
        # D4: 意义确权层
        d4_features = self.extract_d4_meaning_features(context)
        
        # D5: 逻辑坍缩层
        d5_result = self.perform_d5_collapse(
            d1_features, d2_features, d3_features, d4_features
        )
        
        # 构建高维特征向量
        high_dim_vector = TCDHighDimVector(
            d1_features=d1_features,
            d2_features=d2_features,
            d3_features=d3_features,
            d4_features=d4_features,
            d5_result=d5_result
        )
        
        logger.info("TCD Origin完整分析完成")
        return high_dim_vector
    
    # =========================================================================
    # 拓扑同源性距离公式实现
    # =========================================================================
    
    def calculate_homology_distance(self, 
                                   vector1: TCDHighDimVector,
                                   vector2: TCDHighDimVector,
                                   semantic_type: Optional[SemanticType] = None) -> Dict[str, Any]:
        """
        核心公式: 拓扑同源性距离公式
        
        D(S_a, S_b) = Σ ω_i |T_i(a) - T_i(b)|
        
        其中 T_i 代表第i阶拓扑特征向量，ω_i 为权重系数
        
        Args:
            vector1: 第一个符号的特征向量
            vector2: 第二个符号的特征向量
            semantic_type: 语义类型
        
        Returns:
            包含距离计算结果的字典
        """
        logger.info("计算拓扑同源性距离...")
        
        # 获取特征向量
        t1 = np.array(vector1.to_vector())
        t2 = np.array(vector2.to_vector())
        
        # 获取权重
        if semantic_type is None:
            semantic_type = SemanticType.UNKNOWN
        
        weights = self._get_layer_weights(semantic_type)
        
        # 计算加权距离
        # 将权重应用到对应的特征维度
        vec1_weighted = t1 * np.array(list(weights.values()))
        vec2_weighted = t2 * np.array(list(weights.values()))
        
        # D = Σ ω_i |T_i(a) - T_i(b)|
        distance = np.sum(np.abs(vec1_weighted - vec2_weighted))
        
        # 转换为相似度 (0-1, 1表示完全相同)
        max_possible_distance = np.sum(list(weights.values()))
        similarity = max(0, 1 - distance / max_possible_distance)
        
        # 分层距离分析
        layer_distances = self._calculate_layer_distances(vector1, vector2, weights)
        
        result = {
            "distance": float(distance),
            "similarity": float(similarity),
            "semantic_type": semantic_type.value,
            "layer_weights": weights,
            "layer_distances": layer_distances,
            "formula": "D(S_a, S_b) = Σ ω_i |T_i(a) - T_i(b)|",
            "interpretation": self._interpret_distance(similarity, layer_distances)
        }
        
        logger.info(f"距离计算完成: D={distance:.4f}, 相似度={similarity:.4f}")
        return result
    
    def _get_layer_weights(self, semantic_type: SemanticType) -> Dict[str, float]:
        """获取指定语义类型的D1-D5层权重"""
        return self.config.LAYER_WEIGHTS.get(
            semantic_type,
            self.config.LAYER_WEIGHTS[SemanticType.UNKNOWN]
        )
    
    def _calculate_layer_distances(self, 
                                   vector1: TCDHighDimVector,
                                   vector2: TCDHighDimVector,
                                   weights: Dict[str, float]) -> Dict[str, float]:
        """计算各层的距离"""
        distances = {}
        
        # D1距离
        d1_diff = np.abs(
            np.array(vector1.d1_features.to_vector()) - 
            np.array(vector2.d1_features.to_vector())
        )
        distances["D1_visual"] = float(np.mean(d1_diff))
        
        # D2距离 (核心)
        d2_diff = np.abs(
            np.array(vector1.d2_features.to_vector()) - 
            np.array(vector2.d2_features.to_vector())
        )
        distances["D2_topology"] = float(np.mean(d2_diff))
        
        # D3距离
        d3_diff = np.abs(
            np.array(vector1.d3_features.to_vector()) - 
            np.array(vector2.d3_features.to_vector())
        )
        distances["D3_evolution"] = float(np.mean(d3_diff))
        
        # D4距离
        d4_diff = np.abs(
            np.array(vector1.d4_features.to_vector()) - 
            np.array(vector2.d4_features.to_vector())
        )
        distances["D4_meaning"] = float(np.mean(d4_diff))
        
        return distances
    
    def _interpret_distance(self, similarity: float, 
                           layer_distances: Dict[str, float]) -> str:
        """解释距离计算结果"""
        if similarity > 0.8:
            base_interpretation = "高度同源"
        elif similarity > 0.6:
            base_interpretation = "中等同源"
        elif similarity > 0.4:
            base_interpretation = "低度同源"
        else:
            base_interpretation = "非同源"
        
        # 找出最大差异的层
        max_layer = max(layer_distances, key=layer_distances.get)
        
        return f"{base_interpretation}，D{max_layer.split('_')[0][1]}层差异最大"


class CrossCivilizationAnalyzer:
    """跨文明符号分析器 - TCD Origin版"""
    
    def __init__(self):
        self.tcd_engine = TCDOriginEngine()
        self.config = SemanticTypeConfig()
        logger.info("跨文明符号分析器初始化完成")
    
    def detect_cultural_transmission(self, 
                                   vector1: TCDHighDimVector,
                                   vector2: TCDHighDimVector,
                                   semantic_type: SemanticType) -> Dict[str, Any]:
        """
        检测文化传播信号
        
        Args:
            vector1: 符号1特征
            vector2: 符号2特征
            semantic_type: 语义类型
        
        Returns:
            文化传播分析结果
        """
        logger.info("检测文化传播信号...")
        
        # 环数比较（核心指标）
        rings1 = sum(vector1.d2_features.ring_distribution)
        rings2 = sum(vector2.d2_features.ring_distribution)
        ring_difference = abs(rings1 - rings2)
        
        # 对称性比较
        symmetry1 = vector1.d2_features.rotational_symmetry
        symmetry2 = vector2.d2_features.rotational_symmetry
        symmetry_similarity = 1 - abs(symmetry1 - symmetry2)
        
        # 欧拉示性数比较
        euler1 = vector1.d2_features.euler_characteristic
        euler2 = vector2.d2_features.euler_characteristic
        euler_match = (euler1 == euler2)
        
        # 综合判断
        if ring_difference == 0 and symmetry_similarity > 0.7:
            transmission_signal = "strong"
            interpretation = "环数一致性强，可能存在文化传播或符号借用"
        elif ring_difference > 0 and symmetry_similarity > 0.8:
            transmission_signal = "weak"
            interpretation = "拓扑结构相似但环数不同，可能为独立起源的认知趋同"
        else:
            transmission_signal = "unknown"
            interpretation = "不足以判断是否存在文化传播"
        
        return {
            "ring_comparison": {
                "symbol1_rings": int(rings1),
                "symbol2_rings": int(rings2),
                "difference": int(ring_difference)
            },
            "symmetry_similarity": float(symmetry_similarity),
            "euler_match": bool(euler_match),
            "transmission_signal": transmission_signal,
            "interpretation": interpretation,
            "semantic_type": semantic_type.value
        }
    
    def analyze_homology(self, 
                       symbol1_data: Any, 
                       symbol2_data: Any,
                       semantic_type: Optional[SemanticType] = None) -> Dict[str, Any]:
        """
        分析跨文明符号同源性 - TCD Origin版
        
        Args:
            symbol1_data: 符号1数据
            symbol2_data: 符号2数据
            semantic_type: 语义类型
        
        Returns:
            同源性分析结果
        """
        logger.info("开始TCD Origin跨文明符号同源性分析...")
        
        # 提取D1-D5特征
        vector1 = self.tcd_engine.full_analysis(symbol1_data)
        vector2 = self.tcd_engine.full_analysis(symbol2_data)
        
        # 自动检测语义类型
        if semantic_type is None:
            semantic_type = self._detect_semantic_type(vector1)
        
        # 计算拓扑同源性距离
        distance_result = self.tcd_engine.calculate_homology_distance(
            vector1, vector2, semantic_type
        )
        
        # 检测文化传播
        transmission_result = self.detect_cultural_transmission(
            vector1, vector2, semantic_type
        )
        
        # 同源性判定
        similarity = distance_result["similarity"]
        if similarity > 0.7:
            homology_level = "high"
            interpretation = "拓扑相似度高，可能存在同源性"
        elif similarity > 0.4:
            homology_level = "medium"
            interpretation = "拓扑相似度中等，需要进一步分析"
        else:
            homology_level = "low"
            interpretation = "拓扑相似度低，可能为独立起源"
        
        result = {
            "semantic_type": semantic_type.value,
            "homology_level": homology_level,
            "distance": distance_result["distance"],
            "similarity": similarity,
            "interpretation": interpretation,
            "features": {
                "symbol1": vector1.to_dict(),
                "symbol2": vector2.to_dict()
            },
            "transmission_analysis": transmission_result,
            "layer_analysis": distance_result["layer_distances"],
            "formula": distance_result["formula"]
        }
        
        logger.info(f"同源性分析完成: {homology_level}")
        return result
    
    def _detect_semantic_type(self, vector: TCDHighDimVector) -> SemanticType:
        """根据D2拓扑特征检测语义类型"""
        symmetry = vector.d2_features.rotational_symmetry
        aspect_ratio = vector.d2_features.aspect_ratio
        rings = sum(vector.d2_features.ring_distribution)
        
        if symmetry > 0.8 and rings > 0:
            return SemanticType.CELESTIAL
        elif aspect_ratio > 1.5:
            return SemanticType.NATURAL
        elif symmetry > 0.6 and rings > 0:
            return SemanticType.HUMAN
        elif rings > 0:
            return SemanticType.ARTIFACT
        else:
            return SemanticType.UNKNOWN


# 导出主要类和函数
__all__ = [
    'TCDOriginEngine',
    'CrossCivilizationAnalyzer',
    'DecodingLayer',
    'SemanticType',
    'TCDHighDimVector',
    'D1VisualFeatures',
    'D2TopologyFeatures',
    'D3EvolutionFeatures',
    'D4MeaningFeatures',
    'D5CollapseResult',
    'SemanticTypeConfig'
]
