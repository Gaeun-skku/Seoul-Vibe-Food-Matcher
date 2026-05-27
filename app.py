import streamlit as st
import pandas as pd
import plotly.express as px
import random

# ==========================================
# 1. 페이지 설정 및 사이버펑크/네온 스타일 주입
# ==========================================
st.set_page_config(page_title="서울 분위기 맛집 매칭", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .main { background-color: #0b0c10; }
    h1 { color: #00ffcc !important; text-shadow: 0 0 15px #00ffcc; font-weight: 700; text-align: center; }
    h2, h3 { color: #ff007f !important; text-shadow: 0 0 5px rgba(255,0,127,0.5); }
    .stButton>button {
        background: linear-gradient(45deg, #ff007f, #7928ca) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 10px 25px !important;
        box-shadow: 0 0 20px #ff007f;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px #00ffcc;
    }
    .card {
        background: linear-gradient(135deg, #1f1f2e, #11111b);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #ff007f;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 서울 분위기별 맛集 매칭 대시보드")
st.markdown("<p style='text-align: center; color: #8892b0; font-size: 16px;'>빅데이터와 공간 미학의 만남 | 성균관대학교 무용학과 최가은 기말 프로젝트</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 2. 촘촘하게 보강된 서울 핵심 맛집 데이터 (총 50개)
# ==========================================
data = {
    "식당명": [
        # 성수 (10개)
        "성수 미오", "할아버지공장", "중앙감속기", "소문난성수감자탕", "제스티살룬 성수",
        "대림창고", "성수다락", "난포 성수", "보울룸 성수", "로우키 성수",
        # 한남 (10개)
        "한남 오아시스", "닷츠 (DOTZ)", "파이프그라운드", "바 위스퍼", "뮤트커피",
        "다운타운너 한남", "부자피자 1호점", "한남 한방통닭", "리틀넥 한남", "베이비칙 한남",
        # 홍대/연남 (10개)
        "홍대 네온펍", "연남 연하동", "감칠 연남", "티앤프루프", "오레노라멘",
        "연남동 테일러커피", "소이연남", "하쿠텐라멘", "바다회사랑", "연남 취향",
        # 익선동 (10개)
        "익선반주", "살라댕방콕", "청수당", "온천집", "뜰안 전통찻집",
        "창화당 익선점", "밀토스트", "익선동 열두달", "송암여관", "지오쿠치나 익선",
        # 강남/압구정 (10개)
        "강남 미트테일러", "압구정 클랩피자", "스케줄청담", "먼데이투썬데이", "땀땀 강남",
        "미즈컨테이너 강남", "바빌론 스테이크", "새벽집 청담", "도산맘마", "카멜커피 도산"
    ],
    "지역": [
        "성수", "성수", "성수", "성수", "성수", "성수", "성수", "성수", "성수", "성수",
        "한남", "한남", "한남", "한남", "한남", "한남", "한남", "한남", "한남", "한남",
        "홍대", "홍대", "홍대", "홍대", "홍대", "홍대", "홍대", "홍대", "홍대", "홍대",
        "익선동", "익선동", "익선동", "익선동", "익선동", "익선동", "익선동", "익선동", "익선동", "익선동",
        "강남", "강남", "강남", "강남", "강남", "강남", "강남", "강남", "강남", "강남"
    ],
    "분위기": [
        "#인스타감성", "#미니멀한", "#힙한", "#아늑한", "#힙한", "#힙한", "#인스타감성", "#아늑한", "#미니멀한", "#미니멀한",
        "#미니멀한", "#인스타감성", "#힙한", "#힙한", "#아늑한", "#힙한", "#아늑한", "#전통적인", "#인스타감성", "#인스타감성",
        "#힙한", "#인스타감성", "#아늑한", "#힙한", "#미니멀한", "#미니멀한", "#힙한", "#아늑한", "#힙한", "#인스타감성",
        "#힙한", "#인스타감성", "#전통적인", "#전통적인", "#전통적인", "#아늑한", "#미니멀한", "#전통적인", "#전통적인", "#인스타감성",
        "#미니멀한", "#힙한", "#인스타감성", "#인스타감성", "#아늑한", "#힙한", "#미니멀한", "#아늑한", "#인스타감성", "#미니멀한"
    ],
    "대표메뉴": [
        "트러플 파스타", "콜드브루 & 팡도르", "바질조개찜", "감자탕", "와사비 쉬림프버거", "아인슈페너", "매콤크림파스타", "강된장쌈밥", "연어 포케", "필터 커피",
        "아보카도 토스트", "카츠산도", "옥수수 피자", "내추럴 와인", "플랫화이트", "아보카도버거", "마르게리따 피자", "한방통닭구이", "명란크림파스타", "로제 떡볶이",
        "수제맥주 & 플래터", "대왕후토마끼", "달래된장크림파스타", "시그니처 칵테일", "토리빠이탄 라멘", "크림모카", "소고기 쌀국수", "돈코츠 라멘", "대방어 회", "항정살 매콤크림파스타",
        "깻잎크림뇨끼", "푸팟퐁커리", "말차 타르트 & 드립커피", "1인 샤브샤브", "쌍화차 & 한과", "모둠만두", "수플레 식빵", "연잎밥 정식", "대창 덮밥", "고르곤졸라 피자",
        "티본 스테이크", "트러플 머쉬룸 피자", "블랙트러플 크림리조또", "크로플 & 아메리카노", "매운 소곱창쌀국수", "샐러드 스파게티", "안심 스테이크", "육회비빔밥", "도산 맘마미아 디저트", "카멜커피"
    ],
    "평균가격": [
        23000, 8000, 28000, 11000, 14000, 7500, 22000, 16000, 13000, 6000,
        19000, 22000, 24000, 38000, 7000, 11500, 26000, 21000, 18000, 16500,
        16000, 28000, 17000, 20000, 11000, 6500, 12000, 10000, 35000, 17000,
        21000, 32000, 9500, 26000, 8000, 8500, 13000, 18500, 15000, 24000,
        55000, 18000, 33000, 12000, 15000, 16500, 48000, 19000, 14000, 6000
    ],
    # 정밀 매핑을 위한 좌표값 분산 보정
    "lat": [
        37.5446, 37.5412, 37.5430, 37.5427, 37.5460, 37.5405, 37.5452, 37.5480, 37.5435, 37.5421,
        37.5340, 37.5362, 37.5381, 37.5315, 37.5322, 37.5350, 37.5375, 37.5330, 37.5368, 37.5390,
        37.5565, 37.5610, 37.5622, 37.5540, 37.5525, 37.5585, 37.5590, 37.5570, 37.5550, 37.5605,
        37.5744, 37.5732, 37.5748, 37.5750, 37.5741, 37.5739, 37.5746, 37.5752, 37.5755, 37.5735,
        37.4980, 37.5245, 37.5252, 37.5230, 37.4992, 37.4988, 37.5010, 37.5240, 37.5260, 37.5225
    ],
    "lon": [
        127.0560, 127.0541, 127.0512, 127.0544, 127.0495, 127.0530, 127.0522, 127.0465, 127.0570, 127.0555,
        127.0026, 127.0011, 126.9992, 127.0055, 127.0080, 126.9985, 127.0035, 127.0060, 127.0005, 127.0019,
        126.9239, 126.9245, 126.9270, 126.9212, 126.9205, 126.9260, 126.9220, 126.9250, 126.9195, 126.9280,
        126.9890, 126.9899, 126.9885, 126.9882, 126.9875, 126.9880, 126.9895, 126.9868, 126.9860, 126.9905,
        127.0280, 127.0372, 127.0410, 127.0435, 127.0264, 127.0275, 127.0250, 127.0420, 127.0395, 127.0380
    ]
}

df = pd.DataFrame(data)

# ==========================================
# 3. 사이드바 필터 제어 패널
# ==========================================
st.sidebar.markdown("<h2 style='color:#00ffcc !important;'>🧭 취향 필터링</h2>", unsafe_allow_html=True)

# 지역 선택
all_neighborhoods = df["지역"].unique().tolist()
selected_neighborhoods = st.sidebar.multiselect(
    "원하는 탐색 지역을 선택하세요 (중복 가능)", 
    options=all_neighborhoods, 
    default=all_neighborhoods
)

# 분위기 선택
all_vibes = df["분위기"].unique().tolist()
selected_vibes = st.sidebar.multiselect(
    "원하는 공간 분위기를 선택하세요", 
    options=all_vibes, 
    default=all_vibes
)

# 예산 제한 슬라이더
max_price = int(df["평균가격"].max())
min_price = int(df["평균가격"].min())
budget = st.sidebar.slider(
    "1인당 최대 허용 예산 (원)", 
    min_value=min_price, 
    max_value=max_price, 
    value=max_price,
    step=1000
)

# 데이터 필터링 실행
filtered_df = df[
    (df["지역"].isin(selected_neighborhoods)) & 
    (df["분위기"].isin(selected_vibes)) &
    (df["평균가격"] <= budget)
]

# ==========================================
# 4. 메인 대시보드 화면 구성 (좌/우 2단 배치)
# ==========================================
left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("🗺️ 핫플레이스 분위기 지도")
    if not filtered_df.empty:
        st.map(filtered_df, latitude="lat", longitude="lon", zoom=12)
    else:
        st.error("선택한 조건에 맞는 식당이 없습니다. 필터를 조정해 주세요!")

    st.subheader("📊 지역별 분위기 및 평균 가격 비교")
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df, 
            x="지역", 
            y="평균가격", 
            color="분위기",
            hover_data=["식당명", "대표메뉴"],
            barmode="group",
            title="조건에 맞는 식당들의 지역별 예산 분포",
            labels={"평균가격": "평균 가격 (원)", "지역": "지역 구분"},
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("🎰 분위기 맛집 룰렛")
    st.write("메뉴 결정이 어려우신가요? 필터 조건에 맞춰 오늘의 최적 공간을 추천해 드립니다.")
    
    if st.button("🔮 오늘 어디서 뭐 먹지? 버튼 클릭!"):
        if not filtered_df.empty:
            random_pick = filtered_df.sample(n=1).iloc[0]
            st.balloons() 
            
            st.markdown(f"""
            <div class="card">
                <h3 style="margin-top:0; color:#00ffcc !important; font-size:24px;">✨ 오늘의 추천: {random_pick['식당명']}</h3>
                <hr style="border-color:#ff007f;">
                <p style="font-size:16px;"><b>📍 위치:</b> {random_pick['지역']}</p>
                <p style="font-size:16px;"><b>🎨 공간 감성:</b> <span style="color:#ff007f; font-weight:bold;">{random_pick['분위기']}</span></p>
                <p style="font-size:16px;"><b>🍽️ 시그니처 메뉴:</b> {random_pick['대표메뉴']}</p>
                <p style="font-size:18px; color:#00ffcc;"><b>💰 평균 가격:</b> {random_pick['평균가격']:,}원</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("필터 조건에 맞는 맛집이 없어 룰렛을 돌릴 수 없습니다!")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("📋 매칭된 식당 리스트")
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df["평균가격"] = display_df["평균가격"].map("{:,}원".format)
        st.dataframe(
            display_df[["식당명", "지역", "분위기", "대표메뉴", "평균가격"]], 
            use_container_width=True,
            hide_index=True
        )
