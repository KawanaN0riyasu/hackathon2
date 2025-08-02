import streamlit as st
from utils.constants import VIEWPOINTS

def collect_reflection_data():
    data = []

    # 🟢 困りごと
    data.append({
        "セクション": "困りごと",
        "内容": st.session_state.get("user_input", "")
    })

    # 📘 メニュー③：視点別編集
    for i, viewpoint in enumerate(VIEWPOINTS):
        edited = (
            st.session_state.get(f"choice_edit_{i}")
            or st.session_state.get(f"free_edit_{i}")
            or (st.session_state.get("answers") or [])[i]
            or ""
        )
        data.append({
            "セクション": f"視点{i+1}：{viewpoint}",
            "内容": edited
        })

    # その他の気付き
    additional = st.session_state.get("additional_thoughts", "")
    data.append({
        "セクション": "その他の気付き",
        "内容": additional
    })

    # 💡 メニュー④：提案アプリ
    for i, idea in enumerate(st.session_state.get("app_ideas", [])):
        data.append({
            "セクション": f"提案アプリ{i+1}",
            "内容": f"{idea['title']}：{idea['description']}"
        })

    return data
