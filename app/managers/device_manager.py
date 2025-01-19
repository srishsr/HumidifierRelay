from app.devices.dpad import Dpad
from app.devices.humidity_sensors import HumiditySensors
from app.devices.io.io_process import IoProcess
from app.devices.lcd import Lcd
from app.devices.relay import Relay


class DeviceManager:
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

    def stop(self) -> None:
        for io in self.io:
            io.stop()
