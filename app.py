import streamlit as st
import folium
from streamlit_folium import st_folium

# 세션 상태에 북마크 리스트 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

st.title("📍 나만의 북마크 지도")
st.markdown("직접 장소를 입력하고 북마크를 지도에 추가해보세요!")

# 입력 폼
with st.form("bookmark_form"):
    name = st.text_input("📌 장소 이름", "")
    lat = st.number_input("🌍 위도 (예: 37.5665)", format="%.6f")
    lon = st.number_input("🌏 경도 (예: 126.9780)", format="%.6f")
    note = st.text_input("📝 간단한 설명", "")
    submitted = st.form_submit_button("북마크 추가")

    if submitted:
        if name and lat and lon:
            st.session_state.bookmarks.append({
                "name": name,
                "lat": lat,
                "lon": lon,
                "note": note
            })
            st.success(f"'{name}' 북마크가 추가되었습니다!")
        else:
            st.error("장소 이름과 위도/경도를 모두 입력해주세요.")

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for bookmark in st.session_state.bookmarks:
    folium.Marker(
        location=[bookmark["lat"], bookmark["lon"]],
        popup=f"<b>{bookmark['name']}</b><br>{bookmark['note']}",
        tooltip=bookmark["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=700, height=500)

# 리셋 버튼
if st.button("🗑️ 모든 북마크 삭제"):
    st.session_state.bookmarks = []
    st.success("모든 북마크가 삭제되었습니다.")
