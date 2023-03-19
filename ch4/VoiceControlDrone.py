from urllib import response
from vosk import Model, KaldiRecognizer
import pyaudio
from djitellopy import tello

me = tello.Tello()
me.connect()
print(me.get_battery())

model = Model(
    r"/Users/quentin/Desktop/TBSI/HCI projects/drone_object_detection/ch4/vosk-model-small-en-us-0.15")

recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()

listening = False


def get_command():
    listening = True
    stream = mic.open(format=pyaudio.paInt16, channels=1,
                      rate=16000, input=True, frames_per_buffer=8192)
    while listening:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                response = result[14:-3]
                listening = False
                stream.close()
                return response
        except OSError:
            pass


def analyze_command(command):
    try:
        if command == "take off":
            me.takeoff()
            print("ok!take off")
        elif command == "land":
            me.land()
            print("ok!land")
        elif command == "move up":
            me.move_up(20)
            print("ok!move up")
        elif command == "move down":
            me.move_down(20)
            print("ok!move down")
        elif command == "move right":
            me.move_right(20)
            print("ok!move right")
        elif command == "move left":
            me.move_left(20)
            print("ok!move left")
        elif command == "spiderman" or command == "spider man":
            print("ok!flip")
            me.flip_left()
            print("ok!flip")
        else:
            print("I don't understand the shit")
    except Exception:
        pass


while True:
    print('wait for command...')
    command = get_command()
    print(command)
    analyze_command(command)
