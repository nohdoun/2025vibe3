import streamlit as st
import pandas as pd
import plotly.express as px

# 위도/경도 정보
region_coords = {
    "서울": [37.5665, 126.9780],
    "부산": [35.1796, 129.0756],
    "인천": [37.4563, 126.7052],
    "대구": [35.8722, 128.6025],
    "광주": [35.1595, 126.8526],
    "대전": [36.3504, 127.3845],
    "울산": [35.5384, 129.3114],
    "세종": [36.4801, 127.2890],
    "경기": [37.4138, 127.5183],
    "강원": [37.8228, 128.1555],
    "충북": [36.6358, 127.4917],
    "충남": [36.5184, 126.8000],
    "전북": [35.7167, 127.1442],
    "전남": [34.8161, 126.4630],
    "경북": [36.4919, 128.8889],
    "경남": [35.4606, 128.2132],
    "제주": [33.4996, 126.5312]
}

st.set_page_config(layout="wide")
st.title("🧬 바이오 업종별 지역 분포 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    # CSV 로딩 (컬럼 없이 불러옴)
    df_raw = pd.read_csv(uploaded_file, encoding='cp949', header=None)

    # 컬럼 설정: 두 번째 행이 지역명
    df_raw.columns = df_raw.iloc[1]
    df = df_raw.iloc[3:].reset_index(drop=True)

    # 업종명 추출
    df = df.rename(columns={df.columns[0]: '업종'})

    # 숫자형으로 변환
    region_columns = df.columns[1:]
    for col in region_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 모든 조합 생성
    all_regions = region_columns.tolist()
    all_industries = df['업종'].unique().tolist()
    all_combinations = pd.MultiIndex.from_product(
        [all_industries, all_regions],
        names=['업종', '지역']
    ).to_frame(index=False)

    # long format
    df_long = df.melt(id_vars=['업종'], value_vars=all_regions,
                      var_name='지역', value_name='사업장 수')

    # 누락 조합 포함 + NaN -> 0
    df_full = all_combinations.merge(df_long, on=['업종', '지역'], how='left')
    df_full['사업장 수'] = df_full['사업장 수'].fillna(0)

    # 위경도 추가
    df_full['위도'] = df_full['지역'].map(lambda x: region_coords.get(x, [None, None])[0])
    df_full['경도'] = df_full['지역'].map(lambda x: region_coords.get(x, [None, None])[1])
    df_full = df_full.dropna(subset=['위도', '경도'])

    # ✅ 지역 필터
    available_regions = sorted(df_full['지역'].unique())
    selected_regions = st.multiselect(
        "확인할 지역을 선택하세요:",
        options=available_regions,
        default=available_regions
    )
    filtered = df_full[df_full['지역'].isin(selected_regions)]

    # ✅ 지도 시각화
    st.subheader("🗺️ 선택 지역의 업종별 바이오 사업장 분포 (지도)")
    fig_map = px.scatter_mapbox(
        filtered,
        lat='위도',
        lon='경도',
        size='사업장 수',
        color='업종',
        hover_name='지역',
        hover_data={'사업장 수': True},
        size_max=40,
        zoom=5.5,
        mapbox_style='carto-positron',
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ✅ 막대그래프 시각화
    st.subheader("📊 지역별 업종별 바이오 사업장 수 (막대그래프)")
    fig_bar = px.bar(
        filtered,
        x='지역',
        y='사업장 수',
        color='업종',
        text='사업장 수',
        barmode='stack',
        title='지역별 업종별 바이오 사업장 수'
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_bar, use_container_width=True)
