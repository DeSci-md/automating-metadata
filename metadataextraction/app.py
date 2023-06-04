from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files: # Check if the post request has the file
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '': # Check; if user doesn't upload a file in the request
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.root_path + '/uploads', filename))
            return 'File uploaded successfully'
        
        return '''
            <!doctype html>
            <html>
                <body>
                    <h1>Upload a file</h1>
                    <form method="POST" enctype="multipart/form-data">
                        <input type="file" name="file">
                        <input type="submit" values="Upload">
                    </form>
                </body>
            </html>
        '''

if __name__ == '__main__':
    app.run()