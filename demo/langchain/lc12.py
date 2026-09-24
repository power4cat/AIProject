# **通过batch方法(原apply方法)**:batch方法允许输入列表运行链，一次处理多个输入


from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


# 创建模型实例
template = PromptTemplate(
    input_variables=["role", "fruit"],
    template="{role}喜欢吃{fruit}?",
)

# 创建LLM
llm = ChatOpenAI(api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 model='qwen-plus',
                 temperature=0)


llm_chain = template | llm

# 输入列表
input_list = [
    {"role": "猪八戒", "fruit": "人参果"}, {"role": "孙悟空", "fruit": "仙桃"}
]

# 调用LLMChain，返回结果
result = llm_chain.batch(input_list)
print(result[0].content)
print(result[1].content)