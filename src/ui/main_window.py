from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QComboBox
import sounddevice as sd
from widgets.status import StatusLabel
from src.widgets.toggle_recording_button import ToggleRecordingButton
from src.widgets.transcript_button import TranscriptButton
from src.widgets.summary_button import SummaryButton
from src.widgets.filesystem_tree import FileSystemTreeWidget
from src.actions.button_actions import (
    start_recording_action,
    stop_recording_action,
    transcript_action,
    summary_action,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meeting Recorder")
        self.setMinimumSize(700, 400)
        main_layout = QVBoxLayout()

        self.status_label = StatusLabel()
        main_layout.addWidget(self.status_label)

        # Audio device dropdown and label in horizontal layout
        device_layout = QHBoxLayout()
        self.device_dropdown_label = QLabel("Select Audio Device:")
        self.device_dropdown = QComboBox()
        self.device_dropdown.setFixedWidth(180)
        device_layout.addWidget(self.device_dropdown_label)
        device_layout.addWidget(self.device_dropdown)
        device_layout.addStretch(1)
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
                name = (
                    d["name"]
                    if isinstance(d, dict) and "name" in d
                    else getattr(d, "name", str(d))
                )
            except Exception:
                continue
            if isinstance(max_input, (int, float)) and max_input > 0:
                self.input_devices.append((i, name))
                self.device_dropdown.addItem(f"{name} (ID: {i})", i)

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

        self.setLayout(main_layout)

        self.start_btn.clicked.connect(self.handle_recording)
        self.transcript_btn.clicked.connect(self.handle_transcript)
        self.summary_btn.clicked.connect(self.handle_summary)
        self.device_dropdown.currentIndexChanged.connect(self.handle_device_change)

    def handle_device_change(self, index):
        device_index = self.device_dropdown.itemData(index)
        device_name = self.device_dropdown.currentText()
        print(f"Selected audio device: {device_name} (ID: {device_index})")

    def handle_recording(self):
        device_index = self.device_dropdown.currentData()
        if self.start_btn.text() == "Start Recording":
            start_recording_action(self.status_label, self.start_btn, device_index)
        else:
            stop_recording_action(
                self.status_label, self.start_btn, parent=self, device=device_index
            )

    def handle_transcript(self):
        transcript_action(self.fs_tree, self.status_label)

    def handle_summary(self):
        summary_action()
