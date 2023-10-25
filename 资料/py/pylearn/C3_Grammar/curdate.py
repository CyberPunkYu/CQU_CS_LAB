#curdate.py
import datetime
curDate = datetime.datetime.now()
print(curDate.year,"-",curDate.month,"-",curDate.day,"\n",\
    curDate.hour,":",curDate.minute,":",curDate.second)
print(type(curDate))