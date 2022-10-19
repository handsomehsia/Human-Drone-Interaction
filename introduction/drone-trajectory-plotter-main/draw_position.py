from djitellopy import tello
import cv2
from cvzone.FaceDetectionModule import FaceDetector
from plotter import plotter
from threading import Thread
from multiprocessing import Process, Manager
from flight_controller import FlightController
# connect to tello
me = tello.Tello()
me.connect()
# get battery
print(me.get_battery())

manager = Manager()
coordinates = manager.list()
p = Process(target=plotter, args=(coordinates,))
p.start()
fly_controller = FlightController(coordinates)
positioner = Thread(target=fly_controller.positioner)
positioner.start()
positioner.join()
