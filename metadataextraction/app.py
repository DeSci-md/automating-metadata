from flask import Flask, request, redirect, url_for
import os
 
app = Flask(__name__)
 
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
            file.save(os.path.join(app.root_path, filename))
            return 'File uploaded successfully.'
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
 
if __name__ == '__main__':
    app.run()