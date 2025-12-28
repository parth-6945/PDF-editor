import sys
import PySide6
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QListWidget Example")
        self.resize(300, 200)

        # Create the list widget
        self.list_widget = QListWidget()

        # Add items (method 1: simple text)
        self.list_widget.addItem("Item 1")
        self.list_widget.addItem("Item 2")

        # Add items (method 2: QListWidgetItem object)
        item3 = QListWidgetItem("Item 3")
        item4 = QListWidgetItem("Item 4")

        # Optional: make item 4 non-selectable
        item4.setFlags(item4.flags() & ~Qt.ItemIsSelectable)

        self.list_widget.addItem(item3)
        self.list_widget.addItem(item4)

        # Set list widget as central widget
        self.setCentralWidget(self.list_widget)

        self.list_widget.setDragDropMode(PySide6.QtWidgets.QAbstractItemView.InternalMove)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
