import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# ==========================================
# 1. 🤎 고급스러운 딥 브라운 그라데이션 테마
# ==========================================
st.set_page_config(page_title="서울 분위기 맛집 매칭 시스템", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Noto+Sans+KR:wght@300;500;700&display=swap');
    
    .main { 
        background: linear-gradient(135deg, #121214 0%, #1e1b18 100%); 
        color: #f4f4f6; 
    }
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .gold-title {
        font-family: 'Playfair Display', 'Noto Sans KR', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #d4af37;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }
    .sub-text {
        text-align: center;
        color: #bfae9e;
        font-size: 0.95rem;
        letter-spacing: 3px;
        margin-bottom: 40px;
    }
    
    .premium-card {
        background: #1f1e22;
        border: 2px solid #d4af37;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        color: #f4f4f6 !important;
    }
    
    .card-label {
        font-size: 14px;
        color: #a3a19a;
        margin-bottom: 2px;
        margin-top: 10px;
    }
    .card-value {
        font-size: 17px;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 10px;
    }
    
    .roulette-display {
        font-size: 22px;
        font-weight: 700;
        color: #d4af37;
        text-align: center;
        background-color: #262429;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #4a4335;
        margin: 15px 0;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa841c 100%) !important;
        color: #121214 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #f3cd57 0%, #d4af37 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="gold-title">SEOUL VIBE MATCHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">BIG DATA BASED SPATIAL CURATION SYSTEM</p>', unsafe_allow_html=True)

# ==========================================
# 2. 📊 서울 핵심 맛집 데이터셋 (100개)
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
    ("성수연방", "성수", "#인스타감성", "천상 가옥 베이커리", 7000, 37.5440, 127.0600),
    ("밀도 성수점", "성수", "#미니멀한", "담백식빵", 6500, 37.5472, 127.0441),
    ("소바식당", "성수", "#아늑한", "전복 한우육회 소바", 15000, 37.5455, 127.0528),
    ("핑거팁스", "성수", "#힙한", "수제 수제버거", 11500, 37.5419, 127.0511),
    ("eert 성수", "성수", "#전통적인", "박스 박스차", 8500, 37.5482, 127.0430),
    ("쵸이다이닝 성수", "성수", "#힙한", "연어 후토마끼", 22000, 37.5438, 127.0549),
    ("누메로도스", "성수", "#아늑한", "마스카포네 피자", 19000, 37.5468, 127.0477),
    ("오레노카츠 성수", "성수", "#인스타감성", "체다치즈 돈카츠", 13500, 37.5429, 127.0538),
    ("뚝떡", "성수", "#힙한", "치즈 부추 떡볶이", 7500, 37.5461, 127.0412),

    # 한남 (20개)
    ("한남 오아시스", "한남", "#미니멀한", "아보카도 토스트", 19000, 37.5340, 127.0026),
    ("닷츠 (DOTZ)", "한남", "#인스타감성", "카츠산도", 22000, 37.5362, 127.0011),
    ("파이프그라운드", "한남", "#힙한", "옥수수 피자", 24000, 37.5381, 126.9992),
    ("바 위스퍼", "한남", "#힙한", "내추럴 와인", 38000, 37.5315, 127.0055),
    ("뮤트커피", "한남", "#아늑한", "플랫화이트", 7000, 37.5322, 127.0080),
    ("다운타운너 한남", "한남", "#힙한", "아보카도버거", 11500, 37.5350, 126.9985),
    ("부자피자 1호점", "한남", "#아늑한", "마르게리따 피자", 26000, 37.5375, 127.0035),
    ("한남 한방통닭", "한남", "#전통적인", "한방통닭구이", 21000, 37.5330, 127.0060),
    ("리틀넥 한남", "한남", "#인스타감성", "명란크림파스타", 18000, 37.5368, 127.0005),
    ("베이비칙 한남", "한남", "#인스타감성", "로제 떡볶이", 16500, 37.5390, 127.0019),
    ("올드페리도넛", "한남", "#힙한", "피넛버터 도넛", 5500, 37.5372, 127.0010),
    ("사운즈한남 일호식", "한남", "#미니멀한", "제철 생선구이 정식", 19500, 37.5345, 127.0072),
    ("세컨드키친", "한남", "#미니멀한", "런치 다이닝 코스", 45000, 37.5332, 127.0065),
    ("콘하스 한남", "한남", "#미니멀한", "바닐라라떼 & 브런치", 9000, 37.5360, 127.0020),
    ("라라브레드 한남", "한남", "#아늑한", "쫄깃식빵 & 잼", 5000, 37.5329, 127.0091),
    ("마일스톤 커피
