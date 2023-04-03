# Defines app models and routing

@app.route('/')
def index():
    #### Return a rendered index.html file
    return render_template("index.html")

@app.route('/navpage')
def navpage():
    return render_template('navpage.html')
@app.route('/upload')
def analysis():
    return render_template("upload.html")
@app.route('/analysis')
def analysis():
    return render_template("analysis.html")