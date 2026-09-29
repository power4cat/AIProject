#langchain 实现Memory

# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# import os
# load_dotenv()

# llm = ChatOpenAI(api_key=os.getenv("AIROBOT_LLM_API_KEY"),
#                  base_url=os.getenv("AIROBOT_LLM_BASE_URL"),
#                  model_name="qwen-plus")

# # 直接提供问题，并调用llm
# response = llm.invoke("你好我是柏汌")
# # print(response)
# print(response.content)
# print("=" * 50)
# response = llm.invoke("我是谁?")

# print(response.content)


from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message("hi!")
history.add_user_message("你好")
history.add_ai_message("whats up?")
print(history.messages)