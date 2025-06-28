def get_tongyi_llm():
    # 引入依赖
    from langchain_openai import ChatOpenAI
    # 连接信息
    api_key = "sk-b44c48bc661a42c9a5c5706a59c989e9"
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model = "qwen-turbo"
    # 连接模型
    llm = ChatOpenAI(base_url=base_url, api_key=api_key, model=model)
    return llm