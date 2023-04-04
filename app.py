from flask import Flask, render_template, request
#from flask_wtf import Flaskform
#from wtforms import Stringfield, Submitfield

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'mysecret'

@app.route('/')
def index():
    #### Return a rendered index.html file
    return render_template("index.html")

"""
@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/analysis')
def analysis():
    return render_template("analysis.html")
"""

if __name__ == '__app__':
    app.debug = True
    app.run()
