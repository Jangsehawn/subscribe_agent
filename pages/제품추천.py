import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_core.messages.chat import ChatMessage
from langchain_teddynote.messages import random_uuid
from modules.handler import stream_handler, format_search_result
from modules.agent import create_agent_executor
from modules.tools import (
    CustomerProfileTool,
    ProductRecommendationTool,
    ScriptGeneratorTool
)

# Load environment variables
load_dotenv()

st.title("고객 맞춤 제품 추천 및 상담 스크립트 생성기 💡")
st.markdown("고객 데이터를 기반으로 제품을 추천하고 상담 스크립트를 생성합니다.")

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "agent" not in st.session_state:
    st.session_state["agent"] = None
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = random_uuid()

# 사이드바 설정
with st.sidebar:
    st.subheader("고객 데이터 입력")
    customer_id = st.text_input("고객번호 입력")
    mart_file = st.file_uploader("마트 메타데이터 업로드 (CSV)", type="csv")
    product_file = st.file_uploader("제품 메타데이터 업로드 (CSV)", type="csv")
    start_btn = st.button("분석 시작", type="primary")

# 이전 대화 출력 함수
def print_messages():
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])

# 새 메시지 저장 함수
def add_message(role, content):
    st.session_state["messages"].append({"role": role, "content": content})

# 이전 대화 출력
print_messages()

if start_btn and customer_id and mart_file and product_file:
    customer_df = pd.read_csv(mart_file)
    product_df = pd.read_csv(product_file)

    # 툴 정의
    tools = [
        CustomerProfileTool(customer_df=customer_df, customer_id=customer_id),
        ProductRecommendationTool(product_df=product_df),
        ScriptGeneratorTool()
    ]

    # 에이전트 생성
    agent = create_agent_executor(
        model_name="gpt-4o",
        tools=tools
    )
    st.session_state["agent"] = agent

    # 사용자 질문 입력 받기
    user_input = st.chat_input("상담을 시작하려면 질문을 입력하세요")

    if user_input:
        add_message("user", user_input)
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            container = st.empty()
            config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

            container_messages, tool_args, agent_answer = stream_handler(
                container,
                agent,
                {"messages": [("human", user_input)]},
                config
            )

            for tool_arg in tool_args:
                with st.expander(f"🔍 {tool_arg['tool_name']} 결과"):
                    st.markdown(format_search_result(tool_arg['tool_result']))

            container.write(agent_answer)
            add_message("assistant", agent_answer)

else:
    st.warning("사이드바에서 고객번호 및 데이터를 입력하고 시작 버튼을 눌러주세요.")
