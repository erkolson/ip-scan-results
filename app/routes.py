import os
from flask import render_template, flash, request, redirect, url_for
from app import app
from modules.storage.sqlite import load_db, get_ip, get_host, get_hosts_open_port, get_all
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['xml'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('XSS_KEY')

def allowed_extension(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/scan')
def all():
    hosts = get_all()
    return render_template('hosts.html', hosts=hosts)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_extension(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            (num_stored, summary) = load_db(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/scan')
    # GET
    return render_template('load.html')

@app.route('/scan/open/<port>')
def open_port(port):
    hosts = get_hosts_open_port(port)
    return render_template('hosts.html', hosts=hosts)
