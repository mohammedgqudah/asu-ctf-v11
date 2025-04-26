from hashlib import sha512
from flask import Flask, redirect, render_template, request
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

import os
import pathlib
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", files=os.listdir(UPLOAD_FOLDER))

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "File is missing", 400

    file = request.files['file']

    if file.filename == '':
        return "Filename is empty", 400

    # the file exists and the extension is allowed
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    else:
        return "Only txt files are allowed", 400

@app.route('/process', methods=['get'])
def flag():
    filename = request.args.get('filename')
    if filename is None:
        return "You must specify a file", 400

    path = safe_join(UPLOAD_FOLDER, filename)

    if path is None:
        return "Invalid file name", 400

    path = pathlib.Path(path)

    if not os.path.exists(path):
        return "File does not exist", 404

    with open(path, 'r') as f:
        content = f.read()
        if "flag()" in content:
            # reject the file
            return "File rejected.", 400
        else:
            # process the file
            fhash = sha512(content.encode()).hexdigest()
            print(f"process `{path}`, hash = `{fhash}`", flush=True)
            return render_template("process.html", content=process_file(path))

def process_file(path: pathlib.Path):
    """
    Returns the flag if the file contains `flag()`
    """
    with open(path) as f:
        content = f.read()

        if "flag()" in content:
            return os.getenv("FLAG", "ASU{fake_flag}")
        else:
            return content

