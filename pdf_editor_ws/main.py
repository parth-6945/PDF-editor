# main.py
import sys
from PySide6.QtWidgets import QApplication
from viewer import PDFViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())
