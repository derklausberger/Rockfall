import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
#from flask_wtf import Flaskform
#from wtforms import Stringfield, Submitfield

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'mysecret'

@app.route('/')
def index():
    #### Return a rendered index_old.html file
    return render_template("index.html")

@app.route('/upload') #, methods='POST')
def upload():
    files = request.files.getlist('files')
    for file in files:
        fn = secure_filename(file.filename)
        file.save(os.path.join("./static/upload", fn))  # replace FILES_DIR with your own directory
    #return redirect('/')  # change to redirect to your own url
    return render_template("upload.html")

"""
@app.route('/analysis')
def analysis():
    return render_template("analysis.html")
"""

if __name__ == '__main__':
    app.debug = True
    app.run()
