from PyQt5.QtWidgets import QPushButton

class SummaryButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Summary", parent)
