"""アプリ全体の設定値をまとめるモジュール。"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
THUMBNAIL_DIR = OUTPUT_DIR / "thumbnails"

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"

THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
