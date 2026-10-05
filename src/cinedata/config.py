import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "openrouter/free").strip()

if not OPENROUTER_API_KEY:
    raise ValueError(
        "Configure OPENROUTER_API_KEY no arquivo .env da raiz do projeto."
    )

if not MODEL_NAME:
    raise ValueError(
        "Configure MODEL_NAME no arquivo .env da raiz do projeto."
    )