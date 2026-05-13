from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    language: str | None
    language_probability: float | None

class FasterWhisperTranscriber:
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
        beam_size: int = 5,
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.beam_size = beam_size
        self._model = None

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        model = self._get_model()
        segments, info = model.transcribe(str(audio_path), beam_size=self.beam_size)
        text = " ".join(segment.text.strip() for segment in segments if segment.text.strip()).strip()
        return TranscriptionResult(
            text=text,
            language=getattr(info, "language", None),
            language_probability=getattr(info, "language_probability", None),
        )

    def _get_model(self):
        if self._model is None:
            from faster_whisper import WhisperModel

            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )
        return self._model
