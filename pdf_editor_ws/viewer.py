# viewer.py
from PySide6.QtWidgets import (
    QLabel, QMainWindow, QToolBar, QVBoxLayout, QPushButton,
    QStatusBar, QFileDialog, QLineEdit, QScrollArea, QDialog
)
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtCore import Qt
from document_model import Document
import fitz  # PyMuPDF

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About PDF Editor")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        title = QLabel("<h2>PDF Editor</h2>")
        title.setAlignment(Qt.AlignCenter)

        version = QLabel("Version: 1.0")
        version.setAlignment(Qt.AlignCenter)

        author = QLabel("Developed by Parth Gargate")
        author.setAlignment(Qt.AlignCenter)

        description = QLabel(
            "A lightweight PDF editor to view, rearrange, rotate, duplicate,\n"
            "merge, and export PDF pages across platforms.\n"
            "You can contribute to the project on Github in the repository : \n"
            "parth-6945/PDF-editor."
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(author)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(btn_close)

        self.setLayout(layout)


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.resize(900, 700)

        # ---------- State ----------
        self.document = None
        self.zoom = 1.0

        # ---------- Central Widget ----------
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.label)

        self.setCentralWidget(self.scroll)

        # ---------- UI ----------
        self._create_toolbar()
        self._create_menu()

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.setFocusPolicy(Qt.StrongFocus)

    # ---------- Toolbar ----------
    def _create_toolbar(self):
        toolbar = QToolBar("View")
        self.addToolBar(toolbar)

        toolbar.addAction(QAction("◀", self, triggered=self.prev_page))

        self.page_input = QLineEdit("1")
        self.page_input.setFixedWidth(60)
        self.page_input.setAlignment(Qt.AlignCenter)
        self.page_input.returnPressed.connect(self.apply_page_from_input)
        toolbar.addWidget(self.page_input)

        toolbar.addAction(QAction("▶", self, triggered=self.next_page))

        toolbar.addSeparator()

        toolbar.addAction(QAction("-", self, triggered=self.zoom_out))

        self.zoom_input = QLineEdit("100")
        self.zoom_input.setFixedWidth(60)
        self.zoom_input.setAlignment(Qt.AlignCenter)
        self.zoom_input.returnPressed.connect(self.apply_zoom_from_input)
        toolbar.addWidget(self.zoom_input)

        toolbar.addAction(QAction("+", self, triggered=self.zoom_in))

        toolbar.addSeparator()

        toolbar.addAction(QAction("Fit Width", self, triggered=self.fit_width))
        toolbar.addAction(QAction("Fit Height", self, triggered=self.fit_height))

        toolbar.addSeparator()

        toolbar.addAction(QAction("Rotate", self, triggered=self.rotate_page))
        # inside _create_toolbar() in viewer.py
        edit_action = QAction("Edit PDF", self)
        edit_action.triggered.connect(self.open_editor)
        toolbar.addAction(edit_action)


    # ---------- Menu ----------
    def _create_menu(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(QAction("Open PDF", self, triggered=self.open_pdf))
        file_menu.addAction(QAction("Exit", self, triggered=self.close))
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        file_menu.addAction(about_action)

    # ---------- PDF ----------
    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.document = Document(file_path)
            self.zoom = 1.0
            self.render_page()
            self.setFocus()

    def render_page(self):
        if not self.document:
            return

        page_obj = self.document.pages[self.document.current_index]
        page = self.document.doc[page_obj.source_page_index]

        mat = fitz.Matrix(self.zoom, self.zoom).prerotate(page_obj.rotation)
        pix = page.get_pixmap(matrix=mat)

        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)

        self.label.setPixmap(QPixmap.fromImage(img))

        self.page_input.setText(str(self.document.current_index + 1))
        self.zoom_input.setText(str(int(self.zoom * 100)))

        self.status.showMessage(
            f"Page {self.document.current_index + 1}/{len(self.document.pages)} | "
            f"Zoom {int(self.zoom * 100)}%"
        )

    # ---------- Navigation ----------
    def next_page(self):
        if self.document and self.document.current_index < len(self.document.pages) - 1:
            self.document.current_index += 1
            self.render_page()

    def prev_page(self):
        if self.document and self.document.current_index > 0:
            self.document.current_index -= 1
            self.render_page()

    def apply_page_from_input(self):
        if not self.document:
            return
        try:
            page = int(self.page_input.text()) - 1
            if 0 <= page < len(self.document.pages):
                self.document.current_index = page
                self.render_page()
        except ValueError:
            pass
        self.setFocus()

    # ---------- Zoom ----------
    def zoom_in(self):
        if self.document:
            self.zoom *= 1.25
            self.render_page()

    def zoom_out(self):
        if self.document:
            self.zoom /= 1.25
            self.render_page()

    def apply_zoom_from_input(self):
        if not self.document:
            return
        try:
            value = int(self.zoom_input.text())
            if value > 0:
                self.zoom = value / 100.0
                self.render_page()
        except ValueError:
            pass
        self.setFocus()

    # ---------- Fit Modes ----------
    def fit_width(self):
        if not self.document:
            return

        page = self.document.doc[self.document.pages[self.document.current_index].source_page_index]
        view_width = self.scroll.viewport().width()
        self.zoom = view_width / page.rect.width
        self.render_page()

    def fit_height(self):
        if not self.document:
            return

        page = self.document.doc[self.document.pages[self.document.current_index].source_page_index]
        view_height = self.scroll.viewport().height()
        self.zoom = view_height / page.rect.height
        self.render_page()

    # ---------- Rotate ----------
    def rotate_page(self):
        if self.document:
            page = self.document.pages[self.document.current_index]
            page.rotation = (page.rotation + 90) % 360
            self.render_page()

    # ---------- Keyboard ----------
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Right, Qt.Key_Down):
            self.next_page()
        elif event.key() in (Qt.Key_Left, Qt.Key_Up):
            self.prev_page()
        elif event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            self.zoom_in()
        elif event.key() == Qt.Key_Minus:
            self.zoom_out()
        elif event.key() == Qt.Key_R:
            self.rotate_page()

    def open_editor(self):
        if not self.document:
            return
        from edit_mode.editor import PDFEditor
        self.editor_window = PDFEditor(self.document)
        self.editor_window.show()

    def show_about(self):
        dlg = AboutDialog()
        dlg.exec()  # Modal dialog

