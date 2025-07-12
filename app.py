from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os # 環境変数を読み込むために必要

# Webアプリの基本設定と概要・操作方法の表示
st.set_page_config(page_title="専門家AIチャットアプリ", page_icon="🤖")
st.title("🤖 専門家AIチャットアプリ")

st.markdown("""
このアプリは、あなたが選択した専門家の視点から、入力された質問に回答するAIチャットボットです。
以下の手順でご利用ください。

1.  **専門家を選択:** ラジオボタンから、回答してほしい専門家の種類を選んでください。
2.  **質問を入力:** 下のテキストボックスに、AIに聞きたいことを入力してください。
3.  **送信:** 「回答を生成」ボタンをクリックすると、選択した専門家があなたの質問に答えます。
""")

# 専門家の種類と対応するシステムメッセージを定義
expert_roles = {
    "健康・医療専門家": "あなたは世界一有名な健康・医療専門家です。最新の研究結果に基づき、専門的かつ分かりやすい言葉で健康や医療に関する質問に答えてください。",
    "IT・テクノロジー専門家": "あなたは最先端のIT・テクノロジー専門家です。複雑な技術トレンドやプログラミング、AIに関する質問を、初心者にも理解できるように解説してください。",
    "歴史・文化専門家": "あなたは世界的に著名な歴史・文化専門家です。歴史的背景、文化的意義、芸術に関する質問に、深い洞察と魅力的なストーリーテリングで答えてください。"
}

# LLMからの回答を生成する関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数。
    """
    # OpenAI APIキーの設定
    # Streamlit Cloudにデプロイする際は、st.secrets["OPENAI_API_KEY"]を使用します。
    # ローカルでテストする場合は、環境変数にOPENAI_API_KEYを設定するか、
    # 以下のように直接記述することも可能ですが、本番環境では絶対に避けてください。
    try:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
    except KeyError:
        # Streamlit secretsにキーがない場合、環境変数から取得を試みる
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            return "エラー: OpenAI APIキーが設定されていません。Streamlit secretsまたは環境変数に'OPENAI_API_KEY'を設定してください。"

    # LangChainのChatOpenAIモデルを初期化
    # モデル名は必要に応じて変更してください（例: "gpt-4", "gpt-3.5-turbo"）
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # 選択された専門家に応じたシステムメッセージを取得
    system_message_content = expert_roles.get(expert_type, "あなたは親切なAIアシスタントです。")

    # LLMに渡すメッセージリストを作成
    messages = [
        SystemMessage(content=system_message_content),
        HumanMessage(content=user_input),
    ]

    try:
        # LLMを呼び出し、回答を取得
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {e}\nOpenAI APIの呼び出し中に問題が発生しました。APIキーが有効か、または支払い情報が登録されているか確認してください。"

# ラジオボタンで専門家を選択するUI
selected_expert = st.radio(
    "回答してほしい専門家を選んでください:",
    list(expert_roles.keys()), # expert_rolesのキーをリストにしてラジオボタンの選択肢にする
    index=0 # デフォルトでリストの最初の要素（健康・医療専門家）を選択
)

# ユーザーからの質問を入力するテキストエリア
user_question = st.text_area("AIに質問を入力してください:", height=150)

# 回答生成ボタン
if st.button("回答を生成"):
    if user_question:
        # 質問が入力されている場合のみ処理を実行
        with st.spinner("AIが回答を生成中です...しばらくお待ちください。"):
            # 定義した関数を呼び出し、LLMからの回答を取得
            llm_answer = get_llm_response(user_question, selected_expert)
            st.subheader("AIからの回答:")
            st.info(llm_answer) # 回答を情報ボックスで表示
    else:
        # 質問が入力されていない場合の警告
        st.warning("質問を入力してください。")

st.markdown("---")
st.markdown("© 2024 専門家AIチャットアプリ")

# Streamlit Community Cloud デプロイ時のPythonバージョン指定に関するコメント
# Streamlit Community Cloudにデプロイする際、Pythonのバージョンを3.11に指定するには、
# プロジェクトのルートディレクトリに .streamlit/config.toml ファイルを作成し、
# 以下の内容を記述してください。
#
# [runner]
# python_version = "3.11"
#
# また、必要なライブラリは requirements.txt ファイルに記述してください。
# pip freeze > requirements.txt コマンドで現在の環境のライブラリを自動生成できます。
# 例:
# streamlit==X.X.X
# langchain==0.3.0
# openai==1.47.0
# langchain-community==0.3.0
# langchain-openai==0.2.2
# httpx==0.27.2