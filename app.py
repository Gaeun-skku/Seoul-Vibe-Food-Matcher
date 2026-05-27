import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import os

# 1. 🌐 글로벌 완벽 번역 사전 (300개 확장 레이블 동기화)
LANG_DICT = {
    "KO": {
        "title": "서울 & 경기 감성 미식 매칭 시스템", "sub": "300개 대형 프리미엄 로케이션 큐레이션", "filter": "🧭 큐레이션 필터",
        "region_label": "📍 행정 구역 및 지역 선택", "vibe_label": "🎨 공간 디자인 무드", "budget_label": "💰 1인 다이닝 상한선 (원)",
        "map_title": "🗺️ 광역 다이닝 공간 분포 지도", "chart_title": "📊 다이닝 가치 포지셔닝 분석",
        "roulette_title": "🎰 프리미엄 다이닝 매칭 룰렛", "roulette_sub": "선택된 조건 아래 엄선된 매장을 스캔하여 무작위 매칭합니다.",
        "btn_roll": "✨ 디스커버리 룰렛 가동", "rolling": "🔄 매칭 풀 초고속 분석 중... [ {} ]", "match_success": "🍷 매칭 완벽 공간: {}",
        "loc": "📍 파트 로케이션", "vd": "✨ 스타일 무드", "mn": "🍽️ 시그니처 다이닝", "bg": "💰 코스트 밸류",
        "pool_title": "📋 오픈 매칭 데이터 풀 (Pool)", "pool_sub": "현재 알고리즘 내 유효 스팟: **{}**개 매칭 가능",
        "err_no_data": "필터에 부합하는 맛집이 없습니다. 상한선이나 구역을 늘려보세요!", "err_empty": "풀이 비어있습니다. 필터 제약을 완화해 주세요."
    },
    "EN": {
        "title": "Seoul & Gyeonggi Dining Matcher", "sub": "300 Massive Premium Location Curations", "filter": "🧭 Curation Filter",
        "region_label": "📍 Select District & Suburbs", "vibe_label": "🎨 Spatial Design Vibe", "budget_label": "💰 Max Budget per Guest (KRW)",
        "map_title": "🗺️ Regional Dining Spatial Map", "chart_title": "📊 Dining Value Positioning Analysis",
        "roulette_title": "🎰 Premium Dining Discovery Roulette", "roulette_sub": "Scans and randomly matches one finest dining spot matching filters.",
        "btn_roll": "✨ Activate Discovery Roulette", "rolling": "🔄 Analyzing Match Pool... [ {} ]", "match_success": "🍷 Matched Hotplace: {}",
        "loc": "📍 Location", "vd": "✨ Style Vibe", "mn": "🍽️ Signature Culinary", "bg": "💰 Cost Value",
        "pool_title": "📋 Open Matching Data Pool", "pool_sub": "Active Algorithm Spots: **{}** locations available",
        "err_no_data": "No dining matches found. Please expand your budget or area!", "err_empty": "The matching pool is empty. Please release filter restrictions."
    },
    "ZH": {
        "title": "首尔 & 京畿感性美食品配系统", "sub": "300个大型奢华空间专业精选策展", "filter": "🧭 策展筛选器",
        "region_label": "📍 选择行政区与近郊", "vibe_label": "🎨 空间设计氛围", "budget_label": "💰 单人用餐预算上限 (韩元)",
        "map_title": "🗺️ 广域美食品类分布地图", "chart_title": "📊 餐厅价值定位量化分析",
        "roulette_title": "🎰 奢华美食推荐智慧轮盘", "roulette_sub": "在您启用的搜索过滤范围内自动检索并随机匹配一个空间。",
        "btn_roll": "✨ 启动感性推荐轮盘", "rolling": "🔄 匹配池超高速分析中... [ {} ]", "match_success": "🍷 智选匹配空间: {}",
        "loc": "📍 地区位置", "vd": "✨ 风格氛围", "mn": "🍽️ 核心招牌菜单", "bg": "💰 用餐成本",
        "pool_title": "📋 开放式数据匹配池 (Pool)", "pool_sub": "当前算法有效餐饮店: **{}** 间可供查看",
        "err_no_data": "找不到符合当前筛选条件的餐厅。请扩大预算或区域范围！", "err_empty": "匹配池处于真空状态。请放宽筛选限制。"
    },
    "JA": {
        "title": "ソウル＆京畿 感性グルメマッチング", "sub": "300の大規模プレミアムロケーション選定", "filter": "🧭 キュレーションフィルタ",
        "region_label": "📍 行政区・郊外エリアの選択", "vibe_label": "🎨 空間デザインのムード", "budget_label": "💰 1人あたりの上限予算 (ウォン)",
        "map_title": "🗺️ 広域ダイニング空間分布マップ", "chart_title": "📊 ダイニング価値ポジショニング分析",
        "roulette_title": "🎰 プレミアムダイニング マッチングルーレット", "roulette_sub": "選択された条件を満たす極上の空間をスキャンし、ランダムでマッチングします。",
        "btn_roll": "✨ ディスカバリールーレット起動", "rolling": "🔄 マッチングプールを高速分析中... [ {} ]", "match_success": "🍷 マッチング空間: {}",
        "loc": "📍 ロケーション", "vd": "✨ スタイルムード", "mn": "🍽️ シグネチャーメニュー", "bg": "💰 コストバリュー",
        "pool_title": "📋 オープンマッチングデータプール", "pool_sub": "現在アルゴリズム内の有効スポット: **{}** 軒がマッチ可能",
        "err_no_data": "条件に合うグルメが見つかりません。予算上限やエリアを広げてみてください！", "err_empty": "プールが空です。フィルターの制約を緩和してください。"
    }
}

st.set_page_config(page_title="SEOUL METRO DINING MATCHER", layout="wide")

# 2. 👑 글로벌 플래그십 네오-럭셔리 테마 디자인 보완 (단순함 타파)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    .main { background: linear-gradient(180deg, #fefdfa 0%, #f1eae0 100%); color: #352e27; }
    * { font-family: 'Noto Sans KR', sans-serif; }
    .gold-title { font-family: 'Cinzel', sans-serif; font-size: 2.8rem; font-weight: 800; color: #4a3423; text-align: center; letter-spacing: 2px; margin-top: 10px; }
    .lang-container { display: flex; justify-content: center; gap: 10px; margin-bottom: 25px; }
    .lang-btn { background: #ffffff; border: 1px solid #d8ccbe; border-radius: 30px; padding: 6px 16px; font-size: 13px; font-weight: 700; color: #6e5f52; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
    .premium-card { background: #ffffff !important; border-top: 5px solid #825430 !important; border-left: 1px solid #dfd5c9 !important; border-right: 1px solid #dfd5c9 !important; border-bottom: 1px solid #dfd5c9 !important; border-radius: 6px 6px 20px 20px !important; padding: 28px !important; box-shadow: 0 20px 45px rgba(84,62,44,0.1) !important; margin-top: 20px; }
    .card-label { font-size: 11px !important; color: #a19081 !important; text-transform: uppercase; font-weight: 700 !important; letter-spacing: 1.5px; margin-top: 14px !important; }
    .card-value { font-size: 16px !important; font-weight: 700 !important; color: #211c18 !important; }
    .roulette-display { font-size: 21px !important; font-weight: 700 !important; color: #ffffff !important; text-align: center; background: linear-gradient(135deg, #a67550 0%, #704423 100%) !important; padding: 22px !important; border-radius: 14px !important; box-shadow: 0 8px 25px rgba(112,68,35,0.25) !important; margin: 18px 0 !important; }
    .stButton>button { background: linear-gradient(135deg, #38271a 0%, #170f0a 100%) !important; color: #e3d2be !important; border-radius: 6px !important; border: 1px solid #543b27 !important; padding: 15px 28px !important; font-size: 16px !important; font-weight: 700 !important; width: 100%; letter-spacing: 1.5px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); transition: all 0.35s ease; }
    .stButton>button:hover { background: linear-gradient(135deg, #825430 0%, #543b27 100%) !important; color: #ffffff !important; box-shadow: 0 8px 25px rgba(130,84,48,0.3); }
    </style>
    """, unsafe_allow_html=True)

# 3. 🌐 가은 님의 취향 저격 멀티링구얼 헤더 제어기
if "lang" not in st.session_state:
    st.session_state.lang = "KO"

st.markdown('<div class="lang-container">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns([4, 1, 1, 1, 1])
with c2:
    if st.button("🇰🇷 KO", key="btn_ko"): st.session_state.lang = "KO"
with c3:
    if st.button("🇺🇸 EN", key="btn_en"): st.session_state.lang = "EN"
with c4:
    if st.button("🇨🇳 ZH", key="btn_zh"): st.session_state.lang = "ZH"
with c5:
    if st.button("🇯🇵 JA", key="btn_ja"): st.session_state.lang = "JA"

T = LANG_DICT[st.session_state.lang]

st.markdown(f'<h1 class="gold-title">{T["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#8c7b6e; letter-spacing:5px; font-size:0.95rem; font-weight:500; margin-bottom:40px;">{T["sub"]}</p>', unsafe_allow_html=True)

# 4. 📁 300선 외부 인덱스 파싱
txt_file = "restaurants.txt"
if os.path.exists(txt_file):
    df = pd.read_csv(txt_file, encoding="utf-8")
else:
    st.error("⚠️ 'restaurants.txt' 파일 링크가 끊어졌습니다. 경로를 확인하세요.")
    st.stop()

regions_pool = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정", "경기 근교"]
vibes_pool = ["#힙한", "#인스타감성", "#미니멀한", "#아늑한", "#전통적인"]

# 5. 🧭 프리미엄 레이아웃 서브 필터링 가동
st.sidebar.markdown(f"<h3 style='color:#4a3423;'>{T['filter']}</h3>", unsafe_allow_html=True)
selected_regions = st.sidebar.multiselect(T["region_label"], options=regions_pool, default=regions_pool)
selected_vibes = st.sidebar.multiselect(T["vibe_label"], options=vibes_pool, default=vibes_pool)
budget = st.sidebar.slider(T["budget_label"], min_value=int(df["평균가격"].min()), max_value=int(df["평균가격"].max()), value=95000, step=1000)

filtered_df = df[(df["지역"].isin(selected_regions)) & (df["분위기"].isin(selected_vibes)) & (df["평균가격"] <= budget)]

# 6. 🎛️ 스패셜 대시보드 화면 렌더링
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown(f"### {T['map_title']}")
    if not filtered_df.empty:
        st.map(filtered_df, latitude="lat", longitude="lon", zoom=10)
    else:
        st.error(T["err_no_data"])

    st.markdown(f"### {T['chart_title']}")
    if not filtered_df.empty:
        fig = px.scatter(filtered_df, x="지역", y="평균가격", color="분위기", size="평균가격", hover_data=["식당명", "대표메뉴"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#352e27"))
        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.markdown(f"### {T['roulette_title']}")
    st.write(T["roulette_sub"])
    
    roulette_placeholder = st.empty()
    result_placeholder = st.empty()
    
    if st.button(T["btn_roll"]):
        if not filtered_df.empty:
            result_placeholder.empty()
            duration = 1.5
            start_time = time.time()
            all_matching_names = filtered_df["식당명"].tolist()
            
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                wait_time = 0.03 + (elapsed / duration) ** 2 * 0.11
                temp_name = random.choice(all_matching_names)
                roulette_placeholder.html(f'<div class="roulette-display">{T["rolling"].format(temp_name)}</div>')
                time.sleep(wait_time)
            
            roulette_placeholder.empty()
            random_pick = filtered_df.sample(n=1).iloc[0]
            
            card_html = f"""
            <div class="premium-card">
                <h3 style="margin-top:0; color:#704423 !important; font-size:23px; font-weight:800;">{T["match_success"].format(random_pick['식당명'])}</h3>
                <hr style="border-top: 1px solid #ebdccb; margin:14px 0;">
                <div class="card-label">{T["loc"]}</div><div class="card-value">{random_pick['지역']}</div>
                <div class="card-label">{T["vd"]}</div><div class="card-value" style="color:#a67550 !important;">{random_pick['분위기']}</div>
                <div class="card-label">{T["mn"]}</div><div class="card-value">{random_pick['대표메뉴']}</div>
                <div class="card-label">{T["bg"]}</div><div class="card-value" style="font-size:19px; color:#38271a;">₩{random_pick['평균가격']:,}원</div>
            </div>
            """
            result_placeholder.html(card_html)
        else:
            st.error(T["err_empty"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {T['pool_title']}")
    st.markdown(T["pool_sub"].format(len(filtered_df)))
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df["평균가격"] = display_df["평균가격"].map("{:,}원".format)
        st.dataframe(display_df[["식당명", "지역", "분위기", "대표메뉴", "평균가격"]], use_container_width=True, hide_index=True)
