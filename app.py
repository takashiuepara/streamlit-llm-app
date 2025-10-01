#LLMに渡すプロンプトを画面上で入力し、
#そのプロンプトをLLMに渡して、LLMからの応答を画面上に表示する簡単なWebアプリ
#ラジオボタンでLLMを選択できるようにする。一方は経済に関する専門家、もう一方は歴史に関する専門家

# APIキー読み込み
from dotenv import load_dotenv
load_dotenv()

# streamlit_app.py
import streamlit as st
import os
from langchain_openai import ChatOpenAI   # チャットモデル
from langchain.llms import OpenAI

st.title("AIとお話ししましょう！")

st.write("これはChatGPTを利用した会話プログラムです。")
st.write("経済に関するAI専門家、歴史に関するAI専門家を選択し、質問を入力してください。")

# ラジオボタンで動作モードを選択
selected_item = st.radio(
    "会話する専門家を選択してください。",
    ["経済専門家", "歴史専門家"]    
)
# 入力テキストの取得
input_message = st.text_input(label="質問を入力してください。")


# 選択された専門家を表示
st.write(f"選択された専門家: **{selected_item}**")

# LangChainのLLMを初期化
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1024, model="gpt-4o-mini", temperature=0)

def generate_response(expert_type, question):
    """
    選択された専門家タイプと質問を引数に応じて応答を生成する関数。

    Args:
        expert_type (str): 選択された専門家タイプ（例: "経済専門家" または "歴史専門家"）。
        question (str): ユーザーからの質問。

    Returns:
        str: 専門家からの応答。
    """
    if not question:
        return "質問を入力してください。"

    try:
        if expert_type == "経済専門家":
            # 経済専門家としてのプロンプト
            prompt = f"あなたは経済の専門家です。以下の質問に答えてください: {question}"
        else:
            # 歴史専門家としてのプロンプト
            prompt = f"あなたは歴史の専門家です。以下の質問に答えてください: {question}"

        # LangChainを使用して応答を生成
        answer = llm(prompt)
        return f"{expert_type}の回答: {answer}"
    except Exception as e:
        return f"エラーが発生しました: {e}"

if st.button("実行"):
    response = generate_response(selected_item, input_message)
    st.write(response)

# 実行コマンド
# streamlit run env/app.py  --server.port 8501 --server.address 0.0.0.0