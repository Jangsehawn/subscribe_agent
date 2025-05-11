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
st.set_page_config(page_title="제품정보 조회", page_icon="📦")
st.title("📦 제품 정보 조회 시스템")

# 제품 이름 입력
product_name = st.text_input("제품 이름을 입력하세요:")

# 조회 버튼
if st.button("조회"):
    if product_name in PRODUCTS:
        product = PRODUCTS[product_name]
        st.success(f"✅ '{product_name}' 제품 정보")
        st.write(f"**카테고리:** {product['카테고리']}")
        st.write(f"**가격:** {product['가격']}")
        st.write(f"**재고:** {product['재고']}개")
    else:
        st.error(f"❌ '{product_name}' 제품을 찾을 수 없습니다.")