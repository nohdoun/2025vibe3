import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 앱 제목
st.title("📊 서울특별시 연령별 남녀 인구 현황 (2025년 6월)")

# CSV 업로드
file_total = st.file_uploader("🔼 [필수] 연령별 인구 현황 - 합계 파일 업로드", type=["csv"])
file_gender = st.file_uploader("🔼 [필수] 연령별 인구 현황 - 남녀구분 파일 업로드", type=["csv"])

if file_total and file_gender:
    try:import streamlit as st
import plotly.express as px

# 타이틀
st.title("📊 서울특별시 연령별 남녀 인구 시각화 (2025년 6월)")

# CSV 업로드
file_total = st.file_uploader("🟦 [1] 연령별 인구(합계) CSV 업로드", type=["csv"])
file_gender = st.file_uploader("🟦 [2] 연령별 인구(남녀구분) CSV 업로드", type=["csv"])

# 실행 조건
if file_total and file_gender:
    try:
        # 데이터 불러오기
        df_total = pd.read_csv(file_total, encoding="euc-kr")
        df_gender = pd.read_csv(file_gender, encoding="euc-kr")

        # 서울 전체 인구 데이터 (첫 번째 행 기준)
        total_row = df_total.iloc[0]
        gender_row = df_gender.iloc[0]

        # 연령별 컬럼 추출
        male_cols = [col for col in df_gender.columns if "세" in col and "남" in col]
        female_cols = [col for col in df_gender.columns if "세" in col and "여" in col]
        age_labels = [col.split("_")[-1].replace("세", "").replace("100세 이상", "100+") for col in male_cols]

        # 숫자 변환
        male_pop = gender_row[male_cols].str.replace(",", "").fillna("0").astype(int).reset_index(drop=True)
        female_pop = gender_row[female_cols].str.replace(",", "").fillna("0").astype(int).reset_index(drop=True)

        # 시각화용 데이터 구성
        df_plot = pd.DataFrame({
            "연령": pd.Series(age_labels),
            "남자": male_pop,
            "여자": female_pop
        })

        # 긴 포맷으로 변환
        df_long = df_plot.melt(id_vars="연령", value_vars=["남자", "여자"],
                               var_name="성별", value_name="인구수")

        # Plotly 그래프
        fig = px.bar(df_long, x="연령", y="인구수", color="성별", barmode="group",
                     title="2025년 6월 서울특별시 연령별 남녀 인구",
                     labels={"연령": "연령", "인구수": "인구 수"})
        fig.update_layout(xaxis_tickangle=-45)

        # 출력
        st.plotly_chart(fig, use_container_width=True)

        # 데이터 테이블
        with st.expander("🔍 원본 데이터 보기"):
            st.dataframe(df_plot)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("CSV 파일 2개를 모두 업로드하면 시각화됩니다.")

        # 파일 불러오기
        df_total = pd.read_csv(file_total, encoding="euc-kr")
        df_gender = pd.read_csv(file_gender, encoding="euc-kr")

        # 서울시 전체 데이터 (첫 번째 행)
        total_row = df_total.iloc[0]
        gender_row = df_gender.iloc[0]

        # 연령별 컬럼 추출
        male_cols = [col for col in df_gender.columns if "세" in col and "남" in col]
        female_cols = [col for col in df_gender.columns if "세" in col and "여" in col]
        age_labels = [col.split("_")[-1].replace("세", "").replace("100세 이상", "100+") for col in male_cols]

        # 숫자로 변환
        male_pop = gender_row[male_cols].str.replace(",", "").fillna("0").astype(int)
        female_pop = gender_row[female_cols].str.replace(",", "").fillna("0").astype(int)

        # 시각화
        st.subheader("📉 연령별 남녀 인구 막대 그래프")

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(age_labels, male_pop, label="남자", alpha=0.7)
        ax.bar(age_labels, female_pop, label="여자", alpha=0.7, bottom=male_pop)
        ax.set_xlabel("연령")
        ax.set_ylabel("인구 수")
        ax.set_title("서울특별시 연령별 남녀 인구 (2025년 6월)")
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        # 원본 표 보기
        with st.expander("📄 원본 데이터 보기"):
            df_melted = pd.DataFrame({
                "연령": age_labels,
                "남자": male_pop,
                "여자": female_pop
            })
            st.dataframe(df_melted)

    except Exception as e:
        st.error(f"❌ 데이터 처리 중 오류 발생: {e}")

else:
    st.info("CSV 파일 2개를 모두 업로드하면 시각화가 시작됩니다.")
