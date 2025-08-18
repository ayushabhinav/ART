import os
import sys

base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_folder)
sys.path.insert(0, base_folder)

print(sys.path)

from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
