import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

from utils.constants import VIEWPOINTS

def generate_question_and_choices(user_input, depth):
    prompt = f"""
あなたは、教育現場の先生に共感的な問いかけを行うアシスタントです。
困りごと：「{user_input}」
今回の視点：「{VIEWPOINTS[depth]}」

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
