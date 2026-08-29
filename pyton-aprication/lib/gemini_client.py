"""Gemini APIとのやり取りをまとめる共通クライアント。"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

from google import genai
from google.genai import types

from lib.config import GEMINI_API_KEY, IMAGE_MODEL, TEXT_MODEL, THUMBNAIL_DIR


class GeminiNotConfiguredError(RuntimeError):
    """APIキーが未設定のときに発生するエラー。"""


def _get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise GeminiNotConfiguredError(
            "GEMINI_API_KEYが設定されていません。.envファイルにAPIキーを設定してください。"
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, system_instruction: str | None = None, temperature: float = 0.9) -> str:
    """テキスト生成の共通関数。プロンプトを渡して生成結果の文字列を返す。"""
    client = _get_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt,
        config=config,
    )
    return (response.text or "").strip()


def generate_thumbnail(prompt: str, filename_prefix: str = "thumbnail") -> Path:
    """Gemini画像生成モデルでサムネイル画像を生成し、outputフォルダに保存してパスを返す。"""
    client = _get_client()
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
    )

    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None) is not None:
            timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = THUMBNAIL_DIR / f"{filename_prefix}_{timestamp}.png"
            file_path.write_bytes(part.inline_data.data)
            return file_path

    raise RuntimeError("画像データが生成結果に含まれていませんでした。プロンプトを変えて再試行してください。")
