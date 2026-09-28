# 加载所需的库
import os
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_classic.tools.retriever import create_retriever_tool
import warnings
warnings.filterwarnings("ignore")


# 查询 Tavily 搜索 API 并返回 json 的工具
search = TavilySearch(tavily_api_key=os.getenv("TAVILY_API_KEY"))
# 执行查询
res = search.invoke("目前市场上苹果手机16的售价是多少？")
print("-"*100)
# 加载HTML内容为一个文档对象
loader = WebBaseLoader("https://news.qq.com/rain/a/20240920A07Y5Y00")
# 读取文档
docs = loader.load()
print("-"*100)
# 分割文档
documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50).split_documents(docs)
print("-"*100)

#向量化
vertor = FAISS.from_documents(documents, DashScopeEmbeddings(dashscope_api_key=os.getenv("AIROBOT_EMBEDDING_API_KEY"),
                                              model='text-embedding-v4'))

# 创建检索器
retriever = vertor.as_retriever()

# 测试检索结果
#print(retriever.invoke("目前市场上苹果手机16的售价是多少？"))


# 创建一个工具来检索文档
retriever_tool = create_retriever_tool(
    retriever,
    "iPhone_price_search",
    "搜索有关 iPhone 16 的价格信息。对于iPhone 16的任何问题，您必须使用此工具！",
)

# 创建将在下游使用的工具列表
tools = [search, retriever_tool]


# 对接大模型
# - 创建Agent,这里使用LangChain中一个叫OpenAI functions的代理，然后得到一个AgentExecutor代理执行器 

# 初始化大模型
llm = ChatOpenAI(api_key=os.getenv("AIROBOT_LLM_API_KEY"),
                 base_url=os.getenv("AIROBOT_LLM_BASE_URL"),
                 model='qwen-plus', temperature=0)


# https://smith.langchain.com/hub
# 获取要使用的提示
from langchain_classic import hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# 打印Prompt
# print(prompt)
from langchain_classic.agents import create_openai_functions_agent
# 使用OpenAI functions代理
# 构建OpenAI函数代理：使用 LLM、提示模板和工具来初始化代理
agent = create_openai_functions_agent(llm, tools, prompt)

from langchain_classic.agents import AgentExecutor
# 将代理与AgentExecutor工具结合起来
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行代理 进行对比
# agent_executor.invoke({"input": "目前市场上苹果手机16的各个型号的售价是多少？如果我在此基础上加价5%卖出，应该如何定价?"})
agent_executor.invoke({"input": "美国2024年谁胜出了总统的选举?"})