import streamlit as st
import pandas as pd
import random

# 1. 페이지 기본 설정 및 디자인 (다크/네온 미학 반영)
st.set_page_config(page_title="Seoul Vibe Food Matcher", layout="wide")

# 가은 님의 전공을 녹여낸 멋진 상단 타이틀
st.title("🎬 Seoul \"Vibe\" Food Matcher")
st.caption("A Spatial & Aesthetic Dining Guide by Gaeun Choe (Dance Major, SKKU)")
st.markdown("---")

# 2. 가짜 데이터셋 (CSV 파일을 대신할 프로토타입 데이터)
# 서울의 핫플레이스 식당 10곳의 데이터입니다.
data = {
    "Restaurant": [
        "Seongsu Pastamio", "Hannam Oasis", "Hongdae Neon Pub", 
        "Ikseon Hanok Tea", "Gangnam Bistro", "Seongsu Wood Studio", 
        "Hannam Soundbar", "Yeonnam Coziness", "Apgujeong Glam", "Euljiro Vintage"
    ],
    "Neighborhood": [
        "Seongsu", "Hannam", "Hongdae", 
        "Ikseon-dong", "Gangnam", "Seongsu", 
        "Hannam", "Hongdae", "Apgujeong", "Euljiro"
    ],
    "Vibe": [
        "#Instagrammable", "#Minimalist", "#Hip", 
        "#Traditional", "#Cozy", "#Minimalist", 
        "#Hip", "#Cozy", "#Instagrammable", "#Hip"
    ],
    "MainMenu": [
        "Truffle Pasta", "Avocado Toast", "Craft Beer & Fries", 
        "Matcha Tart & Tea", "Ribeye Steak", "Filter Coffee", 
        "Natural Wine & Cheese", "Cream Brick Pasta", "Champagne & Sushi", "Euljiro Cider & Platter"
    ],
    "AvgPrice": [22000, 18000, 15000, 9000, 45000, 7000, 35000, 19000, 60000, 12000]
}

# 데이터를 Pandas DataFrame 형식으로 변환
df = pd.DataFrame(data)

# 3. 사이드바 제어 패널 (Sidebar Input Controls)
st.sidebar.header("🧭 Filter Your Vibe")

# 지역 선택 (전체 선택 가능하도록 기본값 설정)
all_neighborhoods = df["Neighborhood"].unique().tolist()
selected_neighborhoods = st.sidebar.multiselect(
    "Select Neighborhood(s):", 
    options=all_neighborhoods, 
    default=all_neighborhoods
)

# 분위기 태그 선택
all_vibes = df["Vibe"].unique().tolist()
selected_vibes = st.sidebar.multiselect(
    "Select Mood Vibe(s):", 
    options=all_vibes, 
    default=all_vibes
)

# 예산 범위 설정 슬라이더
max_price = int(df["AvgPrice"].max())
min_price = int(df["AvgPrice"].min())
budget = st.sidebar.slider(
    "Maximum Budget (KRW):", 
    min_value=min_price, 
    max_value=max_price, 
    value=max_price,
    step=1000
)

# 4. 데이터 필터링 로직 구동 (Filtering Logic)
filtered_df = df[
    (df["Neighborhood"].isin(selected_neighborhoods)) & 
    (df["Vibe"].isin(selected_vibes)) &
    (df["AvgPrice"] <= budget)
]

# 5. 메인 화면 레이아웃 구성
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Recommended Spots")
    if not filtered_df.empty:
        # 가격 데이터를 보기 좋게 원화(₩) 포맷으로 변경하여 출력
        display_df = filtered_df.copy()
        display_df["AvgPrice"] = display_df["AvgPrice"].map("₩{:,}".format)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("No restaurants match your active filters. Try adjusting the sidebar!")

with col2:
    st.subheader("🎰 Vibe Roulette")
    st.write("Can't decide? Roll the roulette based on your filters!")
    
    # 3단계 기능 맛보기: 랜덤 추천 버튼
    if st.button("What should I eat today?"):
        if not filtered_df.empty:
            random_pick = filtered_df.sample(n=1).iloc[0]
            st.balloons() # 축하 풍선 이펙트
            st.success(f"✨ Today's Pick: **{random_pick['Restaurant']}**")
            st.write(f"• **Location:** {random_pick['Neighborhood']}")
            st.write(f"• **Vibe:** {random_pick['Vibe']}")
            st.write(f"• **Menu:** {random_pick['MainMenu']}")
        else:
            st.error("Set filters first before rolling the roulette!")
