import os
import json
import src.data.data_classes as dc
import src.import_csv as ic

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath('src/html/')
static_dir = os.path.abspath('res/')
# create the app
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


# create the extension
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the app with the extension
db.init_app(app)

with app.app_context():
	db.drop_all()

	#with open("src/data/data_classes.py") as f:
	#	exec(f.read())
	Measurements = dc.setup_db(db)
	
	#with open("src/import_csv.py") as f:
	#	exec(f.read())

	ic.import_db(db, Measurements)
	

@app.route('/')
def index():
	measurements = db.session.query(Measurements).all()
	return render_template('index.html', data=measurements)

from werkzeug.utils import secure_filename

@app.route('/upload') #, methods='POST')
def upload():
    files = request.files.getlist('files')
    for file in files:
        fn = secure_filename(file.filename)
        file.save(os.path.join("./static/upload", fn))  # replace FILES_DIR with your own directory
    #return redirect('/')  # change to redirect to your own url
    return render_template("upload.html")

@app.route('/plot')
def output_plot():
	#crack distance datetimes
	dt = [e.dateTime for e in db.session.query(Measurements).all()]
	cdy = [e.distance for e in db.session.query(Measurements).all()]

	#rock temperature datetimes
	#rtdt = [e.dateTime for e in db.session.query(Measurements).all()]
	rt25y = [e.rockT25 for e in db.session.query(Measurements).all()]
	rt50y = [e.rockT50 for e in db.session.query(Measurements).all()]
	rt75y = [e.rockT75 for e in db.session.query(Measurements).all()]
	sty = [e.sensorT for e in db.session.query(Measurements).all()]

	return render_template(
		'/plot.html',
		dt=dt,
		cdy=json.loads(json.dumps(cdy)),
		rt25y=json.loads(json.dumps(rt25y)),
		rt50y=json.loads(json.dumps(rt50y)),
		rt75y=json.loads(json.dumps(rt75y)),
		sty=json.loads(json.dumps(sty))
	)

if __name__ == '__main__':
	app.run(port=5000)