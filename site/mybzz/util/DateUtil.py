import time
import datetime

def currentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def currentDate():
    return datetime.date.today()