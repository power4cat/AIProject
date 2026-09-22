#把字符转换成向量

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"), base_url=os.getenv("AIROBOT_EMBEDDING_BASE_URL"))


def get_embeddings(texts, model="text-embedding-v1"):
    #  texts 是一个包含要获取嵌入表示的文本的列表，
    #  model 则是用来指定要使用的模型的名称
    #  生成文本的嵌入表示。结果存储在data中。
    data = client.embeddings.create(input=texts, model=model).data
    # print(data)
    # 返回了一个包含所有嵌入表示的列表
    return [x.embedding for x in data]


test_query = ["我爱你"]

vec = get_embeddings(test_query)
print(vec)
#  "我爱你" 文本嵌入表示的列表。
print(len(vec))
#  "我爱你" 文本的嵌入表示。
print(vec[0])
#  "我爱你" 文本的嵌入表示的维度。3072
print(len(vec[0]))
