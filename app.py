import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

st.title("📍 주소 기반 나만의 북마크 지도")

# 주소 입력 폼
with st.form("address_form"):
    address = st.text_input("주소를 입력하세요 (예: 광주광역시 북구 금호로40번길 40)")
    note = st.text_input("장소 설명 (선택)", "")
    submitted = st.form_submit_button("📌 북마크 추가")

    if submitted and address:
        geolocator = Nominatim(user_agent="bookmark_map_app")
        location = geolocator.geocode(address)

        if location:
            st.session_state.bookmarks.append({
                "name": address,
                "lat": location.latitude,
                "lon": location.longitude,
                "note": note
            })
            st.success(f"'{address}' 북마크가 추가되었습니다!")
        else:
            st.error("❌ 주소를 찾을 수 없습니다. 다시 확인해주세요.")

# 지도 중심 좌표 (초기값: 광주)
map_center = [35.1667, 126.9167]
m = folium.Map(location=map_center, zoom_start=13)

# 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=f"<b>{bm['name']}</b><br>{bm['note']}",
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="map-marker")
    ).add_to(m)

# 지도 출력
st_folium(m, width=700, height=500)

# 리셋 버튼
if st.button("🗑️ 모든 북마크 삭제"):
    st.session_state.bookmarks = []
    st.success("모든 북마크가 삭제되었습니다.")
