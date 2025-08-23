import os
import sounddevice as sd
from widgets.status import StatusLabel
from src.widgets.summary_button import SummaryButton
from src.widgets.transcript_button import TranscriptButton
from src.widgets.filesystem_tree import FileSystemTreeWidget
from src.widgets.toggle_recording_button import ToggleRecordingButton

from src.actions import (
    start_recording_action,
    stop_recording_action,
    transcript_action,
    summary_action,
    save_transcript,
    handle_settings_action,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QComboBox,
    QTextEdit,
    QPushButton,
    QDialog,
    QLineEdit,
)

from src.transcriber.transcripts import transcripts, speaker_dict


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meeting Recorder")
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "app_icon.png"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(700, 400)
        main_layout = QVBoxLayout()

        self.status_label = StatusLabel()
        main_layout.addWidget(self.status_label)

        # Audio device dropdown and label in horizontal layout
        device_layout = QHBoxLayout()
        self.device_dropdown_label = QLabel("Select Audio Device:")
        self.device_dropdown = QComboBox()
        self.device_dropdown.setMinimumWidth(120)
        self.device_dropdown.setMaximumWidth(350)
        device_layout.addWidget(self.device_dropdown_label)
        device_layout.addWidget(self.device_dropdown)
        device_layout.addStretch(1)
        self.settings_btn = QPushButton("Settings")
        device_layout.addWidget(self.settings_btn)
        main_layout.addLayout(device_layout)

        self.devices = sd.query_devices()
        self.input_devices = []
        for i, d in enumerate(self.devices):
            try:
                max_input = (
                    d["max_input_channels"]
                    if isinstance(d, dict) and "max_input_channels" in d
                    else getattr(d, "max_input_channels", 0)
                )
                max_output = (
                    d["max_output_channels"]
                    if isinstance(d, dict) and "max_output_channels" in d
                    else getattr(d, "max_output_channels", 0)
                )
                name = (
                    d["name"]
                    if isinstance(d, dict) and "name" in d
                    else getattr(d, "name", str(d))
                )
                sample_rate = (
                    d["default_samplerate"]
                    if isinstance(d, dict) and "default_samplerate" in d
                    else getattr(d, "default_samplerate", 44100)
                )
            except Exception:
                continue
            if isinstance(max_input, (int, float)):  # and max_input > 0:
                self.input_devices.append((i, name, max_input, max_output, sample_rate))
                if max_input > 0:
                    name = f"Input - {name}"
                else:
                    name = f"Output - {name}"
                self.device_dropdown.addItem(
                    f"{name} (ID:{i} CHANNEL [In:{max_input}, Out:{max_output}])",
                    i,
                )

        btn_layout = QHBoxLayout()
        self.start_btn = ToggleRecordingButton()
        btn_layout.addWidget(self.start_btn)
        self.transcript_btn = TranscriptButton()
        btn_layout.addWidget(self.transcript_btn)
        self.summary_btn = SummaryButton()
        btn_layout.addWidget(self.summary_btn)
        main_layout.addLayout(btn_layout)

        self.fs_tree = FileSystemTreeWidget()
        main_layout.addLayout(self.fs_tree)

        # Add QTextEdit for transcription output
        self.transcription_text_edit = QTextEdit()
        self.transcription_text_edit.setReadOnly(True)
        self.transcription_text_edit.setPlaceholderText(
            "Transcription will appear here..."
        )
        main_layout.addWidget(self.transcription_text_edit)

        # Place Save Transcript and Update Speaker Name buttons side by side
        transcript_btn_layout = QHBoxLayout()
        self.save_transcript_btn = QPushButton("Save Transcript")
        self.save_transcript_btn.clicked.connect(self.save_transcript)
        transcript_btn_layout.addWidget(self.save_transcript_btn)
        self.update_speaker_name_btn = QPushButton("Update Speaker Name")
        self.update_speaker_name_btn.clicked.connect(self.update_speaker_name)
        transcript_btn_layout.addWidget(self.update_speaker_name_btn)
        main_layout.addLayout(transcript_btn_layout)

        self.setLayout(main_layout)

        self.start_btn.clicked.connect(self.handle_recording)
        self.transcript_btn.clicked.connect(self.handle_transcript)
        self.summary_btn.clicked.connect(self.handle_summary)
        self.device_dropdown.currentIndexChanged.connect(self.handle_device_change)

        self.settings_btn.clicked.connect(self.handle_settings)

    def handle_settings(self):
        handle_settings_action(self)

    def update_speaker_name(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Speaker Names")
        layout = QVBoxLayout()

        # For each speaker, show a label with the ID and a textbox for the name
        name_edits = {}
        for sp_id, sp in speaker_dict.items():
            print(sp_id)
            print(sp)
            row_layout = QHBoxLayout()
            id_label = QLabel(f"Speaker ID: {sp_id}")
            row_layout.addWidget(id_label)
            name_edit = QLineEdit()
            name_edit.setText(sp.name)
            row_layout.addWidget(name_edit)
            name_edits[sp_id] = name_edit
            layout.addLayout(row_layout)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)

        def on_ok():
            for sp_id, name_edit in name_edits.items():
                new_name = name_edit.text()
                print(f"Speaker ID: {sp_id}, Speaker Name: {new_name}")
                speaker_dict.get(sp_id).name = new_name
            dialog.accept()
            self.transcription_text_edit.setPlainText(str(transcripts))

        ok_btn.clicked.connect(on_ok)
        cancel_btn.clicked.connect(dialog.reject)
        dialog.exec_()

    def handle_device_change(self, index):
        print("------input_devices----------")
        print(self.input_devices)
        print("-----------------------------")
        device_index = self.device_dropdown.itemData(index)
        device_name = self.device_dropdown.currentText()
        print(f"Selected audio device: {device_name} (ID: {device_index})")
        self.selected_device_index = device_index
        self.selected_device_sample_rate = self.input_devices[device_index][4]
        self.selected_device_type = (
            "Input" if self.input_devices[device_index][2] > 0 else "Output"
        )
        self.selected_device_channel = (
            self.input_devices[device_index][2]
            if self.selected_device_type == "Input"
            else self.input_devices[device_index][3]
        )

    def handle_recording(self):
        # device_index = self.device_dropdown.currentData()
        # print("-------DEVICE INDEX----------")
        # print(device_index)
        # print("-----------------------------")
        if self.start_btn.text() == "Start Recording":
            if not hasattr(self, "selected_device_index"):
                self.handle_device_change(0)
            start_recording_action(
                self.status_label,
                self.start_btn,
                self.selected_device_index,
                self.selected_device_sample_rate,
                self.selected_device_channel,
            )
        else:
            stop_recording_action(
                self.status_label,
                self.start_btn,
                parent=self,
                device=self.selected_device_index,
            )

    def handle_transcript(self):
        transcripts.remove_all()
        speaker_dict.clear()
        transcript_action(self.fs_tree, self.status_label, self.transcription_text_edit)

    def handle_summary(self):
        summary_action(self)

    def save_transcript(self):
        save_transcript(self, self.transcription_text_edit)
