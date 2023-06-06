from flask import Flask, request, redirect, url_for, render_template
import os
import textract
 
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
def extract_text_from_file(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser may submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_text = extract_text_from_file(file_path)
            return render_template('result.html', filename=filename, extracted_text=extracted_text)
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
 
if __name__ == '__main__':
    app.run()