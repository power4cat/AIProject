#提示模版
# langchain03版本提供的 PromptTemplate导入方式
# from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    ChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# 导入LangChain中的OpenAI模型接口
from langchain_openai import ChatOpenAI
# 导入LangChain中的提示模板
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

#String提示模板
# 创建模型实例
# model = ChatOpenAI(api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
#                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#                    model='qwen-plus')

# prompt = PromptTemplate(
#     template="您是一位专业的程序员。\n对于信息 {text} 进行简短描述"
# )

# # 输入提示
# input = prompt.format(text="大模型langchain")

# # 得到模型的输出
# output = model.invoke(input)
# # output = model.invoke("您是一位专业的程序员。对于信息 langchain 进行简短描述")

# # 打印输出内容
# print(output.content)



# 聊天提示模板
template = "你是一个数学家，你可以计算任何算式"
# template = "你是一个翻译专家,擅长将 {input_language} 语言翻译成 {output_language}语言."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),# 系统角色：设定AI的身份和行为
    ("human", human_template),# 用户角色：具体的问题/指令
])
# print(chat_prompt)


# 创建模型实例
model = ChatOpenAI(api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
                   base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                   model='qwen-plus')
# 输入提示
messages = chat_prompt.format_messages(text="我今年18岁，我的舅舅今年38岁，我的爷爷今年72岁，我和舅舅一共多少岁了？")
# print(messages)
# messages = chat_prompt.format_messages(input_language="英文", output_language="中文", text="I love Large Language Model.")
print(messages)
# 得到模型的输出
output = model.invoke(messages)
# 打印输出内容
print(output.content)