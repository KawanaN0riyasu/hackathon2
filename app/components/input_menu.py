import streamlit as st

def render_input_menu():
    st.markdown("### 🍰 メニュー①：モヤモヤをそっとひと言")
    st.caption("どんな些細なことでも大歓迎です。“ちょっとした違和感”がヒントになるかも。☕")
    user_input = st.text_area(
        "📋 今日の気になることをどうぞ：",
        value=st.session_state.user_input,
        placeholder="例：生徒の出席簿を付けるのがたいへんで困っています"
    )
    if user_input != st.session_state.user_input:
        st.session_state.user_input = user_input
        for key in ["questions", "answers", "free_texts", "current_question", "current_choices"]:
            st.session_state[key] = []
