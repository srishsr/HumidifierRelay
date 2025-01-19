from dataclasses import dataclass

import numpy as np

from app.managers.device_manager import DeviceManager


@dataclass
class AmbientData:
    humidity: float
    temperature: float


class AmbientsManager:
    def __init__(self, device: DeviceManager) -> None:
        self.humidity_sensors = device.humidity_sensors
        self.prev_humidity = 0.0
        self.prev_temperature = 0.0

    def get(self) -> AmbientData:
        humidities = []
        temperatures = []
        if humidity_data := self.humidity_sensors.get():
            for sensor_data in humidity_data.sensors:
                humidities.append(sensor_data.humidity)
                temperatures.append(sensor_data.temperature)
        if len(humidities) != 0:
            self.prev_humidity = float(np.mean(humidities))
        if len(temperatures) != 0:
            self.prev_temperature = float(np.mean(temperatures))

        return AmbientData(self.prev_humidity, self.prev_temperature)
