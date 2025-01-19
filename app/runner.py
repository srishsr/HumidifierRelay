import time

from app.devices.dpad import Dpad
from app.devices.humidity_sensors import HumiditySensors
from app.devices.io.io_process import IoProcess
from app.devices.lcd import Lcd
from app.devices.relay import Relay


class Runner:
    def __init__(self):
        self.lcd = Lcd()
        self.humidity_sensors = HumiditySensors()
        self.relay = Relay()
        self.dpad = Dpad()
        self.io: list[IoProcess] = [
            self.lcd,
            self.humidity_sensors,
            self.relay,
            self.dpad,
        ]

    def start(self) -> None:
        for io in self.io:
            io.start()

    def tick(self) -> None:
        self.lcd.set_message(["Hello", f"World! {time.perf_counter():0.1f}"])
        if humidity_data := self.humidity_sensors.get():
            for index, sensor_data in enumerate(humidity_data.sensors):
                print(
                    f"{index} Temperature: {sensor_data.temperature}°C, Humidity: {sensor_data.humidity}%"
                )
        if dpad_data := self.dpad.get():
            for index, button_data in enumerate(dpad_data.buttons):
                print(f"{index} Button: {button_data.is_pressed}")

    def run(self) -> None:
        while True:
            self.tick()
            time.sleep(0.1)

    def stop(self) -> None:
        for io in self.io:
            io.stop()
