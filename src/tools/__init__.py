"""
古文字破译系统 - 工具集
"""

# 导入现有工具（如果有）
# from tools.some_tool import some_function

# 导入火山引擎知识库工具
from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat,
    VolcengineKnowledgeConfig
)

__all__ = [
    # 火山引擎知识库工具
    "search_volcengine_knowledge",
    "search_volcengine_knowledge_with_context",
    "multi_round_knowledge_chat",
    "VolcengineKnowledgeConfig",
]
