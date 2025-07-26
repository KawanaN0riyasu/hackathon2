# --- 必要ライブラリ ---
import streamlit as st
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# --- Gemini API 認証と初期化 ---
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- ページデザイン設定 ---
st.set_page_config(page_title="お悩み深堀りアプリ", layout="centered", page_icon="☕")
st.markdown("""
<div style='text-align:center; background-color:#f2e8dc; padding:20px; border-radius:10px;'>
    <h1 style='color:#6b4f3c;'>☕️ お悩み深堀りアプリ</h1>
    <p style='color:#4a3f35;'>今日もお疲れさまです。ふと思ったこと、気になっていること…ほっとひと息つきながらお話ししませんか？</p>
</div>
""", unsafe_allow_html=True)

# --- セッション初期化 ---
default_states = {
    "user_input": "",
    "questions": [],
    "answers": [],
    "free_texts": [],
    "current_question": "",
    "current_choices": [],
}
for key, default in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- メニュー①：困りごとの入力 ---
st.markdown("### 🍰 メニュー①：モヤモヤをそっとひと言")
st.caption("どんな些細なことでも大歓迎です。“ちょっとした違和感”がヒントになるかも。☕")

user_input = st.text_area(
    "📋 今日の気になることをどうぞ：",
    value=st.session_state.user_input,
    placeholder="例：生徒の出席簿を付けるのがたいへんで困っています"
)
if user_input != st.session_state.user_input:
    st.session_state.user_input = user_input
    # 入力が更新されたら履歴リセット
    for key in ["questions", "answers", "free_texts", "current_question", "current_choices"]:
        st.session_state[key] = []

# --- Gemini質問生成 ---
def generate_question_and_choices(user_input, depth):
    viewpoints = [
        "困りごとの背景にある本質課題",
        "仕組み、体制、分担について",
        "個人の工夫",
    ]
    prompt = f"""
あなたは、教育現場の先生に共感的な問いかけを行うアシスタントです。
困りごと：「{user_input}」
今回の視点：「{viewpoints[depth]}」

制約：
- 質問文は簡潔で親しみやすく
- 選択肢3つ＋自由記述Dを加えること

出力形式：
Q: [質問文]
- A: 
- B: 
- C: 
- D: 自由記述
"""
    response = model.generate_content(prompt).text.strip()
    question = re.search(r"Q[:：]\s*(.*)", response)
    choices = re.findall(r"-\s*[A-C]:\s*(.*)", response)
    return question.group(1).strip() if question else "", choices

# --- メニュー②：深掘りトークタイム ---
if st.session_state.user_input and len(st.session_state.questions) < 3:
    st.markdown("### 🪴 メニュー②：深掘りトークタイム")

    if not st.session_state.current_question:
        with st.spinner("☕️ 今日のトークテーマを考えています..."):
            depth = len(st.session_state.questions)
            q_text, choice_list = generate_question_and_choices(user_input, depth)
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

# --- メニュー③：まとめ表示 ＋ 編集UI ---
if len(st.session_state.questions) == 3:
    st.markdown("### 📚 メニュー③：回答まとめ ＋ 編集・視点チェック")

    viewpoints = {
        0: "困りごとの再定義",
        1: "仕組み・分担",
        2: "個人工夫"
    }

    for i in range(3):
        st.markdown(f"#### 🏷️ 視点：{viewpoints[i]}")

        # 質問文は表示のみ（編集不要の場合はこちらでOK）
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

    # --- メニュー③：その他の気付き入力欄 ---
    st.markdown("### 🪄 その他の気付き・改善コメント（任意）")
    st.text_area("🗒️ 現場の感覚・追加のアイディアなど自由にどうぞ", key="additional_thoughts")

# --- メニュー④：アプリ提案 ---
if len(st.session_state.questions) == 3:
    st.markdown("## 📱 メニュー④：現場の困りごと × 解決アプリ構想")
