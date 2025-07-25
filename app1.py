import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="지역별 인구 시각화", layout="wide")
st.title("📊 지역별 연령별 인구 시각화 (2025년 6월 기준)")

# 파일 업로드
col1, col2 = st.columns(2)
with col1:
    file_total = st.file_uploader("① 연령별 인구 총합 CSV 업로드", type="csv", key="total")
with col2:
    file_gender = st.file_uploader("② 연령별 남녀 인구 구분 CSV 업로드", type="csv", key="gender")

if file_total and file_gender:
    try:
        df_total = pd.read_csv(file_total, encoding='cp949')
        df_gender = pd.read_csv(file_gender, encoding='cp949')

        # ▶ 지역 선택
        regions = df_total['행정구역'].unique().tolist()
        selected_region = st.selectbox("지역 선택", regions)

        row_total = df_total[df_total['행정구역'] == selected_region].iloc[0]
        row_gender = df_gender[df_gender['행정구역'] == selected_region].iloc[0]

        ### 1. 연령별 전체 인구 ###
        age_cols = [col for col in df_total.columns if '2025년06월_계_' in col and '총' not in col and '연령구간' not in col]
        ages = [col.replace('2025년06월_계_', '') for col in age_cols]
        pops = row_total[age_cols].astype(str).str.replace(',', '').replace('nan', '0').astype(int)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=ages, y=pops, mode='lines+markers', name='전체 인구'))

        fig1.update_layout(
            title=f'{selected_region} 연령별 전체 인구 (2025년 6월)',
            xaxis_title='연령',
            yaxis_title='인구 수',
            xaxis=dict(tickangle=-45),
            template='plotly_white'
        )

        ### 2. 남녀 인구 피라미드 ###
        male_cols = [col for col in df_gender.columns if '2025년06월_남_' in col and '총' not in col and '연령구간' not in col]
        female_cols = [col for col in df_gender.columns if '2025년06월_여_' in col and '총' not in col and '연령구간' not in col]
        age_labels = [col.replace('2025년06월_남_', '') for col in male_cols]

        male_pops = row_gender[male_cols].astype(str).str.replace(',', '').replace('nan', '0').astype(int) * -1
        female_pops = row_gender[female_cols].astype(str).str.replace(',', '').replace('nan', '0').astype(int)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=age_labels, x=male_pops, name='남성', orientation='h'))
        fig2.add_trace(go.Bar(y=age_labels, x=female_pops, name='여성', orientation='h'))

        fig2.update_layout(
            title=f'{selected_region} 연령별 남녀 인구 피라미드 (2025년 6월)',
            xaxis_title='인구 수',
            yaxis_title='연령',
            barmode='relative',
            template='plotly_white'
        )

        # 출력
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"📛 오류 발생: {e}")

else:
    st.warning("👆 두 개의 CSV 파일을 모두 업로드해주세요.")
