import json

import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="タイトル・説明文・タグ生成", page_icon="🏷️", layout="wide")
st.title("🏷️ タイトル・説明文・ハッシュタグ・タグ生成")
st.caption("動画やブログの内容から、タイトル案・説明文・ハッシュタグ・タグをまとめて生成します。")

check_api_key()

with st.form("meta_form"):
    content_summary = st.text_area(
        "コンテンツの内容（台本の概要、動画の内容、記事の要点など）",
        height=200,
        placeholder="例: 初心者向けにPythonの環境構築を解説する10分動画。VSCodeのインストールから最初のプログラム実行まで。",
    )
    platform = st.selectbox("用途", ["YouTube", "ブログ", "Instagram", "X(Twitter)", "TikTok"])
    title_count = st.slider("タイトル案の数", min_value=3, max_value=10, value=5)
    submitted = st.form_submit_button("生成する", type="primary")

if submitted:
    if not content_summary:
        st.error("コンテンツの内容を入力してください。")
    else:
        prompt = f"""以下のコンテンツについて、{platform}向けのメタ情報を作成してください。

# コンテンツの内容
{content_summary}

# 出力形式
必ず以下のJSON形式のみで出力してください。説明文やコードブロックの記号(```)は不要です。

{{
  "titles": ["タイトル案1", "タイトル案2", ... ({title_count}個)],
  "description": "説明文（{platform}に適した長さと文体で、120〜300字程度）",
  "hashtags": "ハッシュタグをカンマ区切りで（#付き、5〜10個）",
  "tags": "タグをカンマ区切りで（#なし、検索されやすいキーワード、5〜10個）"
}}
"""
        try:
            with st.spinner("生成中..."):
                result = generate_text(prompt, temperature=0.8)
            cleaned = result.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(cleaned)
            st.session_state["meta_result"] = data
            st.session_state["meta_raw"] = None
        except json.JSONDecodeError:
            st.session_state["meta_result"] = None
            st.session_state["meta_raw"] = result
        except Exception as exc:
            show_error(exc)

if st.session_state.get("meta_result"):
    data = st.session_state["meta_result"]
    st.divider()
    st.subheader("タイトル案")
    for i, t in enumerate(data.get("titles", []), start=1):
        st.write(f"{i}. {t}")

    st.subheader("説明文")
    st.text_area("説明文", value=data.get("description", ""), height=120, label_visibility="collapsed")

    st.subheader("ハッシュタグ（カンマ区切り）")
    st.text_area("ハッシュタグ", value=data.get("hashtags", ""), height=80, label_visibility="collapsed")

    st.subheader("タグ（カンマ区切り）")
    st.text_area("タグ", value=data.get("tags", ""), height=80, label_visibility="collapsed")
elif st.session_state.get("meta_raw"):
    st.divider()
    st.warning("整形に失敗したため、生成結果をそのまま表示します。")
    st.text_area("生成結果", value=st.session_state["meta_raw"], height=300)
