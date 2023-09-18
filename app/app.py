from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
#import langchain_metadata
import os
from os.path import join, dirname, realpath
import re
import langchain_api as res
import secrets
from dotenv import load_dotenv, find_dotenv  # loading in API keys

# Load in API keys from .env file
load_dotenv(find_dotenv())
api_key = os.getenv("apikey")
openai_api_key = os.getenv("OPENAI_API_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/')
                          
os.environ['OPENAI_API_KEY'] 
#UPLOAD_FOLDER = '/Users/desot1/Downloads/'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['pdf']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 *1000 #accepts upto mb 16 files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Generate a secret key and set it for the Flask app
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


def allowed_file(filename):
    bool1 = '.' in filename and filename.rsplit('.', 1)[1].lower()
    bool = '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']
    print(str(bool1) + str(bool))
    return bool

"""def validate_doi_format(doi):
    doi_pattern = r"^10.\d{4,9}/[-._;()/:A-Z0-9]+$"
    doicheck = re.match(doi_pattern, doi, re.IGNORECASE) is not None
    print("IN validate DOI:" + str(doicheck))
    return doicheck"""

def validate_doi_format(doi):
    doi_pattern_url = r"https?://doi\.org/10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$"
    doi_pattern = r"^10.\d{4,9}/[-._;()/:a-zA-Z0-9]+$"
    doicheck = re.match(doi_pattern, doi) or re.match(doi_pattern_url, doi) is not None
    print("In validate DOI:" + str(doicheck))
    return doicheck


@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # Check if there is a file. If not - go to DOI
       
        file = request.files.get('file')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and file.filename != '':
            if os.path.getsize(os.path.join(basedir, "uploads", file.filename)) > app.config['MAX_CONTENT_LENGTH']: #this function checks the size
                flash('File too large - maximum size is 1 GB')
                return redirect(request.url)
            
            print("Allowed_file:" + str(allowed_file(file.filename)) +"Filename" + str(file.filename))

            if allowed_file(file.filename):
                print("Do we enter this function?")
                filename = secure_filename(file.filename)
                #save_path = os.path.join(basedir, 'uploads', filename)
                #os.makedirs(save_path, exist_ok=True) 
                print(filename)
                file.save(os.path.join(basedir, "uploads", filename))
                print("Before redirecting to Metadata")
                return redirect(url_for('metadata', identifier = filename))
        
        #Handle a DOI upload
        global doi
        doi = request.form.get('doi')  # Get the entered DOI from the form
        if doi and validate_doi_format(doi):  # Validate DOI format
            return redirect(url_for('metadata_doi', doi = doi))
        else:
            flash('Invalid DOI format')
            return redirect(request.url)
        
    return render_template('upload.html')

@app.route('/metadata/<identifier>')
def metadata(identifier): 
    filepath = os.path.join(basedir, "uploads", identifier)
    results = res.pdfprocess(filepath)
    print(results)
    return render_template('metadata.html', results=results)

@app.route('/metadata_doi')
def metadata_doi(): 
    #results = res.paper_data_json_single(doi)
    results = res.openalex(doi)
    #print(results)
    return render_template('metadata_doi.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
