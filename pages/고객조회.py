from attr import dataclass
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_teddynote import logging
from langchain_teddynote.messages import random_uuid
from modules.agent import create_agent_executor
from dotenv import load_dotenv
from modules.handler import stream_handler, format_search_result
from modules.tools import WebSearchTool

# API KEY 정보로드
load_dotenv()

# 프로젝트 이름
logging.langsmith("Perplexity")
# 페이지 설정
st.set_page_config(page_title="고객정보 조회", page_icon="📇")
st.title("📇 고객정보 조회 시스템")

# 고객번호 입력
customer_id = st.text_input("고객번호를 입력하세요:")

# 조회 버튼
if st.button("조회"):
    if customer_id in CUSTOMERS:
        customer = CUSTOMERS[customer_id]
        st.success(f"✅ 고객번호 {customer_id} 조회 완료")
        st.write(f"**이름:** {customer['이름']}")
        st.write(f"**등급:** {customer['등급']}")
        st.write(f"**최근 구매:** {customer['최근 구매']}")
        st.write(f"**누적 구매액:** {customer['누적 구매액']}")
    else:
        st.error("해당 고객번호는 존재하지 않습니다.")