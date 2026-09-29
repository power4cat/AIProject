from langchain_core.stores import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
from langchain_classic.retrievers import MultiVectorRetriever
import uuid
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# 本地embedding模型地址
embedding_model_path = r'D:\LLM\Local_model\BAAI\bge-large-zh-v1___5'

url = "https://news.pku.edu.cn/mtbdnew/15ac0b3e79244efa88b03a570cbcbcaa.htm"
# 初始化文档加载器列表（加载多个文本文件）
loaders = [
    UnstructuredWordDocumentLoader("人事管理流程.docx"),
    WebBaseLoader(url)
]

# 加载并合并所有文档
docs = []
for loader in loaders:
    docs.extend(loader.load())
# print(docs)
# 初始化递归文本分割器（设置块大小和重叠）
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
docs = text_splitter.split_documents(docs)
# print(docs)

llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

# 创建摘要生成链
chain = (
        {"doc": lambda x: x.page_content}
        | ChatPromptTemplate.from_template("总结下面的文档:\n\n{doc}")
        | llm
        | StrOutputParser()
)

# 批量生成文档摘要（最大并发数5）
summaries = chain.batch(docs, {"max_concurrency": 5})
# print(summaries)

# 初始化嵌入模型（用于文本向量化）
embeddings_model = HuggingFaceEmbeddings(
    model_name=embedding_model_path
)
# 初始化Chroma实例（用于存储摘要向量）
vectorstore = Chroma(
    collection_name="summaries",
    embedding_function=embeddings_model
)

# 初始化内存字节存储（用于存储原始文档）
store = InMemoryByteStore()


# 初始化多向量检索器（结合向量存储和文档存储）
id_key = "doc_id"
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)

# 为每个文档生成唯一ID
doc_ids = [str(uuid.uuid4()) for _ in docs]

# 创建摘要文档列表（包含元数据） metadata可以用来关联原始文档和摘要文档会自动找到匹配关系
summary_docs = [
    Document(page_content=s, metadata={id_key: doc_ids[i]}) for i, s in enumerate(summaries)
]

# 将摘要添加到向量数据库
retriever.vectorstore.add_documents(summary_docs)

# 将原始文档存储到字节存储（使用ID关联）
retriever.docstore.mset(list(zip(doc_ids, docs)))


# 执行相似性搜索测试
sub_docs = retriever.vectorstore.similarity_search("病假的请假流程?")
print("-------------匹配的摘要内容--------------")
print(sub_docs[0])

# 获取第一个匹配摘要的ID
matched_id = sub_docs[0].metadata[id_key]

# 通过ID获取原始文档
original_doc = retriever.docstore.mget([matched_id])
print("-------------对应的原始文档--------------")
print(original_doc)


prompt = ChatPromptTemplate.from_template("根据下面的文档回答问题:\n\n{doc}\n\n问题: {question}")
# 生成问题回答链
chain = RunnableMap({
    "doc": lambda x: retriever.invoke(x["question"]),
    "question": lambda x: x["question"]
}) | prompt | llm | StrOutputParser()

# 生成问题回答
query = "病假的请假流程?"
answer = chain.invoke({"question": query})
print("-------------回答--------------")
print(answer)

retrieved_docs = retriever.invoke(query)
print("-------------检索到的文档--------------")
print(retrieved_docs)