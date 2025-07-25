import streamlit as st
import folium
from geopy.geocoders import Nominatim
from geopy.distance import distance
from streamlit_folium import st_folium

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

st.title("📍 나만의 북마크 지도 with 거리 계산")

st.markdown("위치를 입력하고, 현재 위치에서 얼마나 떨어져 있는지 확인해보세요!")

# 🔹 사용자 기준 위치 입력
st.sidebar.header("📌 기준 위치 설정 (예: 현재 내 위치)")
current_lat = st.sidebar.number_input("현재 위치 위도", value=35.1667, format="%.6f")
current_lon = st.sidebar.number_input("현재 위치 경도", value=126.9167, format="%.6f")
current_location = (current_lat, current_lon)

# 🔹 위치 입력 방식 선택
input_method = st.radio("위치 입력 방식", ["주소 입력", "위도/경도 직접 입력"], horizontal=True)

# 🔹 북마크 입력 폼
with st.form("location_form"):
    if input_method == "주소 입력":
        address = st.text_input("주소 입력 (예: 광주광역시 북구 금호로40번길 40)")
        note = st.text_input("장소 설명 (선택)", "")
        submitted = st.form_submit_button("📌 북마크 추가")

        if submitted:
            if address:
                geol
