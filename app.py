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
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght=0,700;1,400&family=Noto+Sans+KR:wght=300;500;700&display=swap');
    
    .main { 
        background: linear-gradient(135deg, #fdfbf7 0%, #f5efe6 100%); 
        color: #3e362e; 
    }
    * { font-family: 'Noto Sans KR', sans-serif; }
    
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
    
    .premium-card {
        background: #ffffff !important;
        border: 1px solid #dcd1c4 !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(99, 72, 50, 0.08) !important;
        color: #3e362e !important;
        margin-top: 15px;
    }
    
    .card-label {
        font-size: 14px !important;
        color: #8c7b6e !important;
        margin-bottom: 2px !important;
        margin-top: 12px !important;
        font-weight: 500 !important;
    }
    .card-value {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #2b241e !important;
        margin-bottom: 12px !important;
    }
    
    .roulette-display {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #8f5b34 !important;
        text-align: center !important;
        background-color: #fcf8f2 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 2px dashed #d1bcac !important;
        margin: 15px 0 !important;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.03) !important;
    }
    
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
# 2. 📊 서울 핫플레이스 데이터셋 (세로 줄바꿈 가공)
# ==========================================
neighborhoods = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정"]
vibes = ["#힙한", "#인스타감성", "#미니멀한", "#아늑한", "#전통적인"]

spots_data = [
    # 성수
    {
        "식당명": "성수 미오", "지역": "성수", "분위기": "#인스타감성", 
        "대표메뉴": "트러플 파스타", "평균가격": 23000, "lat": 37.5446, "lon": 127.0560
    },
    {
        "식당명": "할아버지공장", "지역": "성수", "분위기": "#미니멀한", 
        "대표메뉴": "소갈비찜 다이닝", "평균가격": 25000, "lat": 37.5412, "lon": 127.0541
    },
    {
        "식당명": "중앙감속기", "지역": "성수", "분위기": "#힙한", 
        "대표메뉴": "바질조개찜", "평균가격": 28000, "lat": 37.5430, "lon": 127.0512
    },
    {
        "식당명": "소문난성수감자탕", "지역": "성수", "분위기": "#아늑한", 
        "대표메뉴": "감자탕", "평균가격": 11000, "lat": 37.5427, "lon": 127.0544
    },
    {
        "식당명": "제스티살룬 성수", "지역": "성수", "분위기": "#힙한", 
        "대표메뉴": "와사비 쉬림프버거", "평균가격": 14000, "lat": 37.5460, "lon": 127.0495
    },
    {
        "식당명": "난포 성수", "지역": "성수", "분위기": "#아늑한", 
        "대표메뉴": "강된장쌈밥", "평균가격": 16000, "lat": 37.5480, "lon": 127.0465
    },
    {
        "식당명": "eert 성수", "지역": "성수", "분위기": "#전통적인", 
        "대표메뉴": "3단 디저트 박스", "평균가격": 24000, "lat": 37.5482, "lon": 127.0430
    },

    # 한남
    {
        "식당명": "한남 오아시스", "지역": "한남", "분위기": "#미니멀한", 
        "대표메뉴": "아보카도 토스트", "평균가격": 19000, "lat": 37.5340, "lon": 127.0026
    },
    {
        "식당명": "닷츠 (DOTZ)", "지역": "한남", "분위기": "#인스타감성", 
        "대표메뉴": "카츠산도", "평균가격": 22000, "lat": 37.5362, "lon": 127.0011
    },
    {
        "식당명": "파이프그라운드", "지역": "한남", "분위기": "#힙한", 
        "대표메뉴": "옥수수 피자", "평균가격": 24000, "lat": 37.5381, "lon": 126.9992
    },
    {
        "식당명": "한남 한방통닭", "지역": "한남", "분위기": "#전통적인", 
        "대표메뉴": "한방통닭구이", "평균가격": 21000, "lat": 37.5330, "lon": 127.0060
    },
    {
        "식당명": "부자피자 1호점", "지역": "한남", "분위기": "#아늑한", 
        "대표메뉴": "마르게리따 피자", "평균가격": 26000, "lat": 37.5375, "lon": 127.0035
    },
    {
        "식당명": "소와나", "지역": "한남", "분위기": "#미니멀한", 
        "대표메뉴": "한우 오마카세", "평균가격": 69000, "lat": 37.5359, "lon": 126.9975
    },

    # 홍대/연남
    {
        "식당명": "홍대 네온펍", "지역": "홍대/연남", "분위기": "#힙한", 
        "대표메뉴": "수제맥주 & 플래터", "평균가격": 16000, "lat": 37.5565, "lon": 126.9239
    },
    {
        "식당명": "연남 연하동", "지역": "홍대/연남", "분위기": "#인스타감성", 
        "대표메뉴": "대왕후토마끼", "평균가격": 28000, "lat": 37.5610, "lon": 126.9245
    },
    {
        "식당명": "감칠 연남", "지역": "홍대/연남", "분위기": "#아늑한", 
        "대표메뉴": "달래된장크림파스타", "평균가격": 17000, "lat": 37.5622, "lon": 126.9270
    },
    {
        "식당명": "오레노라멘", "지역": "홍대/연남", "분위기": "#미니멀한", 
        "대표메뉴": "토리빠이탄 라멘", "평균가격": 11000, "lat": 37.5525, "lon": 126.9205
    },
    {
        "식당명": "연남동 감나무집", "지역": "홍대/연남", "분위기": "#전통적인", 
        "대표메뉴": "돼지불백 정식", "평균가격": 10000, "lat": 37.5635, "lon": 126.9189
    },

    # 익선동
    {
        "식당명": "익선반주", "지역": "익선동", "분위기": "#힙한", 
        "대표메뉴": "깻잎크림뇨끼", "평균가격": 21000, "lat": 37.5744, "lon": 126.9890
    },
    {
        "식당명": "살라댕방콕", "지역": "익선동", "분위기": "#인스타감성", 
        "대표메뉴": "푸팟퐁커리 메인", "평균가격": 32000, "lat": 37.5732, "lon": 126.9899
    },
    {
        "식당명": "청수당", "지역": "익선동", "분위기": "#전통적인", 
        "대표메뉴": "말차 타르트 디저트", "평균가격": 15500, "lat": 37.5748, "lon": 126.9885
    },
    {
        "식당명": "창화당 익선점", "지역": "익선동", "분위기": "#아늑한", 
        "대표메뉴": "모둠 지짐만두", "평균가격": 9500, "lat": 37.5739, "lon": 126.9880
    },
    {
        "식당명": "밀토스트", "지역": "익선동", "분위기": "#미니멀한", 
        "대표메뉴": "스팀 수플레 식빵", "평균가격": 13000, "lat": 37.5746, "lon": 126.9895
    },

    # 강남/압구정
    {
        "식당명": "강남 미트테일러", "지역": "강남/압구정", "분위기": "#미니멀한", 
        "대표메뉴": "프리미엄 티본 스테이크", "평균가격": 55000, "lat": 37.4980, "lon": 127.0280
    },
    {
        "식당명": "압구정 자유피자", "지역": "강남/압구정", "분위기": "#힙한", 
        "대표메뉴": "트러フル 머쉬룸 피자", "평균가격": 18000, "lat": 37.5245, "lon": 127.0372
    },
    {
        "식당명": "스케줄청담", "지역": "강남/압구정", "분위기": "#인스타감성", 
        "대표메뉴": "블랙트러플 크림리조또", "평균가격": 33000, "lat": 37.5252, "lon": 127.0410
    },
    {
        "식당명": "땀땀 강남", "지역": "강남/압구정", "분위기": "#아늑한", 
        "대표메뉴": "매운 소곱창 쌀국수", "평균가격": 15000, "lat": 37.4992, "lon": 127.0264
    },
    {
        "식당명": "새마을식당 강남역점", "지역": "강남/압구정", "분위기": "#전통적인", 
        "대표메뉴": "매콤 열탄불고기 2인", "평균가격": 20000, "lat": 37.4990, "lon": 127.0285
    }
]

df = pd.DataFrame(spots_data)

# ==========================================
# 3. 🧭 사이드바 조절 필터
# ==========================================
st.sidebar.markdown("<h3 style='color:#634832 !important;'>🧭 조건별 탐색</h3>", unsafe_allow_html=True)

selected_neighborhoods = st.sidebar.multiselect("📍 행정 구역 선택", options=neighborhoods, default=neighborhoods)
selected_vibes = st.sidebar.multiselect("🎨 공간 무드 선택", options=vibes, default=vibes)

max_price = int(df["평균가격"].max())
min_price = int(df["평균가격"].min())
budget = st.sidebar.slider("💰 1인 예산 상한선 (원)", min_value=min_price, max_value=max_price, value=70000, step=1000)

filtered_df = df[
    (df["지역"].isin(selected_neighborhoods)) & 
    (df["분위기"].
