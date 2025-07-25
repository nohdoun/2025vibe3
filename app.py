import streamlit as st
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

st.title("📍 나만의 북마크 지도")
st.markdown("위치 입력 방법을 선택하고, 지도에 마커를 추가해보세요!")

# 입력 방식 선택
input_method = st.radio("위치 입력 방식 선택", ["주소 입력", "위도/경도 직접 입력"], horizontal=True)

with st.form("location_form"):
    if input_method == "주소 입력":
        address = st.text_input("주소를 입력하세요 (예: 광주광역시 북구 금호로40번길 40)")
        note = st.text_input("장소 설명", "")
        submitted = st.form_submit_button("📌 북마크 추가")
        if submitted:
            if address:
                geolocator = Nominatim(user_agent="bookmark_map_app")
                location = geolocator.geocode(address)
                if location:
                    st.session_state.bookmarks.append({
                        "name": address,
                        "lat": location.latitude,
                        "lon": location.longitude,
                        "note": note
                    })
                    st.success(f"✅ '{address}' 북마크가 추가되었습니다!")
                else:
                    st.error("❌ 주소를 찾을 수 없습니다.")
            else:
                st.warning("주소를 입력해주세요.")
    
    elif input_method == "위도/경도 직접 입력":
        name = st.text_input("장소 이름")
        lat = st.number_input("위도 (Latitude)", format="%.6f")
        lon = st.number_input("경도 (Longitude)", format="%.6f")
        note = st.text_input("장소 설명", "")
        submitted = st.form_submit_button("📌 북마크 추가")
        if submitted:
            if name and lat and lon:
                st.session_state.bookmarks.append({
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "note": note
                })
                st.success(f"✅ '{name}' 북마크가 추가되었습니다!")
            else:
                st.warning("장소 이름과 좌표를 모두 입력해주세요.")

# 지도 생성 (광주 중심)
map_center = [35.1667, 126.9167]
m = folium.Map(location=map_center, zoom_start=13)

# 북마크 마커 추가
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
