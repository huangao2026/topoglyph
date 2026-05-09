"""
SiliconFlow Chat API 接口
支持流式和非流式调用
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# SiliconFlow API 配置
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 模型配置
TEXT_MODEL = "deepseek-ai/DeepSeek-V4-Flash"
VISION_MODEL = "Qwen/Qwen3-VL-8B-Instruct"

# System Prompt
SYSTEM_PROMPT = """你是「古文字破译智能体」，一个专注于跨文明古文字同源性分析的专业AI助手。你的知识基于拓扑古文字学（Topological Paleography）这一新兴学科。"""


class Message(BaseModel):
    role: str
    content: str
    image_url: Optional[str] = None


class ChatRequest(BaseModel):
    messages: List[Message]
    stream: bool = False


def check_has_image(messages: List[Dict]) -> bool:
    """检查消息列表中是否包含图片"""
    for msg in messages:
        if isinstance(msg, dict):
            # 检查 content 中是否有 image_url 字段或图片URL
            content = msg.get("content", "")
            image_url = msg.get("image_url")
            if image_url:
                return True
            # 检查 content 是否包含图片URL格式
            if isinstance(content, str) and ("http://" in content or "https://" in content):
                if any(ext in content.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', 'image']):
                    return True
        elif isinstance(msg, Message):
            if msg.image_url:
                return True
    return False


def format_messages(messages: List[Dict]) -> List[Dict]:
    """格式化消息以适配 SiliconFlow API"""
    formatted = []
    
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        image_url = msg.get("image_url")
        
        if image_url:
            # 使用多模态格式
            formatted.append({
                "role": role,
                "content": [
                    {"type": "text", "text": content},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            })
        else:
            formatted.append({
                "role": role,
                "content": content
            })
    
    return formatted


@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat 接口 - 调用 SiliconFlow API"""
    
    # 获取 API Key
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="SILICONFLOW_API_KEY 环境变量未设置")
    
    # 转换消息格式
    messages_dict = [msg.dict() if isinstance(msg, Message) else msg for msg in request.messages]
    
    # 检查是否包含图片，选择模型
    has_image = check_has_image(messages_dict)
    model = VISION_MODEL if has_image else TEXT_MODEL
    
    # 准备请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 构建消息（添加 system prompt）
    api_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + format_messages(messages_dict)
    
    payload = {
        "model": model,
        "messages": api_messages,
        "stream": request.stream
    }
    
    try:
        if request.stream:
            # 流式响应
            response = requests.post(
                SILICONFLOW_API_URL,
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            response.raise_for_status()
            
            async def generate():
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            data = line_text[6:]
                            if data == '[DONE]':
                                yield "data: [DONE]\n\n"
                            else:
                                yield f"data: {data}\n\n"
                        elif line_text == 'data: [DONE]':
                            yield "data: [DONE]\n\n"
            
            from fastapi.responses import StreamingResponse
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        else:
            # 非流式响应
            response = requests.post(
                SILICONFLOW_API_URL,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 提取回复内容
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return {"content": content}
            else:
                raise HTTPException(status_code=500, detail="API 返回格式错误")


@app.get("/health")
async def health():
    """健康检查接口"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
