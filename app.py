import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import os

# 1. ☕ 프리미엄 디자인 보완 테마
st.set_page_config(page_title="서울 감성 맛집 매칭 시스템", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght=0,700&family=Noto+Sans+KR:wght=300;500;700&display=swap');
    .main { background: linear-gradient(135deg, #fdfbf7 0%, #f5efe6 100%); color: #3e362e; }
    * { font-family: 'Noto Sans KR', sans-serif; }
    .gold-title { font-family: 'Playfair Display', sans-serif; font-size: 2.8rem; font-weight: 700; color: #634832; text-align: center; margin-bottom: 5px; }
    .premium-card { background: #ffffff !important; border: 1px solid #dcd1c4 !important; border-radius: 16px !important; padding: 25px !important; box-shadow: 0 10px 30px rgba(99, 72, 50, 0.06) !important; margin-top: 15px; }
    .card-label { font-size: 13px !important; color: #8c7b6e !important; margin-top: 10px !important; font-weight: 500 !important; }
    .card-value { font-size: 16px !important; font-weight: 700 !important; color: #2b241e !important; }
    .roulette-display { font-size: 20px !important; font-weight: 700 !important; color: #8f5b34 !important; text-align: center; background-color: #fcf8f2 !important; padding: 18px !important; border-radius: 12px !important; border: 2px dashed #d1bcac !important; margin: 15px 0 !important; }
    .stButton>button { background: linear-gradient(135deg, #8f5b34 0%, #634832 100%) !important; color: white !important; border-radius: 8px !important; border: none !important; padding: 12px 24px !important; font-size: 16px !important; font-weight: 700 !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="gold-title">SEOUL DINING MATCHER</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8c7b6e; letter-spacing:3px; font-size:0.85rem;">SPATIAL CURATION SYSTEM (100 SELECTS)</p>', unsafe_allow_html=True)

# 2. 📁 외부 데이터 불러오기 안전 처리
txt_file = "restaurants.txt"
if os.path.exists(txt_file):
    df = pd.read_csv(txt_file, encoding="utf-8")
else:
    st.error("⚠️ 폴더에 'restaurants.txt' 파일이 보이지 않습니다. 파일을 꼭 만들어 주세요!")
    st.stop()

neighborhoods = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정"]
vibes = ["#힙한", "#인스타감성", "#미니멀한", "#아늑한", "#전통적인"]

# 3. 🧭 사이드바 필터
st.sidebar.markdown("<h3 style='color:#634832;'>🧭 필터 시스템</h3>", unsafe_allow_html=True)
selected_neighborhoods = st.sidebar.multiselect("📍 행정 구역 선택", options=neighborhoods, default=neighborhoods)
selected_vibes = st.sidebar.multiselect("🎨 공간 무드 선택", options=vibes, default=vibes)
budget = st.sidebar.slider("💰 1인 예산 상한선 (원)", min_value=int(df["평균가격"].min()), max_value=int(df["평균가격"].max()), value=70000, step=1000)

filtered_df = df[(df["지역"].isin(selected_neighborhoods)) & (df["분위기"].isin(selected_vibes)) & (df["평균가격"] <= budget)]

# 4. 🎛️ 메인 레이아웃 구성
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("### 🗺️ 공간 큐레이션 분포 지도")
    if not filtered_df.empty:
        st.map(filtered_df, latitude="lat", longitude="lon", zoom=11)
    else:
        st.error("설정하신 필터 조건에 부합하는 공간이 존재하지 않습니다.")

    st.markdown("### 📊 다이닝 가치 분석 (분포도)")
    if not filtered_df.empty:
        fig = px.scatter(filtered_df, x="지역", y="평균가격", color="분위기", size="평균가격", hover_data=["식당명", "대표메뉴"], labels={"평균가격": "가격대 (원)", "지역": "로케이션"}, template="plotly_dark")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#3e362e"))
        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.markdown("### 🎰 감성 맛집 추천 룰렛")
    roulette_placeholder = st.empty()
    result_placeholder = st.empty()
    
    if st.button("🎲 맛집 룰렛 돌리기"):
        if not filtered_df.empty:
            result_placeholder.empty()
            duration = 1.8
            start_time = time.time()
            all_matching_names = filtered_df["식당명"].tolist()
            
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                wait_time = 0.05 + (elapsed / duration) ** 2 * 0.15
                temp_name = random.choice(all_matching_names)
                roulette_placeholder.html(f'<div class="roulette-display">🔄 탐색 중... [ {temp_name} ]</div>')
                time.sleep(wait_time)
            
            roulette_placeholder.empty()
            random_pick = filtered_df.sample(n=1).iloc[0]
            
            card_html = f"""
            <div class="premium-card">
                <h3 style="margin-top:0; color:#8f5b34 !important; font-size:22px; font-weight:700;">🍷 매칭 공간: {random_pick['식당명']}</h3>
                <hr style="border-top: 1px solid #dcd1c4; margin:12px 0;">
                <div class="card-label">📍 로케이션</div><div class="card-value">{random_pick['지역']}</div>
                <div class="card-label">✨ 공간 분위기</div><div class="card-value" style="color:#b57c4a !important;">{random_pick['분위기']}</div>
                <div class="card-label">🍽️ 시그니처 다이닝 메뉴</div><div class="card-value">{random_pick['대표메뉴']}</div>
                <div class="card-label">💰 평균 예산</div><div class="card-value" style="font-size:18px; color:#3e362e;">₩{random_pick['평균가격']:,}원</div>
            </div>
            """
            result_placeholder.html(card_html)
        else:
            st.error("매칭 풀이 비어있습니다. 필터를 조정해 주세요.")

    st.markdown("<br>### 📋 분석 매칭 풀 (Pool)")
    st.markdown(f"분석 대상 맛집: **{len(filtered_df)}**개 개방됨")
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df["평균가격"] = display_df["평균가격"].map("{:,}원".format)
        st.dataframe(display_df[["식당명", "지역", "분위기", "대표메뉴", "평균가격"]], use_container_width=True, hide_index=True)
