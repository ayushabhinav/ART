import sounddevice as sd
import numpy as np
import threading
import time
import sys
from scipy.io.wavfile import write
from src.widgets.save_file_dialog import SaveFileDialog
from src.widgets.error_message_box import ErrorMessageBox
from src.transcriber.whisper_transcriber import AudioTranscriber
from PyQt5.QtCore import QThread, pyqtSignal, QObject

_transcription_thread = None
_worker = None
_recording_thread = None
_recording = False
_audio_data = []


def _record_audio(device=None):
    global _recording, _audio_data
    _audio_data = []
    samplerate = 44100
    duration = 3600  # max duration 1 hour

    def callback(indata, frames, time, status):
        if _recording:
            _audio_data.append(indata.copy())

    try:
        with sd.InputStream(
            samplerate=samplerate, channels=1, callback=callback, device=device
        ):
            while _recording:
                time.sleep(0.1)
    except Exception as e:
        ErrorMessageBox.show_error(
            f"Error starting recording: {e}", title="Recording Error"
        )


def start_recording_action(recording_status_label, button, device=None):
    global _recording, _recording_thread
    button.setText("Stop Recording")
    recording_status_label.setVisible(True)
    _recording = True
    _recording_thread = threading.Thread(
        target=_record_audio, kwargs={"device": device}
    )
    try:
        _recording_thread.start()
    except Exception as e:
        stop_recording_action(recording_status_label, button)


def stop_recording_action(recording_status_label, button, parent=None, device=None):
    global _recording, _recording_thread, _audio_data
    button.setText("Start Recording")
    recording_status_label.setVisible(False)
    _recording = False
    if _recording_thread is not None:
        _recording_thread.join()
        _recording_thread = None
    if _audio_data:
        print(f"len audio data: {len(_audio_data)}")
        audio = np.concatenate(_audio_data, axis=0)
        if parent is not None:
            filename = SaveFileDialog.get_save_file(parent, "output.wav")
        else:
            filename = "output.wav"
        if filename:
            write(filename, 44100, audio)


class TranscriptionWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        print(f"file path:{self.file_path}", file=sys.stdout)

    def run(self):
        print("transcriber run", file=sys.stdout)
        try:
            transcriber = AudioTranscriber(disable_SSL=True)
            print("transcriber initialized", file=sys.stdout)
            text = transcriber.transcribe(self.file_path)
            print(f"text: {text}", file=sys.stdout)
            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))


def transcript_action(fs_tree_widget, banner_widget=None):
    global _transcription_thread, _worker
    selected_file_path = getattr(fs_tree_widget, "selected_file_path", None)
    if selected_file_path is None:
        ErrorMessageBox.show_error("No file selected.", title="Transcript Error")
        return
    if not selected_file_path.lower().endswith(".wav"):
        ErrorMessageBox.show_error(
            "Selected file is not a WAV file.", title="Transcript Error"
        )
        return
    if banner_widget is not None:
        print("[DEBUG] Setting banner: Transcription is in progress...")
        banner_widget.setText("Transcription is in progress...")
        banner_widget.setVisible(True)

    def on_finished(text):
        print("[DEBUG] on_finished called")
        print(f"Transcription:\n{text}")
        if banner_widget is not None:
            print("[DEBUG] Setting banner: Transcription is complete.")
            banner_widget.setText("Transcription is complete.")
        # Add logic here to display the transcription in your UI

    def on_error(error_msg):
        print("[DEBUG] on_error called")
        ErrorMessageBox.show_error(
            f"Transcription failed: {error_msg}", title="Transcript Error"
        )
        if banner_widget is not None:
            print("[DEBUG] Setting banner: Transcription failed.")
            banner_widget.setText("Transcription failed.")

    _worker = TranscriptionWorker(selected_file_path)
    _transcription_thread = QThread()
    _worker.moveToThread(_transcription_thread)

    _transcription_thread.started.connect(_worker.run)

    _worker.finished.connect(on_finished)
    _worker.finished.connect(_transcription_thread.quit)

    _worker.error.connect(on_error)
    _worker.error.connect(_transcription_thread.quit)

    _transcription_thread.start()


def summary_action():
    # Add logic to show summary here
    print("Summary button clicked")
