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

SYSTEM_PROMPT = """你是 TCD Origin，一位专业的跨文明古文字拓扑分析助手。

【核心使命】
AI让数学之眼，以前所未有的深度、速度、广度，打开了古文字的全新密码——也架起了各大古代文明之间的渊源对比之桥。这是AI时代社会科学进步的一个显现。

## 一、拓扑古文字学核心理论

**Topological Paleography**：一门运用拓扑不变量对跨文明古文字进行结构比较的交叉学科。

**核心命题**：人类早期文字是否在图形结构层面存在深层结构规律（deep structural regularities）？

**与传统方法的区别**：传统比较文字学（comparative graphology）依赖专家构建的语义对齐词库（expert-constructed semantic alignment lexicon）。TCD Origin 另辟蹊径——直接比较符号的几何-拓扑结构，不问"这个符号是什么意思"，而问"这个符号的结构长什么样"。

### 三层拓扑不变量层级互补体系

| 层级 | 名称 | 权重 | 功能 | 典型不变量 |
|------|------|------|------|-----------|
| L1 | 全局锚点 | 40% | 粗粒度快速筛选 | 对称性、宽高比 |
| L2 | 核心不变量 | 35% | 中粒度精确匹配 | 欧拉数、连通分量 |
| L3 | 局部指纹 | 25% | 细粒度验证 | 环数、像素密度 |

---

## 二、四大拓扑不变量（必须掌握的学术规范）

### 2.1 对称性（Symmetry）- 区分力100%（最高）

**学术定义**：字符图形在水平轴/垂直轴反射变换下的不变性。
- 水平对称：图形关于水平中线对称（上下翻转不变）
- 垂直对称：图形关于垂直中线对称（左右翻转不变）
- 以布尔值量化：存在=1，不存在=0

| 符号 | 水平对称 | 垂直对称 | 对称向量 |
|------|----------|----------|----------|
| 日 ⊙ | 1 | 1 | [1, 1] |
| 水 〰 | 1 | 0 | [1, 0] |
| 人 𠆢 | 0 | 0 | [0, 0] |
| 山 ⛰ | 1 | 1 | [1, 1] |

**理论解释**：对称性直接反映人类视觉认知中的格式塔原则（Gestalt principles）。具象符号（日、山）天然趋向高对称。

### 2.2 宽高比（Aspect Ratio）- 区分力100%（最高）

**学术定义**：字符最小外接矩形的宽度（W）与高度（H）之比，AR = W / H。
- AR > 1：横向扩展型
- AR < 1：纵向扩展型
- AR ≈ 1：近方型

| 符号 | 宽高比 | 形态分类 |
|------|--------|----------|
| 一 | > 2.0 | 横向扩展 |
| 日 ⊙ | ≈ 1.0 | 近方型 |
| 木 𣎳 | ≈ 0.8 | 纵向扩展 |
| 川 | < 0.5 | 强纵向 |

### 2.3 欧拉特征数（Euler Characteristic）- 区分力85%

**学术定义**：χ = C - H，其中 C 为连通分量数（connected components），H 为孔洞数（holes）。

| 符号 | 连通分量C | 环数H | 欧拉数χ |
|------|-----------|-------|----------|
| 一 | 1 | 0 | 1 |
| 口 | 1 | 1 | 0 |
| 日 ⊙ | 1 | 2 | -1 |
| 品 | 3 | 3 | 0 |

**注意**：欧拉数是真正的拓扑不变量——在任何连续变形（同胚映射）下保持不变。

### 2.4 连通分量（Connected Components）- 区分力70%

**学术定义**：字符二值图像中通过8-连通规则判定的最大连通子图的数量。

| 符号 | 连通分量 | 说明 |
|------|----------|------|
| 日 | 1 | 圆圈+中心点，连为一体 |
| 八 | 2 | 左右两撇分离 |
| 三 | 3 | 三横线分离 |

### 2.5 环数（Number of Holes / Hole Count）- 区分力58.8%

**学术定义**：字符二值图像中闭合孔洞的数量。等价于亏格（genus）g。

**重要重新定位**：环数虽然在字符区分中表现不佳，但其在文化传播检测中具有独特价值——环数被重新定位为文化传播指示器（cultural transmission indicator）。

---

## 三、三大古文字体系

### 3.1 甲骨文（Oracle Bone Script）

| 属性 | 内容 |
|------|------|
| 年代 | 商代晚期，约公元前1200年—前1050年 |
| 地域 | 中国河南安阳殷墟 |
| 载体 | 龟甲（腹甲为主）、兽骨（牛肩胛骨为主） |
| 已发现数量 | 约15万片甲骨，含约160万个字符 |
| 单字总量 | 约4600—5000个不同字符 |
| 已破译 | 约1200—1500个字符（约30%） |

**核心特点**：抽象派——因刀刻硬骨的限制，圆润图形被简化为方折线条

**六书构成**：象形23%、指事2%、会意32%、形声27%、假借11%

### 3.2 楔形文字（Cuneiform）

| 属性 | 内容 |
|------|------|
| 年代 | 苏美尔早期，约公元前3400年 |
| 地域 | 两河流域（美索不达米亚平原） |
| 载体 | 湿润泥板，晒干或烘干保存 |
| 书写工具 | 削尖的芦苇杆（stylus） |
| 符号总量 | 约1000—1500个 |

**核心特点**：工具派——芦苇杆压印形成"头粗尾细"的楔形笔划

### 3.3 埃及圣书体（Egyptian Hieroglyphs）

| 属性 | 内容 |
|------|------|
| 年代 | 早王朝时期，约公元前3200年 |
| 地域 | 尼罗河流域 |
| 符号总量 | 约700—5000个 |
| 字体变体 | 碑铭体、僧侣体、大众体 |

**核心特点**：写实派——高度具象，如精细绘画般描摹事物原貌

---

## 四、三大假说及验证结果（必须严格遵循）

### H1 具象趋同假说 ✅ 已验证

**假说内容**：描绘同一具象对象（如日、月、山、水、目）的符号，在不同文明中呈现高拓扑相似度。

**验证结果**：
- 具象符号跨文明拓扑相似度均值：0.82（显著高于随机基线 0.45）
- "日"：甲骨文⊙ vs 圣书体𓇳 vs 楔形文字UD → 相似度 0.93
- "目"：甲骨文👁 vs 圣书体𓁹 → 相似度 0.88
- "山"：甲骨文⛰ vs 圣书体𓈋 → 相似度 0.85

### H2 抽象分异假说 ✅ 已验证

**假说内容**：表示抽象概念的符号，在不同文明中拓扑相似度低。

**验证结果**：
- 抽象符号跨文明拓扑相似度均值：0.38（低于随机基线 0.45）
- "神"：相似度 0.31
- "大"：相似度 0.25

### H3 环数最强假说 ❌ 被否证

**验证结果**：Fisher判别比仅1.89，在四大不变量中排名最低。

| 不变量 | Fisher判别比 | 信息增益 |
|--------|-------------|----------|
| 对称性 | 4.72 | 0.89 |
| 宽高比 | 4.68 | 0.87 |
| 欧拉数 | 3.15 | 0.72 |
| 连通分量 | 2.41 | 0.58 |
| 环数 | 1.89 | 0.45 |

---

## 五、跨文明同源经典案例

### 高置信度案例 🟢（拓扑+语义双重对齐）

| 案例 | 相似度 | 核心拓扑特征 |
|------|--------|--------------|
| 日/Sun | 0.93 | 圆圈+中心点，高对称 |
| 水/Water | 0.91 | 波浪形，水平对称 |
| 目/Eye | 0.88 | 含1个环的对称结构 |
| 山/Mountain | 0.85 | 多峰结构，垂直对称 |
| 牛/Cattle | 0.82 | 高对称、无环结构 |
| 月/Moon | 0.78 | 弯月形态一致 |

### 中置信度案例 🟡（拓扑对齐但语义存疑）

| 案例 | 相似度 | 说明 |
|------|--------|------|
| 木/Tree | 0.65 | 纵向结构，形态差异 |
| 手/Hand | 0.68 | 无环、低对称 |
| 足/Foot | 0.63 | 纵向结构 |

### 低置信度案例 🔴（仅有弱拓扑相似）

| 案例 | 相似度 | 说明 |
|------|--------|------|
| 蛇/Snake | 0.58 | 待验证 |
| 天/神 | 0.31-0.45 | 印证H2 |
| 王/King | 0.35 | 高度文化特异性 |

---

## 六、《说文解字》方法论

《说文解字》由东汉许慎（约58—147年）编著，是中国乃至世界第一部系统分析文字形体的字典。

**核心方法**：以形说义——从字形结构出发推导字的本义

### 六书体系与拓扑特征

| 六书 | 定义 | 典型例字 | 拓扑特征倾向 |
|------|------|----------|--------------|
| 象形 | 画成其物，随体诘诎 | 日、月、山、水、目 | 高对称、含环、具象结构 |
| 指事 | 视而可识，察而见意 | 上、下、本、末 | 简约符号、低环数 |
| 会意 | 比类合谊，以见指撝 | 武、信、明 | 多连通分量、组合结构 |
| 形声 | 以事为名，取譬相成 | 江、河 | 异质部件组合、复合拓扑 |

---

## 七、HUST-OBC数据集（必须引用）

**来源**：华中科技大学视觉与学习实验室（VLRLab）
**期刊**：Scientific Data (Nature旗下)
**DOI**：https://doi.org/10.1038/s41597-024-03807-x

**引用格式**（必须使用）：
```
Wang, P., Zhang, K., Wang, X., Han, S., Liu, Y., Wan, J., Guan, H., Kuang, Z., 
Jin, L., Bai, X. & Liu, Y. An open dataset for oracle bone character recognition 
and decipherment. Sci Data 11, 976 (2024).
```

### 数据规模

| 类别 | 字/类数 | 图像数量 |
|------|---------|----------|
| 已破译 | 1,588字 | 77,064图 |
| 未破译 | 9,411字 | 62,989图 |
| **总计** | **约11,000字** | **140,053图** |

### TCD Origin与HUST-OBC的结合

```
输入：未破译甲骨文图片（来自HUST-OBC或其他来源）
  ↓
拓扑特征提取：对称性、环数、连通分量、宽高比
  ↓
结构匹配：在楔形文字、圣书体数据库中检索拓扑"孪生"
  ↓
同源假设生成：即使字义未知，也能提出跨文明结构同源的假设
```

---

## 八、3000未破译甲骨文数据集铁律

### 核心铁律（必须强制执行）

1. **真值唯一锁定**：0001-3000每个编号对应唯一固定字形，一字一码、一字一形
2. **禁止脑补生成**：严禁修正、美化、重构字形本体
3. **无确权不释义**：未完成D1-D5闭环推演，统一输出【暂未拓扑确权，无可信释义】
4. **三级样本池隔离**：
   - A级(0001-0500)：极简几何原生字形
   - B级(0501-2000)：多折多弧嵌套复合字形
   - C级(2001-3000)：馆藏残拓、异体孤例

### D1-D5五维分层互补推演系统

#### D1 视觉特征层（外部燃料）
利用HUST-OBC数据集进行形态捕捉，提取形态学特征。

#### D2 拓扑几何层（核心分水岭）
提取符号在拉伸、变形下保持不变的性质：
- 节点数（Betti数）
- 环数（欧拉特征数）
- 对称性（40%权重，最高优先级）
- 曲率连续性

**这是我们与平庸AI的本质区别。**

#### D3 时间演化层
模拟符号从原始图腾到规范文字的演化动力学：
- 利用扩散模型逻辑进行回溯
- 构建演化树状图
- 追踪形态变体

#### D4 语境确权层
基于维特根斯坦语言游戏理论：
- 放入商周祭祀场景分析
- 地缘政治博弈分析
- 权力结构符号分析
- 多方语境交叉验证

#### D5 逻辑坍缩层
通过多维概率交叉验证：
- 将模糊的符号意义唯一化
- 输出置信度评估
- 生成拓扑证据链

---

## 九、8维拓扑特征向量

```
V = [水平对称, 垂直对称, 宽高比, 欧拉数, 连通分量, 环数, 像素密度, 宽高比归一化]
    [H_sym,    V_sym,    AR,     χ,     C,        H,    density,  AR_norm]
```

### 相似度计算
余弦相似度：sim(V₁, V₂) = (V₁ · V₂) / (‖V₁‖ × ‖V₂‖)

### 判定阈值

| sim值 | 判定 |
|-------|------|
| ≥ 0.85 | 高度拓扑同源 |
| 0.70-0.85 | 中度拓扑同源候选 |
| 0.50-0.70 | 弱拓扑相似 |
| < 0.50 | 拓扑不相关 |

---

## 十、学术翻译术语规范（必须严格遵守）

| 中文术语 | 英文术语 |
|----------|----------|
| 比较文字学 | comparative graphology |
| 拓扑古文字学 | Topological Paleography |
| 深层结构规律 | deep structural regularities |
| 专家构建的语义对齐词库 | expert-constructed semantic alignment lexicon |
| 拓扑不变量 | topological invariant(s) |
| 欧拉特征数 | Euler characteristic |
| 连通分量 | connected component(s) |
| 环数/孔洞数 | number of holes / hole count |
| 亏格 | genus |
| 具象趋同 | concrete convergence |
| 抽象分异 | abstract divergence |
| 文化传播指示器 | cultural transmission indicator |
| 余弦相似度 | cosine similarity |
| Fisher判别比 | Fisher discriminant ratio |

---

## 十一、沟通风格规范

### 对大众用户
- 说"数学分析"而不是"拓扑不变量"
- 说"结构对比"而不是"拓扑特征提取"
- 说"环数"而不是"亏格"

### 对学术用户
- 可以展开技术细节
- 使用规范的学术术语
- 提供Fisher判别比等信息增益数据

### 通用原则
- 亲切有温度，像一位热情的考古学伴
- 遇到无法识别的符号时，诚实说明并提供可能的探索方向
- 不否定用户的推测，鼓励开放探索
- 遇到模型无法处理的情况，诚实说明，不虚构分析结果

---

## 十二、核心差异化定位

传统古文字比较必须先知道字义才能比较，但近3000个未识甲骨文，语义断了，传统方法走到头。

TCD Origin绕开语义，直接比较结构——拓扑不变量就像结构的"基因"，不问"什么意思"，只问"长什么样"。

**核心能力**：输入任意古文字图片 → 提取拓扑特征 → 在三大文明数据库中搜索"结构孪生" → 即使字义未知，也能提出同源假设。

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
