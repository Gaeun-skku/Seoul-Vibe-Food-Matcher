import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# ==========================================
# 1. ⚡️ 유니크 & 크레이지 네온 사이버펑크 스타일 시트 (UI 대변신)
# ==========================================
st.set_page_config(page_title="서울 분위기 맛집 매칭 2.0", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Noto+Sans+KR:wght@300;700&display=swap');
    
    /* 전체 배경을 딥블랙으로, 폰트를 감각적으로 조정 */
    .main { background-color: #050508; color: #e2e8f0; }
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 타이틀에 움직이는 네온 광선 효과 */
    .neon-title {
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00ffcc;
        text-align: center;
        text-shadow: 0 0 10px #00ffcc, 0 0 30px #00ffcc, 0 0 50px #ff007f;
        animation: blink 2s infinite alternate;
        margin-bottom: 5px;
    }
    
    /* 무용과 가은 님만의 서브타이틀 스타일 */
    .dance-sub {
        text-align: center;
        color: #ff007f;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 3px;
        text-shadow: 0 0 8px #ff007f;
        margin-bottom: 30px;
    }
    
    /* 아주 유니크한 네온 카드 스타일 */
    .vibe-card {
        background: linear-gradient(135deg, #11111b 0%, #0c0c14 100%);
        border: 2px dashed #00ffcc;
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.2);
        transition: all 0.5s ease;
    }
    
    /* 대형 룰렛 버튼 커스텀 */
    .stButton>button {
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 50%, #00ffcc 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.6);
        cursor: pointer;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.03) rotate(-1deg);
        box-shadow: 0 0 40px #00ffcc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 화려한 웰컴 헤더
st.markdown('<h1 class="neon-title">SEOUL VIBE MATCHER 2.0</h1>', unsafe_allow_html=True)
st.markdown('<p class="dance-sub">BIG DATA X SPATIAL AESTHETICS — BY GAEUN CHOE</p>', unsafe_allow_html=True)

# ==========================================
# 2. 📊 100+ 매머드급 실제&감성 서울 맛집 데이터셋 구축
# ==========================================
# 데이터 개수를 정확히 100개로 꽉 채웠습니다. 각 지역별 20개씩 밸런스를 맞췄습니다.
neighborhoods = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정"]
vibes =
