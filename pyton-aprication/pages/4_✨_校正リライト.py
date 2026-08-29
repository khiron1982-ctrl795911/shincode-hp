import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="校正・リライト", page_icon="✨", layout="wide")
st.title("✨ 文章校正・リライト")
st.caption("誤字脱字のチェックや、トーン変更・言い回しの改善を行います。")

check_api_key()

with st.form("rewrite_form"):
    source_text = st.text_area("元の文章", height=200)
    mode = st.selectbox(
        "モード",
        ["誤字脱字・文法チェックのみ", "より丁寧な文章にリライト", "よりカジュアルにリライト", "簡潔に短くリライト", "自由指定"],
    )
    free_instruction = ""
    if mode == "自由指定":
        free_instruction = st.text_input("どのように直してほしいか指定してください")
    submitted = st.form_submit_button("実行する", type="primary")

if submitted:
    if not source_text:
        st.error("元の文章を入力してください。")
    else:
        instruction = free_instruction if mode == "自由指定" else mode
        prompt = f"""以下の文章を校正・リライトしてください。

# 元の文章
{source_text}

# 指示
{instruction}

# 出力形式
1. 修正後の文章
2. 主な変更点の簡単な説明（箇条書き）
"""
        try:
            with st.spinner("校正・リライト中..."):
                result = generate_text(prompt, temperature=0.5)
            st.session_state["rewrite_result"] = result
        except Exception as exc:
            show_error(exc)

if "rewrite_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["rewrite_result"])
