import streamlit as st
import pandas as pd
import io
from utils.data_collector import collect_reflection_data
from utils.gemini_ideas import generate_app_ideas
from utils.constants import VIEWPOINTS

def render_proposal_menu():
    # 🔧 初期化
    if "app_ideas" not in st.session_state:
        st.session_state.app_ideas = []
    if "reflection_excel" not in st.session_state:
        st.session_state.reflection_excel = None

    if len(st.session_state.questions) == len(VIEWPOINTS):
        st.markdown("### 📱 メニュー④：困りごと解決アプリ構想")

        # ✨ 提案生成
        if st.button("✨ Geminiにアプリを提案してもらう"):
            st.session_state.app_ideas = generate_app_ideas()

        # 💡 提案表示
        if st.session_state.app_ideas:
            st.markdown("### 💡 提案されたアプリアイディア")
            for i, idea in enumerate(st.session_state.app_ideas):
                st.markdown(f"**{i+1}. {idea['title']}**")
                st.markdown(idea["description"])

        # 💾 保存ボタン（未生成時のみ表示）
        if st.session_state.reflection_excel is None:
            if st.button("💾 この相談記録をExcelで保存"):
                data = collect_reflection_data()
                df = pd.DataFrame(data)
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='ReflectionLog')
                st.session_state.reflection_excel = output.getvalue()

        # 📥 ダウンロードボタン（生成済みのみ表示）
        if st.session_state.reflection_excel:
            st.download_button(
                label="📄 相談記録ダウンロード（Excel）",
                data=st.session_state.reflection_excel,
                file_name="reflection_log.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
