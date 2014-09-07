import os
import time
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import requests
import hmac
import hashlib
import base64

UPLOAD_FOLDER = 'C:\Users\SoniaAzad\Documents\GitHub\mhacks-2014\MHFall14\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def hmac_sha256(key, msg):
    hash_obj = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    return hash_obj

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    client_id="hhmXl0qEFxM"
    client_secret="hQbxcqM20TQ"
    timestamp=time.time()
    unique_id="story"

    hash=hmac_sha256(client_secret, client_id+unique_id+str(timestamp))
    signature=base64.urlsafe_b64encode(str(hash))
    
    access_token = requests.post("https://api.moxtra.com/oauth/token"+
    "client_id=client_id&"+
    "client_secret=client_secret&"+
    "grant_type=http://www.moxtra.com/auth_uniqueid&"+
    "uniqueid=story&"+
    "timestamp=timestamp&"+
    "signature=signature")

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file', filename=file.filename, access_token=access_token))
    return render_template('first.html')

@app.route('/show/<filename>')
def uploaded_file(filename, access_token='None'):
    r = requests.post("https://api.moxtra.com/BhsT7RE7i0aJYacX8Svwaf1/pageupload?access_token=access_token", data=filename)
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('template.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/view')
def view_gallery():
    r = requests.get("https://api.moxtra.com/BhsT7RE7i0aJYacX8Svwaf1")
    pages = r.data.pages
    return render_template('index.html', pages = pages)

if __name__ == '__main__':
    app.run(debug=True)