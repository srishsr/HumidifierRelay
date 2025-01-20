import time
from dataclasses import dataclass
from queue import Queue
from typing import cast

import adafruit_dht
import board

from app.devices.io.io_read_process import IoReadProcess


@dataclass
class SensorData:
    humidity: float
    temperature: float


@dataclass
class HumidifierData:
    sensors: list[SensorData]


class HumiditySensors(IoReadProcess[HumidifierData]):
    def __init__(self):
        self.poll_interval = 1.0
        self.recovery_delay = 1.0
        queue: Queue[HumidifierData] = cast(Queue[HumidifierData], Queue())

        self.sensor1 = adafruit_dht.DHT11(board.D9)
        self.sensor2 = adafruit_dht.DHT11(board.D27)

        super().__init__(queue)

    def first_tick(self) -> None:
        pass

    def tick(self) -> HumidifierData | None:
        all_data = []
        for sensor in (self.sensor1, self.sensor2):
            sensor_data = self._get_sensor(sensor)
            if sensor_data is not None:
                all_data.append(sensor_data)
        time.sleep(self.poll_interval)
        if len(all_data) == 0:
            return None
        return HumidifierData(all_data)

    def _get_sensor(self, sensor) -> SensorData | None:
        try:
            temperature_c = sensor.temperature
            humidity = sensor.humidity
            return SensorData(humidity, temperature_c)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(self.recovery_delay)
            return None
