import streamlit as st
from utils.gemini_api import generate_question_and_choices
from utils.constants import VIEWPOINTS

def render_talk_menu():
    if st.session_state.user_input and len(st.session_state.questions) < len(VIEWPOINTS):
        st.markdown("### 🪴 メニュー②：深掘りトークタイム")

        if not st.session_state.current_question:
            with st.spinner("☕️ 今日のトークテーマを考えています..."):
                depth = len(st.session_state.questions)
                # 💡 既存の質問履歴を渡す（0件 → 空リスト、以降も自動更新）
                previous_questions = st.session_state.questions
                q_text, choice_list = generate_question_and_choices(
                    st.session_state.user_input,
                    depth,
                    prev_questions=previous_questions
                )
                if q_text:
                    st.session_state.current_question = q_text
                    st.session_state.current_choices = choice_list + ["自由記述"]

        st.subheader(f"🗨️ Q{len(st.session_state.questions)+1}: {st.session_state.current_question}")
        selected = st.radio("📌 お好きな選択肢をお選びください", st.session_state.current_choices)
        free_text = st.text_area("✍️ あなたの考えを自由にどうぞ") if selected == "自由記述" else ""

        if st.button("🌟 回答を保存する"):
            st.session_state.questions.append(st.session_state.current_question)
            st.session_state.answers.append(selected)
            st.session_state.free_texts.append(free_text)
            st.session_state.current_question = ""
            st.session_state.current_choices = []
            st.rerun()