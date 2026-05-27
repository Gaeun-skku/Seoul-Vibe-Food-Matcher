import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# ==========================================
# 1. 🤎 모던 럭셔리 다크 & 골드 테마 (네온 제거)
# ==========================================
st.set_page_config(page_title="서울 분위기 맛집 매칭 시스템", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Noto+Sans+KR:wght@300;500;700&display=swap');
    
    /* 네온을 제거하고 차분한 브라운/차콜 계열 배경 적용 */
    .main { background-color: #121214; color: #e8e6e3; }
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 타이틀: 고풍스럽고 세련된 세리프 서체와 골드 컬러 */
    .gold-title {
        font-family: 'Playfair Display', 'Noto Sans KR', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #d4af37;
        text-align: center;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #a3a3a6;
        font-size: 1rem;
        letter-spacing: 2px;
        margin-bottom: 35px;
    }
    
    /* 미니멀하고 고급스러운 카드 디자인 */
    .premium-card {
        background-color: #1a1a1e;
        border: 1px solid #383223;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* 룰렛 연출용 텍스트 박스 */
    .roulette-display {
        font-size: 22px;
        font-weight: 700;
        color: #d4af37;
        text-align: center;
        background-color: #1a1a1e;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333;
        margin: 10px 0;
    }
    
    /* 클래식한 버튼 스타일 */
    .stButton>button {
        background: #d4af37 !important;
        color: #121214 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #f3cd57 !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더 영역
st.markdown('<h1 class="gold-title">SEOUL VIBE MATCHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">BIG DATA BASED SPATIAL CURATION SYSTEM</p>', unsafe_allow_html=True)

# ==========================================
# 2. 📊 서울 핵심 맛집 데이터셋 (정확히 100개 검수 완료)
# ==========================================
neighborhoods = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정"]
vibes = ["#힙한", "#인스타감성", "#미니멀한", "#아늑한", "#전통적인"]

raw_spots = [
    # 성수 (20개)
    ("성수 미오", "성수", "#인스타감성", "트러플 파스타", 23000, 37.5446, 127.0560),
    ("할아버지공장", "성수", "#미니멀한", "콜드브루 & 팡도르", 8000, 37.5412, 127.0541),
    ("중앙감속기", "성수", "#힙한", "바질조개찜", 28000, 37.5430, 127.0512),
    ("소문난성수감자탕", "성수", "#아늑한", "감자탕", 11000, 37.5427, 127.0544),
    ("제스티살룬 성수", "성수", "#힙한", "와사비 쉬림프버거", 14000, 37.5460, 127.0495),
    ("대림창고", "성수", "#힙한", "아인슈페너", 7500, 37.5405, 127.0530),
    ("성수다락", "성수", "#인스타감성", "매콤크림파스타", 22000, 37.5452, 127.0522),
    ("난포 성수", "성수", "#아늑한", "강된장쌈밥", 16000, 37.5480, 127.0465),
    ("보울룸 성수", "성수", "#미니멀한", "연어 포케", 13000, 37.5435, 127.0570),
    ("로우키 성수", "성수", "#미니멀한", "필터 커피", 6000, 37.5421, 127.0555),
    ("소문난식당", "성수", "#아늑한", "묵은지 고등어조림", 10000, 37.5410, 127.0580),
    ("성수연방", "성수", "#인스타감성", "천상 가옥 베이커리",
