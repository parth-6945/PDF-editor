# PDF Editor -- Page Manager

A lightweight, open-source desktop application for **page-level PDF
editing**, built with **Python**, **PySide6**, and **PyMuPDF**.\
It focuses on common but often cumbersome PDF tasks such as reordering,
rotating, deleting, duplicating, and merging pages --- all through a
clean and interactive GUI.

------------------------------------------------------------------------

## Project Aim

The goal of **PDF Editor -- Page Manager** is to provide a **simple,
transparent, and cross-platform** PDF tool dedicated specifically to
**page management operations**.

Many existing PDF editors are either: 
- Overly complex for basic page edits
- Closed-source or paid
- Web-based, requiring file uploads

This project was created to offer a **fast, offline, and extensible
alternative** that users can freely inspect, modify, and improve.

------------------------------------------------------------------------

## Features

-   View PDF pages as thumbnails
-   Drag-and-drop page reordering
-   Page selection modes:
    -   All pages
    -   Even pages
    -   Odd pages
    -   Custom ranges (e.g. `1,3-5,8`)
-   Rotate pages clockwise or counter-clockwise
-   Duplicate selected pages
-   Delete selected pages
-   Merge external PDFs:
    -   At the beginning
    -   At the end
    -   After a specific page
-   Export selected pages as a new PDF
-   Save the modified PDF document

------------------------------------------------------------------------

## Installation

### 1. Clone the repository

``` bash
git clone <repository_url>
cd <repository_folder>
```

### 2. (Optional but recommended) Create a virtual environment

``` bash
python3 -m venv pdfenv
source pdfenv/bin/activate      # Linux / macOS
pdfenv\Scripts\activate       # Windows
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Usage

1.  Run the application:

``` bash
python3 main.py
```

2.  Open a PDF file to begin editing
3.  Use the sidebar to:
    -   Select pages
    -   Rotate, duplicate, or delete pages
    -   Merge another PDF
4.  Save the edited PDF or export selected pages as a new file

------------------------------------------------------------------------

## Build Standalone Binaries

You can build a single-file executable using **PyInstaller**.

### Steps

1.  Ensure dependencies are installed
2.  Install PyInstaller:

``` bash
pip install pyinstaller
```

3.  Build the executable:

``` bash
pyinstaller --onefile --windowed --name pdf-editor main.py
```

4.  Find the executable in the `dist/` directory

> Note: Platform-specific installers (Snap, MSI, DMG) are not yet
> provided.

------------------------------------------------------------------------

## Project Structure

    pdf_editor_ws/
    ├─ edit_mode/
    │  ├─ editor.py          # Main editor GUI logic
    │  ├─ pdf_operations.py  # PDF manipulation functions
    │  ├─ __init__.py
    ├─ document_model.py     # Document and Page models
    ├─ main.py               # Application entry point
    ├─ requirements.txt      # Python dependencies
    ├─ README.md

------------------------------------------------------------------------

## Supported Platforms

-   Linux
-   Windows
-   macOS (requires Python & PySide6)

------------------------------------------------------------------------

## Dependencies

-   **PySide6** --- GUI framework
-   **PyMuPDF** --- PDF rendering and manipulation

Install all dependencies via:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Roadmap

Planned or potential future improvements:

-   Undo / Redo support
-   Page cropping
-   Password-protected PDF support
-   Multi-page drag selection
-   Platform-specific installers (Snap, MSI, DMG)
-   UI/UX refinements

Feature requests and suggestions are welcome via GitHub Issues.

------------------------------------------------------------------------

## Contributing

Contributions are welcome and encouraged.

You can help by: 
- Fixing bugs 
- Improving performance 
- Enhancing UI/UX 
- Adding new PDF operations 
- Improving documentation

### Contribution Steps

1.  Fork the repository

2.  Create a feature branch:

    ``` bash
    git checkout -b feature/my-feature
    ```

3.  Commit your changes

4.  Push to your fork and open a Pull Request

Please keep changes focused and consistent with the existing code style.

------------------------------------------------------------------------

## License

This project is licensed under the **MIT License**.
