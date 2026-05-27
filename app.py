import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# 1. ☕ 미식 테마 디자인 및 웹 타이틀 설정
st.set_page_config(page_title="서울 감성 맛집 매칭", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #fdfbf7; color: #3e362e; }
    .premium-card {
        background: #ffffff; border: 1px solid #dcd1c4; border-radius: 12px;
        padding: 20px; box-shadow: 0 4px 15px rgba(99, 72, 50, 0.05); margin-top: 15px;
    }
    .roulette-display {
        font-size: 20px; font-weight: 700; color: #8f5b34; text-align: center;
        background-color: #fcf8f2; padding: 15px; border: 2px dashed #d1bcac; border-radius: 8px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8f5b34 0%, #634832 100%) !important; color: white !important;
        font-weight: 700 !important; padding: 10px !important; border-radius: 6px !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h2 style="text-align:center; color:#634832;">🍷 SEOUL DINING MATCHER</h2>', unsafe_allow_html=True)

# 2. 📊 서울 핵심 핫플레이스 미니 데이터셋
spots_data = [
    {"식당명": "성수 미오", "지역": "성수", "분위기": "#인스타감성", "대표메뉴": "트러플 파스타", "평균가격": 23000, "lat": 37.5446, "lon": 127.0560},
    {"식당명": "중앙감속기", "지역": "성수", "분위기": "#힙한", "대표메뉴": "바질조개찜", "평균가격": 28000, "lat": 37.5430, "lon": 127.0512},
    {"식당명": "소문난성수감자탕", "지역": "성수", "분위기": "#아늑한", "대표메뉴": "감자탕", "평균가격": 11000, "lat": 37.5427, "lon": 127.0544},
    {"식당명": "한남 오아시스", "지역": "한남", "분위기": "#미니멀한", "대표메뉴": "아보카도 토스트", "평균가격": 19000, "lat": 37.5340, "lon": 127.0026},
    {"식당명": "파이프그라운드", "지역": "한남", "분위기": "#힙한", "대표메뉴": "옥수수 피자", "평균가격": 24000, "lat": 37.5381, "lon": 126.9992},
    {"식당명": "소와나", "지역": "한남", "분위기": "#미니멀한", "대표메뉴": "한우 오마카세", "평균가격": 69000, "lat": 37.5359, "lon": 126.9975},
    {"식당명": "연남 연하동", "지역": "홍대/연남", "분위기": "#인스타감성", "대표메뉴": "대왕후토마끼", "평균가격": 28000, "lat": 37.5610, "lon": 126.9245},
    {"식당명": "오레노라멘", "지역": "홍대/연남", "분위기": "#미니멀한", "대표메뉴": "토리빠이탄 라멘", "평균가격": 11000, "lat": 37.5525, "lon": 126.9205},
    {"식당명": "익선반주", "지역": "익선동", "분위기": "#힙한", "대표메뉴": "깻잎크림뇨끼", "평균가격": 21000, "lat": 37.5744, "lon": 126.9890},
    {"식당명": "청수당", "지역": "익선동", "분위기": "#전통적인", "대표메뉴": "말차 타르트", "평균가격": 15500, "lat": 37.5748, "lon": 126.9885},
    {"식당명": "스케줄청담", "지역": "강남/압구정", "분위기": "#인스타감성", "대표메뉴": "트러플 리조또", "평균가격": 33000, "lat": 37.5252, "lon": 127.0410},
    {"식당명": "땀땀 강남", "지역": "강남/압구정", "분위기": "#아늑한", "대표메뉴": "매운 곱창 쌀국수", "평균가격": 15000, "lat": 37.4992, "lon": 127.0264}
]
df = pd.DataFrame(spots_data)

# 3. 🧭 사이드바 조절 필터
st.sidebar.markdown("### 🧭 조건별 탐색")
sel_regions = st.sidebar.multiselect("📍 구역 선택", options=list(df["지역"].unique()), default=list(df["지역"].unique()))
sel_vibes = st.sidebar.multiselect("🎨 분위기 선택", options=list(df["분위기"].unique()), default=list(df["분위기"].unique()))
budget = st.sidebar.slider("💰 1인 예산 제한 (원)", min_value=10000, max_value=80000, value=70000, step=5000)

# ⭐️ 잘려 나갔던 필터 조건 구문 완벽 복구 및 정렬
filtered_df = df[(df["지역"].isin(sel_regions)) & (df["분위기"].isin(sel_vibes)) & (df["평균가격"] <= budget)]

# 4. 🎛️ 메인 레이아웃 (좌: 대시보드 / 우: 추천 룰렛)
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("### 🗺️ 분포 및 시각화")
    if not filtered_df.empty:
        st.map(filtered_df, latitude="lat", longitude="lon", zoom=11)
        fig = px.scatter(filtered_df, x="지역", y="평균가격", color="분위기", size="평균가격", hover_data=["식당명", "대표메뉴"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("조건에 맞는 장소가 없습니다.")

with right_col:
    st.markdown("### 🎰 장소 추천 룰렛")
    r_place = st.empty()
    res_place = st.empty()
    
    if st.button("🎲 맛집 룰렛 돌리기"):
        if not filtered_df.empty:
            res_place.empty()
            names = filtered_df["식당명"].tolist()
            for _ in range(15):
                r_place.html(f'<div class="roulette-display">🔄 탐색 중... [ {random.choice(names)} ]</div>')
                time.sleep(0.1)
            r_place.empty()
            
            pick = filtered_df.sample(n=1).iloc[0]
            card_html = f"""
            <div class="premium-card">
                <h4 style="margin:0; color:#8f5b34;">🍷 추천: {pick['식당명']}</h4>
                <p style="margin:5px 0 0 0; font-size:14px;">
                    <b>위치:</b> {pick['지역']} | <b>무드:</b> {pick['분위기']}<br>
                    <b>메뉴:</b> {pick['대표메뉴']} | <b>가격:</b> ₩{pick['평균가격']:,}원
                </p>
            </div>
            """
            res_place.html(card_html)
        else:
            st.error("선택된 맛집 풀이 비어있습니다.")

    st.markdown("<br>### 📋 현재 검색 풀")
    if not filtered_df.empty:
        st.dataframe(filtered_df[["식당명", "지역", "분위기", "대표메뉴", "평균가격"]], use_container_width=True, hide_index=True)
