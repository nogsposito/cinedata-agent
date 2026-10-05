import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY não encontrada no .env."
    )

if not MODEL_NAME:
    raise ValueError(
        "MODEL_NAME não encontrado no .env."
    )