import os
import pytesseract  # Optical Character Recognition library to extract text from images
from pdf2image import convert_from_path  # Converts PDF pages into images for OCR processing
import pandas as pd  # Data analysis library, used here to create Excel spreadsheets
from PyPDF2 import PdfReader  # Library to read PDF files (not actively used in this snippet)
import re  # Regular expression library for pattern matching
from PIL import Image  # Imaging library to handle image processing
import logging  # Standard logging module for tracking events and errors

# Configure the logging to output messages at the INFO level or higher
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Processes PDF files to extract transaction information and generate Excel spreadsheets.

    Workflow:
      - Convert PDF pages to images.
      - Use OCR (via pytesseract) to extract text from each image.
      - Identify the bank by matching text with predefined regex patterns.
      - Parse transaction details (date, amount, description) from the extracted text.
      - Generate an Excel file with the parsed transactions.
    """
    def __init__(self):
        # Dictionary mapping bank names to regex patterns for identification
        self.bank_patterns = {
            'Bank1': r'Account\s*Statement.*Bank1',
            'Bank2': r'Statement.*Bank2',
            # Add patterns for additional banks as required
        }
    
    def identify_bank(self, text):
        """
        Identify the bank by searching the combined text for known bank-specific patterns.

        Args:
            text (str): The full text extracted from the PDF.

        Returns:
            str: The bank name if a matching pattern is found; otherwise, 'Unknown'.
        """
        for bank, pattern in self.bank_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return bank
        return 'Unknown'

    def extract_text_from_image(self, image):
        """
        Extract text from a given image using OCR.

        Args:
            image (PIL.Image): The image from which to extract text.

        Returns:
            str: The text extracted from the image. Returns an empty string on failure.
        """
        try:
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            # Log the error and return an empty string if OCR fails
            logger.error(f"OCR failed: {str(e)}")
            return ""

    def process_pdf(self, pdf_path):
        """
        Process the PDF file to extract transactions and generate an Excel file.

        Steps:
          1. Convert PDF pages to images.
          2. Perform OCR on each image to extract text.
          3. Identify the bank using the extracted text.
          4. Parse transactions using regex-based patterns.
          5. Generate an Excel file with the transaction data.

        Args:
            pdf_path (str): The file path of the PDF to process.

        Returns:
            str: The file path of the generated Excel spreadsheet.

        Raises:
            Exception: Propagates any exception encountered during processing.
        """
        try:
            # Convert all PDF pages into images
            images = convert_from_path(pdf_path)
            
            # Extract text from each image using OCR
            extracted_text = []
            for image in images:
                text = self.extract_text_from_image(image)
                extracted_text.append(text)
            
            # Combine text from all pages to identify the bank
            full_text = ' '.join(extracted_text)
            bank_name = self.identify_bank(full_text)
            
            # Parse transaction data from the extracted text
            transactions = self.parse_transactions(extracted_text)
            
            # Create an Excel file containing the transaction details
            excel_path = self.create_excel(transactions, bank_name)
            
            return excel_path
            
        except Exception as e:
            # Log the error and re-raise the exception for further handling
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise

    def parse_transactions(self, text_list):
        """
        Parse transaction details from a list of extracted text strings.

        Uses regular expressions to extract transaction date, amount, and description.
        Note: Adjust the regex pattern based on the actual format of the PDFs.

        Args:
            text_list (list): List of strings, each containing text from one PDF page.

        Returns:
            list: A list of dictionaries, each representing a transaction.
        """
        transactions = []
        
        for text in text_list:
            # Regex pattern to extract:
            # - Date in format dd/mm/yyyy
            # - Amount which may contain negative signs, digits, commas, and a decimal
            # - Description with non-numeric characters
            pattern = r'(\d{2}/\d{2}/\d{4})\s+([-\d,]+\.\d{2})\s+([^0-9\n]+)'
            matches = re.finditer(pattern, text)
            
            for match in matches:
                date, amount, description = match.groups()
                transactions.append({
                    'Date': date,
                    'Amount': amount,
                    'Description': description.strip()
                })
        
        return transactions

    def create_excel(self, transactions, bank_name):
        """
        Create an Excel file from the list of transactions.

        Converts transaction data into a pandas DataFrame and writes it to an Excel file.
        Ensures the output directory exists before saving.

        Args:
            transactions (list): List of transaction dictionaries.
            bank_name (str): The identified bank name to be used in the filename.

        Returns:
            str: The file path of the generated Excel file.
        """
        # Convert the transactions list to a DataFrame
        df = pd.DataFrame(transactions)
        
        # Define and create the output directory if it doesn't exist
        output_dir = 'processed_files'
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the Excel file path incorporating the bank name
        excel_path = os.path.join(output_dir, f'{bank_name}_transactions.xlsx')
        df.to_excel(excel_path, index=False)
        
        return excel_path

def process_pdf_file(pdf_path):
    """
    Convenience function to process a PDF file using the PDFProcessor class.

    Instantiates the PDFProcessor and processes the provided PDF file.

    Args:
        pdf_path (str): The file path of the PDF to be processed.

    Returns:
        str: The file path of the generated Excel spreadsheet.
    """
    processor = PDFProcessor()
    return processor.process_pdf(pdf_path)
