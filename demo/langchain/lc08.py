#Langchain数据检索
import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建嵌入模型
model_name = r"D:\LLM\Local_model\BAAI\bge-large-zh-v1___5"

embeddings = HuggingFaceEmbeddings(model_name=model_name)


# 加载现有 Chroma 数据库
persist_directory = "./testdb"

db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)
print(f"成功加载 Chroma 数据库从 {persist_directory}")

# 实例化检索器
retriever = db.as_retriever(search_kwargs={"k": 4})  # 设置返回文档数量

# 获取问题相关文档
query = "会计核算基础规范"

docs = retriever.invoke(query)
for i, doc in enumerate(docs, 1):
    print(f"结果 {i}:\n{doc.page_content}")