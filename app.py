import base64
import io
import mpld3
import os
import json

from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy

from matplotlib import pyplot as plt
from matplotlib import dates as mdates

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath('src/templates')

# create the app
app = Flask(__name__, template_folder=template_dir)

# create the extension
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the app with the extension
db.init_app(app)

with app.app_context():
	db.drop_all()

	with open("src/data/data_classes.py") as f:
		exec(f.read())
	
	with open("src/import_csv.py") as f:
		exec(f.read())
	

@app.route('/')
def index():
	measurements = db.session.query(Measurements).all()
	return render_template('/index.html', data=measurements)

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