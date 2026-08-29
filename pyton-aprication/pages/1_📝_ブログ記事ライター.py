import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="ブログ記事ライター", page_icon="📝", layout="wide")
st.title("📝 ブログ記事ライター")
st.caption("テーマとキーワードを入力すると、ブログ記事を執筆します。")

check_api_key()

with st.form("blog_form"):
    theme = st.text_input("記事のテーマ（例: 副業で始めるブログ運営）")
    keywords = st.text_input("盛り込みたいキーワード（カンマ区切り、任意）")
    target = st.text_input("想定読者（例: 30代の会社員、初心者ブロガー など）", value="")
    tone = st.selectbox("文体・トーン", ["丁寧・解説調", "カジュアル", "ビジネス寄り", "エモーショナル"])
    length = st.select_slider("記事の長さの目安", options=["短め(800字)", "標準(1500字)", "長め(3000字)"], value="標準(1500字)")
    extra = st.text_area("その他の指示（任意）", placeholder="例: 見出しはH2/H3で構成、体験談を入れてほしい など")
    submitted = st.form_submit_button("記事を生成する", type="primary")

if submitted:
    if not theme:
        st.error("記事のテーマを入力してください。")
    else:
        prompt = f"""あなたはプロのブログライターです。以下の条件でブログ記事を執筆してください。

# テーマ
{theme}

# キーワード
{keywords or "指定なし"}

# 想定読者
{target or "指定なし"}

# 文体・トーン
{tone}

# 長さの目安
{length}

# その他の指示
{extra or "特になし"}

# 出力形式
- タイトル案を1つ
- 導入文
- 見出し（H2/H3相当）で構成された本文
- まとめ
Markdown形式で出力してください。
"""
        try:
            with st.spinner("記事を執筆中..."):
                result = generate_text(prompt)
            st.session_state["blog_result"] = result
        except Exception as exc:
            show_error(exc)

if "blog_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["blog_result"])
    st.download_button(
        "Markdownファイルでダウンロード",
        data=st.session_state["blog_result"],
        file_name="blog_article.md",
        mime="text/markdown",
    )
