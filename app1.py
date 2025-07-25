import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 제목
st.title("📊 서울특별시 연령별 남녀 인구 현황 (2025년 6월)")

# CSV 파일 업로드
uploaded_file_total = st.file_uploader("🔼 [필수] 연령별 인구 현황 (합계) CSV 업로드", type=["csv"], key="total")
uploaded_file_gender = st.file_uploader("🔼 [필수] 연령별 인구 현황 (남녀구분) CSV 업로드", type=["csv"], key="gender")

if uploaded_file_total and uploaded_file_gender:
    try:
        # 데이터 불러오기
        df_total = pd.read_csv(uploaded_file_total, encoding="euc-kr")
        df_gender = pd.read_csv(uploaded_file_gender, encoding="euc-kr")

        # 서울시 전체 행만 사용 (첫 번째 행)
        total_row = df_total.iloc[0]
        gender_row = df_gender.iloc[0]

        # 연령 관련 컬럼 추출
        age_cols = [col for col in df_total.columns if "세" in col and "계" in col]
        male_cols = [col for col in df_gender.columns if "세" in col and "남" in col]
        female_cols = [col for col in df_gender.columns if "세" in col and "여" in col]
        age_labels = [col.split("_")[-1].replace("세", "").replace("100세 이상", "100+") for col in male_cols]

        # 문자열 → 숫자 변환
        total_pop = total_row[age_cols].str.replace(",", "").fillna("0").astype(int).reset_index(drop=True)
        male_pop = gender_row[male_cols].str.replace(",", "").fillna("0").astype(int).reset_index(drop=True)
        female_pop = gender_row[female_cols].str.replace(",", "").fillna("0").astype(int).reset_index(drop=True)

        # 시각화용 데이터프레임
        df_plot = pd.DataFrame({
            "나이": pd.Series(age_labels),
            "남자": male_pop,
            "여자": female_pop,
            "합계": total_pop
        })

        # 긴 포맷 변환
        df_long = df_plot.melt(id_vars="나이", value_vars=["남자", "여자"],
                               var_name="성별", value_name="인구수")

        # Plotly 그래프
        fig = px.bar(df_long, x="나이", y="인구수", color="성별", barmode="group",
                     title="서울특별시 연령별 남녀 인구 현황 (2025년 6월)",
                     labels={"나이": "연령", "인구수": "인구 수"})
        fig.update_layout(xaxis_tickangle=-45)

        # 출력
        st.plotly_chart(fig, use_container_width=True)

        # 원본 데이터프레임도 보기
        with st.expander("📄 원본 데이터 보기"):
            st.dataframe(df_plot)

    except Exception as e:
        st.error(f"❌ 데이터 처리 중 오류 발생: {e}")

else:
    st.info("위의 두 개 CSV 파일을 모두 업로드하면 시각화가 시작됩니다.")
