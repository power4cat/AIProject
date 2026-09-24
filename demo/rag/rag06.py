#**基于RAG知识库实现智能AI系统**
from dotenv import load_dotenv
from openai import OpenAI
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import chromadb
import os


# 按照固定字符切割文档
def sliding_window_chunks(text, chunk_size, stride):
    return [text[i:i + chunk_size] for i in range(0, len(text), stride)]


# 读取PDF
def extract_text_from_pdf(filename, page_numbers=None):
    '''从 PDF 文件中（按指定页码）提取文字'''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            # 检查element是不是文本
            if isinstance(element, LTTextContainer):
                # print(element.get_text())
                # 将换行和空格去掉
                full_text += element.get_text().replace("\n", "").replace(" ", "")

    text_chunks = sliding_window_chunks(full_text, 250, 100)

    return text_chunks


# 向量数据库类
class MyVectorDBConnector:
    def __init__(self, collection_name, openai_client):
        chroma_client = chromadb.PersistentClient(path=r"/Users/shenma/Documents/project/AI-Robot/testdb")
        # 创建一个 collection
        self.collection = chroma_client.get_or_create_collection(name=collection_name)
        self.openai_client = openai_client

    # 使用智谱的模型进行向量化
    def get_embeddings(self, texts, model="text-embedding-v4", batch_size=10):
        '''封装 qwen 的 Embedding 模型接口'''
        all_embeddings = []
        # 分批处理，每批最多 batch_size 条文本
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            data = self.openai_client.embeddings.create(input=batch, model=model).data
            all_embeddings.extend([x.embedding for x in data])
        return all_embeddings

    def add_documents(self, documents):
        '''向 collection 中添加文档与向量'''
        self.collection.add(
            embeddings=self.get_embeddings(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[f"id{i}" for i in range(len(documents))]  # 每个文档的 id
        )

    def search(self, query, top_n):
        '''检索向量数据库'''
        results = self.collection.query(
            query_embeddings=self.get_embeddings([query]),
            n_results=top_n
        )
        return results

# RAG 机器人类
class RAG_Bot:
    def __init__(self, vector_db, openai_client, n_results=2):
        self.vector_db = vector_db
        self.openai_client = openai_client
        self.n_results = n_results

    # llm模型
    def get_completion(self, prompt, model="qwen-plus"):
        '''封装 千问 接口'''
        messages = [{"role": "user", "content": prompt}]
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,  # 模型输出的随机性，0 表示随机性最小
        )
        # print(response)
        return response.choices[0].message.content

    def chat(self, user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)
        print('search_results:', search_results)
        # 2. 构建 Prompt
        prompt = prompt_template.replace("__INFO__", "\n".join(search_results['documents'][0])).replace("__QUERY__",
                                                                                                        user_query)
        print('prompt:', prompt)
        # 3. 调用 LLM
        response = self.get_completion(prompt)
        return response

#主函数
if __name__ == '__main__':
    load_dotenv()
    client = OpenAI(api_key=os.getenv("AIROBOT_LLM_API_KEY"),
                    base_url=os.getenv("AIROBOT_LLM_BASE_URL"))
    prompt_template = """
    你是一个问答机器人。
    你的任务是根据下述给定的已知信息回答用户问题。
    确保你的回复完全依据下述已知信息。不要编造答案。
    如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

    已知信息:
    __INFO__

    用户问：
    __QUERY__

    请用中文回答用户问题。
    """
    # 使用示例
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_filename = os.path.join(script_dir, "财务管理文档.pdf")
    # 读取Word文件
    # paragraphs = extract_text_from_docx(docx_filename, min_line_length=10)
    paragraphs = extract_text_from_pdf(docx_filename, page_numbers=[0, 1, 2])
    # print(paragraphs)

    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo", client)
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)

    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        client
    )
    user_query = "财务管理权限划分?"
    response = bot.chat(user_query)
    print(response)