# Imports
from os import environ, remove,listdir
from os.path import join, dirname, abspath, exists, isfile
from flask_wtf.csrf import CSRFProtect
from utils.scrapper import check_plagiarism
from utils.reporter import generate_report
from utils.file_processor import parse, tokenize, get_meta
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from markupsafe import escape

file_path = None
report_path = None

# App Instantiation & Config.
app = Flask(__name__)
#environment_configuration = environ['CONFIGURATION_SETUP']
#app.config.from_object(environment_configuration)
app.config["APP_NAME"] = "PlagPatrol"
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["DOWNLOAD_FOLDER"] = dirname(abspath(__file__)) + '/tmp/'
app.config["ENV"] = "development"
app.config["SECRET_KEY"] = "69535ae0bbbcaf0e3ab71bbb626e36541b8c0c61d9180f6e"
app.config["DEBUG"] = True

csrf = CSRFProtect(app)

# Function For File Validity Check.
def check_file_extension(filename):
    '''Conducts file validity checking via extension comparison.
    Args:
        filename (str): Name of the file to be checked.
    Returns:
        bool: Returns True if it is valid and False elsewise.
    ''' 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf','txt','docx']

# Renders The Default Upload Page, Listens For Files and Downloads Them.
@app.route('/', methods=['GET','POST'])
def upload_file():
    '''Renders the default upload page, listens for files in requests 
    and downloads them to /tmp/.
    Returns:
        str: Returns the html parsed string to jinja2 for rendering 
        the requested page.
    '''
    global file_path
    global report_path
    if file_path != None and exists(file_path):
        remove(file_path)
    if report_path != None and exists(report_path):
        remove(report_path)

    if request.method == 'POST' and 'file' in request.files:
        # Restricts multiple-file upload.
        if len(request.files.getlist('file')) > 1:
            error = "You are only allowed to upload one file per transaction."
            return render_template("upload.html", error=error)
        else:
            # Fetches the file from request and secures the filename from injection.
            file = request.files['file']
            filename = secure_filename(escape(file.filename))
            # Flashes message if empty upload pressed.
            if filename == '': 
                flash("No selected file.")
                return redirect(request.url)
            # Saves the file if everything is valid.
            if file and check_file_extension(filename):
                userfile = join(app.config['DOWNLOAD_FOLDER'], filename)
                file_path = userfile
                file.save(userfile)
                rawContent = parse(userfile)
                tokContent = tokenize(rawContent)
                wordCount, charCount = get_meta(rawContent)
                plagIndex, results = check_plagiarism(tokContent, wordCount)
                report = generate_report(filename.split('.', 1)[0], plagIndex, results, wordCount, charCount, app.config['DOWNLOAD_FOLDER'])
                report_path = report
                return render_template('download.html', filename=filename, report=report)
    
    if request.method == 'POST' and 'text' in request.form:
        rawContent = request.form['text']
        print(rawContent)
        if rawContent == '': 
            flash("No text.")
            return redirect(request.url)
        else:
            tokContent = tokenize(rawContent)
            wordCount, charCount = get_meta(rawContent)
            plagIndex, results = check_plagiarism(tokContent, wordCount)
            report = generate_report('txt', plagIndex, results, wordCount, charCount, app.config['DOWNLOAD_FOLDER']) 
            return render_template('download.html', filename='txt.txt', report=report)

    # Renders the main upload file view.
    return render_template('upload.html')          

# Listens For Download, Sends The Requested File.
@app.route('/files/<filename>', methods=['GET','POST'])
def download_file(filename):
    '''Listens for download request and sends the requested file.
    Args:
        filename (str): The name of the requested file.
    Returns:
        file: The requested file sent to the frontend.
    '''
    # Secures the file name from injection.
    filename = secure_filename(escape(filename))
    filename = filename.split('.', 1)[0]
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], f'{filename}_plagiarism_report.pdf', as_attachment=True)

# Hidden route to delete files in '\tmp\' folder.
@app.route('/delete')
def delete_files():
    for file_name in listdir(app.config['DOWNLOAD_FOLDER']):
        file_path = join(app.config['DOWNLOAD_FOLDER'], file_name)
        if isfile(file_path) and file_name != 'placeholder.txt':
            remove(file_path)
    return redirect('/')

# Execution Config.
if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)