# Imports
from os import environ
from os.path import join, dirname, abspath
from utils.scrapper import check_plagiarism
from utils.reporter import generate_report
from utils.file_processor import parse, tokenize, get_meta
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from flask import Flask, flash, request, escape, redirect, url_for, render_template, send_from_directory

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
    if request.method == 'POST' and 'file' in request.files:
        # Restricts multiple-file upload.
        if len(request.files.getlist('file')) > 1:
            error = "You are only allowed to upload one file per transaction."
            return render_template("main/upload.html", error=error)
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
                file.save(userfile)
                rawContent = parse(userfile)
                tokContent = tokenize(rawContent)
                wordCount, charCount = get_meta(rawContent)
                plagIndex, results = check_plagiarism(tokContent, wordCount)
                print(10 * '-')
                print(results)
                print(10 * '-')
                print(app.config['DOWNLOAD_FOLDER'])
                generate_report(filename.split('.', 1)[0], plagIndex, results, wordCount, charCount, app.config['DOWNLOAD_FOLDER'])
                
                #for key, value in results.items():
                #    if value != "":
                #        print(f"'{key}' --> '{value}'")
                #    else:
                #        print(f"No source for '{key}'")
                return render_template('main/download.html', filename=filename)
    # Renders the main upload file view.
    return render_template('main/upload.html')          

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

# Execution Config.
if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)