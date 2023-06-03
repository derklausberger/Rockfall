from typing import List, Union
from datetime import datetime

def get_freeze_thaw_cycles(datetimes: List[datetime], air_temp: List[float]) -> List[float]:
    cycles = []

    cooling_begin = freezing_begin = warming_begin = thawing_begin = None

    print(air_temp)
    for idx, x in enumerate(air_temp):
        if (x):
            if (x > 0):
                if (freezing_begin == None and len(air_temp) > (idx + 1) and air_temp[idx + 1] != None):
                    if (x > air_temp[idx + 1] and cooling_begin == None):
                        cooling_begin = idx
                    elif (x < air_temp[idx + 1]):
                        cooling_begin = None
                
                if (cooling_begin != None and freezing_begin != None and warming_begin != None):
                    thawing_begin = idx

            elif (x < 0 and cooling_begin != None):
                if (freezing_begin == None):
                    freezing_begin = idx

                if (freezing_begin != None):
                    if (warming_begin == None and len(air_temp) > (idx + 1) and air_temp[idx + 1] != None):
                        if (air_temp[idx + 1] > air_temp[freezing_begin]):
                            warming_begin = idx
                    elif (warming_begin != None and air_temp[warming_begin] > x):
                        warming_begin = None

            if (cooling_begin != None and freezing_begin != None and warming_begin != None and thawing_begin != None):
                print(cooling_begin, freezing_begin, warming_begin, thawing_begin)
                cycles.append({
                    "cb": datetimes[cooling_begin],
                    "fb": datetimes[freezing_begin],
                    "wb": datetimes[warming_begin],
                    "tb": datetimes[thawing_begin]
                    })
                
                cooling_begin = thawing_begin
                freezing_begin = warming_begin = thawing_begin = None
                
    return cycles