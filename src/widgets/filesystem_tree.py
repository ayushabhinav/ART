from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QVBoxLayout, QLabel
from PyQt5.QtCore import QModelIndex


class FileSystemTreeWidget(QVBoxLayout):
    def __init__(self, root_path="/home/ayushabhinav", parent=None):
        super().__init__()
        self.tree_label = QLabel("Choose a file from the filesystem:")
        self.addWidget(self.tree_label)
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.setRootIndex(self.file_model.index(root_path))
        self.tree.setColumnWidth(0, 250)
        self.addWidget(self.tree)
        self.selected_file_path = None
        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            self.selected_file_path = self.file_model.filePath(index)
        else:
            self.selected_file_path = None
