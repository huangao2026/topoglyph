#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古文字破译智能体 - 增强版
集成拓扑特征分析和跨文明同源性分析功能

基于专利技术文档实现：
1. 三层拓扑不变量层级互补体系
2. 语义类型自适应权重调整
3. 文化传播信号检测
4. 跨文明符号同源性分析
"""

import os
import json
from typing import Annotated, List, Dict, Any
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入所有工具
from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat
)

from tools.cross_civilization_tools import (
    extract_topology_features,
    analyze_cross_civilization_homology,
    detect_cultural_transmission,
    analyze_semantic_type_from_features,
    get_topology_tools,
    handle_topology_tool_errors
)

# 配置路径
LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]


class AgentState(MessagesState):
    """增强版Agent状态，包含消息历史和上下文"""
    messages: Annotated[list[AnyMessage], _windowed_messages]
    current_analysis: Annotated[Dict[str, Any], add_messages] = {}


def build_enhanced_agent(ctx=None) -> Any:
    """
    构建增强版古文字破译智能体
    
    集成功能：
    1. 火山引擎知识库查询
    2. 拓扑特征提取与分析
    3. 跨文明同源性分析
    4. 文化传播检测
    5. 语义类型识别
    
    Returns:
        配置好的Agent实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    # 加载配置
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # 获取API配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    # 初始化大语言模型
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 获取拓扑分析工具
    topology_tools = get_topology_tools()
    
    # 所有工具列表
    all_tools = [
        # 火山引擎知识库工具
        search_volcengine_knowledge,
        search_volcengine_knowledge_with_context,
        multi_round_knowledge_chat,
        # 拓扑分析工具
        extract_topology_features,
        analyze_cross_civilization_homology,
        detect_cultural_transmission,
        analyze_semantic_type_from_features
    ]
    
    # 构建增强版System Prompt
    enhanced_system_prompt = """你是古文字破译专家智能体，集成了专利技术文档中的前沿分析方法。

## 核心能力

### 1. 拓扑特征分析（基于专利技术）
采用"三层拓扑不变量层级互补体系"：
- **第一层：全局形态锚点特征**（权重40%）
  - 对称性指数：水平、垂直、旋转对称度
  - 宽高比：符号整体形态
  
- **第二层：核心拓扑不变量**（权重35%）
  - 欧拉示性数 χ = 连通分量数 - 环数
  - 贝蒂数序列：描述连通分支、独立环、空腔数
  
- **第三层：局部结构指纹**（权重25%）
  - 环数分布：不同大小、位置的封闭区域
  - 连通分量数：独立连通区域数量
  - 像素密度：符号繁简程度

### 2. 语义类型识别
根据拓扑特征自动识别符号语义类型：
- **天体类**（日、月、星）：对称性最强指标
- **自然类**（山、水、火）：宽高比最强指标
- **人体类**（人、目、口）：对称性+环数共同指标
- **器物类**（田、皿、弓）：环数最强指标

### 3. 跨文明同源性分析
- 计算两个符号的拓扑相似度
- 判定同源性等级（高/中/低）
- 语义类型自适应权重调整

### 4. 文化传播检测
基于重要发现：环数是最强的文化传播指示器
- 环数相同 + 拓扑相似 → 强文化传播信号
- 环数不同 + 拓扑相似 → 独立起源认知趋同
- 其他情况 → 无法判断

### 5. 火山引擎知识库
提供企业级专业知识查询，支持图文混合查询和多轮对话。

## 工作流程

1. **接收输入**：分析用户提供的古文字图片或文本
2. **特征提取**：使用拓扑分析工具提取三层特征
3. **语义识别**：根据特征判断符号的语义类型
4. **知识查询**：必要时查询知识库获取背景信息
5. **同源性分析**：如需比较，分析跨文明同源性
6. **文化传播检测**：判断是否存在文化传播信号
7. **综合解读**：给出专业、完整的分析报告

## 重要原则

- 拓扑特征分析是核心，要充分利用三层特征体系
- 语义类型决定权重配置，要先识别再分析
- 环数的价值在于区分独立起源与文化传播
- 结合知识库信息，提供全面的专业分析
- 保持学术严谨性，不确定性要如实说明

## 可用工具

### 知识库工具
- `search_volcengine_knowledge`: 基础查询
- `search_volcengine_knowledge_with_context`: 带上下文查询
- `multi_round_knowledge_chat`: 多轮对话

### 拓扑分析工具
- `extract_topology_features`: 提取拓扑特征
- `analyze_cross_civilization_homology`: 同源性分析
- `detect_cultural_transmission`: 文化传播检测
- `analyze_semantic_type_from_features`: 语义类型识别

## 输出要求

提供结构化、专业化的分析报告，包括：
1. 基本信息（符号描述、来源）
2. 拓扑特征分析（三层特征详情）
3. 语义类型判定及置信度
4. 同源性分析结果（如适用）
5. 文化传播信号（如适用）
6. 专业知识补充
7. 综合结论与建议
"""
    
    # 创建Agent，集成错误处理中间件
    agent = create_agent(
        model=llm,
        system_prompt=enhanced_system_prompt,
        tools=all_tools,
        middleware=[handle_topology_tool_errors],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
    
    return agent


# ============================================================================
# 便捷函数
# ============================================================================

def create_topology_analysis_agent(ctx=None) -> Any:
    """创建仅包含拓扑分析功能的简化Agent"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    topology_tools = get_topology_tools()
    
    return create_agent(
        model=llm,
        system_prompt="""你是拓扑特征分析专家，专注于古文字符号的拓扑特征提取和分析。
        
使用提供的拓扑分析工具，可以：
1. 提取符号的三层拓扑特征（全局形态、核心不变量、局部指纹）
2. 分析符号的语义类型
3. 比较两个符号的同源性
4. 检测文化传播信号

请准确、专业地执行分析任务。""",
        tools=topology_tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )


def create_knowledge_agent(ctx=None) -> Any:
    """创建仅包含知识库功能的简化Agent"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    knowledge_tools = [
        search_volcengine_knowledge,
        search_volcengine_knowledge_with_context,
        multi_round_knowledge_chat
    ]
    
    return create_agent(
        model=llm,
        system_prompt="""你是古文字知识专家，通过火山引擎知识库提供专业知识支持。
        
你可以：
1. 查询古文字的基础知识（甲骨文、楔形文字、埃及象形文字等）
2. 提供符号的历史背景和文化语境
3. 解释古文字的演变规律
4. 推荐研究工具和资源

请使用知识库工具获取准确的信息。""",
        tools=knowledge_tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("构建增强版古文字破译智能体...")
    
    # 构建主Agent
    agent = build_enhanced_agent()
    print("✓ 增强版Agent构建成功")
    
    # 构建专用Agent
    topology_agent = create_topology_analysis_agent()
    print("✓ 拓扑分析Agent构建成功")
    
    knowledge_agent = create_knowledge_agent()
    print("✓ 知识库Agent构建成功")
    
    print("\n所有Agent构建完成！")
