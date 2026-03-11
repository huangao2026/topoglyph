#!/usr/bin/env python3
"""
火山引擎知识库工具测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from tools.volcengine_knowledge import (
    search_volcengine_knowledge,
    search_volcengine_knowledge_with_context,
    multi_round_knowledge_chat,
    VolcengineKnowledgeConfig
)


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_config():
    """测试配置"""
    print_section("配置检查")
    
    print(f"✓ API Key已配置: {VolcengineKnowledgeConfig.is_configured()}")
    print(f"✓ Account ID: {VolcengineKnowledgeConfig.ACCOUNT_ID or '未设置'}")
    print(f"✓ API Key: {'*' * 10 if VolcengineKnowledgeConfig.API_KEY else '未设置'}")
    print(f"✓ Domain: {VolcengineKnowledgeConfig.DOMAIN}")
    print(f"✓ Service ID: {VolcengineKnowledgeConfig.SERVICE_RESOURCE_ID}")
    
    if not VolcengineKnowledgeConfig.is_configured():
        print("\n⚠️  警告：火山引擎知识库未完全配置")
        print("\n请设置以下环境变量：")
        print("  export VOLCENGINE_API_KEY='your_api_key'")
        print("  export VOLCENGINE_SERVICE_ID='your_service_id'")
        return False
    
    return True


def test_search():
    """测试知识库搜索"""
    print_section("测试：知识库搜索")
    
    if not VolcengineKnowledgeConfig.is_configured():
        print("⚠️  跳过测试：未配置火山引擎知识库")
        return
    
    queries = [
        "什么是甲骨文？",
        "埃及象形文字荷鲁斯的含义",
        "楔形文字的起源"
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        print("-" * 70)
        try:
            result = search_volcengine_knowledge(query)
            print(result[:500] + "..." if len(result) > 500 else result)
        except Exception as e:
            print(f"❌ 错误: {e}")


def test_search_with_context():
    """测试带上下文的搜索"""
    print_section("测试：带上下文的搜索")
    
    if not VolcengineKnowledgeConfig.is_configured():
        print("⚠️  跳过测试：未配置火山引擎知识库")
        return
    
    context = "用户正在研究古文字，特别关注文字系统的演变和发展历史"
    query = "甲骨文和楔形文字有什么相似之处？"
    
    print(f"\n上下文: {context}")
    print(f"查询: {query}")
    print("-" * 70)
    try:
        result = search_volcengine_knowledge_with_context(query, context)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ 错误: {e}")


def test_multi_round_chat():
    """测试多轮对话"""
    print_section("测试：多轮对话")
    
    if not VolcengineKnowledgeConfig.is_configured():
        print("⚠️  跳过测试：未配置火山引擎知识库")
        return
    
    messages = [
        {"role": "user", "content": "什么是甲骨文？"},
    ]
    
    print("\n第1轮: 什么是甲骨文？")
    print("-" * 70)
    try:
        result1 = search_volcengine_knowledge("什么是甲骨文？")
        print(result1[:300] + "..." if len(result1) > 300 else result1)
        
        # 添加回答到对话历史
        messages.append({"role": "assistant", "content": result1})
        
        # 追问
        messages.append({"role": "user", "content": "它有什么特点？"})
        
        print("\n第2轮: 它有什么特点？")
        print("-" * 70)
        result2 = multi_round_knowledge_chat(messages)
        print(result2[:300] + "..." if len(result2) > 300 else result2)
        
    except Exception as e:
        print(f"❌ 错误: {e}")


def test_image_search():
    """测试图文混合搜索（需要提供真实图片URL）"""
    print_section("测试：图文混合搜索")
    
    if not VolcengineKnowledgeConfig.is_configured():
        print("⚠️  跳过测试：未配置火山引擎知识库")
        return
    
    # 注意：这里需要一个真实的图片URL
    image_url = os.getenv("TEST_IMAGE_URL", "")
    
    if not image_url:
        print("⚠️  跳过测试：未提供测试图片URL")
        print("   请设置环境变量: export TEST_IMAGE_URL='https://example.com/image.jpg'")
        return
    
    query = "图片中是什么古文字？"
    
    print(f"\n查询: {query}")
    print(f"图片: {image_url}")
    print("-" * 70)
    try:
        result = search_volcengine_knowledge(query, image_url)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ 错误: {e}")


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "火山引擎知识库工具测试" + " " * 26 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # 检查配置
    config_ok = test_config()
    
    if config_ok:
        # 运行测试
        test_search()
        test_search_with_context()
        test_multi_round_chat()
        test_image_search()
    else:
        print("\n❌ 配置未完成，无法进行功能测试")
        print("\n请先配置环境变量，然后重新运行测试")
    
    print_section("测试完成")
    print("\n提示：")
    print("  1. 配置环境变量后重新运行测试")
    print("  2. 如需测试图文搜索，设置 TEST_IMAGE_URL")
    print("  3. 查看详细文档：VOLCENGINE_KNOWLEDGE_INTEGRATION.md")
    print()


if __name__ == "__main__":
    main()
