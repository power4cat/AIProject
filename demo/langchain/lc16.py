# `LangChain`之Tools工具

from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化工具 可以根据需要进行配置
tool = TavilySearch(top_k_results=1, doc_content_chars_max=100)

# 工具默认名称
print("name:", tool.name)
print("=="*50)
# 工具默认的描述
print("description:", tool.description)
print("=="*50)
# 输入内容 默认JSON模式
print("args:", tool.args)
print("=="*50)
# 是否直接返回工具的输出。
print("return_direct:", tool.return_direct)
print("=="*50)
# 可以用字典输入来调用这个工具
print(tool.run({"query": "langchain是什么"}))
# 使用单个字符串输入来调用该工具。
#print(tool.run("langchain"))
# 需要科学上网