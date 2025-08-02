import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from utils.data_collector import collect_reflection_data

# 🔧 Gemini初期化（.envからAPIキーを読み込む）
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_app_ideas():
    """
    相談記録から教師向けアプリアイデアを3つ生成する
    """
    reflection_data = collect_reflection_data()
    prompt = build_prompt_from_data(reflection_data)
    response = model.generate_content(prompt).text
    ideas = parse_app_ideas(response)  # ← parse関数は別途実装
    return ideas


def build_prompt_from_data(reflection_data: list[dict]) -> str:
    """
    セッションデータをもとにGemini用プロンプトを生成する
    """
    section_map = {item["セクション"]: item["内容"] for item in reflection_data}

    # 空欄時にフォールバックを入れると、出力品質が安定します
    def get(section_name: str) -> str:
        return section_map.get(section_name) or "（未入力）"

    # 各要素を抽出
    worry = get("困りごと")
    challenge = get("取り組む課題")
    environment = get("仕事環境(体制・仕組み・分担)")
    creativity = get("個人の創意工夫")
    wishes = get("叶えたいこと")

    # Geminiへの指示文
    prompt = f"""
あなたは教師向けの課題解決型アプリを提案する専門家です。
以下の相談内容をもとに、Streamlitアプリとして、90min程度で写経できるアイデアを3つ考えてください。

## 共通条件
- 「困りごと」と「取り組む課題」を踏まえて考案してください
- アイデアはすべて異なる切り口で重複しないようにしてください
- 初学者の先生にもわかりやすく親しんでもらうため、アイコン等使いながら簡潔な表現を心がけてください

## アイデア1
- 仕事環境（体制・仕組み・分担）
- 個人の創意工夫
- 叶えたいこと
これらの視点も考慮してください

## アイデア2
- アイデア1の視点とは異なる観点で
- ユーザーの盲点を突く既存の習慣に囚われない提案

## アイデア3
- アイデア1・2とは違う切り口で
- 仕事環境（体制・仕組み・分担）
- 個人の創意工夫
- 叶えたいこと
これらの視点を考慮した提案


## 教師の相談内容
困りごと：{worry}
取り組む課題：{challenge}
仕事環境（体制・仕組み・分担）：{environment}
個人の創意工夫：{creativity}
叶えたいこと：{wishes}

## 出力形式
【1つ目のアイデア】
タイトル：
説明：
    ・用途
    ・扱う技術
    ・より楽しく使うために

【2つ目のアイデア】
タイトル：
説明：
    ・用途
    ・扱う技術
    ・より楽しく使うために

【3つ目のアイデア】
タイトル：
説明：
    ・用途
    ・扱う技術
    ・より楽しく使うために
"""
    return prompt.strip()


def parse_app_ideas(response_text: str) -> list[dict]:
    """
    Geminiの応答テキストからアイデア3件分のタイトルと説明を抽出する
    """
    ideas = []

    # 各アイデアを区切るための正規表現パターン
    pattern = r"【\d+つ目のアイデア】\s*タイトル：(.+?)\s*説明：(.+?)(?=【|\Z)"
    matches = re.findall(pattern, response_text, re.DOTALL)

    for title, description in matches:
        ideas.append({
            "title": title.strip(),
            "description": description.strip()
        })

    return ideas
