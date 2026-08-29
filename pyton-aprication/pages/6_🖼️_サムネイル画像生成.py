import streamlit as st

from lib.gemini_client import generate_thumbnail
from lib.ui import check_api_key, show_error

st.set_page_config(page_title="サムネイル画像生成", page_icon="🖼️", layout="wide")
st.title("🖼️ サムネイル画像生成")
st.caption("Gemini画像生成モデルでYouTube・ブログ用のサムネイル画像を作成します。")

check_api_key()

with st.form("thumbnail_form"):
    title_text = st.text_input("サムネイルに入れたいタイトル文言（任意）", placeholder="例: 初心者でもわかる！Python入門")
    description = st.text_area(
        "画像の内容・雰囲気の説明",
        height=120,
        placeholder="例: プログラミングを勉強するイメージ、明るく親しみやすい色合い、驚いた表情の人物イラスト",
    )
    style = st.selectbox(
        "スタイル",
        ["写真風でリアル", "フラットイラスト", "ポップでカラフル", "ビジネス・シンプル", "アニメ風"],
    )
    aspect = st.selectbox("縦横比", ["16:9（YouTube横型）", "9:16（ショート・縦型）", "1:1（正方形）"])
    submitted = st.form_submit_button("サムネイルを生成する", type="primary")

if submitted:
    if not description:
        st.error("画像の内容・雰囲気の説明を入力してください。")
    else:
        prompt_parts = [
            f"サムネイル画像を生成してください。縦横比は{aspect.split('（')[0]}。",
            f"スタイル: {style}。",
            f"内容: {description}",
        ]
        if title_text:
            prompt_parts.append(f"画像内に大きく読みやすい日本語のテキストで「{title_text}」という文言を目立つように配置してください。")
        prompt_parts.append("クリックしたくなるような、目を引く構図と配色にしてください。")
        prompt = "\n".join(prompt_parts)

        try:
            with st.spinner("画像を生成中...（数十秒かかる場合があります）"):
                image_path = generate_thumbnail(prompt)
            st.session_state["thumbnail_path"] = str(image_path)
        except Exception as exc:
            show_error(exc)

if "thumbnail_path" in st.session_state:
    st.divider()
    st.image(st.session_state["thumbnail_path"], caption="生成されたサムネイル")
    with open(st.session_state["thumbnail_path"], "rb") as f:
        st.download_button("画像をダウンロード", data=f.read(), file_name="thumbnail.png", mime="image/png")
    st.caption(f"保存先: {st.session_state['thumbnail_path']}")
