import streamlit as st

def render_summary_menu():
    if len(st.session_state.questions) == 3:
        st.markdown("### 📚 メニュー③：回答まとめ ＋ 編集・視点チェック")

        viewpoints = {
            0: "困りごとの再定義",
            1: "仕組み・分担",
            2: "個人工夫"
        }

        for i in range(3):
            st.markdown(f"#### 🏷️ 視点：{viewpoints[i]}")
            st.markdown(f"📝 Q{i+1}：{st.session_state.questions[i]}")

            selected = st.session_state.answers[i]
            free_text = st.session_state.free_texts[i]

            if selected != "自由記述":
                st.markdown("**🖋️ 回答内容（選択肢ベース）**")
                st.markdown(f"🗨️ 回答内容：「{selected}」")
                st.text_input("🖋️ 回答の手書き編集（任意）", value=selected, key=f"choice_edit_{i}")
            else:
                st.markdown("**🖋️ 回答内容（自由記述）**")
                st.markdown(f"✒️ 回答内容：「{free_text}」")
                st.text_input("🖋️ 自由記述の手書き編集（任意）", value=free_text, key=f"free_edit_{i}")

            st.markdown("---")

        st.markdown("### 🪄 その他の気付き・改善コメント（任意）")
        st.text_area("🗒️ 現場の感覚・追加のアイディアなど自由にどうぞ", key="additional_thoughts")
