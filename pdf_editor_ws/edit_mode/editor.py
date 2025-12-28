# edit_mode/editor.py
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QLabel,
    QVBoxLayout, QToolBar, QFileDialog, QDockWidget, QGroupBox,
    QPushButton, QInputDialog
)
from PySide6.QtGui import QPixmap, QImage, QAction
from PySide6.QtCore import Qt, QSize
import fitz  # PyMuPDF
from document_model import Document, Page
import edit_mode.pdf_operations as pdf_ops  # your pdf_operations.py


def render_page_thumbnail(document: Document, page_obj: Page, zoom=0.2) -> QPixmap:
    """
    Render thumbnail from the correct source PDF,
    not always from document.doc.
    """

    # Lazily create a cache for opened PDFs
    if not hasattr(document, "_doc_cache"):
        document._doc_cache = {}

    src = page_obj.source_document

    # Determine which PDF to read from
    if src is None or src == document.file_path:
        pdf = document.doc
    else:
        if src not in document._doc_cache:
            document._doc_cache[src] = fitz.open(src)
        pdf = document._doc_cache[src]

    # Now this index is guaranteed to be correct
    page = pdf[page_obj.source_page_index]

    mat = fitz.Matrix(zoom, zoom).prerotate(page_obj.rotation)
    pix = page.get_pixmap(matrix=mat)

    fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
    img = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)

    return QPixmap.fromImage(img)


class PageItemWidget(QWidget):
    """Thumbnail + page number widget."""
    def __init__(self, pixmap: QPixmap, page_number: int):
        super().__init__()
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(f"Page {page_number}")
        self.text_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)


class PDFEditor(QMainWindow):
    def __init__(self, document: Document):
        super().__init__()
        self.setWindowTitle("PDF Editor – Pages")
        self.resize(1000, 700)

        self.document = document

        # Main list widget
        self.list_widget = QListWidget()
        self.setCentralWidget(self.list_widget)
        self.list_widget.setViewMode(QListWidget.ListMode)
        self.list_widget.setFlow(QListWidget.LeftToRight)
        self.list_widget.setWrapping(True)
        self.list_widget.setIconSize(QSize(160, 220))
        self.list_widget.setGridSize(QSize(180, 240))
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)

        self.list_widget.model().rowsMoved.connect(self.on_rows_moved)

        self._create_toolbar()
        self._create_sidebar()
        self._load_pages()

    # --------------------------
    # Toolbar
    # --------------------------
    def _create_toolbar(self):
        toolbar = QToolBar("Edit Toolbar")
        self.addToolBar(toolbar)
        save_action = QAction("Save PDF", self)
        save_action.triggered.connect(self.save_pdf)
        toolbar.addAction(save_action)

    # --------------------------
    # Sidebar
    # --------------------------
    def _create_sidebar(self):
        dock = QDockWidget("Options", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)

        # Selection group
        sel_group = QGroupBox("Selection")
        sel_layout = QVBoxLayout()
        btn_select_all = QPushButton("Select All")
        btn_select_all.clicked.connect(lambda: self.select_pages("all"))
        btn_select_even = QPushButton("Select Even")
        btn_select_even.clicked.connect(lambda: self.select_pages("even"))
        btn_select_odd = QPushButton("Select Odd")
        btn_select_odd.clicked.connect(lambda: self.select_pages("odd"))
        btn_clear_all = QPushButton("Clear all")
        btn_clear_all.clicked.connect(lambda: self.select_pages("clear"))
        btn_select_custom = QPushButton("Select Custom")
        btn_select_custom.clicked.connect(self.select_custom_pages)
        sel_layout.addWidget(btn_select_all)
        sel_layout.addWidget(btn_select_even)
        sel_layout.addWidget(btn_select_odd)
        sel_layout.addWidget(btn_select_custom)
        sel_layout.addWidget(btn_clear_all)
        sel_group.setLayout(sel_layout)
        sidebar_layout.addWidget(sel_group)

        # Actions group
        act_group = QGroupBox("Actions")
        act_layout = QVBoxLayout()
        btn_delete = QPushButton("Delete Pages")
        btn_delete.clicked.connect(self.delete_selected)
        btn_rotate = QPushButton("Rotate Pages")
        btn_rotate.clicked.connect(lambda: self.rotate_selected(90))
        btn_duplicate = QPushButton("Duplicate Pages")
        btn_duplicate.clicked.connect(self.duplicate_selected)
        act_layout.addWidget(btn_delete)
        act_layout.addWidget(btn_rotate)
        act_layout.addWidget(btn_duplicate)
        act_group.setLayout(act_layout)
        sidebar_layout.addWidget(act_group)

        # Merge PDF group
        merge_group = QGroupBox("Merge/Export PDF")
        merge_layout = QVBoxLayout()
        btn_merge_start = QPushButton("Merge at Start")
        btn_merge_start.clicked.connect(lambda: self.merge_pdf('start'))
        btn_merge_end = QPushButton("Merge at End")
        btn_merge_end.clicked.connect(lambda: self.merge_pdf('end'))
        btn_merge_after = QPushButton("Merge After Page...")
        btn_merge_after.clicked.connect(self.merge_after_page)
        btn_export = QPushButton("Export selected pages")
        btn_export.clicked.connect(lambda: self.export_pages())
        merge_layout.addWidget(btn_merge_start)
        merge_layout.addWidget(btn_merge_end)
        merge_layout.addWidget(btn_merge_after)
        merge_layout.addWidget(btn_export)
        merge_group.setLayout(merge_layout)
        sidebar_layout.addWidget(merge_group)

        dock.setWidget(sidebar_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    # --------------------------
    # Load / refresh
    # --------------------------
    def _load_pages(self):
        self.list_widget.clear()
        for idx, page_obj in enumerate(self.document.pages):
            pixmap = render_page_thumbnail(self.document, page_obj)
            item = QListWidgetItem()
            item.setSizeHint(QSize(180, 240))
            item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setData(Qt.UserRole, page_obj)
            widget = PageItemWidget(pixmap, idx + 1)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    def on_rows_moved(self, parent, start, end, destination, row):
        new_order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            page_obj = item.data(Qt.UserRole)
            new_order.append(page_obj)
        self.document.pages = new_order
        self.refresh_page_numbers()

    def refresh_page_numbers(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            widget.text_label.setText(f"Page {i + 1}")

    # --------------------------
    # Selection handling
    # --------------------------
    def select_pages(self, mode):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if mode == "all":
                item.setSelected(True)
            elif mode == "even":
                item.setSelected((i + 1) % 2 == 0)
            elif mode == "odd":
                item.setSelected((i + 1) % 2 == 1)
            elif mode == "clear":
                item.setSelected(False)

    def select_custom_pages(self):
        text, ok = QInputDialog.getText(
            self,
            "Custom Page Selection",
            "Enter pages (e.g. 1,3-5,8):"
        )
        if not ok or not text.strip():
            return

        max_pages = len(self.document.pages)
        selected_indices = set()

        parts = text.split(",")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Handle ranges like 3-7
            if "-" in part:
                try:
                    start_str, end_str = part.split("-", 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())

                    if start > end:
                        start, end = end, start

                    for page_num in range(start, end + 1):
                        idx = page_num - 1
                        if 0 <= idx < max_pages:
                            selected_indices.add(idx)
                except ValueError:
                    continue

            # Handle single numbers
            else:
                try:
                    page_num = int(part)
                    idx = page_num - 1
                    if 0 <= idx < max_pages:
                        selected_indices.add(idx)
                except ValueError:
                    continue

        # Clear existing selection
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setSelected(False)

        # Apply new selection
        for idx in sorted(selected_indices):
            self.list_widget.item(idx).setSelected(True)


    def get_selected_pages(self):
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.isSelected():
                selected.append(item.data(Qt.UserRole))
        return selected

    # --------------------------
    # Actions
    # --------------------------
    def delete_selected(self):
        pages = self.get_selected_pages()
        pdf_ops.delete_pages(self.document, pages)
        self._load_pages()

    def rotate_selected(self, angle=90):
        pages = self.get_selected_pages()
        pdf_ops.rotate_pages(self.document, pages, angle)
        self._load_pages()

    def duplicate_selected(self):
        pages = self.get_selected_pages()
        pdf_ops.duplicate_pages(self.document, pages)
        self._load_pages()
    
    def export_pages(self):
        pages = self.get_selected_pages()
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if not (path or pages):
            return
        pdf_ops.export_selected_pages(self.document, pages, path)
        self._load_pages()

    def merge_pdf(self, position='end'):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF to Merge", "", "PDF Files (*.pdf)")
        if not path:
            return
        pdf_ops.merge_pdf(self.document, path, position)
        self._load_pages()

    def merge_after_page(self):
        # Ask user for page number
        page_num, ok = QInputDialog.getInt(
            self,
            "Merge After Page",
            f"Enter page number (1-{len(self.document.pages)}):",
            1,
            1,
            len(self.document.pages)
        )
        if not ok:
            return

        # Ask for PDF to merge
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF to Merge", "", "PDF Files (*.pdf)")
        if not path:
            return

        # Merge after the given page (subtract 1 to get 0-based index)
        pdf_ops.merge_pdf(self.document, path, position=page_num)
        self._load_pages()


    # --------------------------
    # Save PDF
    # --------------------------
    def save_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        new_doc = fitz.open()

        for page_obj in self.document.pages:
            # Resolve correct source document
            if page_obj.source_document == self.document.file_path:
                src_doc = self.document.doc
            else:
                src_doc = fitz.open(page_obj.source_document)

            src_page = src_doc[page_obj.source_page_index]

            new_page = new_doc.new_page(
                width=src_page.rect.width,
                height=src_page.rect.height
            )

            mat = fitz.Matrix(1, 1).prerotate(page_obj.rotation)
            pix = src_page.get_pixmap(matrix=mat)

            new_page.insert_image(src_page.rect, pixmap=pix)

            if src_doc is not self.document.doc:
                src_doc.close()

        new_doc.save(file_path)
        new_doc.close()
