from transformers import pipeline
from huggingface_hub import configure_http_backend
from src.transcriber.utils import backend_factory


class MeetingSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn", disable_SSL=False):
        if disable_SSL:
            configure_http_backend(backend_factory=backend_factory)

        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text, max_length=1000, min_length=25):
        processed_text = text.replace(":", " said")
        if len(text) < 4500:
            summary = self.summarizer(
                processed_text, max_length=max_length, min_length=min_length
            )
            return summary[0]["summary_text"]

        # If text is too long, summarize in chunks
        chunk_size = 4000
        chunks = [
            processed_text[i : i + chunk_size]
            for i in range(0, len(processed_text), chunk_size)
        ]
        summaries = [
            self.summarizer(chunk, max_length=max_length, min_length=min_length)[0][
                "summary_text"
            ]
            for chunk in chunks
        ]
        return " ".join(summaries)
