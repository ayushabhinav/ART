from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QFileDialog,
    QDialog,
    QLineEdit,
    QCheckBox,
)

from src.config import load_settings, save_settings, CONFIG


def handle_settings_action(self):
    dialog = QDialog(self)
    dialog.setWindowTitle("Settings")
    layout = QVBoxLayout()

    # Add checkbox for Disable SSL
    self.disable_ssl_checkbox = QCheckBox("Disable SSL?")
    layout.addWidget(self.disable_ssl_checkbox)

    # Add label and text box for Hugging Face token
    token_layout = QHBoxLayout()
    token_label = QLabel("Hugging Face Token:")
    self.hf_token_edit = QLineEdit()
    token_layout.addWidget(token_label)
    token_layout.addWidget(self.hf_token_edit)
    layout.addLayout(token_layout)

    # Add label and path picker for app working folder
    folder_layout = QHBoxLayout()
    folder_label = QLabel("App Working Folder:")
    self.folder_edit = QLineEdit()
    folder_btn = QPushButton("Browse")
    folder_layout.addWidget(folder_label)
    folder_layout.addWidget(self.folder_edit)
    folder_layout.addWidget(folder_btn)
    layout.addLayout(folder_layout)

    def pick_folder():
        folder = QFileDialog.getExistingDirectory(dialog, "Select Working Folder")
        if folder:
            self.folder_edit.setText(folder)

    folder_btn.clicked.connect(pick_folder)

    # Add combo box for language choice
    lang_layout = QHBoxLayout()
    lang_label = QLabel("Language:")
    self.lang_combo = QComboBox()
    self.lang_combo.addItem("English")
    self.lang_combo.addItem("Hindi")
    self.lang_combo.setCurrentText("English")
    lang_layout.addWidget(lang_label)
    lang_layout.addWidget(self.lang_combo)
    layout.addLayout(lang_layout)

    # Load settings from config
    settings = load_settings()
    self.disable_ssl_checkbox.setChecked(settings.get("disable_ssl", False))
    self.hf_token_edit.setText(settings.get("hf_token", ""))
    self.folder_edit.setText(settings.get("working_folder", ""))
    self.lang_combo.setCurrentText(settings.get("language", "English"))

    # ok and cancel buttons
    def on_ok():
        # Save settings to config
        settings = {
            "disable_ssl": self.disable_ssl_checkbox.isChecked(),
            "hf_token": self.hf_token_edit.text(),
            "working_folder": self.folder_edit.text(),
            "language": self.lang_combo.currentText(),
        }
        save_settings(settings)
        CONFIG.update(settings)
        print("Settings saved:", settings)
        dialog.accept()

    btn_layout = QHBoxLayout()
    ok_btn = QPushButton("OK")
    cancel_btn = QPushButton("Cancel")
    btn_layout.addWidget(ok_btn)
    btn_layout.addWidget(cancel_btn)
    layout.addLayout(btn_layout)
    dialog.setLayout(layout)
    ok_btn.clicked.connect(on_ok)
    cancel_btn.clicked.connect(dialog.reject)

    dialog.exec_()
