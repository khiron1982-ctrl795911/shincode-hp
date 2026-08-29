import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
st.title("📄 文章要約")
st.caption("長い文章を貼り付けると、指定した長さ・形式で要約します。")

check_api_key()

with st.form("summary_form"):
    source_text = st.text_area("要約したい文章を貼り付け", height=250)
    length = st.selectbox("要約の長さ", ["一言で(1文)", "短め(3行程度)", "標準(200字程度)", "詳しめ(500字程度)"], index=2)
    style = st.selectbox("形式", ["箇条書き", "文章形式"])
    submitted = st.form_submit_button("要約する", type="primary")

if submitted:
    if not source_text:
        st.error("要約したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を要約してください。

# 元の文章
{source_text}

# 要約の長さ
{length}

# 出力形式
{style}

重要なポイントを漏らさず、簡潔にまとめてください。
"""
        try:
            with st.spinner("要約中..."):
                result = generate_text(prompt, temperature=0.3)
            st.session_state["summary_result"] = result
        except Exception as exc:
            show_error(exc)

if "summary_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["summary_result"])
