from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

import os

# 定义小红书文案提示词
prompt = PromptTemplate.from_template("""
你是一位小红书内容创作者，擅长撰写简洁、吸引人的种草文案。目标是创作100-150字的小红书风格文案，面向18-35岁用户，激发兴趣和互动。

**输入**：
- 产品/主题：{product}
- 核心特点：{features}
- 目标情绪：{emotion}
- 目标行动：{action}

**要求**：
1. 风格：亲切、口语化，带小幽默或生活场景，融入“种草”“安利”等流行词。
2. 结构：吸睛开头（问题/场景），中间突出特点，结尾引导互动（提问/号召）。
3. 使用1-2个emoji，保持自然。
4. 标题：10字以内。

**输出**：
标题:
文案正文:分2-3段，每段2-3句，结尾带互动引导
""")

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
    "action": "分享体验"
}
response = chain.invoke(input_data)
# 输出生成的小红书文案
print(response.content)