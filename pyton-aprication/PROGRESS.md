# AIライティングツール 進捗記録

## 概要
個人用のAIライティングツール（Python / Streamlit / Gemini API）。
複数のライティング系AI機能を1つのアプリにまとめる。

## 機能一覧（合意済み）
1. ブログ記事ライター
2. メール返信文ジェネレーター
3. 文章要約
4. タイトル・説明文・ハッシュタグ（カンマ区切り）・タグ（カンマ区切り）生成
5. サムネイル画像生成（Gemini画像生成モデル / Nano Banana）
6. 台本作成
7. （追加）文章校正・リライト
8. （追加）キャッチコピー・見出し生成

## 技術スタック
- Python 3.11+
- Streamlit（マルチページ構成）
- google-genai SDK（テキスト生成 + 画像生成を1つのAPIキーで）
- python-dotenv（.envでAPIキー管理、gitignore対象）

## フェーズ計画
- [x] Phase 1: プロジェクト雛形（requirements.txt, .env.example, .gitignore, フォルダ構成, Geminiクライアント共通化）
- [x] Phase 2〜5: 全8機能のページ作成（ブログ/メール返信/要約/校正リライト/タイトル説明文タグ生成/サムネイル画像生成/台本作成/キャッチコピー生成）
- [x] Phase 6: pip install、streamlit run で実際に起動しブラウザで各画面を確認、README作成

## Phase 1〜5完了メモ（2026-08-23）
- 完了したこと: プロジェクト雛形一式 + 8機能全ページを実装
- 変更したファイル:
  - requirements.txt, .env.example, .gitignore
  - lib/config.py, lib/gemini_client.py, lib/ui.py
  - app.py
  - pages/1_📝_ブログ記事ライター.py
  - pages/2_📧_メール返信文.py
  - pages/3_📄_文章要約.py
  - pages/4_✨_校正リライト.py
  - pages/5_🏷️_タイトル説明文タグ生成.py
  - pages/6_🖼️_サムネイル画像生成.py
  - pages/7_🎬_台本作成.py
  - pages/8_💡_キャッチコピー生成.py
- テスト結果: 未実施（Phase 6でstreamlit run実行して確認予定）
- 次にやること: pip install -r requirements.txt → streamlit run app.py → ブラウザで起動確認。APIキー未設定なので生成系ボタンは警告表示までの確認になる見込み。
- 次に打つ具体的なコマンド:
  ```
  cd "C:\Users\khiro\OneDrive\Desktop\shincode-hp\pyton-aprication"
  pip install -r requirements.txt
  streamlit run app.py
  ```

## Phase 6完了メモ（2026-08-23）
- 完了したこと: 依存関係インストール（.venv）、streamlit run で実起動、Chromeブラウザで実際の画面遷移・入力・生成ボタン押下まで確認。README.md作成。
- テスト結果（実データでの動作確認、4件実施）:
  1. ブログ記事ライター: 実テーマ「自宅でできる簡単な筋トレ習慣の始め方」で記事生成 → 成功（見出し構成・本文・まとめまで正常出力、ダウンロードボタンも表示）
  2. タイトル・説明文・タグ生成: 実データで生成 → JSON解析成功、タイトル案5件・説明文・ハッシュタグ・タグすべて正しく表示
  3. 台本作成: 実データで生成 → 成功（複数構成要素の指定も反映）
  4. サムネイル画像生成: 生成試行 → **失敗**（429 RESOURCE_EXHAUSTED、画像生成モデルgemini-2.5-flash-preview-imageの無料枠クォータが0のため）。エラーハンドリング自体は正しく動作し、画面にエラーメッセージを表示。
  - 未実施: メール返信文、文章要約、校正・リライト、キャッチコピー生成は画面表示のみ確認（フォーム自体はブログ記事ライターと同一パターンのため未実行）。
- 判明した注意点:
  - サムネイル画像生成を使うには、Google AI Studio側でこのAPIキーのプロジェクトに課金設定（有料プラン）が必要。README.mdに注記済み。
  - テスト時のブラウザ（Claude in Chrome拡張経由）で、日本語テキストの一部が表示上わずかに変化する現象があった（例: 「文章要約」→「論文要約」、「初心者ブロガー」→「ブロガー初心者」）。ソースコードを直接確認し正しいことを確認済みのため、アプリのバグではなくブラウザ環境側の表示問題と判断。ユーザーの通常のブラウザでは問題ない見込み。
- 次にやること: なし（8機能すべて実装・起動確認済み、コア機能は実データで動作確認済み）。ユーザーが実際に使う中で、サムネイル画像生成を使いたい場合はAPI課金設定が必要な旨を伝える。
- 次に打つ具体的なコマンド: 追加要望があれば都度対応。再起動する場合は以下。
  ```
  cd "C:\Users\khiro\OneDrive\Desktop\shincode-hp\pyton-aprication"
  .venv/Scripts/streamlit run app.py
  ```
