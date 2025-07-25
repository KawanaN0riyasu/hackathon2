# ✍️ AI文章問題メーカー（Streamlit × Gemini）

このアプリは、Google Gemini API を使って文章問題（記述式／選択式など）を自動生成できる教育支援ツールです。Python・Streamlit・Gemini API のシンプルな構成で、先生方でも「写経＆アレンジ」が可能です！

---

## 🔧 使用技術
- Python 3.8+
- Streamlit
- Google Generative AI (Gemini API)

---

## 🚀 アプリの使い方

### ① 仮想環境の準備
python -m venv .venv
source .venv/bin/activate
Windowsの場合は .venv\Scripts\activate
pip install -r requirements.txt

### ② Gemini APIキーの取得
Google AI Studio(https://aistudio.google.com/app/apikey)にアクセス
Googleアカウントでログイン
「Get API Key」でキーを取得
→ 発行されたキーを app.py の以下の部分に貼り付けてください：
genai.configure(api_key="YOUR_API_KEY")

### ③ アプリの起動
streamlit run app.py
→ ブラウザが立ち上がり、教科とテーマを選ぶだけで文章問題が生成されます。