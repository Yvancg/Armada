import os
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from PyPDF2 import PdfReader
import re
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.bank_patterns = {
            'Bank1': r'Account\s*Statement.*Bank1',
            'Bank2': r'Statement.*Bank2',
            # Add patterns for other banks
        }
    
    def identify_bank(self, text):
        for bank, pattern in self.bank_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return bank
        return 'Unknown'

    def extract_text_from_image(self, image):
        try:
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            return ""

    def process_pdf(self, pdf_path):
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            # Extract text from each page
            extracted_text = []
            for image in images:
                text = self.extract_text_from_image(image)
                extracted_text.append(text)
            
            # Identify bank
            full_text = ' '.join(extracted_text)
            bank_name = self.identify_bank(full_text)
            
            # Parse transactions
            transactions = self.parse_transactions(extracted_text)
            
            # Create Excel file
            excel_path = self.create_excel(transactions, bank_name)
            
            return excel_path
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise

    def parse_transactions(self, text_list):
        transactions = []
        
        for text in text_list:
            # Extract transaction details using regex patterns
            # This is a simplified example - adjust patterns based on actual PDF format
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
        df = pd.DataFrame(transactions)
        
        # Create output directory if it doesn't exist
        output_dir = 'processed_files'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to Excel
        excel_path = os.path.join(output_dir, f'{bank_name}_transactions.xlsx')
        df.to_excel(excel_path, index=False)
        
        return excel_path

def process_pdf_file(pdf_path):
    processor = PDFProcessor()
    return processor.process_pdf(pdf_path)
