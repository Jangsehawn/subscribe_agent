import streamlit as st
import pandas as pd
import os
import plotly.express as px

# CSV 샘플 데이터 생성 (가안)
if not os.path.exists("data"):
    os.makedirs("data")

pd.DataFrame({
    "사무소": ["서울", "부산", "서울", "부산"],
    "날짜": ["2025-05-11"] * 4,
    "날씨": ["맑음", "흐림", "맑음", "흐림"],
    "기온": [22, 18, 22, 18]
}).to_csv("data/weather.csv", index=False)

pd.DataFrame({
    "사무소": ["서울", "서울", "부산", "부산"],
    "월": ["2025-04", "2025-05", "2025-04", "2025-05"],
    "실적": [120, 150, 100, 130],
    "전월실적": [100, 120, 90, 100]
}).to_csv("data/sales.csv", index=False)

pd.DataFrame({
    "사무소": ["서울", "서울", "부산"],
    "고객명": ["김철수", "이영희", "박지민"],
    "방문예정": ["Y", "N", "Y"],
    "연락처": ["010-1111-2222", "010-2222-3333", "010-3333-4444"]
}).to_csv("data/customers.csv", index=False)

pd.DataFrame({
    "사무소": ["서울", "부산"],
    "고객명": ["김철수", "박지민"],
    "전달사항": ["에어컨 관심 높음", "세탁기 A/S 문의"]
}).to_csv("data/notes.csv", index=False)

pd.DataFrame({
    "사무소": ["서울", "부산"],
    "제품명": ["휘센 에어컨", "트롬 세탁기"],
    "대상 고객 수": [12, 8]
}).to_csv("data/recommend_products.csv", index=False)

pd.DataFrame({
    "제목": ["AI 가전 시장 급성장", "LG전자, 신제품 발표"],
    "링크": ["https://example.com/news1", "https://example.com/news2"]
}).to_csv("data/news.csv", index=False)

# Streamlit 설정
st.set_page_config(page_title="LG전자 데일리 리포트", layout="wide")
st.title("📊 LG전자 사무소장용 데일리 리포트")

# CSV 불러오기
weather = pd.read_csv("data/weather.csv")
sales = pd.read_csv("data/sales.csv")
customers = pd.read_csv("data/customers.csv")
notes = pd.read_csv("data/notes.csv")
recommend = pd.read_csv("data/recommend_products.csv")
news = pd.read_csv("data/news.csv")

# 사이드바: 사무소 선택
offices = sales["사무소"].unique().tolist()
selected_office = st.sidebar.selectbox("사무소 선택", offices)

# 오늘 날짜 필터
today = weather["날짜"].max()

# 상단 2열 구성: 날씨 + 방문 예정 고객 수
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🌤️ 오늘의 날씨")
    weather_today = weather[(weather["사무소"] == selected_office) & (weather["날짜"] == today)]
    st.metric(label="기온", value=f"{weather_today['기온'].values[0]}°C")
    st.write(f"날씨: {weather_today['날씨'].values[0]}")

with col2:
    st.markdown("### 🧍 오늘 방문 예정 고객 수")
    today_customers = customers[(customers["사무소"] == selected_office) & (customers["방문예정"] == "Y")]
    st.metric("방문 예정 고객", len(today_customers))

# 실적 비교 (꺾은선그래프)
st.markdown("### 📈 월 실적 비교")
sales_office = sales[sales["사무소"] == selected_office]
fig = px.line(sales_office, x="월", y=["실적", "전월실적"], markers=True, title="실적 vs 전월실적")
fig.update_layout(font=dict(family="Arial", size=14))
st.plotly_chart(fig, use_container_width=True)

# 추천 제품 시각화
st.markdown("### 🎯 추천 제품별 대상 고객")
rec_office = recommend[recommend["사무소"] == selected_office]
col3, col4 = st.columns(2)
with col3:
    pie = px.pie(rec_office, names="제품명", values="대상 고객 수", title="제품 비율")
    pie.update_layout(font=dict(family="Arial", size=14))
    st.plotly_chart(pie, use_container_width=True)
with col4:
    bar = px.bar(rec_office, x="제품명", y="대상 고객 수", title="제품별 대상 고객 수")
    bar.update_layout(font=dict(family="Arial", size=14))
    st.plotly_chart(bar, use_container_width=True)

# 고객 정보 + 전달사항
st.markdown("### 👥 고객 정보 및 전달사항")
col5, col6 = st.columns(2)
with col5:
    st.markdown("#### 고객 정보")
    st.dataframe(customers[customers["사무소"] == selected_office])
with col6:
    st.markdown("#### 전달사항")
    st.dataframe(notes[notes["사무소"] == selected_office])

# 뉴스
st.markdown("### 📰 구독 뉴스")
for _, row in news.iterrows():
    st.markdown(f"- [{row['제목']}]({row['링크']})")
