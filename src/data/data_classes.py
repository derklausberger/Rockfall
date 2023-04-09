from flask_sqlalchemy import SQLAlchemy

# create the extension



CrackmeterDistance = db.Table('CrackmeterDistance',
    db.Column('dateTime', db.DateTime(timezone=True), primary_key=True),
    db.Column('distance', db.Float)
)
db.drop_all()

db.create_all()