# Tello Drone Trajectory Tracking

With this library you can track the trajectory of your tello drone or swarm of drones in real time. In addition, you can easily configure the plotter in the configuration file. In [this blog](https://tivole.github.io/tello/drone/trajectory/2022/02/02/tello-trajectory-real-time.html), you can read more about how the trajectory is calculated.

https://user-images.githubusercontent.com/45293435/152362184-825e48c6-f588-400e-9d46-4bcbf7b0e18a.mp4

## Usage

Install requirements:

```
pip install -r requirements.txt
```

Write IP address of you tello in `config.py` file:

```python
TELLO_IP_ADDRESSES = ["192.168.1.101",]
```

Write your flight commands in `run` method of `flight_controller.py` file:

```python
def run(self):
    self.tellos.parallel(lambda i, tello: tello.takeoff())

    try:
        # Flight commands:
        self.tellos.parallel(lambda i, tello: tello.move_up(30))
        self.tellos.parallel(lambda i, tello: tello.move_right(30))
        self.tellos.parallel(lambda i, tello: tello.move_forward(30))
        self.tellos.parallel(lambda i, tello: tello.move_left(30))
    except Exception as e:
        print(str(e))
    finally:
        self.tellos.parallel(lambda i, tello: tello.land())
        self.tellos.parallel(lambda i, tello: tello.end())
    self.finish = True
```

Run `main.py`:

```
python main.py
```

## Authors

- [Kamran Asgarov](https://github.com/tivole)
- [Anar Mammadov](https://github.com/anarmammad)