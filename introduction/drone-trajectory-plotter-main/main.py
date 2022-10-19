from threading import Thread
from multiprocessing import Process, Manager

from flight_controller import FlightController
from plotter import plotter

if __name__ == '__main__':

    manager = Manager()

    coordinates = manager.list()
    print('!!!')
    print(coordinates)
    print('!!!')
    fly_controller = FlightController(coordinates)

    p = Process(target=plotter, args=(coordinates,))
    p.start()

    positioner = Thread(target=fly_controller.positioner)
    positioner.start()

    # Main thread start
    fly_controller.run()
    # Main thread end

    fly_controller.end()
    positioner.join()
