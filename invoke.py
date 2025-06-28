from models import get_tongyi_llm

from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

#消息列表 
message = [
    SystemMessage(content="你是一个消息列表"),
    HumanMessage(content="潜江为什么盛产小龙虾？")
]
# 引入大模型
llm = get_tongyi_llm()
# 单次调用
response = llm.invoke(input=message)
print(response.content)
# 基本调用   stream
messages1 = [
    ("user", "你是谁？")
]
for chunk in llm.stream(input=messages1):
    print(chunk.content)

# 基本调用   batch    
messages3 = [
    "你好",
    "武汉有多少人口？"
]
response = llm.batch(inputs=messages3)
print(response[0].content)
print(response[1].content)