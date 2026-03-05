#!/usr/bin/env python3
"""
数据库初始化脚本
用于初始化数据库表和默认数据
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Base, engine, init_db, check_db_connection
from src.storage.models import User, Plugin, Tool
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables():
    """创建所有数据库表"""
    try:
        logger.info("开始创建数据库表...")
        init_db()
        logger.info("✅ 数据库表创建成功！")
        return True
    except Exception as e:
        logger.error(f"❌ 创建数据库表失败: {e}")
        return False

def drop_tables():
    """删除所有数据库表"""
    try:
        logger.warning("⚠️  即将删除所有数据库表...")
        confirm = input("确认删除所有表？此操作不可逆！(yes/no): ")
        if confirm.lower() != 'yes':
            logger.info("操作已取消")
            return False
        
        from src.storage.database import drop_db
        drop_db()
        logger.info("✅ 所有表已删除！")
        return True
    except Exception as e:
        logger.error(f"❌ 删除表失败: {e}")
        return False

def init_default_data():
    """初始化默认数据"""
    try:
        logger.info("开始初始化默认数据...")
        
        # 创建默认插件
        default_plugins = [
            {
                "name": "ocr_tool",
                "version": "1.0.0",
                "description": "OCR 文字识别工具",
                "author": "Ancient Script Team",
                "config": {"supported_formats": ["jpg", "png", "pdf"]},
                "enabled": True
            },
            {
                "name": "translation_tool",
                "version": "1.0.0",
                "description": "翻译工具",
                "author": "Ancient Script Team",
                "config": {"supported_languages": ["zh", "en", "ja", "ko"]},
                "enabled": True
            },
            {
                "name": "analysis_tool",
                "version": "1.0.0",
                "description": "古文字分析工具",
                "author": "Ancient Script Team",
                "config": {"supported_scripts": ["oracle", "bronze", "hieroglyph"]},
                "enabled": True
            }
        ]
        
        for plugin_data in default_plugins:
            existing = engine.execute(
                f"SELECT id FROM plugins WHERE name = '{plugin_data['name']}'"
            ).fetchone()
            
            if not existing:
                plugin = Plugin(**plugin_data)
                engine.session.add(plugin)
                logger.info(f"  ✅ 创建插件: {plugin_data['name']}")
            else:
                logger.info(f"  ⏭️  插件已存在: {plugin_data['name']}")
        
        # 创建默认工具
        default_tools = [
            {
                "name": "殷契文渊",
                "display_name": "殷契文渊",
                "description": "甲骨文识别、字形检索、拓片摹本生成",
                "category": "oracle",
                "api_endpoint": "http://www.jgwlbq.org.cn",
                "api_key_required": False,
                "enabled": True
            },
            {
                "name": "殷契行止",
                "display_name": "殷契行止",
                "description": "微信小程序，甲骨文识别和释义",
                "category": "oracle",
                "api_endpoint": None,
                "api_key_required": False,
                "enabled": True
            },
            {
                "name": "JiaguCopilot",
                "display_name": "JiaguCopilot",
                "description": "清华大学专家级甲骨学AI系统",
                "category": "oracle",
                "api_endpoint": None,
                "api_key_required": True,
                "enabled": True
            },
            {
                "name": "GlyphStudy",
                "display_name": "GlyphStudy",
                "description": "埃及圣书体符号识别和翻译",
                "category": "hieroglyph",
                "api_endpoint": None,
                "api_key_required": False,
                "enabled": True
            },
            {
                "name": "JSesh",
                "display_name": "JSesh",
                "description": "圣书体编辑器和识别工具",
                "category": "hieroglyph",
                "api_endpoint": None,
                "api_key_required": False,
                "enabled": True
            },
            {
                "name": "Transkribus",
                "display_name": "Transkribus",
                "description": "手写体/铭文OCR，多语言支持",
                "category": "general",
                "api_endpoint": "https://www.transkribus.org",
                "api_key_required": False,
                "enabled": True
            }
        ]
        
        for tool_data in default_tools:
            existing = engine.execute(
                f"SELECT id FROM tools WHERE name = '{tool_data['name']}'"
            ).fetchone()
            
            if not existing:
                tool = Tool(**tool_data)
                engine.session.add(tool)
                logger.info(f"  ✅ 创建工具: {tool_data['name']}")
            else:
                logger.info(f"  ⏭️  工具已存在: {tool_data['name']}")
        
        engine.session.commit()
        logger.info("✅ 默认数据初始化成功！")
        return True
    except Exception as e:
        logger.error(f"❌ 初始化默认数据失败: {e}")
        engine.session.rollback()
        return False

def check_connection():
    """检查数据库连接"""
    logger.info("检查数据库连接...")
    if check_db_connection():
        logger.info("✅ 数据库连接正常！")
        return True
    else:
        logger.error("❌ 数据库连接失败！")
        return False

def show_stats():
    """显示数据库统计信息"""
    try:
        logger.info("数据库统计信息：")
        
        # 统计各表的记录数
        tables = [
            "users", "sessions", "messages", "conversations",
            "analysis_history", "plugins", "tools", "system_logs", "system_metrics"
        ]
        
        for table in tables:
            try:
                count = engine.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                logger.info(f"  📊 {table}: {count} 条记录")
            except Exception as e:
                logger.warning(f"  ⚠️  {table}: 查询失败 - {e}")
        
        return True
    except Exception as e:
        logger.error(f"❌ 获取统计信息失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("古文字破译系统 - 数据库初始化脚本")
    print("=" * 60)
    print()
    
    # 检查连接
    if not check_connection():
        logger.error("无法连接到数据库，请检查配置！")
        sys.exit(1)
    
    print()
    print("请选择操作：")
    print("1. 创建所有表")
    print("2. 删除所有表（危险！）")
    print("3. 初始化默认数据")
    print("4. 显示统计信息")
    print("5. 完整初始化（创建表 + 初始化数据）")
    print("0. 退出")
    print()
    
    choice = input("请输入选项 (0-5): ").strip()
    
    if choice == "1":
        create_tables()
    elif choice == "2":
        drop_tables()
    elif choice == "3":
        init_default_data()
    elif choice == "4":
        show_stats()
    elif choice == "5":
        if create_tables():
            init_default_data()
        show_stats()
    elif choice == "0":
        logger.info("退出")
        sys.exit(0)
    else:
        logger.error("无效选项！")
        sys.exit(1)

if __name__ == "__main__":
    main()
