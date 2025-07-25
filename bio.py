import streamlit as st
import pandas as pd
import plotly.express as px

# 지역별 위도/경도
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
st.title("🧬 지역별 바이오사업장 수 시각화 (총합 기준)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    # CSV 로드 및 헤더 처리
    df = pd.read_csv(uploaded_file, encoding='cp949')
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # 주력업종별 데이터만 필터
    df_bio = df[df['현황별(1)'] == '주력업종별'].copy()
    df_bio = df_bio.rename(columns={df_bio.columns[1]: '업종'})
    region_columns = df_bio.columns[2:]

    # 숫자형 변환
    for col in region_columns:
        df_bio[col] = pd.to_numeric(df_bio[col], errors='coerce')

    # Long Format 변환
    df_long = df_bio.melt(
        id_vars=['업종'],
        value_vars=region_columns,
        var_name='지역',
        value_name='사업장 수'
    ).dropna()

    # ✅ 지역별 총합 계산
    df_total = df_long.groupby('지역')['사업장 수'].sum().reset_index()
    df_total['위도'] = df_total['지역'].map(lambda x: region_coords.get(x, [None, None])[0])
    df_total['경도'] = df_total['지역'].map(lambda x: region_coords.get(x, [None, None])[1])
    df_total = df_total.dropna()

    # ✅ 지도 시각화
    st.subheader("🗺️ 지역별 총 바이오 사업장 수 (지도)")
    fig_map = px.scatter_mapbox(
        df_total,
        lat='위도',
        lon='경도',
        size='사업장 수',
        hover_name='지역',
        hover_data={'사업장 수': True},
        size_max=40,
        zoom=5.5,
        mapbox_style='carto-positron',
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ✅ 막대 그래프 시각화
    st.subheader("📊 지역별 총 바이오 사업장 수 (막대 그래프)")
    fig_bar = px.bar(
        df_total,
        x='지역',
        y='사업장 수',
        color='지역',  # 지역별 색상 구분
        text='사업장 수',
        title='지역별 총 바이오 사업장 수 (모든 업종 합산)'
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_bar, use_container_width=True)
