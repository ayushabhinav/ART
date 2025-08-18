from PyQt5.QtWidgets import QLabel


class StatusLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__("Recording in progress...", parent)
        self.setStyleSheet("color: red; font-weight: bold;")
        self.setVisible(False)
