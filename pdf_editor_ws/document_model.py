# document_model.py
import fitz  # PyMuPDF

class Page:
    """
    Represents a logical page in a PDF document.
    Does NOT store rendered data, only metadata.
    """
    def __init__(self, source_document, source_page_index, rotation=0):
        self.source_document = source_document  # path or identifier
        self.source_page_index = source_page_index  # 0-based
        self.rotation = rotation
        self.overlays = []  # optional images/signatures

class Document:
    """
    Represents a PDF document in the viewer/editor.
    Maintains an ordered list of Page objects.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = fitz.open(file_path)  # PyMuPDF document
        self.pages = [Page(file_path, i) for i in range(len(self.doc))]
        self.current_index = 0
