from PyQt5.QtWidgets import QPushButton

class ToggleRecordingButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Start Recording", parent)

    def toggle(self):
        if self.text() == "Start Recording":
            self.setText("Stop Recording")
            return True
        else:
            self.setText("Start Recording")
            return False
