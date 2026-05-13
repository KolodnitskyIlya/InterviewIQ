import base64
from pathlib import Path
from uuid import uuid4
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from app.core.config import settings

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
        self.ensure_bucket()
        audio_bytes = base64.b64decode(audio_base64)
        extension = file_name.rsplit(".", 1)[-1] if "." in file_name else "m4a"
        object_key = f"users/{user_id}/sessions/{session_id}/questions/{question_id}/{uuid4().hex}.{extension}"

        self.client.put_object(
            Bucket=settings.s3_bucket,
            Key=object_key,
            Body=audio_bytes,
            ContentType=content_type,
        )

        public_base = settings.s3_public_url.rstrip("/")
        return {
            "audio_id": object_key,
            "audio_url": f"{public_base}/{settings.s3_bucket}/{object_key}",
            "content_type": content_type,
        }

    def download_audio(self, audio_id: str, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(settings.s3_bucket, audio_id, str(destination))
        return destination

audio_storage = AudioStorage()
