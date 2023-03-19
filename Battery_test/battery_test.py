import cv2
from djitellopy import tello
import datetime

# cap = cv2.VideoCapture(0)
# datetime.datetime.now()
me = tello.Tello()
me.connect()
me.streamoff()
me.streamon()
me.takeoff()

batterytmp = me.get_battery()
timetmp = datetime.datetime.now()
print(timetmp)

timerecord = timetmp
batteryrecord = batterytmp

path = 'output.txt'
f = open(path, 'w')
f.write('Hello World')


while True:
    if batterytmp != batteryrecord:
        print(batterytmp, timetmp)
        batteryrecord = batterytmp
        timerecord = timetmp
    batterytmp = me.get_battery()
    timetmp = datetime.datetime.now()

    me.send_rc_control(0, 0, 0, 0)
