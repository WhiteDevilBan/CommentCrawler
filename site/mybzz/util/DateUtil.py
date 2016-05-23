import time
import datetime


TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
def currentTime():
    return time.strftime(TIMEFORMAT, time.localtime(time.time()))

def currentDate():
    return datetime.date.today()

def lomgToStrTime(t):
    return time.strftime(TIMEFORMAT, time.localtime(t))