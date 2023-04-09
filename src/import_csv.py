import openpyxl
from datetime import datetime

wookbook = openpyxl.load_workbook("Crackmeter_distance_data.xlsx")

ws = wookbook.active

db.session.query(CrackmeterDistance).delete()

for row in ws.iter_rows(2, 100):#, ws.max_row):
    datetime_ = datetime.combine(
        (row[0].value).date(),
        row[1].value)

    insert_data = CrackmeterDistance.insert().values(
        dateTime=datetime_,
        distance=row[2].value)

    db.session.execute(insert_data)
    db.session.commit()

#distances = db.session.query(CrackmeterDistance).all()
