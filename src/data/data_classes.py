from flask_sqlalchemy import SQLAlchemy

# create the extension
"""Measurements = db.Table('Measurements',
    db.Column('dateTime', db.DateTime(timezone=True), primary_key=True),
    db.Column('distance', db.Float),#crackmeter distance
    db.Column('rockT25', db.Float),
    db.Column('rockT50', db.Float),
    db.Column('rockT75', db.Float),
    db.Column('sensorT', db.Float)
)"""

def setup_db(db):
    class Measurements(db.Model):
        dateTime = db.Column(db.DateTime(timezone=True), primary_key=True)
        distance = db.Column(db.Float)
        rockT25 = db.Column(db.Float)
        rockT50 = db.Column(db.Float)
        rockT75 = db.Column(db.Float)
        sensorT = db.Column(db.Float)

    db.drop_all()
    db.create_all()

    db.session.query(Measurements).delete()

    return Measurements