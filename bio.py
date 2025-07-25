import streamlit as st
import pandas as pd
import plotly.express as px

# 지역 위도/경도 정보
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
st.title("🧬 바이오 업종별 지역 분포 시각화 (정확한 엑셀 기반)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')

    # 첫 행이 컬럼명이 아니라면 반영
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # ✔️ 업종별 데이터만 추출 ('소계', '전체' 제외)
    df_bio = df[~df['현황별(2)'].isin(['소계', '전체'])].copy()
    df_bio = df_bio.rename(columns={'현황별(2)': '업종'})

    # 지역 컬럼 추출
    region_columns = df_bio.columns[1:]

    # 숫자형 변환
    for col in region_columns[1:]:
        df_bio[col] = pd.to_numeric(df_bio[col], errors='coerce')

    # Long format 변환
    df_long = df_bio.melt(
        id_vars=['업종'],
        value_vars=region_columns[1:],  # 지역명들
        var_name='지역',
        value_name='사업장 수'
    ).dropna()

    # 위도/경도 추가
    df_long['위도'] = df_long['지역'].map(lambda x: region_coords.get(x, [None, None])[0])
    df_long['경도'] = df_long['지역'].map(lambda x: region_coords.get(x, [None, None])[1])
