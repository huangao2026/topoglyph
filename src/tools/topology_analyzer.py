#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古文字拓扑特征分析工具
基于专利技术文档实现三层拓扑不变量层级互补体系

功能：
1. 全局形态锚点特征提取（对称性指数、宽高比）
2. 核心拓扑不变量计算（欧拉示性数、贝蒂数序列）
3. 局部结构指纹特征提取（环数分布、连通分量数、像素密度）
4. 高维拓扑特征向量生成
5. 语义类型自适应权重调整
6. 跨文明符号同源性分析
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import math

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SemanticType(Enum):
    """语义类型枚举"""
    CELESTIAL = "天体类"      # 日、月、星、天
    NATURAL = "自然类"         # 山、水、火、土
    HUMAN = "人体类"          # 人、目、口、手、首
    ARTIFACT = "器物类"       # 田、皿、弓、宅、矢
    UNKNOWN = "未知"


@dataclass
class GlobalMorphologyFeatures:
    """全局形态锚点特征"""
    horizontal_symmetry: float = 0.0  # 水平对称度
    vertical_symmetry: float = 0.0    # 垂直对称度
    rotational_symmetry: float = 0.0   # 旋转对称度
    aspect_ratio: float = 1.0          # 宽高比
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        return [
            self.horizontal_symmetry,
            self.vertical_symmetry,
            self.rotational_symmetry,
            self.aspect_ratio
        ]


@dataclass
class CoreTopologyInvariants:
    """核心拓扑不变量"""
    euler_characteristic: int = 0      # 欧拉示性数 χ = 连通分量数 - 环数
    betti_0: int = 0                   # 0维贝蒂数（连通分支数）
    betti_1: int = 0                   # 1维贝蒂数（独立环数）
    betti_2: int = 0                   # 2维贝蒂数（空腔数）
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        return [
            float(self.euler_characteristic),
            float(self.betti_0),
            float(self.betti_1),
            float(self.betti_2)
        ]


@dataclass
class LocalStructureFingerprint:
    """局部结构指纹特征"""
    ring_distribution: List[int] = None  # 环数分布
    connected_components: int = 0         # 连通分量数
    pixel_density: float = 0.0            # 像素密度
    
    def __post_init__(self):
        if self.ring_distribution is None:
            self.ring_distribution = []
    
    def to_vector(self) -> List[float]:
        """转换为特征向量"""
        rings = self.ring_distribution if self.ring_distribution else [0]
        return [
            sum(rings),  # 总环数
            float(self.connected_components),
            self.pixel_density
        ]


@dataclass
class TopologyFeatureVector:
    """高维拓扑特征向量"""
    global_features: GlobalMorphologyFeatures = None
    core_invariants: CoreTopologyInvariants = None
    local_fingerprint: LocalStructureFingerprint = None
    
    def __post_init__(self):
        if self.global_features is None:
            self.global_features = GlobalMorphologyFeatures()
        if self.core_invariants is None:
            self.core_invariants = CoreTopologyInvariants()
        if self.local_fingerprint is None:
            self.local_fingerprint = LocalStructureFingerprint()
    
    def to_vector(self) -> List[float]:
        """生成128维高维特征向量"""
        global_vec = self.global_features.to_vector()
        core_vec = self.core_invariants.to_vector()
        local_vec = self.local_fingerprint.to_vector()
        
        # 融合三层特征生成128维向量
        # T = [对称性指数×3, 宽高比, 欧拉示性数, 贝蒂数×3, 环数, 连通分量数, 像素密度, ...]
        base_features = global_vec + core_vec + local_vec
        
        # 填充到128维（简化版本，实际中可能需要更多特征工程）
        padding = [0.0] * (128 - len(base_features))
        return base_features + padding
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "global_features": asdict(self.global_features),
            "core_invariants": asdict(self.core_invariants),
            "local_fingerprint": asdict(self.local_fingerprint),
            "high_dim_vector": self.to_vector()
        }


class SemanticTypeConfig:
    """语义类型配置"""
    
    # 不同语义类型的最优和次优区分特征
    FEATURE_PRIORITY = {
        SemanticType.CELESTIAL: {
            "primary": "symmetry",
            "secondary": "rings",
            "weights": {"symmetry": 1.0, "euler": 0.4, "rings": 0.6, "aspect_ratio": 0.3}
        },
        SemanticType.NATURAL: {
            "primary": "aspect_ratio",
            "secondary": "euler",
            "weights": {"symmetry": 0.3, "euler": 0.6, "rings": 0.4, "aspect_ratio": 1.0}
        },
        SemanticType.HUMAN: {
            "primary": "symmetry+rings",
            "secondary": "betti",
            "weights": {"symmetry": 0.7, "euler": 0.5, "rings": 0.7, "aspect_ratio": 0.4}
        },
        SemanticType.ARTIFACT: {
            "primary": "rings",
            "secondary": "symmetry",
            "weights": {"symmetry": 0.6, "euler": 0.5, "rings": 1.0, "aspect_ratio": 0.3}
        }
    }
    
    # 三层特征权重
    LAYER_WEIGHTS = {
        "global": 0.40,      # 全局形态锚点
        "core": 0.35,        # 核心拓扑不变量
        "local": 0.25         # 局部结构指纹
    }


class TopologyAnalyzer:
    """拓扑特征分析器"""
    
    def __init__(self):
        self.config = SemanticTypeConfig()
        logger.info("拓扑特征分析器初始化完成")
    
    def extract_global_morphology(self, image_data: Any) -> GlobalMorphologyFeatures:
        """
        提取全局形态锚点特征
        
        Args:
            image_data: 图像数据（可以是URL、文件路径或numpy数组）
        
        Returns:
            全局形态特征
        """
        logger.info("提取全局形态锚点特征...")
        
        # 这里应该是实际的图像处理代码
        # 由于是演示，我们返回模拟数据
        features = GlobalMorphologyFeatures(
            horizontal_symmetry=0.85,
            vertical_symmetry=0.90,
            rotational_symmetry=0.75,
            aspect_ratio=1.2
        )
        
        logger.info(f"全局形态特征提取完成: {features}")
        return features
    
    def calculate_core_invariants(self, image_data: Any) -> CoreTopologyInvariants:
        """
        计算核心拓扑不变量
        
        Args:
            image_data: 图像数据
        
        Returns:
            核心拓扑不变量
        """
        logger.info("计算核心拓扑不变量...")
        
        # 欧拉示性数计算公式: χ = 连通分量数 - 环数
        # 这里应该是实际的拓扑计算代码
        connected_components = 1
        ring_count = 1
        euler_characteristic = connected_components - ring_count
        
        invariants = CoreTopologyInvariants(
            euler_characteristic=euler_characteristic,
            betti_0=connected_components,
            betti_1=ring_count,
            betti_2=0  # 通常二维图像没有空腔
        )
        
        logger.info(f"核心拓扑不变量计算完成: {invariants}")
        return invariants
    
    def extract_local_fingerprint(self, image_data: Any) -> LocalStructureFingerprint:
        """
        提取局部结构指纹特征
        
        Args:
            image_data: 图像数据
        
        Returns:
            局部结构指纹
        """
        logger.info("提取局部结构指纹特征...")
        
        # 这里应该是实际的局部特征提取代码
        fingerprint = LocalStructureFingerprint(
            ring_distribution=[1, 0, 0],  # 假设有1个主环
            connected_components=1,
            pixel_density=0.45
        )
        
        logger.info(f"局部结构指纹提取完成: {fingerprint}")
        return fingerprint
    
    def extract_all_features(self, image_data: Any) -> TopologyFeatureVector:
        """
        提取所有拓扑特征
        
        Args:
            image_data: 图像数据
        
        Returns:
            高维拓扑特征向量
        """
        logger.info("开始提取完整拓扑特征...")
        
        global_features = self.extract_global_morphology(image_data)
        core_invariants = self.calculate_core_invariants(image_data)
        local_fingerprint = self.extract_local_fingerprint(image_data)
        
        feature_vector = TopologyFeatureVector(
            global_features=global_features,
            core_invariants=core_invariants,
            local_fingerprint=local_fingerprint
        )
        
        logger.info("完整拓扑特征提取完成")
        return feature_vector
    
    def calculate_topology_similarity(self, features1: TopologyFeatureVector, 
                                     features2: TopologyFeatureVector) -> float:
        """
        计算两个符号的拓扑相似度
        
        Args:
            features1: 第一个符号的特征
            features2: 第二个符号的特征
        
        Returns:
            相似度分数 (0-1)
        """
        vec1 = features1.to_vector()
        vec2 = features2.to_vector()
        
        # 余弦相似度
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return max(0.0, min(1.0, similarity))
    
    def analyze_semantic_type(self, features: TopologyFeatureVector) -> SemanticType:
        """
        根据拓扑特征分析语义类型
        
        Args:
            features: 拓扑特征
        
        Returns:
            语义类型
        """
        logger.info("分析语义类型...")
        
        # 简化版语义分析逻辑
        symmetry = features.global_features.rotational_symmetry
        rings = sum(features.local_fingerprint.ring_distribution)
        
        if symmetry > 0.8 and rings > 0:
            return SemanticType.CELESTIAL
        elif features.global_features.aspect_ratio > 1.5:
            return SemanticType.NATURAL
        elif symmetry > 0.6 and rings > 0:
            return SemanticType.HUMAN
        elif rings > 0:
            return SemanticType.ARTIFACT
        else:
            return SemanticType.UNKNOWN


class CrossCivilizationAnalyzer:
    """跨文明符号分析器"""
    
    def __init__(self):
        self.topology_analyzer = TopologyAnalyzer()
        self.config = SemanticTypeConfig()
        logger.info("跨文明符号分析器初始化完成")
    
    def detect_cultural_transmission(self, symbol1_features: TopologyFeatureVector,
                                     symbol2_features: TopologyFeatureVector,
                                     semantic_type: SemanticType) -> Dict[str, Any]:
        """
        检测文化传播信号
        
        Args:
            symbol1_features: 符号1特征
            symbol2_features: 符号2特征
            semantic_type: 语义类型
        
        Returns:
            文化传播分析结果
        """
        logger.info("检测文化传播信号...")
        
        # 环数比较（文化传播的核心指标）
        rings1 = sum(symbol1_features.local_fingerprint.ring_distribution)
        rings2 = sum(symbol2_features.local_fingerprint.ring_distribution)
        ring_difference = abs(rings1 - rings2)
        
        # 对称性比较
        symmetry1 = symbol1_features.global_features.rotational_symmetry
        symmetry2 = symbol2_features.global_features.rotational_symmetry
        symmetry_similarity = 1 - abs(symmetry1 - symmetry2)
        
        # 欧拉示性数比较
        euler1 = symbol1_features.core_invariants.euler_characteristic
        euler2 = symbol2_features.core_invariants.euler_characteristic
        euler_match = (euler1 == euler2)
        
        # 综合判断
        if ring_difference == 0 and symmetry_similarity > 0.7:
            # 环数相同但拓扑相似度一般 -> 文化传播信号
            transmission_signal = "strong"
            interpretation = "环数一致性强，可能存在文化传播或符号借用"
        elif ring_difference > 0 and symmetry_similarity > 0.8:
            # 环数不同但对称性高度相似 -> 独立起源但认知趋同
            transmission_signal = "weak"
            interpretation = "拓扑结构相似但环数不同，可能为独立起源的认知趋同"
        else:
            # 无法判断
            transmission_signal = "unknown"
            interpretation = "不足以判断是否存在文化传播"
        
        return {
            "ring_comparison": {
                "symbol1_rings": rings1,
                "symbol2_rings": rings2,
                "difference": ring_difference
            },
            "symmetry_similarity": symmetry_similarity,
            "euler_match": euler_match,
            "transmission_signal": transmission_signal,
            "interpretation": interpretation,
            "semantic_type": semantic_type.value
        }
    
    def analyze_homology(self, symbol1_data: Any, symbol2_data: Any,
                        semantic_type: Optional[SemanticType] = None) -> Dict[str, Any]:
        """
        分析跨文明符号同源性
        
        Args:
            symbol1_data: 符号1数据
            symbol2_data: 符号2数据
            semantic_type: 语义类型（可选，自动检测）
        
        Returns:
            同源性分析结果
        """
        logger.info("开始跨文明符号同源性分析...")
        
        # 提取特征
        features1 = self.topology_analyzer.extract_all_features(symbol1_data)
        features2 = self.topology_analyzer.extract_all_features(symbol2_data)
        
        # 自动检测语义类型
        if semantic_type is None:
            semantic_type = self.topology_analyzer.analyze_semantic_type(features1)
        
        # 计算基础相似度
        base_similarity = self.topology_analyzer.calculate_topology_similarity(
            features1, features2
        )
        
        # 获取该语义类型的特征权重
        type_config = self.config.FEATURE_PRIORITY.get(semantic_type, 
            self.config.FEATURE_PRIORITY[SemanticType.UNKNOWN])
        
        # 计算加权相似度
        weighted_similarity = self._calculate_weighted_similarity(
            features1, features2, semantic_type, type_config
        )
        
        # 检测文化传播
        transmission_result = self.detect_cultural_transmission(
            features1, features2, semantic_type
        )
        
        # 同源性判定
        if weighted_similarity > 0.7:
            homology_level = "high"
            interpretation = "拓扑相似度高，可能存在同源性"
        elif weighted_similarity > 0.4:
            homology_level = "medium"
            interpretation = "拓扑相似度中等，需要进一步分析"
        else:
            homology_level = "low"
            interpretation = "拓扑相似度低，可能为独立起源"
        
        result = {
            "semantic_type": semantic_type.value,
            "base_similarity": base_similarity,
            "weighted_similarity": weighted_similarity,
            "homology_level": homology_level,
            "interpretation": interpretation,
            "features": {
                "symbol1": features1.to_dict(),
                "symbol2": features2.to_dict()
            },
            "transmission_analysis": transmission_result,
            "feature_weights": type_config
        }
        
        logger.info(f"同源性分析完成: {homology_level}")
        return result
    
    def _calculate_weighted_similarity(self, features1: TopologyFeatureVector,
                                       features2: TopologyFeatureVector,
                                       semantic_type: SemanticType,
                                       type_config: Dict) -> float:
        """计算加权相似度"""
        weights = type_config["weights"]
        
        # 各层相似度
        global_similarity = 1 - abs(
            features1.global_features.rotational_symmetry - 
            features2.global_features.rotational_symmetry
        )
        
        core_similarity = 1.0 if (
            features1.core_invariants.euler_characteristic == 
            features2.core_invariants.euler_characteristic
        ) else 0.5
        
        ring1 = sum(features1.local_fingerprint.ring_distribution)
        ring2 = sum(features2.local_fingerprint.ring_distribution)
        local_similarity = 1.0 if ring1 == ring2 else 0.5
        
        # 加权平均
        weighted = (
            global_similarity * weights.get("symmetry", 0.4) +
            core_similarity * weights.get("euler", 0.3) +
            local_similarity * weights.get("rings", 0.3)
        )
        
        total_weight = sum(weights.values())
        return weighted / total_weight if total_weight > 0 else 0.0


# 导出主要类和函数
__all__ = [
    'TopologyAnalyzer',
    'CrossCivilizationAnalyzer',
    'SemanticType',
    'GlobalMorphologyFeatures',
    'CoreTopologyInvariants',
    'LocalStructureFingerprint',
    'TopologyFeatureVector',
    'SemanticTypeConfig'
]
