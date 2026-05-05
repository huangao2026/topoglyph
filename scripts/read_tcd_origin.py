#!/usr/bin/env python3
"""
读取跨文明古文字拓扑破译引擎项目说明书
"""
import sys
import os

sys.path.insert(0, '/workspace/projects/src')

from coze_coding_dev_sdk.fetch import FetchClient

# 用户提供的URL
url = "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2FTCD+Origin+%E8%B7%A8%E6%96%87%E6%98%8E%E5%8F%A4%E6%96%87%E5%AD%97%E6%8B%93%E6%89%91%E7%A0%B4%E8%AF%91%E5%BC%95%E6%93%8E+%E9%A1%B9%E7%9B%AE%E8%AF%B4%E6%98%8E%E4%B9%A6.docx&nonce=f1d0eda7-0523-492a-980d-b51d924c0301&project_id=7613053284970184739&sign=fd1a6c828ce95d2f2b1ce696e6ee4df40145996e5c6838a32f1e5a2223dff25f"

print("正在获取文档内容...")
print(f"URL: {url}\n")

client = FetchClient()

try:
    response = client.fetch(url=url)
    
    print(f"状态码: {response.status_code}")
    print(f"标题: {response.title}")
    print(f"文件类型: {response.filetype}")
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
    output_file = "/workspace/projects/assets/TCD_Origin_项目说明书_内容.txt"
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
