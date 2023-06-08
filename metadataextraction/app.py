import os
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
import textract
import json

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_text = extract_text_from_file(file_path)
            if extracted_text is not None:
                metadata = get_metadata(file_path)
                return render_template('result.html', filename=filename, extracted_text=extracted_text, metadata=metadata)
            else:
                flash('Error extracting text from file')
                return redirect(request.url)
    return render_template('upload.html')

def extract_text_from_file(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def get_metadata(file_path):
    metadata = {
        'filename': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'extension': os.path.splitext(file_path)[1][1:]
    }
    return metadata

if __name__ == '__main__':
    app.run(debug=True)