"""
TCD Origin Web - Gradio 网页界面
跨文明古文字拓扑破译引擎 - 在线使用
"""

import gradio as gr
import base64
import json
import sys
import os
from typing import Tuple

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.tools.tcd_origin_engine import TCDOriginEngine

# 初始化分析器
engine = TCDOriginEngine()

def analyze_symbol(
    image,
    symbol_name: str,
    context: str,
    origin_estimate: str
) -> Tuple[str, str, str]:
    """
    分析古文字符号
    
    Args:
        image: 上传的图片
        symbol_name: 符号名称
        context: 分析上下文
        origin_estimate: 起源估计
    
    Returns:
        Tuple: (可视化结果, 详细分析, 解释说明)
    """
    try:
        # 检查输入
        if image is None:
            return (
                "⚠️ 请上传古文字图片",
                "",
                ""
            )
        
        if not symbol_name:
            return (
                "⚠️ 请输入符号名称",
                "",
                ""
            )
        
        # 执行分析
        result = engine.full_analysis(
            image_data=image,
            context=context or "",
            origin_estimate=origin_estimate or "未知"
        )
        
        # 构建可视化结果
        visualization = f"""
## 📊 {symbol_name} 符号分析结果

### 🔍 D1-D5 五层破译架构

| 层级 | 名称 | 特征 |
|------|------|------|
| D1 | 视觉形态层 | 对称性: {result.d1_features.symmetry_score:.2f} |
| D2 | 拓扑几何层 | 欧拉示性数: {result.d2_features.euler_characteristic} |
| D3 | 时间演化层 | 稳定性: {result.d3_features.stability_score:.2f} |
| D4 | 意义确权层 | 语义场: {result.d4_features.semantic_field} |
| D5 | 逻辑坍缩层 | 语义: {result.d5_features.final_semantic} |
"""
        
        # 构建详细分析
        detailed_analysis = f"""
## 📋 详细分析

### D1 视觉形态特征
- **对称性得分**: {result.d1_features.symmetry_score:.2f}
- **宽高比**: {result.d1_features.aspect_ratio:.2f}
- **笔画均匀度**: {result.d1_features.stroke_uniformity:.2f}

### D2 拓扑几何特征
- **欧拉示性数 (χ)**: {result.d2_features.euler_characteristic}
- **贝蒂数 [β₀, β₁, β₂]**: {result.d2_features.betti_numbers}
- **环数**: {result.d2_features.ring_count}
- **对称性**: {result.d2_features.symmetry_score:.2f}

### D3 时间演化特征
- **稳定性得分**: {result.d3_features.stability_score:.2f}
- **变异率**: {result.d3_features.variation_rate:.2%}
- **演化压力**: {result.d3_features.evolutionary_pressure}

### D4 意义确权特征
- **语义场**: {result.d4_features.semantic_field}
- **语义稳定性**: {result.d4_features.semantic_stability:.2f}
- **意义演化**: {result.d4_features.meaning_evolution}

### D5 逻辑坍缩特征
- **最终语义**: {result.d5_features.final_semantic}
- **置信度**: {result.d5_features.confidence:.2%}
- **备选语义**: {', '.join(result.d5_features.alternative_semantics)}
"""
        
        # 构建解释说明
        explanation = f"""
## 💡 分析解释

### 🎯 语义类型识别
- **识别结果**: {result.semantic_type}
- **识别置信度**: {result.semantic_confidence:.2%}

### 🔬 关键特征
1. **高对称性设计** ({result.d1_features.symmetry_score:.2f})
   - 对称性是人类视觉系统的天然偏好
   - 表明该符号易于识别和记忆

2. **拓扑结构稳定** (χ={result.d2_features.euler_characteristic})
   - 欧拉示性数反映了符号的拓扑复杂度
   - 负值表示存在多个环和孔洞

3. **文化传承稳定** ({result.d3_features.stability_score:.2f})
   - 长时间保持结构稳定
   - 表明符号具有重要的文化意义

### 📖 历史意义
该符号经历了 {result.d3_features.evolutionary_pressure} 的演化，
在 {origin_estimate or '未知'} 文明中具有重要的 {result.d4_features.semantic_field} 意义。

### 🎓 学习价值
通过D1-D5五层破译架构，我们可以：
- 从视觉感知到拓扑几何
- 从形态特征到文化意义
- 实现跨文明的古文字比较研究
"""
        
        return (
            visualization,
            detailed_analysis,
            explanation
        )
        
    except Exception as e:
        return (
            f"❌ 分析失败: {str(e)}",
            "",
            ""
        )

def homology_analysis(
    symbol1_name: str,
    symbol1_meaning: str,
    symbol1_origin: str,
    symbol2_name: str,
    symbol2_meaning: str,
    symbol2_origin: str,
    semantic_type: str
) -> str:
    """
    跨文明同源性分析
    
    Args:
        symbol1_name: 第一个符号名称
        symbol1_meaning: 第一个符号含义
        symbol1_origin: 第一个符号起源
        symbol2_name: 第二个符号名称
        symbol2_meaning: 第二个符号含义
        symbol2_origin: 第二个符号起源
        semantic_type: 语义类型
    
    Returns:
        str: 同源性分析结果
    """
    try:
        # 简化的同源性分析
        result = engine.analyze_cross_civilization_homology(
            symbol1_name=symbol1_name,
            symbol1_meaning=symbol1_meaning,
            symbol1_origin=symbol1_origin,
            symbol2_name=symbol2_name,
            symbol2_meaning=symbol2_meaning,
            symbol2_origin=symbol2_origin,
            semantic_type=semantic_type
        )
        
        return f"""
## 🔗 跨文明同源性分析结果

### 📊 分析概要

| 符号 | 名称 | 含义 | 起源 |
|------|------|------|------|
| 符号1 | {symbol1_name} | {symbol1_meaning} | {symbol1_origin} |
| 符号2 | {symbol2_name} | {symbol2_meaning} | {symbol2_origin} |

### 🎯 同源性等级
**{result['homology_level']}** ({result['comprehensive_distance']:.2f})

### 🔍 文化传播信号
{result['cultural_transmission_signal']}

### 📝 详细解释
{result['explanation']}

### 💡 学术价值
该分析基于TCD Origin的五层破译架构和拓扑不变量理论，
为跨文明符号比较研究提供了科学的量化方法。
"""
        
    except Exception as e:
        return f"❌ 分析失败: {str(e)}"

# 创建Gradio界面
with gr.Blocks(
    title="TCD Origin - 跨文明古文字拓扑破译引擎",
    theme=gr.themes.Soft(),
    description="基于D1-D5五层破译架构的AI古文字分析系统"
) as demo:
    # 标题
    gr.Markdown("""
    # 🏛️ TCD Origin - 跨文明古文字拓扑破译引擎
    
    欢迎使用基于D1-D5五层破译架构的AI古文字分析系统！
    
    ### ✨ 核心功能
    - 📷 **智能图像识别**：上传古文字图片，自动识别和分析
    - 🔬 **拓扑特征提取**：三层拓扑不变量体系
    - 🔗 **跨文明比较**：比较不同文明的符号同源性
    - 📊 **可视化分析**：清晰的D1-D5五层分析结果
    """)
    
    # 标签页
    with gr.Tabs():
        # 标签1：单个符号分析
        with gr.TabItem("🔍 单符号分析"):
            with gr.Row():
                with gr.Column(scale=1):
                    # 输入区域
                    gr.Markdown("### 📤 输入")
                    
                    image_input = gr.Image(
                        label="上传古文字图片",
                        type="filepath",
                        height=300
                    )
                    
                    symbol_name = gr.Textbox(
                        label="符号名称",
                        placeholder="例如：日、月、山、水",
                        lines=1
                    )
                    
                    context = gr.Textbox(
                        label="分析上下文（可选）",
                        placeholder="例如：甲骨文、祭祀场景",
                        lines=2
                    )
                    
                    origin_estimate = gr.Textbox(
                        label="起源估计（可选）",
                        placeholder="例如：甲骨文、楔形文字",
                        lines=1
                    )
                    
                    analyze_btn = gr.Button(
                        "🚀 开始分析",
                        variant="primary"
                    )
                
                with gr.Column(scale=2):
                    # 输出区域
                    gr.Markdown("### 📊 分析结果")
                    
                    with gr.Tabs():
                        with gr.TabItem("可视化结果"):
                            visualization_output = gr.Markdown()
                        
                        with gr.TabItem("详细分析"):
                            detailed_output = gr.Markdown()
                        
                        with gr.TabItem("解释说明"):
                            explanation_output = gr.Markdown()
        
        # 标签2：同源性分析
        with gr.TabItem("🔗 跨文明比较"):
            with gr.Row():
                with gr.Column(scale=1):
                    # 符号1
                    gr.Markdown("### 符号 1")
                    s1_name = gr.Textbox(label="名称", placeholder="例如：日")
                    s1_meaning = gr.Textbox(label="含义", placeholder="例如：太阳")
                    s1_origin = gr.Dropdown(
                        label="起源",
                        choices=["甲骨文", "楔形文字", "埃及圣书体", "玛雅文字", "其他"]
                    )
                
                with gr.Column(scale=1):
                    # 符号2
                    gr.Markdown("### 符号 2")
                    s2_name = gr.Textbox(label="名称", placeholder="例如：Ra")
                    s2_meaning = gr.Textbox(label="含义", placeholder="例如：太阳神")
                    s2_origin = gr.Dropdown(
                        label="起源",
                        choices=["甲骨文", "楔形文字", "埃及圣书体", "玛雅文字", "其他"]
                    )
            
            with gr.Row():
                semantic_type = gr.Dropdown(
                    label="语义类型",
                    choices=["天体类", "自然类", "人体类", "器物类"],
                    value="天体类"
                )
                
                homology_btn = gr.Button(
                    "🔍 比较同源性",
                    variant="primary"
                )
            
            homology_output = gr.Markdown()
        
        # 标签3：使用说明
        with gr.TabItem("📖 使用说明"):
            gr.Markdown("""
            ## 🏛️ TCD Origin 使用指南
            
            ### 1️⃣ 单符号分析
            1. 点击"上传古文字图片"按钮，选择要分析的符号图片
            2. 输入符号名称（如：日、月、山）
            3. （可选）输入分析上下文和起源估计
            4. 点击"开始分析"按钮
            5. 查看D1-D5五层分析结果
            
            ### 2️⃣ 跨文明比较
            1. 在"符号1"区域输入第一个符号的信息
            2. 在"符号2"区域输入第二个符号的信息
            3. 选择语义类型（天体类、自然类等）
            4. 点击"比较同源性"按钮
            5. 查看跨文明同源性分析结果
            
            ### 🎯 支持的图片格式
            - JPG / JPEG
            - PNG
            - GIF
            - BMP
            - WebP
            
            ### 📝 注意事项
            - 图片质量越高，分析结果越准确
            - 建议使用清晰的古文字图片
            - 复杂的符号可能需要更长的分析时间
            
            ### 🔬 技术背景
            TCD Origin 基于D1-D5五层破译架构：
            - D1: 视觉形态层
            - D2: 拓扑几何层
            - D3: 时间演化层
            - D4: 意义确权层
            - D5: 逻辑坍缩层
            """)
    
    # 绑定事件
    analyze_btn.click(
        fn=analyze_symbol,
        inputs=[image_input, symbol_name, context, origin_estimate],
        outputs=[visualization_output, detailed_output, explanation_output]
    )
    
    homology_btn.click(
        fn=homology_analysis,
        inputs=[s1_name, s1_meaning, s1_origin, s2_name, s2_meaning, s2_origin, semantic_type],
        outputs=[homology_output]
    )
    
    # 页脚
    gr.Markdown("""
    ---
    ### 📞 联系我们
    - 🌐 项目地址: [GitHub](https://github.com/YOUR_USERNAME/tcd-origin)
    - 📧 邮箱: tcd-origin@example.com
    - 📚 文档: [完整文档](./README.md)
    
    ### ⚠️ 免责声明
    本系统仅供学习和研究使用，分析结果仅供参考。
    """)

import os

# 启动应用
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 8080)),
        share=False,
        debug=False
    )
