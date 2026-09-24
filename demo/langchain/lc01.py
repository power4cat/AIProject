#langchain基本使用
# 安装指定版本的LangChain 
#pip install langchain==1.1.0  -i https://pypi.tuna.tsinghua.edu.cn/simple
#pip install langchain-openai==1.1.0  -i https://pypi.tuna.tsinghua.edu.cn/simple

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("AIROBOT_LLM_API_KEY"),
                      base_url=os.getenv("AIROBOT_LLM_BASE_URL"),
                      model_name="qwen-plus")

response = llm.invoke("什么是langchain")
print(response)
print("-"*100)
print(response.content)