"""
古文字破译系统 - 工具集
"""

# 导入火山引擎知识库工具
from src.tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat,
    VolcengineKnowledgeConfig
)

# 导入TCD Origin破译引擎工具
from src.tools.tcd_origin_engine import (
    TCDOriginEngine,
    CrossCivilizationAnalyzer,
    DecodingLayer,
    SemanticType,
    TCDHighDimVector,
    D1VisualFeatures,
    D2TopologyFeatures,
    D3EvolutionFeatures,
    D4MeaningFeatures,
    D5CollapseResult,
    SemanticTypeConfig
)

from src.tools.tcd_origin_tools import (
    tcd_full_analysis,
    tcd_homology_distance,
    tcd_layer_analysis,
    tcd_cultural_transmission_detect,
    TCD_ORIGIN_TOOLS,
    get_tcd_origin_tools
)

# 导入拓扑分析工具（专利技术）
from src.tools.topology_analyzer import (
    TopologyAnalyzer,
    CrossCivilizationAnalyzer as LegacyCrossAnalyzer,
    SemanticType as LegacySemanticType
)

__all__ = [
    # 火山引擎知识库工具
    "search_volcengine_knowledge",
    "search_volcengine_knowledge_with_context",
    "multi_round_knowledge_chat",
    "VolcengineKnowledgeConfig",
    
    # TCD Origin破译引擎工具
    "TCDOriginEngine",
    "CrossCivilizationAnalyzer",
    "DecodingLayer",
    "SemanticType",
    "TCDHighDimVector",
    "D1VisualFeatures",
    "D2TopologyFeatures",
    "D3EvolutionFeatures",
    "D4MeaningFeatures",
    "D5CollapseResult",
    "SemanticTypeConfig",
    "tcd_full_analysis",
    "tcd_homology_distance",
    "tcd_layer_analysis",
    "tcd_cultural_transmission_detect",
    "TCD_ORIGIN_TOOLS",
    "get_tcd_origin_tools",
    
    # 拓扑分析工具（专利技术）
    "TopologyAnalyzer",
    "LegacyCrossAnalyzer",
    "LegacySemanticType"
]
