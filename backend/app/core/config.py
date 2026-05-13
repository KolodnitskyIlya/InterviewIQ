from dataclasses import dataclass
import os
from pathlib import Path
import sys
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BASE_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

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
    s3_endpoint_url: str = os.getenv("S3_ENDPOINT_URL", "http://127.0.0.1:9000")
    s3_public_url: str = os.getenv("S3_PUBLIC_URL", "http://127.0.0.1:9000")
    s3_access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    s3_secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    s3_bucket: str = os.getenv("S3_BUCKET", "interviewiq-audio")
    s3_region: str = os.getenv("S3_REGION", "us-east-1")
    analyzer_provider: str = os.getenv("ANALYZER_PROVIDER", "baseline")
    gigachat_credentials: str = os.getenv("GIGACHAT_CREDENTIALS", "")
    gigachat_model: str = os.getenv("GIGACHAT_MODEL", "GigaChat")
    gigachat_scope: str = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    gigachat_verify_ssl_certs: bool = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "false").lower() == "true"
    analyzer_timeout_sec: int = int(os.getenv("ANALYZER_TIMEOUT_SEC", "20"))
    max_answer_chars: int = int(os.getenv("MAX_ANSWER_CHARS", "6000"))
    transcriber_provider: str = os.getenv("TRANSCRIBER_PROVIDER", "faster-whisper")
    whisper_model_size: str = os.getenv("WHISPER_MODEL_SIZE", "base")
    whisper_device: str = os.getenv("WHISPER_DEVICE", "cpu")
    whisper_compute_type: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

settings = Settings()
