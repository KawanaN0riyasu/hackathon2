import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# ✅ Gemini APIキー設定（.envから読み込み）
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🌟 ページタイトル
st.set_page_config(page_title="先生向けAI教材メーカー", page_icon="🎓")
st.title("🎓 AI教材メーカー")

# 🔧 教材表示の整形（穴埋め・選択式対応）
def format_output_for_display(text: str, format_type: str) -> str:
    if format_type == "穴埋め式":
        text = text.replace("□□□□", "________")
        text = text.replace("□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□", "_______________________________")
    elif format_type == "選択式（4択）":
        lines = text.split("\n")
        formatted_lines = []
        for line in lines:
            if line.strip().startswith(("A.", "B.", "C.", "D.")):
                formatted_lines.append(f"- {line.strip()}")
            else:
                formatted_lines.append(line)
        text = "\n".join(formatted_lines)
    return text

# 📘 授業設定（アレンジOK！）
grade = st.selectbox("学年を選んでください", ["中1", "中2", "中3", "高1", "高2", "高3"])
subject = st.selectbox("教科を選んでください", ["国語", "英語", "歴史", "理科", "数学"])
theme = st.text_input("テーマ（授業のキーワードなど）", placeholder="例：江戸時代、チャレンジ、化学反応など")
title = st.text_input("教材タイトル（任意）", placeholder="例：江戸時代の暮らしと文化")

# 問題の形式と数（選択可能）
format = st.radio("問題形式を選んでください", ["記述式", "選択式（4択）", "穴埋め式"])
count = st.slider("生成する問題数", 1, 3, 1)

# 表示スタイルの選択（整形 or 生のまま）
display_mode = st.radio("表示スタイル", ["教材として整形する", "Geminiの生出力を表示"])

# 🧠 教材生成ボタン
if st.button("AIで教材を作る！"):
    with st.spinner("生成中…少々お待ちください"):
        # 🎯 PROMPT構造（ここを自由にアレンジ！）
        prompt = f"""
{grade}の{subject}授業用教材として、タイトル「{title}」に対応した{format}形式の文章問題を{count}題作成してください。
各問題には次の要素を含めてください：
- テーマ「{theme}」に沿った問い
- 模範解答
- 解答のポイント解説（先生が授業で使いやすい説明付き）
        """

        # Geminiで教材生成
        response = model.generate_content(prompt)
        st.success("🎉 教材が完成しました！")

        # 整形して表示
        if display_mode == "教材として整形する":
            formatted = format_output_for_display(response.text, format)
            st.markdown(formatted)
        else:
            st.text(response.text)

# 🔐 API管理注意書き
st.caption("※このアプリはGemini APIを使用しています。APIキーは.envファイルで安全に管理されています。")
