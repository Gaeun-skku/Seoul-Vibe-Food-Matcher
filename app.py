import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# ==========================================
# 1. ☕ 따뜻한 크림&우드 미식 테마 디자인
# ==========================================
st.set_page_config(page_title="서울 감성 맛집 매칭 시스템", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Noto+Sans+KR:wght@300;500;700&display=swap');
    
    /* 음식과 잘 어울리는 따뜻한 웜톤 배경 */
    .main { 
        background: linear-gradient(135deg, #fdfbf7 0%, #f5efe6 100%); 
        color: #3e362e; 
    }
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 고급스러운 브라운 타이틀 */
    .gold-title {
        font-family: 'Playfair Display', 'Noto Sans KR', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #634832;
        text-align: center;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #8c7b6e;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }
    
    /* 추천 결과 카드 - 네온을 빼고 따뜻하고 아늑한 베이지 베이스 */
    .premium-card {
        background: #ffffff;
        border: 1px solid #dcd1c4;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(99, 72, 50, 0.08);
        color: #3e362e !important;
    }
    
    .card-label {
        font-size: 14px;
        color: #8c7b6e;
        margin-bottom: 2px;
        margin-top: 12px;
        font-weight: 500;
    }
    .card-value {
        font-size: 17px;
        font-weight: 700;
        color: #2b241e;
        margin-bottom: 12px;
    }
    
    /* 🎰 [가독성 개선] 검정 배경 탈피, 밝고 선명한 베이지&따뜻한 오렌지 폰트 */
    .roulette-display {
        font-size: 22px;
        font-weight: 700;
        color: #8f5b34;
        text-align: center;
        background-color: #fcf8f2;
        padding: 20px;
        border-radius: 12px;
        border: 2px dashed #d1bcac;
        margin: 15px 0;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.03);
    }
    
    /* 따뜻한 다이닝 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #8f5b34 0%, #634832 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100%;
        box-shadow: 0 4px 12px rgba(143, 91, 52, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a66f46 0%, #8f5b34 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(143, 91, 52, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="gold-title">SEOUL DINING MATCHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">SPATIAL CURATION SYSTEM</p>', unsafe_allow_html=True)

# ==========================================
# 2. 📊 서울 핫플레이스 데이터셋 (정밀 검수 완료된 150개)
# ==========================================
neighborhoods = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정"]
vibes = ["#힙한", "#인스타감성", "#미니멀한", "#아늑한", "#전통적인"]

raw_spots = [
    # 성수 (30개)
    ("성수 미오", "성수", "#인스타감성", "트러플 파스타", 23000, 37.5446, 127.0560),
    ("할아버지공장", "성수", "#미니멀한", "소갈비찜 다이닝", 25000, 37.5412, 127.0541),
    ("중앙감속기", "성수", "#힙한", "바질조개찜", 28000, 37.5430, 127.0512),
    ("소문난성수감자탕", "성수", "#아늑한", "감자탕", 11000, 37.5427, 127.0544),
    ("제스티살룬 성수", "성수", "#힙한", "와사비 쉬림프버거", 14000, 37.5460, 127.0495),
    ("대림창고", "성수", "#힙한", "아인슈페너 & 브런치", 15000, 37.5405, 127.0530),
    ("성수다락", "성수", "#인스타감성", "매콤크림파스타", 22000, 37.5452, 127.0522),
    ("난포 성수", "성수", "#아늑한", "강된장쌈밥", 16000, 37.5480, 127.0465),
    ("보울룸 성수", "성수", "#미니멀한", "연어 포케", 13000, 37.5435, 127.0570),
    ("로우키 성수", "성수", "#미니멀한", "필터 커피 & 디저트", 9000, 37.5421, 127.0555),
    ("소문난식당", "성수", "#아늑한", "묵은지 고등어조림", 10000, 37.5410, 127.0580),
    ("성수연방 천상가옥", "성수", "#인스타감성", "베이커리 플레이트", 12000, 37.5440, 127.0600),
    ("밀도 성수점", "성수", "#미니멀한", "담백식빵 & 스프", 9500, 37.5472, 127.0441),
    ("소바식당", "성수", "#아늑한", "전복 한우육회 소바", 15000, 37.5455, 127.0528),
    ("핑거팁스", "성수", "#힙한", "수제 버거 세트", 14500, 37.5419, 127.0511),
    ("eert 성수", "성수", "#전통적인", "3단 디저트 박스", 24000, 37.5482, 127.0430),
    ("쵸이다이닝 성수", "성수", "#힙한", "연어 후토마끼", 22000, 37.5438, 127.0549),
    ("누메로도스", "성수", "#아늑한", "마스카포네 피자", 19000, 37.5468, 127.0477),
    ("오레노카츠 성수", "성수", "#인스타감성", "체다치즈 돈카츠", 13500, 37.5429, 127.0538),
    ("뚝떡", "성수", "#힙한", "치즈 부추 떡볶이", 7500, 37.5461, 127.0412),
    ("조이어스 자이로", "성수", "#미니멀한", "그릭 기로스 랩", 11000, 37.5433, 127.0550),
    ("피자시즌", "성수", "#인스타감성", "하프앤하프 피자", 21000, 37.5445, 127.0573),
    ("와하카", "성수", "#힙한", "엔칠라다", 14000, 37.5415, 127.0520),
    ("까망", "성수", "#아늑한", "가지소고기파스타", 16000, 37.5465, 127.0425),
    ("치차로", "성수", "#힙한", "스페인 타파스", 24000, 37.5450, 127.0510),
    ("쿠나 (KUNA)", "성수", "#
