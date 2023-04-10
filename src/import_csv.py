import openpyxl
from datetime import datetime

#import crackmeterDistance data
def import_crackmeterDistance():
    wookbook = openpyxl.load_workbook("Crackmeter_distance_data.xlsx")
    ws = wookbook.active

    for row in ws.iter_rows(2, 100):#, ws.max_row):
        datetime_ = datetime.combine(
            (row[0].value).date(),
            row[1].value)

        m = db.session.execute(db.select(Measurements).filter_by(dateTime=datetime_)).scalar()

        if m is None:
            item = Measurements(
                dateTime=datetime_,
                distance=row[2].value,
                rockT25=None,
                rockT50=None,
                rockT75=None,
                sensorT=None)
                
            db.session.add(item)
        else:
            m.distance=0

    db.session.commit()


#import rockTemp data
def import_rockTemp():
    wookbook = openpyxl.load_workbook("Rock_Temp_data.xlsx")
    ws = wookbook.active

    for row in ws.iter_rows(2, 100):#, ws.max_row):
        datetime_ = datetime.combine(
            (row[0].value).date(),
            row[1].value)

        m = db.session.execute(db.select(Measurements).filter_by(dateTime=datetime_)).scalar()

        if m is None:
            print("hier")
            insert_data = Measurements.insert().values(
                dateTime=datetime_,
                distance=None,
                rockT25=row[2].value,
                rockT50=row[3].value,
                rockT75=row[4].value,
                sensorT=row[5].value)
                
            db.session.execute(insert_data)
        else:
            m.rockT25=row[2].value
            m.rockT50=row[3].value
            m.rockT75=row[4].value
            m.sensorT=row[5].value

    db.session.commit()

db.session.query(Measurements).delete()

import_crackmeterDistance()
import_rockTemp()