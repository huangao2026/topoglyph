#!/usr/bin/env python3
"""
火山引擎知识库API - 完整调用示例
演示如何在实际项目中使用火山引擎知识库工具
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat,
    VolcengineKnowledgeConfig
)


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def example_1_simple_search():
    """示例1: 简单的文本查询"""
    print_header("示例1: 简单的文本查询")
    
    # 查询1: 什么是甲骨文
    print("查询: 什么是甲骨文？")
    print("-" * 80)
    result = search_volcengine_knowledge("什么是甲骨文？")
    print(result)
    
    print("\n" + "─" * 80 + "\n")
    
    # 查询2: 埃及象形文字荷鲁斯
    print("查询: 埃及象形文字荷鲁斯的含义是什么？")
    print("-" * 80)
    result = search_volcengine_knowledge("埃及象形文字荷鲁斯的含义是什么？")
    print(result)


def example_2_image_search():
    """示例2: 图文混合查询"""
    print_header("示例2: 图文混合查询")
    
    # 注意：这里需要一个真实的图片URL
    # 实际使用时，请替换为真实的图片URL
    image_url = "https://upload.wikimedia.org/wikipedia/commons/2/23/Egyptian_Hieroglyphs.png"
    
    print(f"查询: 图片中是什么古文字？")
    print(f"图片URL: {image_url}")
    print("-" * 80)
    
    result = search_volcengine_knowledge(
        query="图片中是什么古文字？请详细解释",
        image_url=image_url
    )
    print(result)


def example_3_context_search():
    """示例3: 带上下文的查询"""
    print_header("示例3: 带上下文的查询")
    
    # 场景：用户在研究古埃及文字
    context = """
用户正在研究古埃及象形文字系统，特别关注以下几个方面：
1. 符号的分类（表意、表音、限定符号）
2. 书写方向的判断方法
3. 常见神祇符号的含义
4. 王名圈的作用和识别

用户已经了解基础知识，现在需要更深入的专业解答。
"""
    
    query = "如何根据人形和动物符号的朝向判断书写方向？"
    
    print(f"上下文: {context[:100]}...")
    print(f"查询: {query}")
    print("-" * 80)
    
    result = search_volcengine_knowledge_with_context(
        query=query,
        context=context
    )
    print(result)


def example_4_multi_round_chat():
    """示例4: 多轮对话"""
    print_header("示例4: 多轮对话")
    
    # 对话历史
    messages = []
    
    # 第1轮: 用户提问
    print("第1轮对话")
    print("-" * 80)
    question1 = "什么是楔形文字？"
    print(f"用户: {question1}")
    print("\nAgent思考中...\n")
    
    answer1 = search_volcengine_knowledge(question1)
    print(f"知识库: {answer1}")
    
    # 添加到对话历史
    messages.append({"role": "user", "content": question1})
    messages.append({"role": "assistant", "content": answer1})
    
    print("\n" + "─" * 80 + "\n")
    
    # 第2轮: 用户追问
    print("第2轮对话")
    print("-" * 80)
    question2 = "它的发展历史是怎样的？"
    print(f"用户: {question2}")
    print("\nAgent思考中...\n")
    
    answer2 = multi_round_knowledge_chat(messages)
    print(f"知识库: {answer2}")
    
    # 添加到对话历史
    messages.append({"role": "user", "content": question2})
    messages.append({"role": "assistant", "content": answer2})
    
    print("\n" + "─" * 80 + "\n")
    
    # 第3轮: 继续追问
    print("第3轮对话")
    print("-" * 80)
    question3 = "有哪些著名的楔形文字文献？"
    print(f"用户: {question3}")
    print("\nAgent思考中...\n")
    
    answer3 = multi_round_knowledge_chat(messages)
    print(f"知识库: {answer3}")


def example_5_comparative_analysis():
    """示例5: 对比分析查询"""
    print_header("示例5: 对比分析查询")
    
    query = """
请对比分析甲骨文和楔形文字的以下方面：
1. 起源时间和地点
2. 载体材料（刻在什么上面）
3. 符号系统的特点
4. 破译历史
5. 现存数量和研究价值
"""
    
    print(f"查询: {query}")
    print("-" * 80)
    
    result = search_volcengine_knowledge(query)
    print(result)


def example_6_research_assistant():
    """示例6: 研究助手模式"""
    print_header("示例6: 研究助手模式")
    
    print("场景：用户正在准备一篇关于古文字的学术论文")
    print("\n")
    
    # 研究主题
    research_topic = "古埃及象形文字在法老时期的演变"
    
    print(f"研究主题: {research_topic}")
    print("\n")
    
    # 查询1: 背景知识
    print("步骤1: 查询背景知识")
    print("-" * 80)
    background = search_volcengine_knowledge(
        f"请介绍{research_topic}的背景知识"
    )
    print(background)
    print("\n")
    
    # 查询2: 关键符号
    print("步骤2: 查询关键符号")
    print("-" * 80)
    key_symbols = search_volcengine_knowledge(
        "列出古埃及象形文字中最重要的10个符号及其含义"
    )
    print(key_symbols)
    print("\n")
    
    # 查询3: 研究方法
    print("步骤3: 查询研究方法")
    print("-" * 80)
    methods = search_volcengine_knowledge(
        "研究古埃及象形文字有哪些主要方法和工具？"
    )
    print(methods)
    print("\n")
    
    # 查询4: 学术资源
    print("步骤4: 查询学术资源")
    print("-" * 80)
    resources = search_volcengine_knowledge(
        "推荐一些研究古埃及象形文字的权威学术资源和工具"
    )
    print(resources)


def example_7_educational_tutor():
    """示例7: 教育辅导模式"""
    print_header("示例7: 教育辅导模式")
    
    print("场景：为学生讲解古文字知识")
    print("\n")
    
    # 第1课: 甲骨文
    print("第1课: 甲骨文")
    print("-" * 80)
    lesson1 = search_volcengine_knowledge(
        "用通俗易懂的语言介绍什么是甲骨文，适合初中生理解"
    )
    print(lesson1)
    print("\n")
    
    # 第2课: 楔形文字
    print("第2课: 楔形文字")
    print("-" * 80)
    lesson2 = search_volcengine_knowledge(
        "用通俗易懂的语言介绍什么是楔形文字，适合初中生理解"
    )
    print(lesson2)
    print("\n")
    
    # 第3课: 对比
    print("第3课: 两种文字的对比")
    print("-" * 80)
    comparison = search_volcengine_knowledge(
        "对比甲骨文和楔形文字的相似之处和不同之处，用简单的例子说明"
    )
    print(comparison)


def example_8_error_handling():
    """示例8: 错误处理"""
    print_header("示例8: 错误处理和异常捕获")
    
    print("测试各种错误情况\n")
    
    # 测试1: 未配置
    print("测试1: 未配置错误处理")
    print("-" * 80)
    try:
        # 临时清空API Key模拟未配置
        original_key = VolcengineKnowledgeConfig.API_KEY
        VolcengineKnowledgeConfig.API_KEY = ""
        
        result = search_volcengine_knowledge("测试查询")
        print(f"结果: {result}")
        
        # 恢复配置
        VolcengineKnowledgeConfig.API_KEY = original_key
        
    except Exception as e:
        print(f"捕获异常: {e}")
    
    print("\n")
    
    # 测试2: 空查询
    print("测试2: 空查询处理")
    print("-" * 80)
    try:
        result = search_volcengine_knowledge("")
        print(f"结果: {result}")
    except Exception as e:
        print(f"捕获异常: {e}")
    
    print("\n")
    
    # 测试3: 超长查询
    print("测试3: 超长查询处理")
    print("-" * 80)
    try:
        long_query = "测试" * 1000
        result = search_volcengine_knowledge(long_query)
        print(f"结果长度: {len(result)} 字符")
    except Exception as e:
        print(f"捕获异常: {e}")


def example_9_batch_processing():
    """示例9: 批量处理"""
    print_header("示例9: 批量处理多个查询")
    
    # 要查询的问题列表
    queries = [
        "什么是甲骨文？",
        "什么是楔形文字？",
        "什么是埃及象形文字？",
        "什么是金文？",
        "什么是玛雅文字？"
    ]
    
    print(f"批量查询 {len(queries)} 个问题\n")
    
    results = []
    for i, query in enumerate(queries, 1):
        print(f"查询 {i}/{len(queries)}: {query}")
        print("-" * 80)
        
        try:
            result = search_volcengine_knowledge(query)
            results.append({
                "query": query,
                "result": result,
                "success": True
            })
            
            # 显示结果摘要
            preview = result[:100] + "..." if len(result) > 100 else result
            print(f"结果摘要: {preview}")
            
        except Exception as e:
            results.append({
                "query": query,
                "result": str(e),
                "success": False
            })
            print(f"错误: {e}")
        
        print("\n" + "─" * 80 + "\n")
    
    # 统计
    success_count = sum(1 for r in results if r["success"])
    print(f"\n统计: 成功 {success_count}/{len(queries)}")


def example_10_custom_parameters():
    """示例10: 自定义参数（高级用法）"""
    print_header("示例10: 自定义参数和配置")
    
    print("展示如何自定义API调用参数\n")
    
    # 方式1: 修改配置
    print("方式1: 修改全局配置")
    print("-" * 80)
    print(f"当前域名: {VolcengineKnowledgeConfig.DOMAIN}")
    print(f"当前服务ID: {VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID}")
    print("\n")
    
    # 方式2: 构造复杂查询
    print("方式2: 构造复杂查询")
    print("-" * 80)
    
    complex_query = """
请详细分析古埃及象形文字的以下内容：
1. 基本特征（文字性质、书写方向、文字单位）
2. 符号分类（表意、表音、限定符号）
3. 语法结构（词序、人称、时态）
4. 著名文献（罗塞塔石碑、金字塔文等）
5. 破译方法论（罗塞塔方法、频率分析等）

请用结构化的方式回答，包含具体例子。
"""
    
    result = search_volcengine_knowledge(complex_query)
    print(result)


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "火山引擎知识库API - 完整调用示例" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # 检查配置
    print("\n配置检查:")
    print(f"  ✓ API Key已配置: {VolcengineKnowledgeConfig.is_configured()}")
    
    if not VolcengineKnowledgeConfig.is_configured():
        print("\n⚠️  警告：火山引擎知识库未配置")
        print("\n请先配置环境变量:")
        print("  export VOLCENGINE_API_KEY='your_api_key'")
        print("  export VOLCENGINE_SERVICE_ID='your_service_id'")
        print("\n然后重新运行此脚本")
        return
    
    print("\n" + "─" * 80)
    print("  即将运行10个示例，按Ctrl+C可随时停止")
    print("─" * 80)
    
    input("\n按Enter键开始运行示例...")
    
    try:
        # 运行所有示例
        example_1_simple_search()
        input("\n按Enter键继续...")
        
        example_2_image_search()
        input("\n按Enter键继续...")
        
        example_3_context_search()
        input("\n按Enter键继续...")
        
        example_4_multi_round_chat()
        input("\n按Enter键继续...")
        
        example_5_comparative_analysis()
        input("\n按Enter键继续...")
        
        example_6_research_assistant()
        input("\n按Enter键继续...")
        
        example_7_educational_tutor()
        input("\n按Enter键继续...")
        
        example_8_error_handling()
        input("\n按Enter键继续...")
        
        example_9_batch_processing()
        input("\n按Enter键继续...")
        
        example_10_custom_parameters()
        
        print("\n" + "=" * 80)
        print("  ✅ 所有示例运行完成！")
        print("=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了示例运行")
    except Exception as e:
        print(f"\n\n❌ 运行示例时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
