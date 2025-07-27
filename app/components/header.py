import streamlit as st

def render_header():
    st.set_page_config(page_title="お悩み深堀りアプリ", layout="centered", page_icon="☕")
    st.markdown("""
    <div style='text-align:center; background-color:#f2e8dc; padding:20px; border-radius:10px;'>
        <h1 style='color:#6b4f3c;'>☕️ お悩み深堀りアプリ</h1>
        <p style='color:#4a3f35;'>今日もお疲れさまです。ふと思ったこと、気になっていること…ほっとひと息つきながらお話ししませんか？</p>
    </div>
    """, unsafe_allow_html=True)
