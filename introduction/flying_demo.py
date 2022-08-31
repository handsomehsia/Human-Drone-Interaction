from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()
me.move_up(80)

me.send_rc_control(0, 0, 0, 20)

time.sleep(5)
me.send_rc_control(0, 0, 0, 0)

me.land()
