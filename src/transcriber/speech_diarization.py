import os
import scipy.io.wavfile
from typing import List, Tuple
from pyannote.audio import Pipeline

from huggingface_hub import configure_http_backend
from src.transcriber.utils import backend_factory

# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import sys

# sys.path.append(
#     os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# )


class SpeechDiarizer:
    """
    Speaker segmentation class using pyannote.audio for speaker diarization.
    """

    def __init__(self, hf_token: str, disable_ssl=False):
        """
        Initialize the pyannote.audio speaker diarization pipeline.
        You need a Hugging Face token with access to pyannote models.
        """
        if disable_ssl:
            configure_http_backend(backend_factory=backend_factory)

        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speech-separation-ami-1.0", use_auth_token=hf_token
        )

    def execute(self, audio_path: str) -> Tuple[float, float]:
        """
        Segments the audio file into speaker turns.
        Returns a list of tuples: (start_time, end_time, speaker_label)
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        diarization, sources = self.pipeline(audio_path)
        return (diarization, sources)


if __name__ == "__main__":

    # Example usage:
    hf_token = ""
    diarizer = SpeechDiarizer(hf_token, disable_ssl=True)
    diarizer.execute("recording.wav")
    # Each segment: (start_time, end_time, speaker_label)
