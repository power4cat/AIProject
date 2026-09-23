import chromadb
from chromadb.config import Settings
import json
from openai import OpenAI
from dotenv import load_dotenv
import os


class MyVectorDBConnector:
    def __init__(self, collection_name):
        # 创建一个客户端
        chroma_client = chromadb.Client(Settings(allow_reset=True))

        # 创建一个 collection
        # cosine余弦相似度  默认欧式距离
        self.collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def get_embeddings(self, texts, model="text-embedding-v4"):
        '''封装 qwen 的 Embedding 模型接口'''
        # print('texts', texts)
        data = client.embeddings.create(input=texts, model=model).data
        return [x.embedding for x in data]

    def add_documents(self, instructions, outputs):
        '''向 collection 中添加文档与向量'''
        # get_embeddings(instructions)
        # 将(问题)数据向量化
        embeddings = self.get_embeddings(instructions)

        # 把向量化的数据和原文存入向量数据库
        # 存入数据库时：
        self.collection.add(
            embeddings=embeddings,      # 问题的向量（用于检索）
            documents=outputs,          # 回答的原文（作为元数据存储）
            ids=[f"id{i}" for i in range(len(outputs))]# 每个文档的 id
        )
        

        # print(self.collection.count())

    def search(self, query):
        '''检索向量数据库'''
        # 把我们查询的问题向量化, 在chroma当中进行查询
        # D:\software\miniconda\envs\py_ai\Lib\site-packages\chromadb\segment\impl\vector\local_hnsw.py  默认相似度匹配欧式距离
        results = self.collection.query(
            query_embeddings=self.get_embeddings([query]),
            n_results=2,
        )
        return results


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI(api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"), base_url=os.getenv("AIROBOT_EMBEDDING_BASE_URL"))
    # 读取文件
    with open('train_zh.json', 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    # print(data)
    # print(data[0:100])

    # 获取前10条的问题和输出
    instructions = [entry['instruction'] for entry in data[0:10]]
    outputs = [entry['output'] for entry in data[0:10]]

    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo")

    # 向向量数据库中添加文档
    vector_db.add_documents(instructions, outputs)
    # print(vector_db.collection.get())
    # user_query = "白癜风"
    user_query = "得了白癜风怎么办？"
    results = vector_db.search(user_query)
    # print(results)

    for doc in results['documents'][0]:
        print(f"【内容】: {doc}\n")
        print("-" * 50)