import os

# import sys

# sys.path.append(
#     os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# )


from typing import Optional, List, Tuple
from src.transcriber.transcripts import transcripts, speaker_dict, Speaker
from src.transcriber.speech_diarization import SpeechDiarizer
from src.transcriber.whisper_transcriber import AudioTranscriber


class Transcriber:
    @classmethod
    def transcribe(
        cls,
        audio_path: str,
        hf_token: str,
        disable_SSL: bool = False,
    ):
        # Check if audio file exists
        if not os.path.exists(audio_path):
            return "Audio file not found."

        # Perform diarization

        diarizer = SpeechDiarizer(hf_token, disable_ssl=disable_SSL)
        diarization, sources = diarizer.execute(audio_path)

        # import pickle

        # diarization = pickle.load(
        #     open(
        #         "C:\\softwares\\venv\\gui_development\\src\\transcriber\\test_folder\\diarization.p",
        #         "rb",
        #     )
        # )
        # sources = pickle.load(
        #     open(
        #         "C:\\softwares\\venv\\gui_development\\src\\transcriber\\test_folder\\separated_speakers.p",
        #         "rb",
        #     )
        # )

        audio_transcriber = AudioTranscriber(disable_SSL=disable_SSL)

        for seg, _, sp in diarization.itertracks(yield_label=True):
            print(f"Segment: {seg}, Speaker: {sp}")
            if sp not in speaker_dict:
                new_speaker = Speaker(id=sp)
                speaker_dict[sp] = new_speaker
            transcript = audio_transcriber._transcribe(
                sources[
                    int(seg.start * 16000) : int(seg.end * 16000),
                    int(sp.split("_")[-1]),
                ],
            )
            transcripts.add_transcript(transcript, speaker_dict[sp])
        # Add actual transcription logic here
        # return (speakers, transcripts) Donot return as both are module variables (singleton pattern)


if __name__ == "__main__":
    Transcriber.transcribe(
        audio_path="C:\\softwares\\venv\\gui_development\\recording.wav",
        hf_token="",
        disable_SSL=True,
    )
