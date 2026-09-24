from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# 创建解析器
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, XMLOutputParser
from langchain_classic.chains import LLMChain  # 新增：导入 LLMChain 用于非 LCEL 链式调用
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化语言模型
model = ChatOpenAI(
    api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)

# output_parser = StrOutputParser()
output_parser = JsonOutputParser()
# xml_parser = XMLOutputParser()

# 提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的程序员"),
    ("user", "{input}")
])

# 使用 LLMChain 构建链（非 LCEL 方式）
chain = LLMChain(
    llm=model,
    prompt=prompt,
    output_parser=output_parser  # 指定输出解析器
)

# res = chain.invoke({"input": "langchain是什么? 使用xml格式输出"})
res = chain.invoke({"input": "langchain是什么? 问题用question 回答用ans 返回一个JSON格式"})
# res = chain.invoke({"input": "大模型中的langchain是什么?"})
print(res)