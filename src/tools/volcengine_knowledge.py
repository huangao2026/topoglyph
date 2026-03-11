"""
火山引擎知识库工具
用于调用火山引擎知识库服务API
"""

import json
import os
import requests
from typing import Optional, Dict, Any, List
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context


class VolcengineKnowledgeConfig:
    """火山引擎知识库配置"""
    
    # 从环境变量读取配置
    ACCOUNT_ID = os.getenv("VOLCENGINE_ACCOUNT_ID", "")
    API_KEY = os.getenv("VOLCENGINE_API_KEY", "")
    DOMAIN = os.getenv("VOLCENGINE_KB_DOMAIN", "api-knowledgebase.mlp.cn-beijing.volces.com")
    SERVICE_RESOURCE_ID = os.getenv("VOLCENGINE_SERVICE_ID", "kb-service-14ae584a2d80c3f9")
    
    @classmethod
    def is_configured(cls) -> bool:
        """检查是否已配置"""
        return bool(cls.API_KEY and cls.SERVICE_RESOURCE_ID)


def prepare_request(method: str, path: str, params: Optional[Dict] = None,
                   data: Optional[Dict] = None, doseq: bool = 0) -> Dict[str, Any]:
    """
    准备HTTP请求
    
    Args:
        method: HTTP方法（GET, POST等）
        path: API路径
        params: 查询参数
        data: 请求体数据
        doseq: 是否序列化列表
    
    Returns:
        请求字典
    """
    if params:
        for key in params:
            if isinstance(params[key], (int, float, bool)):
                params[key] = str(params[key])
            elif isinstance(params[key], list) and not doseq:
                params[key] = ",".join(params[key])
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": VolcengineKnowledgeConfig.DOMAIN,
        "Authorization": f'Bearer {VolcengineKnowledgeConfig.API_KEY}'
    }
    
    return {
        "method": method,
        "url": f"http://{VolcengineKnowledgeConfig.DOMAIN}{path}",
        "headers": headers,
        "params": params,
        "body": json.dumps(data) if data else None
    }


@tool
def search_volcengine_knowledge(
    query: str,
    image_url: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    搜索火山引擎知识库
    
    该工具用于查询火山引擎知识库中的古文字相关信息。
    支持纯文本查询和图文混合查询。
    
    Args:
        query: 查询文本，例如"埃及象形文字荷鲁斯的含义"、"甲骨文的起源"等
        image_url: 图片URL（可选），用于图文混合查询，例如上传的古文字图片链接
        runtime: 工具运行时上下文
    
    Returns:
        知识库搜索结果，包含相关知识和详细解释
    
    Examples:
        >>> # 纯文本查询
        >>> result = search_volcengine_knowledge("埃及象形文字荷鲁斯的含义")
        >>> 
        >>> # 图文查询
        >>> result = search_volcengine_knowledge(
        ...     "这是什么古文字？",
        ...     image_url="https://example.com/egyptian_text.jpg"
        ... )
    """
    # 检查配置
    if not VolcengineKnowledgeConfig.is_configured():
        return "火山引擎知识库未配置，请设置环境变量：VOLCENGINE_API_KEY 和 VOLCENGINE_SERVICE_ID"
    
    try:
        # 准备查询内容
        if image_url:
            content = [
                {"text": query, "type": "text"},
                {"image_url": {"url": image_url}, "type": "image_url"}
            ]
        else:
            content = query
        
        # 准备请求数据
        request_data = {
            "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
            "messages": [
                {"role": "user", "content": content}
            ],
            "stream": False
        }
        
        # 发送请求
        req = prepare_request(
            method="POST",
            path="/api/knowledge/service/chat",
            data=request_data
        )
        
        response = requests.post(
            url=req["url"],
            headers=req["headers"],
            data=req["body"],
            timeout=30
        )
        
        response.encoding = "utf-8"
        result = response.json()
        
        # 解析结果
        if "answer" in result:
            return f"知识库回答:\n{result['answer']}"
        elif "message" in result:
            return f"知识库消息:\n{result['message']}"
        elif "data" in result:
            return f"知识库数据:\n{json.dumps(result['data'], ensure_ascii=False, indent=2)}"
        else:
            return f"知识库响应:\n{json.dumps(result, ensure_ascii=False, indent=2)}"
            
    except requests.exceptions.Timeout:
        return "知识库查询超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        return "无法连接到知识库服务，请检查网络连接"
    except Exception as e:
        return f"搜索知识库时出错: {str(e)}"


@tool
def search_volcengine_knowledge_with_context(
    query: str,
    context: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    带上下文的知识库搜索
    
    该工具用于在特定上下文环境中查询知识库。
    适用于需要结合上下文的场景，例如：
    - 用户提供了之前的对话历史
    - 需要在特定主题下查询
    - 需要结合之前的分析结果
    
    Args:
        query: 查询文本，例如"这个符号代表什么？"
        context: 上下文信息，例如"用户正在研究古埃及象形文字，特别是关于神祇的符号"
        runtime: 工具运行时上下文
    
    Returns:
        知识库搜索结果，结合上下文信息
    
    Examples:
        >>> # 带上下文查询
        >>> result = search_volcengine_knowledge_with_context(
        ...     query="这个符号代表什么？",
        ...     context="用户正在研究古埃及象形文字，特别是关于神祇的符号"
        ... )
    """
    # 检查配置
    if not VolcengineKnowledgeConfig.is_configured():
        return "火山引擎知识库未配置，请设置环境变量：VOLCENGINE_API_KEY 和 VOLCENGINE_SERVICE_ID"
    
    try:
        # 准备查询内容
        if context:
            full_query = f"上下文信息:\n{context}\n\n问题:\n{query}"
        else:
            full_query = query
        
        # 准备请求数据
        request_data = {
            "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
            "messages": [
                {"role": "user", "content": full_query}
            ],
            "stream": False
        }
        
        # 发送请求
        req = prepare_request(
            method="POST",
            path="/api/knowledge/service/chat",
            data=request_data
        )
        
        response = requests.post(
            url=req["url"],
            headers=req["headers"],
            data=req["body"],
            timeout=30
        )
        
        response.encoding = "utf-8"
        result = response.json()
        
        # 解析结果
        if "answer" in result:
            return f"知识库回答:\n{result['answer']}"
        elif "message" in result:
            return f"知识库消息:\n{result['message']}"
        elif "data" in result:
            return f"知识库数据:\n{json.dumps(result['data'], ensure_ascii=False, indent=2)}"
        else:
            return f"知识库响应:\n{json.dumps(result, ensure_ascii=False, indent=2)}"
            
    except requests.exceptions.Timeout:
        return "知识库查询超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        return "无法连接到知识库服务，请检查网络连接"
    except Exception as e:
        return f"搜索知识库时出错: {str(e)}"


@tool
def multi_round_knowledge_chat(
    messages: List[Dict[str, str]],
    runtime: ToolRuntime = None
) -> str:
    """
    多轮知识库对话
    
    该工具支持多轮对话，可以保持对话上下文。
    适用于需要连续提问的场景，例如：
    - 用户连续提问相关问题
    - 需要追问和澄清
    - 需要基于前一个回答继续提问
    
    Args:
        messages: 对话消息列表，格式如下：
            [
                {"role": "user", "content": "第一个问题"},
                {"role": "assistant", "content": "第一个回答"},
                {"role": "user", "content": "追问问题"}
            ]
        runtime: 工具运行时上下文
    
    Returns:
        知识库回答
    
    Examples:
        >>> # 多轮对话
        >>> messages = [
        ...     {"role": "user", "content": "什么是甲骨文？"},
        ...     {"role": "assistant", "content": "甲骨文是中国商代的文字..."},
        ...     {"role": "user", "content": "它有什么特点？"}
        ... ]
        >>> result = multi_round_knowledge_chat(messages)
    """
    # 检查配置
    if not VolcengineKnowledgeConfig.is_configured():
        return "火山引擎知识库未配置，请设置环境变量：VOLCENGINE_API_KEY 和 VOLCENGINE_SERVICE_ID"
    
    try:
        # 准备请求数据
        request_data = {
            "service_resource_id": VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID,
            "messages": messages,
            "stream": False
        }
        
        # 发送请求
        req = prepare_request(
            method="POST",
            path="/api/knowledge/service/chat",
            data=request_data
        )
        
        response = requests.post(
            url=req["url"],
            headers=req["headers"],
            data=req["body"],
            timeout=30
        )
        
        response.encoding = "utf-8"
        result = response.json()
        
        # 解析结果
        if "answer" in result:
            return f"知识库回答:\n{result['answer']}"
        elif "message" in result:
            return f"知识库消息:\n{result['message']}"
        elif "data" in result:
            return f"知识库数据:\n{json.dumps(result['data'], ensure_ascii=False, indent=2)}"
        else:
            return f"知识库响应:\n{json.dumps(result, ensure_ascii=False, indent=2)}"
            
    except requests.exceptions.Timeout:
        return "知识库查询超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        return "无法连接到知识库服务，请检查网络连接"
    except Exception as e:
        return f"多轮对话时出错: {str(e)}"


# 测试函数
if __name__ == "__main__":
    print("火山引擎知识库工具测试")
    print("=" * 50)
    
    # 检查配置
    print(f"API Key已配置: {VolcengineKnowledgeConfig.is_configured()}")
    print(f"Domain: {VolcengineKnowledgeConfig.DOMAIN}")
    print(f"Service ID: {VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID}")
    print()
    
    # 测试查询（如果已配置）
    if VolcengineKnowledgeConfig.is_configured():
        print("测试查询: 什么是甲骨文？")
        result = search_volcengine_knowledge("什么是甲骨文？")
        print(f"结果: {result}")
    else:
        print("⚠️  未配置火山引擎知识库，请设置环境变量")
        print("需要设置的变量:")
        print("  - VOLCENGINE_API_KEY")
        print("  - VOLCENGINE_SERVICE_ID")
