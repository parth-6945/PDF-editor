# PDF Viewer (Python + PySide6)

A minimal PDF viewer built using PySide6 and PyMuPDF, designed as the foundation for a future PDF editor.

---

## Project Structure

pdf_editor_ws/

├── main.py

├── viewer.py

├── document_model.py

├── architecture.txt

├── project_goals.txt

└── README.md

---

## Requirements

The user only needs Python 3.10+ installed.

Required Python packages:
- PySide6
- PyMuPDF

---

## Setup Instructions (Fresh System)

1. Create a virtual environment (recommended):

   ```bash
   python3 -m venv pdfenv
   source pdfenv/bin/activate   # Linux / macOS
   # pdfenv\Scripts\activate  # Windows
   ```

2. Install dependencies:

   ```bash
   pip install PySide6 PyMuPDF
   ```

3. Run the application:

   ```bash
   python3 main.py
   ```

---

## File Descriptions

**main.py**
Entry point of the application. Creates the Qt application and launches the PDF viewer window.

**viewer.py**
Contains the PDFViewer class:
- Renders PDF pages using PyMuPDF
- Page navigation (next / previous)
- Editable page number
- Editable zoom percentage
- Keyboard shortcuts
- Rotation
- Fit-to-width / fit-to-height
- Scroll support inside a page

This file handles all UI and rendering logic.

**document_model.py**
Represents the document structure:
- Loads the PDF file
- Maintains page order
- Stores per-page properties (rotation, source index)

This separation allows future features like:
- Page reordering
- Page deletion
- Multi-page views

**architecture.txt**
High-level design notes explaining:
- Separation of Viewer and Document Model
- Why page state is not stored directly in the UI
- Planned extensibility

**project_goals.txt**
Defines current and future goals, such as:
- Continuous scrolling mode
- Multi-page view for reordering
- Editing tools
- Export functionality

---

## Keyboard Shortcuts

Key           | Action
------------- | ------------------
→ / ↓         | Next page
← / ↑         | Previous page
\+            | Zoom in
\-            | Zoom out
R             | Rotate page
Enter (in input fields) | Apply value

---

## Notes

- The project currently focuses on single-page viewing.
- Continuous scrolling and multi-page layout are planned but intentionally not implemented yet.
- This structure allows clean expansion without rewriting core logic.

---

## Troubleshooting

If PySide6 fails to install:

```bash
pip install --upgrade pip
pip install PySide6
```

If PyMuPDF fails:

```bash
pip install pymupdf
```

---

## License

This project is currently for learning and experimentation purposes.
You may modify and extend it freely.
