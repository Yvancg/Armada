# PDF to Excel Converter

This project provides a Python-based solution to convert scanned bank transaction PDFs into structured Excel spreadsheets. It includes a user-friendly interface for uploading files and processes them securely within a virtual environment.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Batch Processing:** Handle approximately 300 PDF files, each containing multiple pages of bank transactions.
- **OCR Integration:** Utilize Optical Character Recognition (OCR) to extract data from PDFs with varying scan qualities.
- **Automated Excel Generation:** Create one Excel spreadsheet per bank, accurately populated with extracted data.
- **User Interface:** Simple front-end interface for uploading PDF files.
- **Secure Environment:** Code execution within a virtual environment to ensure data security.

## Prerequisites

- **Software:**
  - [Python 3.8 or higher](https://www.python.org/downloads/)
  - [Git](https://git-scm.com/)
  - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yvancg/pdf-to-excel-converter.git
    cd pdf-to-excel-converter
    ```

2. **Set Up a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Tesseract OCR:**

    - **Using Homebrew:**

        ```bash
        brew install tesseract
        ```

    - **Manual Installation:**

        Download and install Tesseract from the [official repository](https://github.com/tesseract-ocr/tesseract).

5. **Configure Environment Variables:**

    Create a `.env` file in the project root directory and add any necessary environment-specific variables, such as API keys or configuration settings.

## Usage

1. **Start the Application:**

    ```bash
    python app.py
    ```

2. **Upload PDF Files:**

    - Access the front-end interface at `http://localhost:5000`.
    - Use the upload feature to select and upload PDF files.

3. **Processing:**

    - The application will process each uploaded PDF, extracting transaction data using OCR.
    - Extracted data is organized and saved into Excel spreadsheets, with one file per bank.

4. **Retrieve Output:**

    - Processed Excel files are saved in the `output` directory within the project folder.

## Project Structure

pdf-to-excel-converter/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── modules/
│   ├── pdf_processor.py
│   └── ocr_utils.py
└── output/

- `app.py`: Main application script.
- `requirements.txt`: Lists required Python packages.
- `templates/`: Contains HTML templates for the front-end.
- `static/`: Stores static files like CSS.
- `modules/`: Includes modules for PDF processing and OCR utilities.
- `output/`: Directory where the resulting Excel files are saved.

## Security Considerations

- **Virtual Environment:** Running the application within a virtual environment isolates dependencies and enhances security.
- **Data Privacy:** Ensure that all processed data is handled in compliance with relevant data protection regulations.
- **Access Control:** Implement appropriate access controls to restrict unauthorized use of the application.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/yvancg`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/yvancg`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Note: This project is designed to process a large number of PDF files with varying qualities. Ensure that Tesseract OCR is properly configured to handle low-quality scans effectively.*

---
