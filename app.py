import base64
import io
import mpld3
import os

from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy

from matplotlib import pyplot as plt
from matplotlib import dates as mdates

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath('src/templates')


# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__, template_folder=template_dir)

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
	crackmeter_data = db.session.query(CrackmeterDistance).all()
	return render_template('/index.html', data=crackmeter_data)


def on_plot_hover(event):
    # Iterating over each data member plotted
    for curve in plot.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            print("over %s" % curve.get_gid())


@app.route('/plot')
def output_plot():
	fig, ax = plt.subplots()
    
	dateTimes = [d.dateTime for d in db.session.query(CrackmeterDistance).all()]
	y = [d.distance for d in db.session.query(CrackmeterDistance).all()]
	
	
	#plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
	plt.plot_date(dateTimes, y)
	plt.gcf().autofmt_xdate()

	plt.xlabel("Date")
	plt.ylabel("Distance in mm")

	plt.title("Crackmeter Distances") 
	
	try:
		mpld3.save_html(fig, "src/templates/plot.html")
	except FileNotFoundError:
		print("File not found.")

	return render_template('/plot.html')


if __name__ == '__main__':
	app.run(port=5000)