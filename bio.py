import streamlit as st
import pandas as pd
import plotly.express as px

# 지역별 위도/경도 정보 (시도 기준)
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

st.title("지역별 바이오 사업장 수 지도 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')
    new_columns = df.iloc[0]
    df = df[1:]
    df.columns = new_columns
    df = df.reset_index(drop=True)

    df_total = df[(df['현황별(1)'] == '전체') & (df['현황별(2)'] == '소계')]
    region_columns = new_columns[2:]
    region_data = df_total[region_columns].T.reset_index(names='지역')
    region_data.columns = ['지역', '사업장 수']
    region_data['사업장 수'] = pd.to_numeric(region_data['사업장 수'], errors='coerce')
    region_data = region_data.dropna()

    # 위도/경도 추가
    region_data['위도'] = region_data['지역'].map(lambda x: region_coords.get(x, [None, None])[0])
    region_data['경도'] = region_data['지역'].map(lambda x: region_coords.get(x, [None, None])[1])
    region_data = region_data.dropna(subset=['위도', '경도'])

    # 지도 시각화
    fig = px.scatter_mapbox(
        region_data,
        lat='위도',
        lon='경도',
        size='사업장 수',
        hover_name='지역',
        hover_data={'사업장 수': True, '위도': False, '경도': False},
        size_max=40,
        zoom=5.5,
        mapbox_style='carto-positron',
        title='지도 위 지역별 바이오 사업장 수 (2023 기준)'
    )

    st.plotly_chart(fig, use_container_width=True)
