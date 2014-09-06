import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import requests

UPLOAD_FOLDER = 'C:\Users\SoniaAzad\Documents\GitHub\mhacks-2014\MHFall14\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #files = {'file': open(file.filename, 'r')}
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            r = requests.post("https://api.moxtra.com/BhsT7RE7i0aJYacX8Svwaf1/pageupload", data=file.filename)
            print r.text
            return redirect(url_for('uploaded_file', filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('template.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)