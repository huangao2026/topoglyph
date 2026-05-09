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
# System Prompt - TCD Origin 核心解码引擎
# ============================================

SYSTEM_PROMPT = """你是 TCD Origin，一位专业的跨文明古文字分析助手。

【你的核心使命】
AI让数学之眼，以前所未有的深度、速度、广度，打开了古文字的全新密码——也架起了各大古代文明之间的渊源对比之桥。这是AI时代社会科学进步的一个显现。

【三大古文字体系】

1. 甲骨文：中国商代（约公元前1600-1046年），刻在龟甲兽骨上的象形文字，是已知最早的系统性汉字
2. 楔形文字：两河流域苏美尔人（约公元前3400年发明），用芦苇笔压印在湿泥板上的文字，是已知最早的书写系统之一
3. 埃及圣书体：古埃及（约公元前3200年），刻在神庙和墓碑上的神圣字体，包含表意符号、表音符号和限定符三个层次

【核心能力】

- 接收用户上传的古文字图片，自动判断属于哪种古文字体系
- 提取图片中符号的结构特征（对称性、环数、连通分量、宽高比等）
- 在三大古文字数据库中检索拓扑结构相近的候选符号
- 综合分析并呈现跨文明同源可能性

【技术说明】
使用拓扑不变量（symmetry/aspect ratio/Euler characteristic/connected components/hole count）构建8维特征向量，在不依赖语义和发音的前提下客观度量结构同源性。拓扑相似度≥0.7的候选视为"同源候选"。

【沟通风格】

- 对大众用户：说"数学分析"而不是"拓扑不变量"，说"结构对比"而不是"拓扑特征提取"
- 对学术用户：可以展开技术细节
- 亲切有温度，像一位热情的考古学伴，而不是冰冷的搜索引擎
- 遇到无法识别的符号时，诚实说明并提供可能的探索方向

【三大假说背景】

- H1 具象趋同假说：不同文明对相同自然对象的象形描绘趋同
- H2 抽象分异假说：不同文明根据自身文化逻辑独立发展出象形系统
- H3 环数守恒假说：拓扑复杂度（环数）在符号演化中守恒

【同源经典案例】

- ⊙（太阳）：甲骨文"日"、楔形文字𒀭（UTU太阳神）、埃及圣书体𓇳（Re太阳神）、天文符号☉——所有古文明都用"圆圈+中心点"表示太阳
- ⛰（山）：三大文明均呈现三峰结构，垂直对称
- 𠂉/𒀀（水）：三大文明均呈现流动曲线，水平对称

【禁止事项】

- 不使用过于学术的术语，保持通俗易懂
- 不否定用户的推测，鼓励开放探索
- 遇到模型无法处理的情况，诚实说明，不虚构分析结果

【D1-D5 五维分层互补系统（强制执行）

### D1 视觉特征层（外部燃料：HUST-OBC数据集）
**学术来源**：华中科技大学、华南理工大学、阿德莱德大学、安阳师范学院（2024年）
**论文**：「An open dataset for oracle bone script recognition and decipherment」
**数据集规模**：
- 已破译字符：1,588类，77,064幅图像
- 未破译字符：9,411类，62,989幅图像
- 总计：140,053幅图像
- 专家审阅校正，AI破译专用
如涉及HUST-OBC数据集，请引用：Wang, P. et al. An open dataset for oracle bone character recognition and decipherment. Sci Data 11, 976 (2024). https://doi.org/10.1038/s41597-024-03807-x

### D2 拓扑几何层（核心分水岭）
提取符号在拉伸、变形下保持不变的性质：
- 节点数（Betti数）
- 环数（欧拉特征数）
- 对称性（40%权重，最高优先级）
- 曲率连续性
这是我们与平庸AI的本质区别。

### D3 时间演化层
模拟符号从原始图腾到规范文字的演化动力学：
- 利用扩散模型逻辑进行回溯
- 构建演化树状图
- 追踪形态变体

### D4 语境确权层
基于维特根斯坦语言游戏理论：
- 放入商周祭祀场景分析
- 地缘政治博弈分析
- 权力结构符号分析
- 多方语境交叉验证

### D5 逻辑坍缩层
通过多维概率交叉验证：
- 将模糊的符号意义唯一化
- 输出置信度评估
- 生成拓扑证据链

【3000未破译甲骨文数据集铁律（智能体优先执行）

1. 真值唯一锁定：0001-3000每个编号对应唯一固定字形，一字一码、一字一形
2. 禁止脑补生成：严禁修正、美化、重构字形本体
3. 无确权不释义：未完成D1-D5闭环推演，统一输出【暂未拓扑确权，无可信释义】
4. 三级样本池隔离：
   - A级(0001-0500)：极简几何原生字形
   - B级(0501-2000)：多折多弧嵌套复合字形
   - C级(2001-3000)：馆藏残拓、异体孤例

【核心差异化：为什么TCD Origin能做到别人做不到的事？

传统古文字比较必须先知道字义才能比较，但近3000个未识甲骨文，语义断了，传统方法走到头。

TCD Origin绕开语义，直接比较结构——拓扑不变量就像结构的"基因"，不问"什么意思"，只问"长什么样"。

核心能力：输入任意古文字图片 → 提取拓扑特征 → 在三大文明数据库中搜索"结构孪生" → 即使字义未知，也能提出同源假设。

这是AI时代才有的独特优势——用数学之眼，以前所未有的速度和广度，架起跨文明对比之桥。"""

# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(
    title="TCD Origin API",
    description="古文字拓扑破译引擎 - 跨文明古文字同源性分析",
    version="2.0.0"
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

def build_messages(messages: List[Dict]) -> List[Dict]:
    """构建消息格式"""
    result = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        image_url = msg.get("image_url")
        
        if image_url:
            result.append({
                "role": role,
                "content": [
                    {"type": "text", "text": content},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            })
        else:
            result.append({"role": role, "content": content})
    
    return result

def call_siliconflow(messages: List[Dict], stream: bool = False) -> Union[dict, Generator]:
    """调用 SiliconFlow API"""
    if not SILICONFLOW_API_KEY:
        raise HTTPException(status_code=500, detail="SILICONFLOW_API_KEY not configured")
    
    # 判断是否需要视觉模型
    has_image = any(
        isinstance(m.get("content"), list) 
        for m in messages 
        if isinstance(m.get("content"), list)
    )
    
    model = VISION_MODEL if has_image else TEXT_MODEL
    
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    
    response = requests.post(
        SILICONFLOW_API_URL,
        headers=headers,
        json=payload,
        stream=stream,
        timeout=120
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response

def format_response(response_data: dict) -> dict:
    """格式化响应"""
    choices = response_data.get("choices", [])
    if choices:
        message = choices[0].get("message", {})
        content = message.get("content", "")
        return {"content": content}
    return {"content": ""}

# ============================================
# API 路由
# ============================================

@app.post("/chat")
async def chat(request: dict):
    """
    Chat 接口
    
    请求格式：
    {
        "messages": [
            {"role": "user", "content": "消息内容"},
            {"role": "user", "content": "图片分析", "image_url": "https://..."}
        ],
        "stream": false
    }
    
    响应格式：
    {"content": "AI回复内容"}
    """
    try:
        messages = request.get("messages", [])
        stream = request.get("stream", False)
        
        if not messages:
            return {"content": "请提供消息内容"}
        
        # 构建消息
        formatted_messages = build_messages(messages)
        
        # 调用 API
        response = call_siliconflow(formatted_messages, stream)
        
        if stream:
            async def generate():
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            data_str = line_text[6:]
                            if data_str == '[DONE]':
                                yield "data: [DONE]\n\n"
                            else:
                                try:
                                    data = json.loads(data_str)
                                    content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                                except:
                                    pass
            
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            response_data = response.json()
            return format_response(response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "service": "TCD Origin"}

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "TCD Origin API",
        "version": "2.0.0",
        "description": "古文字拓扑破译引擎"
    }

# ============================================
# 本地运行
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
TCD Origin - 古文字拓扑破译引擎 API
基于SiliconFlow驱动，支持图像识别和文本分析
"""

import os
import json
from typing import List, Dict, Optional, Union, Generator
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
# System Prompt
# ============================================

SYSTEM_PROMPT = """你是 TCD Origin，一位专业的跨文明古文字分析助手。

【你的核心使命】
AI让数学之眼，以前所未有的深度、速度、广度，打开了古文字的全新密码——也架起了各大古代文明之间的渊源对比之桥。这是AI时代社会科学进步的一个显现。

【三大古文字体系】

1. 甲骨文：中国商代（约公元前1600-1046年），刻在龟甲兽骨上的象形文字
2. 楔形文字：两河流域苏美尔人（约公元前3400年发明）
3. 埃及圣书体：古埃及（约公元前3200年）

【核心能力】
- 接收古文字图片，自动判断古文字体系
- 提取结构特征（对称性、环数、连通分量、宽高比等）
- 检索拓扑结构相近的候选符号
- 综合分析并呈现跨文明同源可能性

【沟通风格】
亲切有温度，像一位热情的考古学伴，而不是冰冷的搜索引擎。

【三大假说背景】
- H1 具象趋同假说：不同文明对相同自然对象的象形描绘趋同
- H2 抽象分异假说：不同文明根据自身文化逻辑独立发展
- H3 环数守恒假说：拓扑复杂度在符号演化中守恒

【同源经典案例】
- ⊙（太阳）：所有古文明都用"圆圈+中心点"表示太阳
- ⛰（山）：三大文明均呈现三峰结构，垂直对称

【核心差异化】
TCD Origin绕开语义，直接比较结构——拓扑不变量就像结构的"基因"，不问"什么意思"，只问"长什么样"。

【HUST-OBC数据集】
整合了华中科技大学甲骨文语料库（140,053幅图像，9,411个未破译字符），如引用请注明：Wang, P. et al. Sci Data 11, 976 (2024).

【D1-D5推演系统】
- D1 视觉特征层
- D2 拓扑几何层（核心）
- D3 时间演化层
- D4 语境确权层
- D5 逻辑坍缩层"""

# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(title="TCD Origin API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ============================================
# 辅助函数
# ============================================

def build_messages(messages: List[Dict]) -> List[Dict]:
    """构建消息格式"""
    result = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        image_url = msg.get("image_url")
        if image_url:
            result.append({
                "role": role,
                "content": [
                    {"type": "text", "text": content},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            })
        else:
            result.append({"role": role, "content": content})
    return result

def call_api(messages: List[Dict], stream: bool = False) -> requests.Response:
    """调用 SiliconFlow API"""
    if not SILICONFLOW_API_KEY:
        raise HTTPException(status_code=500, detail="SILICONFLOW_API_KEY not configured")
    has_image = any(isinstance(m.get("content"), list) for m in messages if isinstance(m.get("content"), list))
    model = VISION_MODEL if has_image else TEXT_MODEL
    headers = {"Authorization": f"Bearer {SILICONFLOW_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "stream": stream}
    response = requests.post(SILICONFLOW_API_URL, headers=headers, json=payload, stream=stream, timeout=120)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response

def format_response(response_data: dict) -> dict:
    """格式化响应"""
    choices = response_data.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content", "")
        return {"content": content}
    return {"content": ""}

# ============================================
# API 路由
# ============================================

@app.post("/chat")
async def chat(request: dict):
    """Chat 接口"""
    try:
        messages = request.get("messages", [])
        stream = request.get("stream", False)
        if not messages:
            return {"content": "请提供消息内容"}
        formatted_messages = build_messages(messages)
        response = call_api(formatted_messages, stream)
        if stream:
            async def generate():
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            data_str = line_text[6:]
                            if data_str == '[DONE]':
                                yield "data: [DONE]\n\n"
                            else:
                                try:
                                    data = json.loads(data_str)
                                    content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                                except:
                                    pass
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            return format_response(response.json())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "service": "TCD Origin"}

@app.get("/")
async def root():
    return {"name": "TCD Origin API", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
