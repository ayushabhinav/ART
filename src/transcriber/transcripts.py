from dataclasses import dataclass
from typing import Optional


@dataclass
class Speaker:
    id: str
    name: Optional[str] = None


class Transcripts:
    def __init__(self):
        self.transcripts = []

    def add_transcript(self, transcript, speaker):
        self.transcripts.append({"transcript": transcript, "speaker": speaker})

    def remove_all(self):
        self.transcripts.clear()

    def __str__(self):
        return "\n".join(
            f"{entry.get('speaker').name if entry.get('speaker').name else entry.get('speaker').id}: {entry['transcript']}"
            for entry in self.transcripts
        )


speaker_dict = dict()
transcripts = Transcripts()
summarized_transcripts = Transcripts()
