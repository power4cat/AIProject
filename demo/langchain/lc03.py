# RAG+Langchain 
import os
# 0.3版本能进行导入 替换导入方式
# from langchain.chains.combine_documents import create_stuff_documents_chain
# langchain_classic 提供向下兼容模块
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

# 加载环境变量（用于 LLM 的 API 密钥）
load_dotenv()

# 创建嵌入模型
embeddings = DashScopeEmbeddings(
    dashscope_api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
    model='text-embedding-v4'
)
# 加载本地 FAISS 索引
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
save_path = os.path.join(project_root, "faiss_index")

vector_store = FAISS.load_local(
    folder_path=save_path,
    embeddings=embeddings,
    allow_dangerous_deserialization=True  # 允许加载 pickle 文件（仅限可信文件）
)

# 创建提示模板
prompt = ChatPromptTemplate.from_template("""仅根据提供的上下文回答以下问题:

<context>
{context}
</context>

问题: {input}""")

# 创建 LLM 连接（继续使用阿里云 qwen-plus）
llm = ChatOpenAI(
    api_key=os.getenv("AIROBOT_LLM_API_KEY"),  # 确保环境变量名为 DASHSCOPE_API_KEY
    base_url=os.getenv("AIROBOT_LLM_BASE_URL"),
    model="qwen-plus"
)

# 创建文档组合链
# langchain_core\prompts\chat.py可以看到提示词拼接
# format_messages 方法拼接提示词
document_chain = create_stuff_documents_chain(llm, prompt)

# 创建检索器
retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # 限制检索 3 个文档

# 创建检索链
# 在langchain_community\vectorstores\faiss.py 可以查看向量检索的实现
# similarity_search_with_score_by_vector 是检索的方法  return docs[:k]
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# 调用检索链并获取回答
# openai\resources\chat\completions\completions.py
# create方法中 self._post()  调用模型请求的api
response = retrieval_chain.invoke({"input": "密云水库水源保护条例什么时候执行"})

print("\n回答:", response["answer"])