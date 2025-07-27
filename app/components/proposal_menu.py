import streamlit as st

def render_proposal_menu():
    if len(st.session_state.questions) == 3:
        st.markdown("## 📱 メニュー④：現場の困りごと × 解決アプリ構想")
        st.markdown("🚧 このパートは現在開発中です。先生の視点を活かした“アプリの種”を生成予定です。")
        st.info("🎁 近日中に自動アプリ提案機能を追加予定です！アイディアや要望があれば教えてください。")
