#向量存储
# pip install faiss-cpu
# pip install langchain_community==0.3.7
# pip install dashscope


import os
from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

load = WebBaseLoader('https://www.gov.cn/zhengce/content/202510/content_7043916.htm',
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(id='UCAP-CONTENT'))
)
docs = load.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs1 = text_splitter.split_documents(docs)
print(docs1)
print("-"*100)
print(f"总文档数量: {len(docs1)}")

embeddings = DashScopeEmbeddings(dashscope_api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
                                 model='text-embedding-v4')

#初始化 FAISS
vertor =None
batch_size = 10

# 分批处理文档
for i in range(0, len(docs1), batch_size):
    batch_docs = docs1[i:i + batch_size]
    print(f'第{i // batch_size + 1}批次 文档数量: {len(batch_docs)}')

    # 第一批：创建新的 FAISS 索引
    if i == 0:
        vector = FAISS.from_documents(batch_docs, embeddings)
    # 后续批次：将新文档添加到现有索引
    else:
        new_vector = FAISS.from_documents(batch_docs, embeddings)
        vector.merge_from(new_vector)  # 合并新索引到现有索引


vector.save_local("faiss_index")
print("FAISS 索引已保存到 faiss_index 文件夹")