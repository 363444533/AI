import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from models import get_tongyi_llm
import base64 
########## streamlit run app.py   运行命令
# 获取 LLM 实例
llm = get_tongyi_llm()

# 设置宽屏
st.set_page_config(layout="wide", page_title="AI Chat")
# 主标题
st.html(body="<h1 style='text-align:center; font-size:60px'>LLM Based Apps</h1>")
# 副标题
st.html(body="<p style='text-align:center; font-size:40px'>Hello 曹磊</p>")
# 分割线
st.divider()
# 初始化会话状态
if "conversations" not in st.session_state:
    st.session_state.conversations = [
        {
            "name": "对话 1",
            "messages": [
                SystemMessage(content="你是一个智能助手，能回答各种问题。")
            ]
        }
    ]
if "current_conversation_index" not in st.session_state:
    st.session_state.current_conversation_index = 0
if "editing_name" not in st.session_state:
    st.session_state.editing_name = False

# 侧边栏
with st.sidebar:
    # 添加头像框
    css = """
    <style>
        .centered-rounded-image {
        margin-top: -50px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 50%;  # 可调整圆角大小
            
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # 显示图片并应用 CSS 样式
    try:
        st.markdown(
            f'<img src="data:image/png;base64,{base64.b64encode(open("avatar.png", "rb").read()).decode()}" class="centered-rounded-image" width="100">',
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("未找到 avatar.png 文件，请检查文件路径。")

    
    st.title("设置")
    # 新建对话
    if st.button("新建对话"):
        new_conversation_name = f"对话 {len(st.session_state.conversations) + 1}"
        st.session_state.conversations.append({
            "name": new_conversation_name,
            "messages": [
                SystemMessage(content="你是一个智能助手，能回答各种问题。")
            ]
        })
        st.session_state.current_conversation_index = len(st.session_state.conversations) - 1

    # 修改对话名
    if st.session_state.conversations:
        if st.button("修改对话名"):
            st.session_state.editing_name = True

        if st.session_state.editing_name:
            current_conversation = st.session_state.conversations[st.session_state.current_conversation_index]
            new_name = st.text_input("请输入新的对话名", value=current_conversation["name"])
            if st.button("保存"):
                if new_name.strip() != current_conversation["name"].strip():
                    current_conversation["name"] = new_name.strip()
                st.session_state.editing_name = False
            elif st.button("取消"):
                st.session_state.editing_name = False

    # 选择对话
    conversation_names = [conv["name"] for conv in st.session_state.conversations]
    if conversation_names:
        def on_conversation_change():
            st.session_state.current_conversation_index = st.session_state.conversation_selectbox

        st.selectbox(
            "选择对话",
            range(len(conversation_names)),
            index=st.session_state.current_conversation_index,
            format_func=lambda x: conversation_names[x],
            key="conversation_selectbox",
            on_change=on_conversation_change
        )

    # 删除对话
    if st.button("删除当前对话") and len(st.session_state.conversations) > 1:
        del st.session_state.conversations[st.session_state.current_conversation_index]
        if st.session_state.conversations:
            st.session_state.current_conversation_index = min(
                st.session_state.current_conversation_index,
                len(st.session_state.conversations) - 1
            )
        else:
            st.session_state.current_conversation_index = 0
        st.rerun()  # 删除对话后重新渲染页面

    # 清除当前对话历史记录
    if st.button("清除当前对话历史记录") and st.session_state.conversations:
        st.session_state.conversations[st.session_state.current_conversation_index]["messages"] = [
            SystemMessage(content="你是一个智能助手，能回答各种问题。")
        ]

# 获取当前对话
if st.session_state.conversations:
    current_conversation = st.session_state.conversations[st.session_state.current_conversation_index]

    # 显示当前对话名称
    st.title(f"当前对话: {current_conversation['name']}")

    # 显示聊天历史
    for message in current_conversation["messages"][1:]:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    # 互动聊天
    if prompt := st.chat_input(placeholder="请输入你的问题..."):
        user_message = HumanMessage(content=prompt)
        current_conversation["messages"].append(user_message)
        with st.chat_message("user"):
            st.markdown(prompt)

        response = llm.invoke(current_conversation["messages"])
        assistant_message = AIMessage(content=response.content)
        current_conversation["messages"].append(assistant_message)
        with st.chat_message("assistant"):
            st.markdown(response.content)