import streamlit as st
import folium
from geopy.geocoders import Nominatim
from geopy.distance import distance
from streamlit_folium import st_folium

# 세션 초기화
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
                geolocator = Nominatim(user_agent="bookmark_map_app")
                location = geolocator.geocode(address)
                if location:
                    dist_km = distance(current_location, (location.latitude, location.longitude)).km
                    st.session_state.bookmarks.append({
                        "name": address,
                        "lat": location.latitude,
                        "lon": location.longitude,
                        "note": note,
                        "distance_km": dist_km
                    })
                    st.success(f"✅ '{address}' 북마크가 추가되었습니다! (거리: {dist_km:.2f} km)")
                else:
                    st.error("❌ 주소를 찾을 수 없습니다.")
            else:
                st.warning("주소를 입력해주세요.")
    else:
        name = st.text_input("장소 이름")
        lat = st.number_input("위도", format="%.6f")
        lon = st.number_input("경도", format="%.6f")
        note = st.text_input("장소 설명 (선택)", "")
        submitted = st.form_submit_button("📌 북마크 추가")

        if submitted:
            if name and lat and lon:
                dist_km = distance(current_location, (lat, lon)).km
                st.session_state.bookmarks.append({
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "note": note,
                    "distance_km": dist_km
                })
                st.success(f"✅ '{name}' 북마크가 추가되었습니다! (거리: {dist_km:.2f} km)")
            else:
                st.warning("장소 이름과 좌표를 모두 입력해주세요.")

# 🔹 지도 생성
m = folium.Map(location=current_location, zoom_start=13)

# 기준 위치 마커
folium.Marker(
    location=current_location,
    popup="현재 위치",
    icon=folium.Icon(color="red", icon="star")
).add_to(m)

# 북마크 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=f"<b>{bm['name']}</b><br>{bm['note']}<br>📏 거리: {bm['distance_km']:.2f} km",
        tooltip=f"{bm['name']} ({bm['distance_km']:.2f} km)",
        icon=folium.Icon(color="blue", icon="map-marker")
    ).add_to(m)

# 지도 출력
st_folium(m, width=700, height=500)

# 리셋
if st.button("🗑️ 모든 북마크 삭제"):
    st.session_state.bookmarks = []
    st.success("모든 북마크가 삭제되었습니다.")
