import os
import torch
import librosa
import logging
from transformers import WhisperProcessor, WhisperForConditionalGeneration

import requests
from huggingface_hub import configure_http_backend


def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session


class AudioTranscriber:
    def __init__(self, model_name="openai/whisper-base", disable_SSL=False):
        self.logger = logging.getLogger(__class__.__name__)
        if disable_SSL:
            configure_http_backend(backend_factory=backend_factory)
            self.logger.info("✓ HTTP backend configured (SSL verification disabled)")
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        audio, sr = librosa.load(audio_path, sr=16000)
        input_features = self.processor(
            audio, sampling_rate=16000, return_tensors="pt"
        ).input_features
        input_features = input_features.to(self.device)
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(
            predicted_ids, skip_special_tokens=True
        )[0]
        return transcription


if __name__ == "__main__":
    # Example usage:
    transcriber = AudioTranscriber(disable_SSL=True)
    text = transcriber.transcribe("C:\\softwares\\venv\\gui_development\\output.wav")
    print(text)
    # Make sure your audio file is mono and 16kHz for best results.
    # You may need ffmpeg or sox to convert formats if needed.
    # Hugging Face Whisper models require internet for first download.
    # For GPU support, install torch with CUDA if available.
