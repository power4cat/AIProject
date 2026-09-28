# `Langchain`之中间件
# - 中间件：在大模型和工具之间插入的代码，用于在请求和响应之间进行处理。
# 中间件是`LangChain` 1.0引入的重要功能，允许你在LLM调用、工具执行、链式调用等关键环节**插入自定义逻辑**，实现监控、修改、记录等能力

from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
import os
from dotenv import load_dotenv
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()


# 定义查询订单状态的函数
def query_order_status(order_id):
    if order_id == "1024":
        return "订单 1024 的状态是：已发货，预计送达时间是 3-5 个工作日。"
    else:
        return f"未找到订单 {order_id} 的信息，请检查订单号是否正确。"


# 定义退款政策说明函数
def company_refund_policy(company_name):
    print(company_name)
    if company_name == "tom":
        return "tom公司的退款政策是：在购买后7天内可以申请全额退款，需提供购买凭证。"
    else:
        print('输入有误')


# 查询年龄
def get_age(name):
    if name == "tom":
        print(name)
        return "我的年龄是56岁！"
    else:
        print('输入有误')


# 初始化工具
tools = [
    TavilySearch(max_results=1, tavily_api_key=os.getenv("TAVILY_API_KEY")),
    Tool(
        name="queryOrderStatus",
        func=query_order_status,
        description="根据订单ID查询订单状态",
        args={"order_id": "订单的ID"}
    ),
    Tool(
        name="companyRefundPolicy",
        func=company_refund_policy,
        description="查询某某公司退款政策详细内容",
        args={"company_name": "公司名称"}
    ),
    Tool(
        name="getAge",
        func=get_age,
        description="查询tom年龄大小",
        args={"name": "查询tom年龄大小"}
    ),
]

# 选择将驱动代理的LLM
llm = ChatOpenAI(api_key=os.getenv("AIROBOT_LLM_API_KEY"),
                 base_url=os.getenv("AIROBOT_LLM_BASE_URL"),
                 model='qwen-plus')

agent = create_agent(
    model=llm,
    tools=tools,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                'tavily_search': {'allowed_decisions': ['approve', 'reject']},
                "queryOrderStatus": {'allowed_decisions': ['approve', 'reject']},
                "companyRefundPolicy": {'allowed_decisions': ['approve', 'reject']},
                "getAge": {'allowed_decisions': ['approve', 'reject']},
            }
        )
    ],
    checkpointer=InMemorySaver(),
    system_prompt="你是一个客服助手，使用工具回答问题。传递给工具的内容必须是准确的json数据不结尾的括号多加一个,如果是字符串数据必须和输入的保持一致要完整,不是篡改**重要规则**, ",
)
# 定义一些测试询问
queries = [
    "请问订单1024的状态是什么？",
    "请问tom公司退款政策是什么？",
    "2024年谁胜出了美国总统的选举"
]
config = {"configurable": {"thread_id": "some_other_id"}}

# 运行代理并输出结果
for que in queries:
    print('客户提问：' + que)
    inputs = {"messages": [{"role": "user", "content": que}]}
    result = agent.invoke(inputs, config=config)
    tool_name = result['__interrupt__'][0].value['action_requests'][0]['name']
    app_or_reject = input("请确认调用{}是否同意(approve or reject)：".format(tool_name))
    res = agent.invoke(
        Command(resume={'decisions': [{'type': app_or_reject}]}),
        config=config
    )
    print(res['messages'][-1].content)