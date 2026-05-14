import base64
import logging
from pathlib import Path
from uuid import uuid4
import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError
from app.core.config import settings

logger = logging.getLogger("interviewiq.audio_storage")
LOCAL_AUDIO_DIR = Path(__file__).resolve().parents[2] / ".audio_uploads"

class AudioStorage:
    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=Config(signature_version="s3v4"),
        )

    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=settings.s3_bucket)
        except ClientError:
            self.client.create_bucket(Bucket=settings.s3_bucket)

    def upload_base64_audio(
        self,
        user_id: str,
        session_id: str,
        question_id: str,
        file_name: str,
        content_type: str,
        audio_base64: str,
    ) -> dict[str, str]:
        audio_bytes = base64.b64decode(audio_base64)
        extension = file_name.rsplit(".", 1)[-1] if "." in file_name else "m4a"
        object_key = f"users/{user_id}/sessions/{session_id}/questions/{question_id}/{uuid4().hex}.{extension}"

        try:
            self.ensure_bucket()
            self.client.put_object(
                Bucket=settings.s3_bucket,
                Key=object_key,
                Body=audio_bytes,
                ContentType=content_type,
            )
        except (BotoCoreError, ClientError) as exc:
            logger.warning("S3 audio upload failed; storing audio locally", exc_info=exc)
            return self._store_local_audio(
                object_key=object_key,
                audio_bytes=audio_bytes,
                content_type=content_type,
            )

        public_base = settings.s3_public_url.rstrip("/")
        return {
            "audio_id": object_key,
            "audio_url": f"{public_base}/{settings.s3_bucket}/{object_key}",
            "content_type": content_type,
        }

    def download_audio(self, audio_id: str, destination: Path) -> Path:
        if audio_id.startswith("local/"):
            source = LOCAL_AUDIO_DIR / audio_id.removeprefix("local/")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
            return destination

        destination.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(settings.s3_bucket, audio_id, str(destination))
        return destination

    def _store_local_audio(
        self,
        object_key: str,
        audio_bytes: bytes,
        content_type: str,
    ) -> dict[str, str]:
        local_path = LOCAL_AUDIO_DIR / object_key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(audio_bytes)
        audio_id = f"local/{object_key}"
        return {
            "audio_id": audio_id,
            "audio_url": audio_id,
            "content_type": content_type,
        }

audio_storage = AudioStorage()
