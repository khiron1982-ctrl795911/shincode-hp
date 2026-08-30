"""要約→台本作成→タイトル/説明文/タグ生成をボタン1つで一気通貫に行うページ。

長尺動画スタジオへの取り込み（AiWritingScriptImportタスク）を前提に、
台本は見出しラベルや目安時間などの余計な文字を含まないクリーンな形式で生成する。
"""
import json

import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="一気通貫パイプライン", page_icon="🚀", layout="wide")
st.title("🚀 一気通貫パイプライン")
st.caption("元の文章から、要約→台本作成→タイトル・説明文・タグ生成までを1回でまとめて行います。")

check_api_key()

with st.form("pipeline_form"):
    source_text = st.text_area("元になる文章（記事・メモ・調査結果など）", height=250)
    theme_hint = st.text_input("テーマ・タイトルのヒント（任意）", placeholder="例: 生成AIの人事活用")
    duration = st.selectbox("尺の目安", ["30秒〜1分（ショート動画）", "3〜5分", "8〜10分", "15分以上"], index=1)
    audience = st.text_input("想定視聴者（任意）", placeholder="例: 人事・バックオフィス担当者")
    submitted = st.form_submit_button("一気通貫で作成する", type="primary")


def strip_code_fence(text: str) -> str:
    return text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()


if submitted:
    if not source_text:
        st.error("元になる文章を入力してください。")
    else:
        try:
            # 1. 要約
            with st.spinner("① 要約中..."):
                summary_prompt = f"""以下の文章を、動画の台本の素材として使える形で要約してください。

# 元の文章
{source_text}

# 条件
- 300〜500字程度
- 文章形式（箇条書きにしない）
- 重要なポイント・数字・固有名詞は漏らさない
"""
                summary = generate_text(summary_prompt, temperature=0.3)
                st.session_state["pipeline_summary"] = summary

            # 2. 台本作成（見出し・目安時間なしのクリーンな形式で生成）
            with st.spinner("② 台本作成中..."):
                script_prompt = f"""次のナレーション原稿を書いてください。これは動画の音声としてそのまま読み上げられます。

# 元になる要約
{summary}

# テーマ・タイトルのヒント
{theme_hint or "指定なし"}

# 尺の目安
{duration}

# 想定視聴者
{audience or "指定なし"}

# 出力形式（重要・必ず守ること。違反すると音声合成にそのまま使えず困る）
- 出力は読み上げ用のナレーション文だけにする。それ以外の文字は1文字も含めない
- 「はい、承知いたしました」「〜の台本を作成します」のように、依頼内容や作業内容を復唱・確認する文は書かない
- 「【動画・音声コンテンツ台本：〜】」のような、タイトルや見出しに見える【】・[]・「」で囲んだ文字列を先頭やどこにも書かない
- 「##」「###」のような見出し記号や、「本編1：」「まとめ：」「冒頭フック：」のようなセクションラベルは書かない
- 「(目安時間：0分30秒)」のような時間の注記は書かない
- 「---」のような区切り線も書かない
- 太字（**）などのMarkdown記法も使わない
- 1行目から、話者が実際に話す言葉そのものを書き始めること
- 段落と段落の間は空行で区切るだけにする
"""
                script = generate_text(script_prompt, temperature=0.8)
                st.session_state["pipeline_script"] = script

            # 3. タイトル・説明文・タグ生成
            with st.spinner("③ タイトル・説明文・タグ生成中..."):
                meta_prompt = f"""以下の動画台本について、YouTube向けのメタ情報を作成してください。

# 台本
{script}

# 出力形式
必ず以下のJSON形式のみで出力してください。説明文やコードブロックの記号(```)は不要です。

{{
  "titles": ["タイトル案1", "タイトル案2", "タイトル案3", "タイトル案4", "タイトル案5"],
  "description": "説明文（YouTubeに適した長さと文体で、120〜300字程度）",
  "hashtags": "ハッシュタグをカンマ区切りで（#付き、5〜10個）"
}}
"""
                meta_result = generate_text(meta_prompt, temperature=0.8)
                meta_data = json.loads(strip_code_fence(meta_result))
                st.session_state["pipeline_meta"] = meta_data

        except Exception as exc:
            show_error(exc)

if "pipeline_script" in st.session_state and "pipeline_meta" in st.session_state:
    st.divider()

    st.subheader("① 要約")
    st.write(st.session_state["pipeline_summary"])

    st.subheader("② 台本")
    st.text_area("台本", value=st.session_state["pipeline_script"], height=300, label_visibility="collapsed")

    meta = st.session_state["pipeline_meta"]
    st.subheader("③ タイトル案（使うものを1つ選んでください）")
    chosen_title = st.selectbox("タイトル", meta.get("titles", []), label_visibility="collapsed")

    st.subheader("説明文")
    description = st.text_area("説明文", value=meta.get("description", ""), height=100, label_visibility="collapsed")

    st.subheader("ハッシュタグ")
    hashtags = st.text_area("ハッシュタグ", value=meta.get("hashtags", ""), height=60, label_visibility="collapsed")

    st.divider()
    output = {
        "title": chosen_title,
        "script": st.session_state["pipeline_script"],
        "description": description,
        "hashtags": hashtags,
    }
    st.download_button(
        "長尺動画スタジオ用にダウンロード（.json）",
        data=json.dumps(output, ensure_ascii=False, indent=2),
        file_name="pipeline_output.json",
        mime="application/json",
    )
    st.caption(
        "ダウンロードした.jsonファイルを `VIDEO\\_台本受け取り` フォルダに置くと、"
        "AiWritingScriptImportタスクが自動で長尺動画スタジオの下書きに登録します。"
    )
