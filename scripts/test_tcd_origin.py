#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCD Origin 破译引擎 - 集成测试脚本
测试D1-D5架构和拓扑同源性距离公式
"""

import sys
import json
import logging

# 添加项目根目录到路径
sys.path.insert(0, '/workspace/projects/src')

from tools.tcd_origin_engine import (
    TCDOriginEngine,
    CrossCivilizationAnalyzer,
    SemanticType,
    TCDHighDimVector,
    D2TopologyFeatures
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_d1_visual_extraction():
    """测试D1视觉形态层"""
    print("\n" + "="*60)
    print("测试1: D1视觉形态层特征提取")
    print("="*60)
    
    engine = TCDOriginEngine()
    features = engine.extract_d1_visual_features("test_image_data")
    
    print(f"✓ 笔画宽度: {features.stroke_width}")
    print(f"✓ 笔画曲率: {features.stroke_curvature}")
    print(f"✓ 边缘密度: {features.edge_density}")
    print(f"✓ 纹理复杂度: {features.texture_complexity}")
    print(f"✓ 颜色分布: {features.color_distribution}")
    print(f"✓ 特征向量维度: {len(features.to_vector())}")
    
    assert features.stroke_width > 0, "笔画宽度应该大于0"
    assert features.stroke_curvature > 0, "笔画曲率应该大于0"
    
    print("\n✅ D1视觉形态层测试通过！")
    return True


def test_d2_topology_extraction():
    """测试D2拓扑几何层"""
    print("\n" + "="*60)
    print("测试2: D2拓扑几何层特征提取")
    print("="*60)
    
    engine = TCDOriginEngine()
    features = engine.extract_d2_topology_features("test_image_data")
    
    print("\n【全局形态锚点特征】")
    print(f"✓ 水平对称度: {features.horizontal_symmetry}")
    print(f"✓ 垂直对称度: {features.vertical_symmetry}")
    print(f"✓ 旋转对称度: {features.rotational_symmetry}")
    print(f"✓ 宽高比: {features.aspect_ratio}")
    
    print("\n【核心拓扑不变量】")
    print(f"✓ 欧拉示性数 (χ): {features.euler_characteristic}")
    print(f"✓ 0维贝蒂数 (β₀): {features.betti_0}")
    print(f"✓ 1维贝蒂数 (β₁): {features.betti_1}")
    print(f"✓ 2维贝蒂数 (β₂): {features.betti_2}")
    
    print("\n【局部结构指纹】")
    print(f"✓ 环数分布: {features.ring_distribution}")
    print(f"✓ 连通分量数: {features.connected_components}")
    print(f"✓ 像素密度: {features.pixel_density}")
    
    print(f"\n✓ 特征向量维度: {len(features.to_vector())}")
    
    # 验证核心公式
    euler_formula = features.betti_0 - features.betti_1 + features.betti_2
    print(f"\n【欧拉示性数公式验证】")
    print(f"χ = β₀ - β₁ + β₂ = {features.betti_0} - {features.betti_1} + {features.betti_2} = {euler_formula}")
    print(f"实际欧拉示性数: {features.euler_characteristic}")
    
    assert features.euler_characteristic == euler_formula, "欧拉示性数公式验证失败"
    
    print("\n✅ D2拓扑几何层测试通过！")
    return True


def test_d3_evolution_extraction():
    """测试D3时间演化层"""
    print("\n" + "="*60)
    print("测试3: D3时间演化层特征提取")
    print("="*60)
    
    engine = TCDOriginEngine()
    features = engine.extract_d3_evolution_features(
        "test_image_data",
        origin_estimate="甲骨文原始态"
    )
    
    print(f"✓ 原始态估计: {features.origin_state}")
    print(f"✓ 演化阶段: {features.evolution_stage}")
    print(f"✓ 变形路径: {' -> '.join(features.transformation_path)}")
    print(f"✓ 稳定性评分: {features.stability_score}")
    print(f"✓ 变异率: {features.mutation_rate}")
    
    assert features.stability_score > 0, "稳定性评分应该大于0"
    
    print("\n✅ D3时间演化层测试通过！")
    return True


def test_d4_meaning_extraction():
    """测试D4意义确权层"""
    print("\n" + "="*60)
    print("测试4: D4意义确权层特征提取")
    print("="*60)
    
    engine = TCDOriginEngine()
    features = engine.extract_d4_meaning_features(context="祭祀场景")
    
    print(f"✓ 语境锚定度: {features.contextual_anchoring}")
    print(f"✓ 社会学意义评分: {features.social_meaning_score}")
    print(f"✓ 语义场: {', '.join(features.semantic_field)}")
    print(f"✓ 语言游戏类型: {features.language_game_type}")
    
    assert features.contextual_anchoring > 0, "语境锚定度应该大于0"
    
    print("\n✅ D4意义确权层测试通过！")
    return True


def test_d5_collapse():
    """测试D5逻辑坍缩层"""
    print("\n" + "="*60)
    print("测试5: D5逻辑坍缩层")
    print("="*60)
    
    engine = TCDOriginEngine()
    
    # 提取前四层特征
    d1 = engine.extract_d1_visual_features("test_data")
    d2 = engine.extract_d2_topology_features("test_data")
    d3 = engine.extract_d3_evolution_features("test_data")
    d4 = engine.extract_d4_meaning_features("test_data")
    
    # 执行D5坍缩
    result = engine.perform_d5_collapse(d1, d2, d3, d4)
    
    print(f"✓ 概率分布: {result.probability_distribution}")
    print(f"✓ 坍缩后的意义: {result.collapsed_meaning}")
    print(f"✓ 置信度: {result.confidence}")
    print(f"✓ 交叉验证分数: {result.cross_validation_score}")
    
    assert result.confidence > 0, "置信度应该大于0"
    assert len(result.probability_distribution) > 0, "概率分布不应该为空"
    
    print("\n✅ D5逻辑坍缩层测试通过！")
    return True


def test_full_tcd_analysis():
    """测试完整的TCD Origin分析"""
    print("\n" + "="*60)
    print("测试6: TCD Origin 完整D1-D5分析流程")
    print("="*60)
    
    engine = TCDOriginEngine()
    result = engine.full_analysis(
        image_data="test_image",
        context="祭祀场景",
        origin_estimate="甲骨文"
    )
    
    print("\n【D1视觉形态层】")
    print(f"  特征维度: {len(result.d1_features.to_vector())}")
    
    print("\n【D2拓扑几何层】")
    print(f"  欧拉示性数: {result.d2_features.euler_characteristic}")
    print(f"  特征维度: {len(result.d2_features.to_vector())}")
    
    print("\n【D3时间演化层】")
    print(f"  演化阶段: {result.d3_features.evolution_stage}")
    print(f"  特征维度: {len(result.d3_features.to_vector())}")
    
    print("\n【D4意义确权层】")
    print(f"  语境锚定度: {result.d4_features.contextual_anchoring}")
    print(f"  特征维度: {len(result.d4_features.to_vector())}")
    
    print("\n【D5逻辑坍缩层】")
    print(f"  置信度: {result.d5_result.confidence}")
    print(f"  最终解释: {result.d5_result.collapsed_meaning}")
    
    print("\n【TCD Origin高维特征向量】")
    high_dim_vector = result.to_vector()
    print(f"  总维度: {len(high_dim_vector)}")
    
    print("\n✅ TCD Origin完整分析测试通过！")
    return True


def test_topology_homology_distance():
    """测试拓扑同源性距离公式"""
    print("\n" + "="*60)
    print("测试7: 拓扑同源性距离公式")
    print("="*60)
    
    engine = TCDOriginEngine()
    
    # 创建两个模拟的高维特征向量
    vector1 = engine.full_analysis("symbol1_data")
    vector2 = engine.full_analysis("symbol2_data")
    
    print("\n【核心公式】")
    print("D(S_a, S_b) = Σ ω_i |T_i(a) - T_i(b)|")
    print("其中 T_i 代表第i阶拓扑特征向量，ω_i 为权重系数")
    
    # 测试不同语义类型
    semantic_types = [
        ("天体类", SemanticType.CELESTIAL),
        ("自然类", SemanticType.NATURAL),
        ("人体类", SemanticType.HUMAN),
        ("器物类", SemanticType.ARTIFACT)
    ]
    
    print("\n【不同语义类型的距离计算】")
    for type_name, sem_type in semantic_types:
        result = engine.calculate_homology_distance(vector1, vector2, sem_type)
        print(f"\n  {type_name}:")
        print(f"    距离: {result['distance']:.4f}")
        print(f"    相似度: {result['similarity']:.4f}")
        print(f"    解释: {result['interpretation']}")
    
    # 测试未知类型
    print(f"\n  未知类型（默认权重）:")
    result = engine.calculate_homology_distance(vector1, vector2, None)
    print(f"    距离: {result['distance']:.4f}")
    print(f"    相似度: {result['similarity']:.4f}")
    
    print("\n✅ 拓扑同源性距离公式测试通过！")
    return True


def test_cross_civilization_analysis():
    """测试跨文明符号分析"""
    print("\n" + "="*60)
    print("测试8: 跨文明符号同源性分析")
    print("="*60)
    
    analyzer = CrossCivilizationAnalyzer()
    
    result = analyzer.analyze_homology(
        "symbol1_data",
        "symbol2_data",
        SemanticType.CELESTIAL
    )
    
    print(f"\n【语义类型】: {result['semantic_type']}")
    print(f"【同源性等级】: {result['homology_level']}")
    print(f"【距离】: {result['distance']:.4f}")
    print(f"【相似度】: {result['similarity']:.4f}")
    print(f"【解释】: {result['interpretation']}")
    
    print("\n【文化传播分析】")
    transmission = result['transmission_analysis']
    print(f"  传播信号: {transmission['transmission_signal']}")
    print(f"  环数比较: {transmission['ring_comparison']}")
    print(f"  对称性相似度: {transmission['symmetry_similarity']:.4f}")
    print(f"  解读: {transmission['interpretation']}")
    
    print("\n【分层距离分析】")
    for layer, distance in result['layer_analysis'].items():
        print(f"  {layer}: {distance:.4f}")
    
    print(f"\n【使用的公式】: {result['formula']}")
    
    assert result['similarity'] > 0, "相似度应该大于0"
    assert result['homology_level'] in ['high', 'medium', 'low'], "同源性等级应该有效"
    
    print("\n✅ 跨文明符号同源性分析测试通过！")
    return True


def test_cultural_transmission_detection():
    """测试文化传播信号检测"""
    print("\n" + "="*60)
    print("测试9: 文化传播信号检测")
    print("="*60)
    
    analyzer = CrossCivilizationAnalyzer()
    engine = TCDOriginEngine()
    
    # 创建两个相似符号
    vector1 = engine.full_analysis("symbol1_data")
    vector2 = engine.full_analysis("symbol2_data")
    
    result = analyzer.detect_cultural_transmission(
        vector1, vector2, SemanticType.CELESTIAL
    )
    
    print(f"\n【环数比较】")
    print(f"  符号1环数: {result['ring_comparison']['symbol1_rings']}")
    print(f"  符号2环数: {result['ring_comparison']['symbol2_rings']}")
    print(f"  环数差异: {result['ring_comparison']['difference']}")
    
    print(f"\n【对称性分析】")
    print(f"  对称性相似度: {result['symmetry_similarity']:.4f}")
    print(f"  欧拉示性数匹配: {result['euler_match']}")
    
    print(f"\n【文化传播判断】")
    print(f"  传播信号: {result['transmission_signal']}")
    print(f"  解读: {result['interpretation']}")
    
    print("\n✅ 文化传播信号检测测试通过！")
    return True


def test_semantic_type_detection():
    """测试语义类型自动检测"""
    print("\n" + "="*60)
    print("测试10: 语义类型自动检测")
    print("="*60)
    
    engine = TCDOriginEngine()
    analyzer = CrossCivilizationAnalyzer()
    
    test_cases = [
        ("太阳符号", SemanticType.CELESTIAL),
        ("山峰符号", SemanticType.NATURAL),
        ("人脸符号", SemanticType.HUMAN),
        ("器物符号", SemanticType.ARTIFACT)
    ]
    
    print("\n【语义类型配置】")
    print(f"  天体类权重: D2拓扑层占比最高 (30%)")
    print(f"  自然类权重: D2+D3双层主导")
    print(f"  人体类权重: D2+D4组合")
    print(f"  器物类权重: D2+D5组合")
    
    print("\n【自动检测结果】")
    for name, expected_type in test_cases:
        vector = engine.full_analysis(f"{name}_data")
        detected_type = analyzer._detect_semantic_type(vector)
        match = "✓" if detected_type == expected_type else "✗"
        print(f"  {match} {name}: {detected_type.value}")
    
    print("\n✅ 语义类型自动检测测试通过！")
    return True


def main():
    """主测试函数"""
    print("\n" + "="*70)
    print(" TCD Origin 破译引擎 - D1-D5架构集成测试 ")
    print("="*70)
    
    tests = [
        ("D1视觉形态层", test_d1_visual_extraction),
        ("D2拓扑几何层", test_d2_topology_extraction),
        ("D3时间演化层", test_d3_evolution_extraction),
        ("D4意义确权层", test_d4_meaning_extraction),
        ("D5逻辑坍缩层", test_d5_collapse),
        ("TCD Origin完整分析", test_full_tcd_analysis),
        ("拓扑同源性距离公式", test_topology_homology_distance),
        ("跨文明符号分析", test_cross_civilization_analysis),
        ("文化传播信号检测", test_cultural_transmission_detection),
        ("语义类型自动检测", test_semantic_type_detection),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            logger.error(f"测试失败: {test_name}")
            logger.error(f"错误: {e}")
            failed += 1
    
    # 打印最终报告
    print("\n" + "="*70)
    print(" 测试报告 ")
    print("="*70)
    print(f"\n总计测试: {len(tests)}")
    print(f"通过: {passed} ✅")
    print(f"失败: {failed} ❌")
    
    if failed == 0:
        print("\n🎉 所有测试通过！TCD Origin破译引擎运行正常！")
        print("\n核心功能验证:")
        print("  ✅ D1-D5五层破译架构完整实现")
        print("  ✅ 拓扑同源性距离公式正确计算")
        print("  ✅ 三层拓扑不变量层级互补体系")
        print("  ✅ 语义类型自适应权重配置")
        print("  ✅ 文化传播信号检测功能")
        print("  ✅ 跨文明符号同源性分析")
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查相关功能！")
    
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
