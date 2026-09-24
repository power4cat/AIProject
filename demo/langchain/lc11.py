from langchain_openai import ChatOpenAI
# from langchain.schema import SystemMessage
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
# from langchain.schema.runnable import RunnableMap, RunnableBranch, RunnableLambda
from langchain_core.runnables import RunnableMap, RunnableBranch, RunnableLambda
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


class TravelQASystem:
    def __init__(self, openai_api_key, serpapi_api_key, embedding_api_key):
        """初始化旅游问答系统核心组件"""

        # 初始化语言模型
        self.llm = ChatOpenAI(api_key=openai_api_key,
                              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                              model="qwen-plus")

        # 初始化搜索工具
        self.search = TavilySearch(tavily_api_key=serpapi_api_key)

        # 初始化嵌入模型
        self.embeddings = DashScopeEmbeddings(dashscope_api_key=embedding_api_key,
                                              model='text-embedding-v4')

        # 构建景点知识库
        self.attraction_data = [
            "故宫：北京地标，明清皇宫，开放时间8:30-17:00",
            "颐和园：皇家园林，昆明湖、长廊等景点",
            "八达岭长城：距离市区70公里，建议游览3-4小时"
        ]

        # 使用内存型向量存储类
        self.vector_store = InMemoryVectorStore.from_texts(
            self.attraction_data, self.embeddings, k=1
        )

    def setup_runnable_pipeline(self):
        """定义Runnable流程管道"""
        # 3.1 问题解析模块：识别地点与查询类型
        parse_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="你是旅游助手，需从用户问题中提取地点和查询类型（天气/景点介绍/行程规划）"),
            ("user", """问题：{user_question}请以JSON格式返回：{{"location": "地点", "type": "查询类型"}}""")
        ])
        parse_module = parse_prompt | self.llm | JsonOutputParser()  # Output JSON string

        # 3.2 并行数据获取：天气查询+景点信息检索
        weather_query = RunnableLambda(
            lambda x: self.search.invoke(f"{x['location']} 今日天气")
        )
        attraction_retrieval = (lambda x: x["location"]) | self.vector_store.as_retriever() | (
            lambda x: x[0].page_content)
        # RunnableMap：并行执行天气查询和景点检索
        data_acquisition = RunnableMap({
            "weather": weather_query,
            "attraction": attraction_retrieval,
            "location": (lambda x: x["location"])
        })

        # 3.3 回答生成模块：整合信息并格式化
        today = datetime.now().strftime("%Y年%m月%d日")
        generate_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"你是专业旅游顾问，需结合景点信息和天气生成建议。今天是{today}。"),
            ("user", """地点：{location}
                景点信息：{attraction}
                天气情况：{weather}
                请生成1条行程建议，包含注意事项（如天气相关准备）""")
        ])
        generate_module = generate_prompt | self.llm | (lambda x: x.content.strip())

        """
        RunnableBranch实现
        RunnableBranch(
            (lambda x: 条件1, 执行的代码),
            (lambda x: 条件2, 执行的代码2),
            lambda x: {"location": x["location"], "attraction": attraction_retrieval.invoke(x)}
        )

        """
        # 3.4 全流程串联
        self.travel_qa_pipeline = (
            # 阶段1：解析问题
                parse_module
                | (lambda x: {"location": x["location"], "type": x["type"]})
                # 阶段2：并行获取数据（仅当查询类型为天气或行程时触发）
                # RunnableBranch：根据查询类型选择数据获取路径
                | RunnableBranch(
            (lambda x: "天气" in x["type"], data_acquisition),
            lambda x: {"location": x["location"], "attraction": attraction_retrieval.invoke(x)}
        )
                # 阶段3：生成回答
                | generate_module
        )

    def process_user_question(self, user_question):
        """处理用户提问并返回回答"""
        input_data = {"user_question": user_question}
        # try:
        response = self.travel_qa_pipeline.invoke(input_data)
        return response


# 示例用法
if __name__ == "__main__":
    # 替换为实际API密钥
    OPENAI_API_KEY = os.getenv("AIROBOT_EMBEDDING_API_KEY")
    # https://www.tavily.com/
    # SERPAPI_API_KEY = os.getenv("TAVILY_API_KEY")
    SERPAPI_API_KEY = "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"
    EMBEDDING_API_KEY = os.getenv("AIROBOT_EMBEDDING_API_KEY")

    # 初始化系统
    travel_qa = TravelQASystem(OPENAI_API_KEY, SERPAPI_API_KEY, EMBEDDING_API_KEY)
    travel_qa.setup_runnable_pipeline()

    # 测试1：查询天气与景点建议
    question1 = "今天故宫的天气怎么样?"
    answer1 = travel_qa.process_user_question(question1)
    print(f"User Question: {question1}\nAI Answer: {answer1}\n")