#chromadb 模块下载 pip install chromadb
import chromadb
client = chromadb.Client()
# 创建 client 时，设置数据持久化路径, 默认存储在内存,程序运行完时会丢失
# client = chromadb.PersistentClient(path=r"D:\software\chroma")
# 存在这个集合就返回，不存在就创建
collection = client.get_or_create_collection(name="test")

# 添加数据
collection.add(
    documents=["Article by john", "Article by Jack", "Article by Jill"], # 文本内容列表，每个元素是一段文本（如文章、句子等）
    embeddings=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],  # 嵌入向量列表，每个元素是一个与 documents 对应的向量表示
    ids=["1", "2", "3"] # 自定义 ID 列表，用于唯一标识每条记录
)

# 查询数据
aa = collection.get(
    ids=["1"],
    where_document={"$contains": "john"}, # 表示文本内容中包含 "john" 的文档
    include=["embeddings","documents"] # 返回向量和文本
)

#  查询结果，包含文档内容、嵌入向量等信息。
print(aa)

# 删除数据
# collection.delete(
#     ids=["1"]
# )
# print(collection.get(include=["embeddings"]))


# 修改数据
collection.update(
    documents=["Article by john", "Article by Jack", "Article by Jill"],
    embeddings=[[10,2,3],[40,5,6],[70,8,9]],
    ids=["1", "2", "3"])
print(collection.get(include=["embeddings"]))

