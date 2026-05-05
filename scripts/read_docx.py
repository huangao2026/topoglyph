#!/usr/bin/env python3
"""
读取古文字拓扑专利升级文档
"""
import sys
import os

sys.path.insert(0, '/workspace/projects/src')

from coze_coding_dev_sdk.fetch import FetchClient
from coze_coding_utils.runtime_ctx.context import Context

# 用户提供的URL
url = "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%8F%A4%E6%96%87%E5%AD%97%E6%8B%93%E6%89%91%E4%B8%93%E5%88%A9%E5%8D%87%E7%BA%A71.docx&nonce=afb842bc-ced7-4def-ac11-77a35bba18b1&project_id=7613053284970184739&sign=1c2c72ecd3fa3595f84b7c6947ef47dfa832b79b9c35ba6497096f4b2eb95511"

print("正在获取文档内容...")
print(f"URL: {url}\n")

ctx = None  # 不需要ctx参数
client = FetchClient(ctx=ctx)

try:
    response = client.fetch(url=url)
    
    print(f"状态码: {response.status_code}")
    print(f"标题: {response.title}")
    print(f"文件类型: {response.filetype}")
    print(f"URL: {response.url}")
    print("-" * 80)
    
    # 提取文本内容
    text_content = []
    for item in response.content:
        if item.type == "text":
            text_content.append(item.text)
    
    full_text = "\n".join(text_content)
    print("\n文档内容:")
    print("=" * 80)
    print(full_text)
    print("=" * 80)
    
    # 保存到文件
    output_file = "/workspace/projects/assets/古文字拓扑专利升级1_内容.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"标题: {response.title}\n")
        f.write(f"文件类型: {response.filetype}\n")
        f.write("-" * 80 + "\n")
        f.write(full_text)
    
    print(f"\n内容已保存到: {output_file}")
    
except Exception as e:
    print(f"获取文档失败: {e}")
    import traceback
    traceback.print_exc()
