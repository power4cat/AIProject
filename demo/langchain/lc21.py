# 使用`Langsmith`生成提示词
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from langsmith import Client

import os

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
prompt = client.pull_prompt("test1")

print(prompt)
llm = ChatOpenAI(
    api_key=os.getenv("AIROBOT_LLM_API_KEY"),
    base_url=os.getenv("AIROBOT_LLM_BASE_URL"),
    model='qwen-plus'
)

# 创建 LangChain 链
chain = prompt | llm

# 输入示例
input_data = {
    "product": "无线耳机",
    "features": "音质清晰、佩戴舒适、续航长",
    "emotion": "科技感、轻松",
    "action": "分享体验",
    "question": "请帮我写一篇小红书种草文案"
}

response = chain.invoke(input_data)

# 输出生成的小红书文案
print(response.content)