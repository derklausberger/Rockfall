import os
import json
import src.data.data_classes as dc
import src.import_csv as ic
from src.py.algorithms import get_freeze_thaw_cycles

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath('src/html/')
static_dir = os.path.abspath('res/')
# create the app
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'asdfasgqwez938z4hosohdphpoHADSKN'

# create the extension
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the app with the extension
db.init_app(app)


with app.app_context():
	#with open("src/data/data_classes.py") as f:
	#	exec(f.read())
	Measurements = dc.createMeasurementsModel(db)
	Users = dc.setupUsers(db)

	dc.setup_db(db)
	
	#with open("src/import_csv.py") as f:
	#	exec(f.read())

	# uncomment to insert---------------
	#ic.import_db(db, Measurements)


	#uncomment for testing cycles algorithm
	#ic.import_file(db, Measurements, "AirTemp.xlsx", ic.FileType["AirTemp"])
	#pilotCases = [e.pilotCase for e in db.session.query(Measurements).group_by(Measurements.pilotCase).all()]
	
	#for pc in pilotCases:
	#at = [e.airTemp for e in db.session.query(Measurements).filter_by(pilotCase="Brezno").all()]
	#dt = [e.dateTime for e in db.session.query(Measurements).filter_by(pilotCase="Brezno").all()]
	#print(get_freeze_thaw_cycles(dt, at))

@app.route('/')
def index():
	#measurements = db.session.query(Measurements).all()
	if 'username' in session:
		print(session['username'])
		return render_template('index.html', loggedIn = True)
	else:
		return redirect(url_for("login"))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if 'username' in session:
		if request.method == 'POST':
			for formname, file in request.files.items():
				if not file.filename == '':
					print(file.filename)
					filename = formname + ".xlsx"
					file.save(filename)

					ic.import_file(db, Measurements, filename, ic.FileType[formname])
		
		return render_template("upload.html", loggedIn = True)
	else:
		return redirect(url_for("login"))

@app.route('/delete', methods=['POST'])
def delete():
	if 'username' in session:
		db.drop_all()
		db.create_all()

		return render_template("upload.html", loggedIn = True)
	else:
		return redirect(url_for("login"))


@app.route('/login_page', methods=['GET'])
def login_page():
	if 'username' in session:
		return redirect(url_for("index"))
	else:
		return redirect(url_for("login"))

@app.route('/login', methods=['GET'])
def login():
	user = request.args.get('username', None)
	pw = request.args.get('password', None)

	user_entry = db.session.execute(db.select(Users).filter_by(username=user)).scalar()
	if (user_entry == None):
		return render_template("login.html", msg="User does not exist")
	else:
		if (user_entry.password != pw):
			return render_template("login.html", msg="Password is incorrect")
		else:
			session['username'] = user
			return redirect(url_for("index"))
		
@app.route('/logout', methods=['GET'])
def logout():
	session.pop('username', None)
	
	return redirect(url_for("login"))

@app.route('/plot')
def output_plot():
	pilotCases = [e.pilotCase for e in db.session.query(Measurements).group_by(Measurements.pilotCase).all()]
	
	data = {}
	for pc in pilotCases:
		#datetimes
		dt = [e.dateTime for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		
		#air temperature
		at = [e.airTemp for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		
		cycles = (get_freeze_thaw_cycles(dt, at) if any(at) else [])
		print("app", cycles)

		#air humidity
		ah = [e.airHumidity for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		
		#crack distance
		cd = [e.crackmeterDistance for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]

		#rainfall
		rf = [e.rainfall for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		
		#temp rock surface
		trsA54C8C = [e.TRockSurface_A54C8C for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		trsA54C8D = [e.TRockSurface_A54C8D for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]

		#rock temperature
		rt25 = [e.rockT25 for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		rt50 = [e.rockT50 for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		rt75 = [e.rockT75 for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]
		st = [e.sensorT for e in db.session.query(Measurements).filter_by(pilotCase=pc).all()]

		data.update(
			{pc: {
				"dt": dt,
				"Air temperature": [at, "degr"],
				"Air humidity": [ah, "perc"],
				"Crackmeter distance": [cd, "mm"],
				"Rainfall": [rf, "mm"],
				"Temp rock surface A54C8C": [trsA54C8C, "degr"],
				"Temp rock surface A54C8D": [trsA54C8D, "degr"],
				"Rock T-25 cm": [rt25, "degr"],
				"Rock T-50 cm": [rt50, "degr"],
				"Rock T-75 cm": [rt75, "degr"],
				"Sensor T": [st, "degr"],
				"ftc": cycles
			}}
		)

	return render_template(
		'/plot.html',
		data = data,
		loggedIn = ('username' in session)
	)

"""dt=dt,
		cdy=json.loads(json.dumps(cdy)),
		rt25y=json.loads(json.dumps(rt25y)),
		rt50y=json.loads(json.dumps(rt50y)),
		rt75y=json.loads(json.dumps(rt75y)),
		sty=json.loads(json.dumps(sty))
	)
"""

if __name__ == '__main__':
	app.run(port=5000)