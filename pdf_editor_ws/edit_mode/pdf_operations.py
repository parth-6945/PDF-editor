# edit_mode/pdf_operations.py
from document_model import Document, Page
import fitz  # PyMuPDF


# ---------------------------
# Actions on pages
# ---------------------------
def delete_pages(document: Document, pages_to_delete: list[Page]):
    """Remove pages from the logical document only."""
    delete_set = set(pages_to_delete)
    document.pages = [p for p in document.pages if p not in delete_set]

def rotate_pages(document: Document, pages_to_rotate: list[Page], angle: int = 90):
    for page in pages_to_rotate:
        page.rotation = (page.rotation + angle) % 360

def duplicate_pages(document: Document, pages_to_duplicate: list[Page]):
    duplicate_set = set(pages_to_duplicate)
    new_pages = []

    for page in document.pages:
        new_pages.append(page)
        if page in duplicate_set:
            new_pages.append(
                Page(
                    page.source_document,
                    page.source_page_index,
                    page.rotation
                )
            )

    document.pages = new_pages

# ---------------------------
# Merge PDF
# ---------------------------
def merge_pdf(document: Document, merge_path: str, position='end'):
    """
    Logically merge another PDF into the document.
    Does NOT rebuild document.doc.
    """
    other_doc = fitz.open(merge_path)

    merged_pages = []

    # Create Page objects referencing the OTHER pdf
    external_pages = [
        Page(
            source_document=merge_path,
            source_page_index=i,
            rotation=0
        )
        for i in range(len(other_doc))
    ]

    if position == 'start':
        merged_pages.extend(external_pages)
        merged_pages.extend(document.pages)

    elif position == 'end':
        merged_pages.extend(document.pages)
        merged_pages.extend(external_pages)

    elif isinstance(position, int):
        merged_pages.extend(document.pages[:position])
        merged_pages.extend(external_pages)
        merged_pages.extend(document.pages[position:])

    else:
        raise ValueError("position must be 'start', 'end', or integer index")

    document.pages = merged_pages

    other_doc.close()

# ---------------------------
# Export Pages as PDF
# ---------------------------

def export_selected_pages(document: Document, pages_to_export: list[Page], export_path: str):
    new_doc = fitz.open()
    for page_obj in pages_to_export:
        orig_page = document.doc[page_obj.source_page_index]
        new_page = new_doc.new_page(width=orig_page.rect.width, height=orig_page.rect.height)
        mat = fitz.Matrix(1, 1).prerotate(page_obj.rotation)
        pix = orig_page.get_pixmap(matrix=mat)
        new_page.insert_image(orig_page.rect, pixmap=pix)

    new_doc.save(export_path)
    new_doc.close()
