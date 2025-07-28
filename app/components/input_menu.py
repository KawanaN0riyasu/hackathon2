import streamlit as st

def render_input_menu():
    st.markdown("### 🍰 メニュー①：モヤモヤをそっとひと言")
    st.caption("どんな些細なことでも大歓迎です。“ちょっとした違和感” がヒントになるかも☕")

    user_input = st.text_area(
        "📋 あなたの立場、ちょっとしたモヤモヤを自由にお書きください：",
        value=st.session_state.user_input,
        placeholder="例：高2のクラス担任ですが、出席簿の出欠をカウントする作業が煩雑で困っています"
    )

    if user_input != st.session_state.user_input:
        st.session_state.user_input = user_input
        for key in ["questions", "answers", "free_texts", "current_question", "current_choices"]:
            st.session_state[key] = []
