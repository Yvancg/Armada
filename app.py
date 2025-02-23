import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from pdf_processor import process_pdf_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            excel_path = process_pdf_file(filepath)
            return send_file(excel_path, as_attachment=True)
        except Exception as e:
            return f'Error processing file: {str(e)}', 500
        finally:
            # Clean up uploaded files
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(debug=False)
