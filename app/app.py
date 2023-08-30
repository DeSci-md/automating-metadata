import os
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
import langchain_metadata
from os.path import join, dirname, realpath

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/')
                          
os.environ['OPENAI_API_KEY'] 
#UPLOAD_FOLDER = '/Users/desot1/Downloads/'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['pdf']
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 *1000 #accepts upto mb 16 files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    bool1 = '.' in filename and filename.rsplit('.', 1)[1].lower()
    bool = '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']
    print(str(bool1) + str(bool))
    return bool

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
        
        #if os.path.getsize(basedir + file.filename) > app.config['MAX_CONTENT_LENGTH']: #this function checks the size
         #   flash('File too large - maximum size is 1 GB')
        #    return redirect(request.url)
        print("Allowed_file:" + str(allowed_file(file.filename)) +"Filename" + str(file.filename))


        if allowed_file(file.filename):
            print("Do we enter this function?")
            filename = secure_filename(file.filename)
            #save_path = os.path.join(basedir, 'uploads', filename)
            #os.makedirs(save_path, exist_ok=True) 
            print(filename)
            file.save(os.path.join(basedir, "uploads", filename))
            #filepath = os.path.join(basedir, "uploads", filename)
            #session['filepath'] = filepath
            print("Before redirecting to Metadata")
            return redirect(url_for('metadata', filename = filename))
    
    return render_template('upload.html')

@app.route('/metadata/<filename>')

def metadata(filename): 
    #if __name__ == "__main__": 
    #metadata('/Users/desot1/Downloads/propermotions.pdf')
    filepath = os.path.join(basedir, "uploads", filename)
    print(filepath)
    results = langchain_metadata.metadata(filepath)
    return render_template('metadata.html', results=results)
    #return langchain_metadata.main(filepath)

if __name__ == "__main__":
    app.run(debug=True)
