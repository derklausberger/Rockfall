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

def createMeasurementsModel(db):
    class Measurements(db.Model):
            pilotCase = db.Column(db.String, primary_key = True)
            dateTime = db.Column(db.DateTime(timezone=True), primary_key=True)
            
            airHumidity = db.Column(db.Float)
            
            airTemp = db.Column(db.Float)

            crackmeterDistance = db.Column(db.Float)
            
            rainfall = db.Column(db.Float)

            TRockSurface_A54C8C = db.Column(db.Float)
            TRockSurface_A54C8D = db.Column(db.Float)
            
            rockT25 = db.Column(db.Float)
            rockT50 = db.Column(db.Float)
            rockT75 = db.Column(db.Float)
            sensorT = db.Column(db.Float)
    return Measurements

def setupUsers(db):
    class Users(db.Model):
            username = db.Column(db.String, primary_key = True)
            password = db.Column(db.String)

    db.create_all()
    
    user = "admin"
    pw = "pw"

    entry = db.session.execute(db.select(Users).filter_by(username=user)).scalar()

    insert = False

    if entry is None:
        insert = True
        entry = Users()
    
    entry.username = user
    entry.password = pw

    if insert == True:
        db.session.add(entry)

    db.session.commit()

    return Users

def setup_db(db):
    # uncomment to insert---------------
    #db.drop_all()
    db.create_all()
    #db.session.query(Measurements).delete()

    #return Measurements