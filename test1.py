import streamlit as st
import random

# 제목
st.title("✊✋✌️ 가위바위보 게임")

# 설명
st.markdown("당신의 선택은? 아래 버튼을 눌러주세요!")

# 선택 버튼
user_choice = st.radio("선택하세요:", ["가위", "바위", "보"], horizontal=True)

# 선택 시 실행
if st.button("대결!"):
    # 컴퓨터 선택
    computer_choice = random.choice(["가위", "바위", "보"])
    
    # 결과 판단
    if user_choice == computer_choice:
        result = "😐 비겼어요!"
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        result = "🎉 당신이 이겼어요!"
    else:
        result = "💀 컴퓨터가 이겼어요!"

    # 결과 출력
    st.write(f"🧍 당신: {user_choice}")
    st.write(f"💻 컴퓨터: {computer_choice}")
    st.subheader(result)

