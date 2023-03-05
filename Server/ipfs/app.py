from operator import and_
from flask import Flask
from flask import render_template, request, redirect, session, url_for, flash, make_response
from sqlalchemy import ForeignKey, desc, asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import ipfsapi
import os
import webbrowser
import pdfkit

UPLOAD_FOLDER = r'static\uploads'

app = Flask(__name__)
app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyLTFTTTRSUTlfLS1IVEpGM0QiLCJpYXQiOjE2NjI5ODc0Nzd9.mCvSd2o2vw5Gs7grkBLkW75dlgVcJ-aiqMzfVUvG-q4'
app.config['SQLALCHEMY_DATABASE_URI']=''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class User(db.Model): 
  __tablename__='user'
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(40))
  email=db.Column(db.String(40))
  password=db.Column(db.String(40))
 
  def __init__(self,name,email,password):
    self.name=name
    self.email=email
    self.password=password

class UploadFile(db.Model):
  __tablename__='upload'
  id=db.Column(db.Integer,primary_key=True)
  id_user=db.Column(db.Integer, ForeignKey(User.id))
  file_name=db.Column(db.String(120))
  date=db.Column(db.Date)
  file_hash=db.Column(db.String(120))
  pin_status=db.Column(db.Integer)
 
  def __init__(self,id_user,file_name,date,file_hash,pin_status):
    self.id_user=id_user
    self.file_name=file_name
    self.date=date
    self.file_hash=file_hash
    self.pin_status=pin_status

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-submit', methods = ['POST'])
def register_submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    user = User(name, email, password)
    db.create_all()
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login-submit', methods = ['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter(and_(User.email == email, User.password == password)).first()
    if user:
      session['user_id'] = user.id
      return redirect('/')
    else:
      flash("Gagal login\nEmail atau Password salah")
      return redirect('/login')

@app.route('/')
def home():
    try:
      user_data = User.query.filter_by(id=session['user_id']).first().name
    except:
      pass
    if 'user_id' in session:
      files_data = UploadFile.query.filter_by(id_user=session['user_id']).order_by(UploadFile.pin_status.desc(), UploadFile.date.asc())
      c = files_data.count()
      return render_template('upload.html', datas = files_data, user = user_data, c = c)
    else:
      return redirect(url_for('login'))
    
@app.route('/filter-pin')
def filter_pin():
    user_data = User.query.filter_by(id=session['user_id']).first().name
    if 'user_id' in session:
      files_data = UploadFile.query.filter_by(id_user=session['user_id'], pin_status=1).order_by(UploadFile.date.asc())
      c = files_data.count()
    return render_template('upload.html', datas = files_data, user = user_data, c = c)

@app.route('/filter-unpin')
def filter_unpin():
    user_data = User.query.filter_by(id=session['user_id']).first().name
    if 'user_id' in session:
      files_data = UploadFile.query.filter_by(id_user=session['user_id'], pin_status=0).order_by(UploadFile.date.asc())
      c = files_data.count()
    return render_template('upload.html', datas = files_data, user = user_data, c = c)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route('/uploader', methods = ['POST'])
def upload_file():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    api = ipfsApi.Client('127.0.0.1', 5001)
    res = api.add(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    file_data = UploadFile.query.filter_by(file_hash=res['Hash']).first()
    if not file_data:
      if 'user_id' in session:
        user = UploadFile(session['user_id'], secure_filename(f.filename), date.today(), res['Hash'], 1)
        db.session.add(user)
        db.session.commit()
      return redirect('/')
    else:
      hash = res['Hash']
      flash(f"{hash} sudah ada")
      return redirect('/')
    
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    # id_file = request.args.get('id')
    file_to_update = UploadFile.query.get_or_404(id)
    return render_template('update.html', file_to_update=file_to_update)
      
@app.route('/edit-file/<int:id>', methods = ['POST', 'GET'])
def edit_file(id):
    file_to_update = UploadFile.query.get_or_404(id)
    if request.method == "POST":
      file_to_update.file_name = request.form['name']
      file_to_update.date = date.today()
      try:
        db.session.commit()
        return redirect('/')
      except:
        return "There was problem"
    else:
        return render_template('update.html', file_to_update=file_to_update)
  
@app.route('/delete-file')
def delete_file():
    id_file = request.args.get('id')
    UploadFile.query.filter(UploadFile.id == id_file).delete()
    db.session.commit()
    return redirect('/')

@app.route('/pin-file')
def pin_file():
    hash_file = request.args.get('file_hash')
    file_data = UploadFile.query.filter(UploadFile.file_hash == hash_file).first()
    file_data.pin_status = 1
    # api = ipfsApi.Client('127.0.0.1', 5001)
    # api.pin_add(id_file[:10])
    db.session.commit()
    return redirect('/')

@app.route('/rm-pin-file')
def rm_pin_file():
    hash_file = request.args.get('file_hash')
    api = ipfsApi.Client('127.0.0.1', 5001)
    # api.pin_rm(hash_file)
    file_data = UploadFile.query.filter(UploadFile.file_hash == hash_file).first()
    file_data.pin_status = 0
    db.session.commit()
    return redirect('/')
  
@app.route('/print-file')
def print_file():
    return render_template('print.html')
  
@app.route('/print-from-hash', methods = ['POST'])
def print_from_hash():
    fileHash = request.form['hash']
    qr_url = f"http://api.qrserver.com/v1/create-qr-code/?data=https://ipfs.io/ipfs/{fileHash}?filename={fileHash}&size=200x200"
    doc_url = f"https://ipfs.io/ipfs/{fileHash}"
    return render_template('file.html', qr = qr_url, doc = doc_url)
    
@app.route('/direct-print')
def direct_print():
    # hash_file = request.args.get('file_hash')
    # file_data = UploadFile.query.filter(UploadFile.file_hash == hash_file).first().file_hash
    # qr_url = f"http://api.qrserver.com/v1/create-qr-code/?data=https://ipfs.io/ipfs/{file_data}?filename={file_data}&size=200x200"
    # doc_url = f"https://ipfs.io/ipfs/{file_data}"
    # hash_file = request.args.get('file_hash')
    # file_data = UploadFile.query.filter(UploadFile.file_hash == hash_file).first().file_hash
    qr_url = f"http://api.qrserver.com/v1/create-qr-code/?data=https://ipfs.io/ipfs/QmauYxe2pwhiRShKkW4GdzN9498FpePAWEimPK5v3tVPY5?filename=QmauYxe2pwhiRShKkW4GdzN9498FpePAWEimPK5v3tVPY5&size=200x200"
    doc_url = f"https://ipfs.io/ipfs/QmauYxe2pwhiRShKkW4GdzN9498FpePAWEimPK5v3tVPY5"
    # rendered = render_template('file.html', qr = qr_url, doc = doc_url)
    # path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    # pdf = pdfkit.from_string(rendered, configuration=config)
    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return render_template('file.html', qr = qr_url, doc = doc_url)

@app.route('/find')
def find():
    return render_template('find.html')
  
@app.route('/verifier')
def verifier():
    return render_template('verifier.html')

@app.route('/find-ipfs', methods = ['POST'])
def find_to_ipfs():
    fileHash = request.form['text']
    webbrowser.open(f"https://ipfs.io/ipfs/{fileHash}")
    return redirect("/")
  
@app.route('/file-verifier', methods = ['POST'])
def verify_file():
    try:
      f = request.files['file1']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      api = ipfsApi.Client('127.0.0.1', 5001)
      res = api.add(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      file_data = UploadFile.query.filter_by(file_hash=res['Hash']).first()
      
      if not file_data:
        flash(f"file asli tidak ditemukan")
        return redirect('/verifier')
      else:
        # tgl = UploadFile.query.filter_by(file_hash=res['Hash']).first().date
        tgl = file_data.date
        nfile = file_data.file_name
        user_data = User.query.filter_by(id=session['user_id']).first().name
        flash(f"file asli terverifikasi!, , file name: {nfile}, pemilik: {user_data}, tanggal upload: {tgl}")
        return redirect('/verifier')
    except:
      flash(f"something wrong about the file checker")
      return redirect('/verifier')

if __name__ == '__main__':
    app.run(debug=True)
