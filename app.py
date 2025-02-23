import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from pdf_processor import process_pdf_file  # Custom module to process PDFs and generate Excel files
from dotenv import load_dotenv

# Load environment variables from a .env file into os.environ
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)

# Configure application settings
# UPLOAD_FOLDER: Directory where uploaded PDFs will be temporarily stored.
# MAX_CONTENT_LENGTH: Limit file size to prevent excessive memory usage (16MB in this case).
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the upload directory exists; if not, create it.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define allowed file extensions for uploads (only PDF files are allowed)
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """
    Check if the provided filename has an allowed extension.
    
    Args:
        filename (str): The name of the file to check.
    
    Returns:
        bool: True if the file extension is allowed; otherwise, False.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """
    Render the homepage with the file upload form.
    
    Returns:
        str: Rendered HTML template for the index page.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file uploads from the user, process the PDF, and return the generated Excel file.
    
    Workflow:
      1. Validate that a file is included in the request.
      2. Check that the file has a valid filename and extension.
      3. Secure the filename and save the file to the designated upload folder.
      4. Process the PDF to generate an Excel spreadsheet.
      5. Return the Excel file as an attachment.
      6. Clean up the uploaded file, regardless of success or failure.
      
    Returns:
        Response: Flask response containing either the generated Excel file or an error message.
    """
    # Check if the file part is present in the request
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    # Validate that a filename is provided
    if file.filename == '':
        return 'No selected file', 400
    
    # Process the file if it is valid and allowed
    if file and allowed_file(file.filename):
        # Sanitize the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the PDF file and generate an Excel file path
            excel_path = process_pdf_file(filepath)
            # Send the generated Excel file back to the client as an attachment
            return send_file(excel_path, as_attachment=True)
        except Exception as e:
            # Return a 500 error if PDF processing fails
            return f'Error processing file: {str(e)}', 500
        finally:
            # Clean up: Remove the uploaded file from the server after processing
            if os.path.exists(filepath):
                os.remove(filepath)
    
    # Return an error response if the file type is invalid
    return 'Invalid file type', 400

if __name__ == '__main__':
    # Run the Flask application; debug is disabled for production use.
    app.run(debug=False)
