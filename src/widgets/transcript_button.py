from PyQt5.QtWidgets import QPushButton

class TranscriptButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Transcript", parent)
