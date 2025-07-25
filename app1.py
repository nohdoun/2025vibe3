import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 연령별 인구 시각화", layout="wide")
st.title("📊 서울시 연령별 인구 분포 (2025년 6월 기준)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file:
    try:
        # 데이터 로딩
        df = pd.read_csv(uploaded_file, encoding='cp949')

        # 서울시 전체 행 선택
        seoul_total = df.iloc[0]

        # 연령별 인구 데이터만 추출
        age_columns = [col for col in df.columns if '2025년06월_계_' in col and '총인구수' not in col and '연령구간인구수' not in col]
        ages = [col.replace('2025년06월_계_', '') for col in age_columns]
        populations = seoul_total[age_columns].astype(str).str.replace(',', '').replace('nan', '0').astype(int)

        # Plotly 시각화
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ages, y=populations, mode='lines+markers', name='서울시'))

        fig.update_layout(
            title='서울시 연령별 인구 분포 (2025년 6월)',
            xaxis_title='연령',
            yaxis_title='인구 수',
            template='plotly_white',
            xaxis=dict(tickangle=-45)
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드해주세요.")
