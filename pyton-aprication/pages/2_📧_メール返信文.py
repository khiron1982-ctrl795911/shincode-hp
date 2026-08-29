import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="メール返信文", page_icon="📧", layout="wide")
st.title("📧 メール返信文ジェネレーター")
st.caption("受信したメールの内容を貼り付けると、返信文の下書きを作成します。")

check_api_key()

with st.form("email_form"):
    original_mail = st.text_area("受信メールの本文を貼り付け", height=200)
    intent = st.text_area("返信の要点・伝えたいこと", placeholder="例: 日程は来週水曜14時でOK、資料は金曜までに送ると伝えたい")
    tone = st.selectbox("トーン", ["丁寧・フォーマル", "柔らかめ・親しみやすい", "簡潔・ビジネスライク"])
    submitted = st.form_submit_button("返信文を生成する", type="primary")

if submitted:
    if not original_mail or not intent:
        st.error("受信メールの本文と、返信の要点の両方を入力してください。")
    else:
        prompt = f"""あなたは優秀なビジネスアシスタントです。以下の受信メールに対する返信メールの下書きを作成してください。

# 受信メールの本文
{original_mail}

# 返信で伝えたい要点
{intent}

# トーン
{tone}

# 出力形式
件名と本文をセットで出力してください。日本のビジネスメールの一般的な形式（宛名・挨拶・本文・結び）に従ってください。
"""
        try:
            with st.spinner("返信文を作成中..."):
                result = generate_text(prompt)
            st.session_state["email_result"] = result
        except Exception as exc:
            show_error(exc)

if "email_result" in st.session_state:
    st.divider()
    st.text_area("生成された返信文", value=st.session_state["email_result"], height=300)
