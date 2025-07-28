import streamlit as st
from utils.constants import VIEWPOINTS

def render_summary_menu():
    if len(st.session_state.questions) == len(VIEWPOINTS):
        st.markdown("## 📚 メニュー③：振り返りまとめ＆視点チェック")

        viewpoints = {
            0: "困りごとの再定義",
            1: "仕組み・分担",
            2: "個人工夫",
            3: "余裕ができたらしたいこと"
        }

        for i in len(VIEWPOINTS):
            st.markdown(f"### 🏷️ 視点 {i+1}：{viewpoints[i]}")
            with st.container():
                st.markdown(f"**📝 質問 {i+1}：** {st.session_state.questions[i]}")

                selected = st.session_state.answers[i]
                free_text = st.session_state.free_texts[i]

                st.markdown("---")

                if selected != "自由記述":
                    st.markdown("**🎯 選択肢による回答**")
                    st.info(f"「{selected}」", icon="🗨️")
                    st.text_input(
                        "✏️ 回答の手書き編集（任意）",
                        value=selected,
                        key=f"choice_edit_{i}",
                        placeholder="自由に書き換えてください"
                    )
                else:
                    st.markdown("**📝 自由記述による回答**")
                    st.success(f"「{free_text}」", icon="✒️")
                    st.text_input(
                        "✏️ 自由記述の手書き編集（任意）",
                        value=free_text,
                        key=f"free_edit_{i}",
                        placeholder="自由に書き換えてください"
                    )

                st.markdown("----")

        st.markdown("### 🌱 その他の気付き・アイディア（任意）")
        st.text_area(
            "🗒️ 現場の感覚や「こうしたい」など、思いついたことをご自由にどうぞ",
            key="additional_thoughts",
            placeholder="例：この話題、教科会で共有すると盛り上がりそう"
        )
