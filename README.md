# PDF Editor – Page Manager

A Python desktop application to view, reorder, rotate, duplicate, delete, and merge PDF pages, with a simple and interactive GUI built with PySide6 and PyMuPDF.

---

## Features

* View PDF pages as thumbnails.
* Drag and drop to reorder pages.
* Select pages: All, Even, Odd, Custom (supports ranges like `1,3-5`).
* Delete, rotate, or duplicate selected pages.
* Merge PDFs at start, end, or after a specific page.
* Export selected pages as a new PDF.
* Save the modified PDF.

---

## Installation

1. Clone this repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv pdfenv
source pdfenv/bin/activate  # Linux/macOS
pdfenv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Run the main script:

```bash
python3 main.py
```

2. Open a PDF file to start editing.
3. Use the sidebar for selecting, rotating, duplicating, deleting pages, and merging PDFs.
4. Save your edited PDF using the toolbar button.
5. Export selected pages as a new PDF.

---

## Project Structure

```
pdf_editor_ws/
├─ edit_mode/
│  ├─ editor.py          # Main editor GUI logic
│  ├─ pdf_operations.py  # PDF manipulation functions
│  ├─ __init__.py
├─ document_model.py      # Document and Page classes
├─ main.py                # Entry point for the application
├─ requirements.txt       # Dependencies
├─ README.md
```

---

## Supported Platforms

* Linux
* Windows
* macOS (requires Python & PySide6 installation)

---

## Python Packages

This project uses:

* `PySide6` for the GUI.
* `PyMuPDF` for PDF processing.

Install all dependencies via `pip install -r requirements.txt`.

---

## Contributing

1. Fork the repository.
2. Make your changes in a feature branch.
3. Submit a pull request.

---

## License

This project is open-source under the MIT License.

---
