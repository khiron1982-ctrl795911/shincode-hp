import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="キャッチコピー生成", page_icon="💡", layout="wide")
st.title("💡 キャッチコピー・見出し生成")
st.caption("商品・サービス・記事のキャッチコピーや見出し案を複数生成します。")

check_api_key()

with st.form("catch_form"):
    subject = st.text_input("対象（商品名・サービス名・記事テーマなど）")
    appeal_points = st.text_area("アピールしたいポイント", height=100)
    tone = st.selectbox("トーン", ["インパクト重視", "誠実・信頼感", "ユーモラス", "高級感", "親しみやすい"])
    count = st.slider("生成する案の数", min_value=5, max_value=20, value=10)
    submitted = st.form_submit_button("生成する", type="primary")

if submitted:
    if not subject:
        st.error("対象を入力してください。")
    else:
        prompt = f"""以下の対象について、キャッチコピー・見出し案を{count}個作成してください。

# 対象
{subject}

# アピールしたいポイント
{appeal_points or "指定なし"}

# トーン
{tone}

# 出力形式
番号付きの箇条書きで、キャッチコピーのみを出力してください（説明文は不要）。
"""
        try:
            with st.spinner("生成中..."):
                result = generate_text(prompt, temperature=1.0)
            st.session_state["catch_result"] = result
        except Exception as exc:
            show_error(exc)

if "catch_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["catch_result"])
