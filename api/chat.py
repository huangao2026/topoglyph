# -*- coding: utf-8 -*-
"""
TCD Origin - 古文字拓扑破译引擎 API
基于SiliconFlow驱动，支持图像识别和文本分析
"""

import os
import json
import re
from typing import List, Dict, Optional, Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests

# ============================================
# 配置
# ============================================

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 模型配置
TEXT_MODEL = "deepseek-ai/DeepSeek-V4-Flash"
VISION_MODEL = "Qwen/Qwen3-VL-8B-Instruct"

# ============================================
# System Prompt - 古文字破译专家
# ============================================

SYSTEM_PROMPT = """你是「TCD Origin」——跨文明古文字拓扑破译引擎，基于拓扑古文字学（Topological Paleography）运作。

## 核心能力
- 识别甲骨文、金文、楔形文字、埃及圣书体等古文字
- D1-D5五层拓扑分析（同源性→结构→形态→语义→历史）
- 三层拓扑不变量：对称性（40%权重）、贝蒂数（35%）、欧拉示性数（25%）

## 3000未破译甲骨文数据集铁律

### 最高优先级强制规则
1. **真值唯一锁定**：0001-3000每个编号对应唯一固定字形，一字一码、一字一形
2. **禁止脑补生成**：严禁修正、美化、重构字形本体
3. **无确权不释义**：未完成D1-D5闭环推演，统一输出【暂未拓扑确权，无可信释义】
4. **三级样本池隔离**：
   - A级(0001-0500)：极简几何原生字形
   - B级(0501-2000)：多折多弧嵌套复合字形
   - C级(2001-3000)：馆藏残拓、异体孤例

### 已知A级样本(0001-0100)
0001:〇 0002:·· 0003:⌒ 0004:✚ 0005:△ 0006:∥ 0007:◎ 0008:⊷ 0009:✧ 0010:〥
0011:⑧ 0012:⋯ 0013:┐ 0014:┃ 0015:⌒⌒ 0016:┅┅ 0017:⊿ 0018:═ 0019:✦ 0020:〘〙
0021:┃┃┃ 0022:⌒━⌒ 0023:✚✚ 0024:⏢ 0025:┏┓┗┛ 0026:┃△ 0027:◎◎ 0028:△/ 0029:˙┃˙ 0030:∿
0031:□ 0032:⏠ 0033:┃┃┃ 0034:⌒┃ 0035:／／ 0036:△┃ 0037:⌒⌒⌒ 0038:┃⏚ 0039:━ ━ 0040:˙⌒
0041:∨ 0042:┃ ┃ 0043:┗┃┛ 0044:└┐ 0045:˙◎ 0046:⌒━ 0047:═ ═ 0048:⊿／ 0049:┣━┫ 0050:⌒┐
0051:┃┃⏗ 0052:⌒⌒━ 0053:━ ━ ━ 0054:┓⌒┗ 0055:□˙ 0056:△━ 0057:┏┃┓ 0058:⌒˙ 0059:✚／ 0060:∿━
0061:◎━◎ 0062:┃└ 0063:△˙△ 0064:□┃ 0065:˙━˙ 0066:⏓ 0067:┣┃┫ 0068:／／━ 0069:⌒˙⌒ 0070:⏚⏗
0071:┃┓┃ 0072:━⌒━ 0073:┃┃┃⏘ 0074:┏⌒┛ 0075:┃┠┨┃ 0076:┳∨ 0077:⌒⌒⌒⌒ 0078:┏┓┗┛ 0079:═ ━ ═ 0080:┃∨┃
0081:⌒┃┃ 0082:━∨━ 0083:✚˙ 0084:⌒┃ 0085:┏┃┃┓ 0086:／△ 0087:⌒⌒ 0088:━━━┃━ 0089:┃⏏┃ 0090:┗⌒┛
0091:□┃˙ 0092:／／／ 0093:⏐⏑⏐ 0094:˙━˙ 0095:⌒━⌒ 0096:┃ ┃⏗ 0097:△━△ 0098:━┃┃━ 0099:⌒／ 0100:┃◎

## 标准输出模板
【当日破译编号】SX-YB-xxxx
【固定真值甲骨字形】对应标准本体字形
【拓扑层级分类】A级/B级/C级
【D1-D5全流程推演状态】已闭环/未闭环
【最终置信度】XX%
【确权结论】已拓扑确权/暂未确权
【学术结论】有合规可信释义/无可信释义
【溯源依据】完整拓扑特征+馆藏拓片属性

## 回答风格
- 严谨专业，引用拓扑古文字学理论
- 字形分析结合D1-D5层级推演
- 保持学术中立，未确权字形直接说明
"""

# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(
    title="TCD Origin - 古文字拓扑破译引擎",
    description="跨文明古文字同源性分析专业AI助手",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 辅助函数
# ============================================

def check_has_image(messages: List[Dict]) -> bool:
    """检查消息列表是否包含图片"""
    for msg in messages:
        if isinstance(msg, dict):
            content = msg.get("content", "")
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "image_url":
                        return True
            elif isinstance(content, str) and "image_url" in content.lower():
                return True
    return False

def convert_messages(messages: List[Dict]) -> List[Dict]:
    """转换消息格式，支持文本和图片"""
    converted = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        # 处理图片
        if isinstance(content, list):
            converted.append({"role": role, "content": content})
        elif isinstance(content, str):
            # 检查是否包含图片URL
            if "image_url" in content.lower() or "http" in content.lower():
                # 尝试解析图片URL
                if msg.get("image_url"):
                    converted.append({
                        "role": role,
                        "content": [
                            {"type": "text", "text": content},
                            {"type": "image_url", "image_url": {"url": msg.get("image_url")}}
                        ]
                    })
                else:
                    converted.append({"role": role, "content": content})
            else:
                converted.append({"role": role, "content": content})
        else:
            converted.append({"role": role, "content": str(content)})
    
    return converted

def build_payload(messages: List[Dict], model: str, stream: bool = False) -> Dict:
    """构建API请求payload"""
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *convert_messages(messages)
        ],
        "stream": stream,
        "temperature": 0.7,
        "max_tokens": 2000
    }

def call_siliconflow(payload: Dict) -> Dict:
    """调用SiliconFlow API"""
    if not SILICONFLOW_API_KEY:
        raise HTTPException(status_code=500, detail="SILICONFLOW_API_KEY未设置")
    
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        SILICONFLOW_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"API调用失败: {response.text}"
        )
    
    return response.json()

# ============================================
# API 路由
# ============================================

@app.post("/chat")
async def chat(request: Dict):
    """
    聊天接口
    
    请求体:
    {
        "messages": [{"role": "user", "content": "消息内容"}],
        "stream": false  // 可选，是否流式输出
    }
    
    返回:
    {
        "content": "AI回复内容"
    }
    """
    messages = request.get("messages", [])
    stream = request.get("stream", False)
    
    if not messages:
        return {"content": "请提供消息内容"}
    
    # 根据消息类型选择模型
    has_image = check_has_image(messages)
    model = VISION_MODEL if has_image else TEXT_MODEL
    
    if stream:
        return StreamingResponse(
            stream_chat(messages, model),
            media_type="text/event-stream"
        )
    
    payload = build_payload(messages, model, stream=False)
    result = call_siliconflow(payload)
    
    # 提取回复
    choices = result.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content", "")
        return {"content": content}
    
    return {"content": "未能生成回复"}

async def stream_chat(messages: List[Dict], model: str):
    """流式响应生成器"""
    has_image = check_has_image(messages)
    actual_model = VISION_MODEL if has_image else model
    
    payload = build_payload(messages, actual_model, stream=True)
    
    if not SILICONFLOW_API_KEY:
        yield "data: {\"error\": \"SILICONFLOW_API_KEY未设置\"}\n\n"
        return
    
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            SILICONFLOW_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )
        
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data: '):
                    yield decoded + '\n'
                elif decoded == 'data: [DONE]':
                    yield 'data: [DONE]\n\n'
    except Exception as e:
        yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

@app.get("/")
async def root():
    """健康检查"""
    return {
        "name": "TCD Origin - 古文字拓扑破译引擎",
        "version": "1.0.0",
        "status": "running",
        "models": {
            "text": TEXT_MODEL,
            "vision": VISION_MODEL
        }
    }

@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "ok"}

# ============================================
# 启动命令
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
