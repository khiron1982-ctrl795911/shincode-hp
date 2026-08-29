# AIライティングツール

個人用のAIライティング支援アプリ。Python / Streamlit / Gemini APIで構築。

## 機能

| 機能 | 説明 |
| --- | --- |
| 📝 ブログ記事ライター | テーマ・キーワードからブログ記事を執筆 |
| 📧 メール返信文 | 受信メールの内容から返信文の下書きを作成 |
| 📄 文章要約 | 長い文章を指定した長さ・形式で要約 |
| ✨ 校正・リライト | 誤字脱字修正やトーン変更 |
| 🏷️ タイトル・説明文・タグ生成 | タイトル案・説明文・ハッシュタグ（カンマ区切り）・タグ（カンマ区切り）をまとめて生成 |
| 🖼️ サムネイル画像生成 | Gemini画像生成モデル（gemini-2.5-flash-image）でサムネイル画像を作成 |
| 🎬 台本作成 | 動画・音声コンテンツ用の台本を作成 |
| 💡 キャッチコピー生成 | キャッチコピー・見出し案を複数生成 |

## セットアップ

```bash
python -m venv .venv
.venv/Scripts/activate   # Windows
pip install -r requirements.txt
```

`.env.example` をコピーして `.env` を作成し、`GEMINI_API_KEY` に [Google AI Studio](https://aistudio.google.com/apikey) で取得したAPIキーを設定してください。

## 起動方法

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

## 注意事項

- サムネイル画像生成（Gemini画像生成モデル）は無料枠のクォータが0の場合があります。生成時に `429 RESOURCE_EXHAUSTED` エラーが出る場合は、[Google AI Studio](https://aistudio.google.com/) でプロジェクトの請求設定（有料プラン）を確認してください。テキスト生成系の機能（記事執筆・要約など）は無料枠でも動作します。
- 生成されたサムネイル画像は `output/thumbnails/` に保存されます。
