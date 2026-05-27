import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import os

# 1. 🌐 글로벌 다국어 번역 및 필터 맵핑 사전
LANG_DICT = {
    "KO": {
        "title": "서울 & 경기 감성 미식 매칭 시스템", "sub": "300개 프리미엄 로케이션 글로벌 큐레이션", "filter": "🧭 큐레이션 필터",
        "region_label": "📍 행정 구역 및 지역 선택", "vibe_label": "🎨 공간 디자인 무드", "budget_label": "💰 1인 다이닝 상한선 (원)",
        "map_title": "🗺️ 광역 다이닝 공간 분포 지도", "chart_title": "📊 다이닝 가치 포지셔닝 분석",
        "roulette_title": "🎰 프리미엄 다이닝 매칭 룰렛", "roulette_sub": "선택된 조건 아래 엄선된 매장을 스캔하여 무작위 매칭합니다.",
        "btn_roll": "✨ 디스커버리 룰렛 가동", "rolling": "🔄 매칭 풀 분석 중... [ {} ]", "match_success": "🍷 매칭 완벽 공간: {}",
        "loc": "📍 파트 로케이션", "vd": "✨ 스타일 무드", "mn": "🍽️ 시그니처 다이닝", "bg": "💰 코스트 밸류",
        "pool_title": "📋 오픈 매칭 데이터 풀 (Pool)", "pool_sub": "현재 알고리즘 내 유효 스팟: **{}**개 매칭 가능",
        "err_no_data": "필터에 부합하는 맛집이 없습니다. 상한선이나 구역을 늘려보세요!", "err_empty": "풀이 비어있습니다. 필터 제약을 완화해 주세요.",
        "regions": {"성수": "성수", "한남": "한남", "홍대/연남": "홍대/연남", "익선동": "익선동", "강남/압구정": "강남/압구정", "경기 근교": "경기 근교"},
        "vibes": {"#힙한": "#힙한", "#인스타감성": "#인스타감성", "#미니멀한": "#미니멀한", "#아늑한": "#아늑한", "#전통적인": "#전통적인"}
    },
    "EN": {
        "title": "Seoul & Gyeonggi Dining Matcher", "sub": "300 Premium Location Global Curations", "filter": "🧭 Curation Filter",
        "region_label": "📍 Select District & Suburbs", "vibe_label": "🎨 Spatial Design Vibe", "budget_label": "💰 Max Budget per Guest (KRW)",
        "map_title": "🗺️ Regional Dining Spatial Map", "chart_title": "📊 Dining Value Positioning Analysis",
        "roulette_title": "🎰 Premium Dining Discovery Roulette", "roulette_sub": "Scans and randomly matches one finest dining spot matching filters.",
        "btn_roll": "✨ Activate Discovery Roulette", "rolling": "🔄 Analyzing Match Pool... [ {} ]", "match_success": "🍷 Matched Hotplace: {}",
        "loc": "📍 Location", "vd": "✨ Style Vibe", "mn": "🍽️ Signature Culinary", "bg": "💰 Cost Value",
        "pool_title": "📋 Open Matching Data Pool", "pool_sub": "Active Algorithm Spots: **{}** locations available",
        "err_no_data": "No dining matches found. Please expand your budget or area!", "err_empty": "The matching pool is empty. Please release filter restrictions.",
        "regions": {"성수": "Seongsu", "한남": "Hannam", "홍대/연남": "Hongdae/Yeonnam", "익선동": "Ikseon-dong", "강남/압구정": "Gangnam/Apgujeong", "경기 근교": "Gyeonggi Suburbs"},
        "vibes": {"#힙한": "#Hip & Trendy", "#인스타감성": "#Instagrammable", "#미니멀한": "#Minimalist", "#아늑한": "#Cozy & Warm", "#전통적인": "#Traditional"}
    },
    "ZH": {
        "title": "首尔 & 京畿感性美食品配系统", "sub": "300个大型奢华空间专业精选策展", "filter": "🧭 策展筛选器",
        "region_label": "📍 选择行政区与近郊", "vibe_label": "🎨 空间设计氛围", "budget_label": "💰 单人用餐预算上限 (韩元)",
        "map_title": "🗺️ 广域美食品类分布地图", "chart_title": "📊 餐厅价值定位量化分析",
        "roulette_title": "🎰 奢华美食推荐智慧轮盘", "roulette_sub": "在您启用的搜索过滤范围内自动检索并随机匹配一个空间。",
        "btn_roll": "✨ 启动感性推荐轮盘", "rolling": "🔄 匹配池超高速分析中... [ {} ]", "match_success": "🍷 智选匹配空间: {}",
        "loc": "📍 地区位置", "vd": "✨ 风格氛围", "mn": "🍽️ 核心招牌菜单", "bg": "💰 用餐成本",
        "pool_title": "📋 开放式数据匹配池 (Pool)", "pool_sub": "当前算法有效餐饮店: **{}** 间可供查看",
        "err_no_data": "找不到符合当前筛选条件的餐厅。请扩大预算或区域范围！", "err_empty": "匹配池处于真空状态。请放宽筛选限制。",
        "regions": {"성수": "圣水", "한남": "汉南", "홍대/연남": "弘大/延南", "익선동": "益善洞", "강남/압구정": "江南/狎鸥亭", "경기 근교": "京畿道近郊"},
        "vibes": {"#힙한": "#时髦潮店", "#인스타감성": "#网红打卡", "#미니멀한": "#极简主义", "#아늑한": "#舒适温馨", "#전통적인": "#传统古風"}
    },
    "JA": {
        "title": "ソウル＆京畿 感性グルメマッチング", "sub": "300の大規模プレミアムロケーション選定", "filter": "🧭 キュレーションフィルタ",
        "region_label": "📍 行政区・郊外エリアの選択", "vibe_label": "🎨 空間デザインのムード", "budget_label": "💰 1人あたりの上限予算 (ウォン)",
        "map_title": "🗺️ 広域ダイニング空間分布マップ", "chart_title": "📊 ダイニング価値ポジショニング分析",
        "roulette_title": "🎰 プレミアムダイニング マッチングルーレット", "roulette_sub": "選択された条件を満たす極上の空間をスキャンし、ランダムでマッチングします。",
        "btn_roll": "✨ ディスカバリールーレット起動", "rolling": "🔄 マッチングプールを高速分析中... [ {} ]", "match_success": "🍷 マッチング空間: {}",
        "loc": "📍 ロケーション", "vd": "✨ スタイルムード", "mn": "🍽️ シグネチャーメニュー", "bg": "💰 コストバリュー",
        "pool_title": "📋 オープンマッチングデータプール", "pool_sub": "現在アルゴリズム内の有効スポット: **{}** 軒がマッチ可能",
        "err_no_data": "条件に合うグルメが見つかりません。予算上限やエリアを広げてみてください！", "err_empty": "プールが空です。フィルターの制約を緩和してください。",
        "regions": {"성수": "聖水(ソンス)", "한남": "漢南(ハンナム)", "홍대/연남": "弘大/延南", "익선동": "益善洞(イクソンドン)", "강남/압구정": "江南/狎鴎亭", "경기 근교": "京畿郊外"},
        "vibes": {"#힙한": "#ヒップな", "#인스타감성": "#インスタ映え", "#미니멀한": "#ミニマルな", "#아늑한": "#ア늑한(居心地の良い)", "#전통적인": "#伝統的な"}
    }
}

st.set_page_config(page_title="SEOUL METRO DINING MATCHER", layout="wide")

# 2. 🎨 트렌디 고딕 폰트 적용 & 눈이 편안한 리얼 화이트 스킨 디자인
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Pretendard:wght@300;500;700;900&display=swap');
    
    /* 배경 흰색으로 전면 수정 및 폰트 변경 */
    .main { background-color: #ffffff !important; color: #1e293b; }
    * { font-family: 'Pretendard', 'Inter', sans-serif !important; }
    
    /* 타이틀 및 네비게이션 데코레이션 */
    .gold-title { font-size: 2.6rem; font-weight: 900; color: #0f172a; text-align: center; letter-spacing: -1px; margin-top: 15px; }
    .lang-container { display: flex; justify-content: center; gap: 8px; margin-bottom: 30px; }
    
    /* 모던 프리미엄 매칭 카드 디자인 */
    .premium-card { background: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 16px !important; padding: 30px !important; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04) !important; margin-top: 20px; }
    .card-label { font-size: 11px !important; color: #64748b !important; text-transform: uppercase; font-weight: 700 !important; letter-spacing: 1px; margin-top: 14px !important; }
    .card-value { font-size: 16px !important; font-weight: 600 !important; color: #0f172a !important; margin-bottom: 2px !important; }
    
    /* 미니멀 룰렛 전광판 */
    .roulette-display { font-size: 20px !important; font-weight: 700 !important; color: #ffffff !important; text-align: center; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important; padding: 22px !important; border-radius: 12px !important; box-shadow: 0 4px 15px rgba(15,23,42,0.15) !important; margin: 18px 0 !important; }
    
    /* 세련된 다크 모던 버튼 */
    .stButton>button { background: #0f172a !important; color: #ffffff !important; border-radius: 8px !important; border: none !important; padding: 14px 28px !important; font-size: 15px !important; font-weight: 700 !important; width: 100%; transition: all 0.25s ease; }
    .stButton>button:hover { background: #334155 !important; box-shadow: 0 4px 12px rgba(51,65,85,0.25); }
    </style>
    """, unsafe_allow_html=True)

# 3. 🌐 세션 언어 감지 시스템
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
st.markdown(f'<p style="text-align:center; color:#64748b; font-size:0.95rem; font-weight:500; margin-bottom:40px;">{T["sub"]}</p>', unsafe_allow_html=True)

# 4. 📁 300선 외부 데이터 인덱싱
txt_file = "restaurants.txt"
if os.path.exists(txt_file):
    df = pd.read_csv(txt_file, encoding="utf-8")
else:
    st.error("⚠️ 'restaurants.txt' 파일이 누락되었습니다.")
    st.stop()

# 5. 🎯 사이드바 내의 선택 박스 실시간 번역 연동 보완
regions_pool = ["성수", "한남", "홍대/연남", "익선동", "강남/압구정", "경기 근교"]
vibes_pool = ["#힙한", "#인스타감성", "#미니멀한", "#아늑한", "#전통적인"]

# 화면에 보여줄 다국어 리스트 구성 및 역추적용 딕셔너리 빌드
translated_regions = [T["regions"][r] for r in regions_pool]
translated_vibes = [T["vibes"][v] for v in vibes_pool]

region_reverse_map = {T["regions"][r]: r for r in regions_pool}
vibe_reverse_map = {T["vibes"][v]: v for v in vibes_pool}

st.sidebar.markdown(f"<h3 style='color:#0f172a;'>{T['filter']}</h3>", unsafe_allow_html=True)

# 선택창 자체에 번역된 언어 노출
selected_regions_trans = st.sidebar.multiselect(T["region_label"], options=translated_regions, default=translated_regions)
selected_vibes_trans = st.sidebar.multiselect(T["vibe_label"], options=translated_vibes, default=translated_vibes)
budget = st.sidebar.slider(T["budget_label"], min_value=int(df["평균가격"].min()), max_value=int(df["평균가격"].max()), value=95000, step=1000)

# 선택된 다국어 값을 다시 한국어 원본 데이터 키값으로 변경하여 필터링 수행
final_regions = [region_reverse_map[tr] for tr in selected_regions_trans]
final_vibes = [vibe_reverse_map[tv] for tv in selected_vibes_trans]

filtered_df = df[(df["지역"].isin(final_regions)) & (df["분위기"].isin(final_vibes)) & (df["평균가격"] <= budget)]

# 6. 🎛️ 모던 럭셔리 대시보드 그래픽 파트
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown(f"##### {T['map_title']}")
    if not filtered_df.empty:
        st.map(filtered_df, latitude="lat", longitude="lon", zoom=10)
    else:
        st.error(T["err_no_data"])

    st.markdown(f"##### {T['chart_title']}")
    if not filtered_df.empty:
        # 차트 범례 및 축 레이블 데이터 번역 치환 적용
        chart_df = filtered_df.copy()
        chart_df["지역"] = chart_df["지역"].map(T["regions"])
        chart_df["분위기"] = chart_df["분위기"].map(T["vibes"])
        
        fig = px.scatter(chart_df, x="지역", y="평균가격", color="분위기", size="평균가격", hover_data=["식당명", "대표메뉴"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"))
        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.markdown(f"##### {T['roulette_title']}")
    st.write(T["roulette_sub"])
    
    roulette_placeholder = st.empty()
    result_placeholder = st.empty()
    
    if st.button(T["btn_roll"]):
        if not filtered_df.empty:
            result_placeholder.empty()
            duration = 1.3
            start_time = time.time()
            all_matching_names = filtered_df["식당명"].tolist()
            
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                wait_time = 0.03 + (elapsed / duration) ** 2 * 0.1
                temp_name = random.choice(all_matching_names)
                roulette_placeholder.html(f'<div class="roulette-display">{T["rolling"].format(temp_name)}</div>')
                time.sleep(wait_time)
            
            roulette_placeholder.empty()
            random_pick = filtered_df.sample(n=1).iloc[0]
            
            card_html = f"""
            <div class="premium-card">
                <h3 style="margin-top:0; color:#0f172a !important; font-size:22px; font-weight:900;">{T["match_success"].format(random_pick['식당명'])}</h3>
                <hr style="border-top: 1px solid #e2e8f0; margin:14px 0;">
                <div class="card-label">{T["loc"]}</div><div class="card-value">{T["regions"][random_pick['지역']]}</div>
                <div class="card-label">{T["vd"]}</div><div class="card-value" style="color:#2563eb !important;">{T["vibes"][random_pick['분위기']]}</div>
                <div class="card-label">{T["mn"]}</div><div class="card-value">{random_pick['대표메뉴']}</div>
                <div class="card-label">{T["bg"]}</div><div class="card-value" style="font-size:18px; color:#0f172a;">₩{random_pick['평균가격']:,}원</div>
            </div>
            """
            result_placeholder.html(card_html)
        else:
            st.error(T["err_empty"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"##### {T['pool_title']}")
    st.markdown(T["pool_sub"].format(len(filtered_df)))
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df["지역"] = display_df["지역"].map(T["regions"])
        display_df["분위기"] = display_df["분위기"].map(T["vibes"])
        display_df["평균가격"] = display_df["평균가격"].map("{:,}원".format)
        st.dataframe(display_df[["식당명", "지역", "분위기", "대표메뉴", "평균가격"]], use_container_width=True, hide_index=True)
