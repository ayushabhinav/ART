from PyQt5.QtWidgets import QFileDialog

class SaveFileDialog:
    @staticmethod
    def get_save_file(parent=None, default_name="output.wav"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            parent,
            "Save Recording As",
            default_name,
            "WAV Files (*.wav)",
            options=options
        )
        return filename
