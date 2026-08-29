import streamlit as st

from lib.gemini_client import generate_text
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="台本作成", page_icon="🎬", layout="wide")
st.title("🎬 台本作成")
st.caption("動画・音声コンテンツ用の台本を作成します。")

check_api_key()

with st.form("script_form"):
    theme = st.text_input("テーマ・タイトル")
    duration = st.selectbox("尺の目安", ["30秒〜1分（ショート動画）", "3〜5分", "8〜10分", "15分以上"])
    audience = st.text_input("想定視聴者", placeholder="例: プログラミング初心者")
    key_points = st.text_area("伝えたいポイント（箇条書きでOK）", height=120)
    structure = st.multiselect(
        "含めたい構成要素",
        ["冒頭フック", "自己紹介", "本編（複数セクション）", "まとめ", "CTA（チャンネル登録・購入誘導など）"],
        default=["冒頭フック", "本編（複数セクション）", "まとめ", "CTA（チャンネル登録・購入誘導など）"],
    )
    submitted = st.form_submit_button("台本を生成する", type="primary")

if submitted:
    if not theme or not key_points:
        st.error("テーマと伝えたいポイントを入力してください。")
    else:
        prompt = f"""以下の条件で動画・音声コンテンツの台本を作成してください。

# テーマ
{theme}

# 尺の目安
{duration}

# 想定視聴者
{audience or "指定なし"}

# 伝えたいポイント
{key_points}

# 含めたい構成要素
{', '.join(structure) if structure else "自由に構成してください"}

# 出力形式
セクションごとに見出しを付け、話し言葉のセリフ調で書いてください。
各セクションの目安の秒数・分数も併記してください。
"""
        try:
            with st.spinner("台本を作成中..."):
                result = generate_text(prompt, temperature=0.8)
            st.session_state["script_result"] = result
        except Exception as exc:
            show_error(exc)

if "script_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["script_result"])
    st.download_button(
        "台本をダウンロード",
        data=st.session_state["script_result"],
        file_name="script.txt",
        mime="text/plain",
    )
