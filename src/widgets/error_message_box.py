from PyQt5.QtWidgets import QMessageBox

class ErrorMessageBox:
    @staticmethod
    def show_error(message, title="Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
