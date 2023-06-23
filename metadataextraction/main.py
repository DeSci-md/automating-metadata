import os
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
import langchain_metadata

os.environ['OPENAI_API_KEY'] 
UPLOAD_FOLDER = '/Users/desot1/Downloads'

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 *1000 #accepts upto mb 16 files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
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
        
        if os.path.getsize(file.filename) > app.config['MAX_CONTENT_LENGTH']: #this function checks the size
            flash('File too large - maximum size is 1 GB')
            return redirect(request.url)
        
        if file in app.config['UPLOAD_EXTENSIONS']:
            filename = secure_filename(file.filename)
            filepath = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['filepath'] = filepath
            redirect(url_for('get_metadata', filename=filename))
    
    return render_template('upload.html')

@app.route('/metadata')

def metadata(filename): 
    #if __name__ == "__main__": 
    #metadata('/Users/desot1/Downloads/propermotions.pdf')
    file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    results = langchain_metadata.metadata(file_location)
    return render_template('metadata.html', results=results)
    #return langchain_metadata.main(filepath)

if __name__ == "__main__":
    app.run(debug=True)
