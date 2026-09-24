# 使用chain
from langchain_classic.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 原始字符串模板
template = "桌上有{number}个苹果，四个桃子和 3 本书，一共有几个水果?"

# 创建模型实例
llm = ChatOpenAI(api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 model='qwen-max',
                 temperature=0)

# 创建LLMChain
# llm_chain = LLMChain(
#     llm=llm,
#     prompt=PromptTemplate.from_template(template)
# )
# # 调用LLMChain，返回结果
# result = llm_chain.invoke({"number": 2})
# print(type(result))
# print(result['text'])

# 新写法（推荐）
chain = PromptTemplate.from_template(template) | llm
result = chain.invoke({"number": 2})
print(result.content)