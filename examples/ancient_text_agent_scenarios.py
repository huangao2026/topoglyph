#!/usr/bin/env python3
"""
古文字破译系统 - 实际应用场景
展示如何在古文字破译系统中使用火山引擎知识库
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat
)


class AncientTextAgent:
    """古文字破译智能体 - 集成火山引擎知识库"""
    
    def __init__(self):
        self.conversation_history = []
    
    def analyze_text(self, text: str, text_type: str = None) -> dict:
        """
        分析古文字文本
        
        Args:
            text: 古文字内容
            text_type: 文字类型（可选）
        
        Returns:
            分析结果字典
        """
        print(f"\n{'='*70}")
        print(f"开始分析古文字")
        print(f"{'='*70}\n")
        
        # 构建查询
        if text_type:
            query = f"""
请分析以下{text_type}文本：
{text}

请提供以下信息：
1. 文字类型识别
2. 主要符号分析
3. 可能的含义
4. 历史背景
"""
        else:
            query = f"""
请分析以下古文字文本：
{text}

请提供以下信息：
1. 识别这是什么文字系统
2. 主要符号分析
3. 可能的含义
4. 历史背景
"""
        
        print(f"查询知识库...\n")
        
        # 查询知识库
        result = search_volcengine_knowledge(query)
        
        print(f"知识库回答：\n{result}\n")
        
        # 保存到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": f"分析文本: {text}"
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })
        
        return {
            "text": text,
            "type": text_type,
            "analysis": result
        }
    
    def analyze_image(self, image_url: str) -> dict:
        """
        分析古文字图片
        
        Args:
            image_url: 图片URL
        
        Returns:
            分析结果字典
        """
        print(f"\n{'='*70}")
        print(f"开始分析古文字图片")
        print(f"{'='*70}\n")
        
        query = "请详细分析图片中的古文字，包括符号识别、含义解释、历史背景等"
        
        print(f"查询知识库（图文混合）...\n")
        
        # 图文查询
        result = search_volcengine_knowledge(
            query=query,
            image_url=image_url
        )
        
        print(f"知识库回答：\n{result}\n")
        
        # 保存到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": f"分析图片: {image_url}"
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })
        
        return {
            "image_url": image_url,
            "analysis": result
        }
    
    def ask_followup(self, question: str) -> str:
        """
        追问
        
        Args:
            question: 追问问题
        
        Returns:
            知识库回答
        """
        print(f"\n{'='*70}")
        print(f"追问")
        print(f"{'='*70}\n")
        
        print(f"问题: {question}\n")
        print(f"查询知识库（带对话历史）...\n")
        
        # 使用多轮对话
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        result = multi_round_knowledge_chat(self.conversation_history)
        
        print(f"知识库回答：\n{result}\n")
        
        # 保存回答
        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })
        
        return result
    
    def get_tools_recommendation(self, requirements: list) -> str:
        """
        获取AI工具推荐
        
        Args:
            requirements: 需求列表
        
        Returns:
        推荐的工具列表
        """
        print(f"\n{'='*70}")
        print(f"获取AI工具推荐")
        print(f"{'='*70}\n")
        
        query = f"""
用户有以下古文字研究需求：
{chr(10).join(f'- {req}' for req in requirements)}

请推荐适合的AI工具，包括：
1. 工具名称
2. 功能特点
3. 适用场景
4. 访问方式
"""
        
        print(f"查询知识库...\n")
        
        result = search_volcengine_knowledge(query)
        
        print(f"知识库回答：\n{result}\n")
        
        return result


def scenario_1_text_analysis():
    """场景1: 文本分析"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "场景1: 文本分析" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    
    agent = AncientTextAgent()
    
    # 示例文本
    text = """
𓀁𓀂𓀃𓀄𓀅
𓁹𓁺𓁻𓁼𓁽
𓂋𓂌𓂍𓂎𓂏
"""
    
    # 分析
    result = agent.analyze_text(text, text_type="埃及象形文字")
    
    # 追问
    question = "这些符号有什么特别含义？"
    agent.ask_followup(question)


def scenario_2_image_analysis():
    """场景2: 图片分析"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "场景2: 图片分析" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    
    agent = AncientTextAgent()
    
    # 示例图片URL
    image_url = "https://upload.wikimedia.org/wikipedia/commons/2/23/Egyptian_Hieroglyphs.png"
    
    # 分析
    result = agent.analyze_image(image_url)
    
    # 追问
    question = "图片中的符号排列有什么规律？"
    agent.ask_followup(question)


def scenario_3_research_assistant():
    """场景3: 研究助手"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "场景3: 研究助手" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    
    agent = AncientTextAgent()
    
    # 研究主题
    text = "我正在研究古埃及象形文字的符号系统，需要了解表意符号、表音符号和限定符号的区别"
    
    # 分析
    result = agent.analyze_text(text, text_type="研究主题")
    
    # 多轮追问
    questions = [
        "请举例说明每个类别",
        "它们在实际文本中如何配合使用？"
    ]
    
    for question in questions:
        agent.ask_followup(question)


def scenario_4_tools_recommendation():
    """场景4: 工具推荐"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "场景4: AI工具推荐" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    
    agent = AncientTextAgent()
    
    # 用户需求
    requirements = [
        "需要识别甲骨文图片",
        "希望有学术级精度",
        "最好是免费的",
        "支持批量处理"
    ]
    
    # 获取推荐
    result = agent.get_tools_recommendation(requirements)


def scenario_5_comprehensive_analysis():
    """场景5: 综合分析"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "场景5: 综合分析" + " " * 32 + "║")
    print("╚" + "═" * 68 + "╝")
    
    agent = AncientTextAgent()
    
    print("用户上传了一张古文字图片，并提供了相关背景信息\n")
    
    # 提供背景
    context = """
用户正在研究古埃及象形文字，这是从一座神庙墙壁上拓印的铭文。
据考古学家推测，这段铭文可能记录了某位法老的功绩。
用户希望了解：
1. 铭文的大致内容
2. 相关的历史背景
3. 推荐进一步研究的工具
"""
    
    print(f"背景信息: {context}\n")
    
    # 图片URL
    image_url = "https://upload.wikimedia.org/wikipedia/commons/2/23/Egyptian_Hieroglyphs.png"
    
    # 分析图片
    result = agent.analyze_image(image_url)
    
    # 结合背景分析
    query = f"""
基于以下背景信息，详细分析图片中的古文字：

{context}
"""
    
    followup_result = search_volcengine_knowledge_with_context(
        query=query,
        context=context
    )
    
    print(f"\n综合分析结果:\n{followup_result}\n")


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "古文字破译系统 - 实际应用场景" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # 检查配置
    try:
        from tools.volcengine_knowledge import VolcengineKnowledgeConfig
        
        if not VolcengineKnowledgeConfig.is_configured():
            print("\n⚠️  警告：火山引擎知识库未配置")
            print("\n请先配置环境变量:")
            print("  export VOLCENGINE_API_KEY='your_api_key'")
            print("  export VOLCENGINE_SERVICE_ID='your_service_id'\n")
            return
        
        print("\n✅ 配置检查通过\n")
    except Exception as e:
        print(f"\n❌ 配置检查失败: {e}\n")
        return
    
    # 运行场景
    scenarios = [
        ("文本分析", scenario_1_text_analysis),
        ("图片分析", scenario_2_image_analysis),
        ("研究助手", scenario_3_research_assistant),
        ("工具推荐", scenario_4_tools_recommendation),
        ("综合分析", scenario_5_comprehensive_analysis),
    ]
    
    print("可用场景:")
    for i, (name, _) in enumerate(scenarios, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = input("\n请选择场景 (1-5, 或0运行所有): ")
        choice = int(choice)
        
        if choice == 0:
            # 运行所有场景
            for name, scenario_func in scenarios:
                scenario_func()
                input("\n按Enter键继续下一个场景...")
        elif 1 <= choice <= len(scenarios):
            # 运行选定场景
            scenarios[choice - 1][1]()
        else:
            print("无效的选择")
    
    except ValueError:
        print("无效的输入")
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
