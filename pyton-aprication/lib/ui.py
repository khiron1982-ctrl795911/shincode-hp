"""各ページで共通して使うUI部品。"""
import streamlit as st

from lib.config import GEMINI_API_KEY


def check_api_key() -> bool:
    """APIキーが設定されているか確認し、未設定なら警告を表示してFalseを返す。"""
    if not GEMINI_API_KEY:
        st.warning(
            "GEMINI_API_KEYが設定されていません。プロジェクト直下に`.env`ファイルを作成し、"
            "`GEMINI_API_KEY=あなたのAPIキー` の形式で保存してからアプリを再起動してください。\n\n"
            "APIキーは [Google AI Studio](https://aistudio.google.com/apikey) から無料で取得できます。"
        )
        return False
    return True


def show_error(exc: Exception) -> None:
    st.error(f"エラーが発生しました: {exc}")
