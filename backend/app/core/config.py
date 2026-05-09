from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / "api.env")

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "InterviewIQ API")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://interviewiq:password@localhost:5432/interviewiq",
    )

settings = Settings()
