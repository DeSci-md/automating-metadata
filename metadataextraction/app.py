import os
from flask import Flask, flash, request, redirect, url_for, session, render_template, jsonify
from werkzeug.utils import secure_filename
import textract
import json

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # accepts up to 16 MB files
app.config['UPLOAD_FOLDER'] = 'uploads'

from langchain.document_loaders import PyMuPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import langchain_metadata

def extract_text_from_file(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def get_metadata(file_path):
    metadata = langchain_metadata.main(file_path)
    return metadata

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_text = extract_text_from_file(file_path)
            metadata = get_metadata(file_path)
            return render_template('result.html', filename=filename, extracted_text=extracted_text, metadata=metadata)
    return '''
    <!doctype html>
    <html>
    <body>
    <h1>Upload a File</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    </body>
    </html>
    '''

@app.route('/api/text', methods=['GET'])
def get_extracted_text():
    filename = request.args.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    extracted_text = extract_text_from_file(file_path)
    if extracted_text:
        return extracted_text
    return 'Error extracting text.'

@app.route('/api/metadata', methods=['GET'])
def get_api_metadata():
    filename = request.args.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    metadata = get_metadata(file_path)
    if metadata:
        return jsonify(metadata)
    return 'Error retrieving metadata.'

if __name__ == '__main__':
    app.run(debug=True)