#自定义工具
from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """这是一个自定义工具，用于将两个整数相加"""
    return a+b

print(add.name)
print(add.description)
print(add.args)

res = add.run({"a": 1, "b": 2})
print(res)