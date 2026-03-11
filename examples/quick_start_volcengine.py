#!/usr/bin/env python3
"""
火山引擎知识库 - 快速开始示例
最简单的使用方式，3步上手
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from tools.volcengine_knowledge import search_volcengine_knowledge


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("  火山引擎知识库 - 快速开始")
    print("=" * 70 + "\n")
    
    # 检查配置
    try:
        from tools.volcengine_knowledge import VolcengineKnowledgeConfig
        
        if not VolcengineKnowledgeConfig.is_configured():
            print("❌ 火山引擎知识库未配置\n")
            print("请先配置环境变量：")
            print("  export VOLCENGINE_API_KEY='your_api_key'")
            print("  export VOLCENGINE_SERVICE_ID='your_service_id'\n")
            return
        
        print("✅ 配置检查通过\n")
    except Exception as e:
        print(f"❌ 配置检查失败: {e}\n")
        return
    
    # 定义查询
    query = "什么是甲骨文？"
    
    # 查询知识库
    print(f"查询: {query}")
    print("-" * 70 + "\n")
    
    try:
        result = search_volcengine_knowledge(query)
        print(result)
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    
    print("\n" + "=" * 70)
    print("  完成！")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
