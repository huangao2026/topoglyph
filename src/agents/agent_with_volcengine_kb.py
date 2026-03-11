"""
如何在Agent中集成火山引擎知识库 - 完整示例
"""

import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入火山引擎知识库工具
from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat
)

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


# 定义工具函数（包装火山引擎知识库API）
@tool
def knowledge_search(query: str, runtime: ToolRuntime = None) -> str:
    """
    查询火山引擎知识库，获取古文字相关的专业知识
    
    Args:
        query: 查询问题，支持文本和图文混合查询
        
    Returns:
        知识库返回的答案
    """
    ctx = runtime.context if runtime else None
    try:
        result = search_volcengine_knowledge(query)
        return result
    except Exception as e:
        return f"知识库查询失败: {str(e)}"


@tool
def knowledge_search_with_context(query: str, context: str, runtime: ToolRuntime = None) -> str:
    """
    带上下文的火山引擎知识库查询
    
    Args:
        query: 当前查询问题
        context: 上下文信息（如用户背景、历史对话等）
        
    Returns:
        知识库返回的答案
    """
    ctx = runtime.context if runtime else None
    try:
        result = search_volcengine_knowledge_with_context(query, context)
        return result
    except Exception as e:
        return f"知识库查询失败: {str(e)}"


@tool
def knowledge_chat(conversation_history: str, runtime: ToolRuntime = None) -> str:
    """
    多轮对话查询火山引擎知识库
    
    Args:
        conversation_history: 对话历史，格式为JSON字符串，包含多轮对话
        
    Returns:
        知识库返回的答案
    """
    ctx = runtime.context if runtime else None
    try:
        messages = json.loads(conversation_history)
        result = multi_round_knowledge_chat(messages)
        return result
    except Exception as e:
        return f"知识库查询失败: {str(e)}"


def build_agent(ctx=None):
    """
    构建集成火山引擎知识库的古文字破译Agent
    """
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
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # 定义工具列表
    tools = [
        knowledge_search,
        knowledge_search_with_context,
        knowledge_chat
    ]

    # 构建Agent
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )


# 配置文件示例
"""
config/agent_llm_config.json 内容示例：
{
    "config": {
        "model": "doubao-pro-32k-241215",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 10000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "你是古文字破译专家助手，擅长识别、分析和解读各类古文字系统。你拥有专业的知识库，可以回答用户关于甲骨文、楔形文字、埃及象形文字等古文字的问题。当用户需要专业知识时，请使用知识库查询工具获取准确信息。",
    "tools": [
        "knowledge_search",
        "knowledge_search_with_context",
        "knowledge_chat"
    ]
}
"""


# 使用示例
"""
from agents.agent import build_agent
from langchain_core.messages import HumanMessage

# 创建Agent
agent = build_agent()

# 示例1: 简单查询
messages = [HumanMessage(content="什么是甲骨文？")]
response = agent.invoke({"messages": messages})
print(response["messages"][-1].content)

# 示例2: 图文查询
messages = [HumanMessage(content="请分析图片中的古文字: https://example.com/hieroglyphs.jpg")]
response = agent.invoke({"messages": messages})
print(response["messages"][-1].content)

# 示例3: 多轮对话
messages = [
    HumanMessage(content="什么是楔形文字？"),
    AIMessage(content="楔形文字是最古老的文字系统之一..."),
    HumanMessage(content="它的发展历史是怎样的？")
]
response = agent.invoke({"messages": messages})
print(response["messages"][-1].content)
"""


if __name__ == "__main__":
    # 测试Agent
    print("构建Agent...")
    agent = build_agent()
    print("Agent构建成功！")
    
    # 测试查询
    print("\n测试查询:")
    messages = [HumanMessage(content="什么是甲骨文？")]
    response = agent.invoke({"messages": messages})
    print(response["messages"][-1].content)
