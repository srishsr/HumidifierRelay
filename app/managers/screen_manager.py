from app.managers.ambients_manager import AmbientsManager
from app.managers.device_manager import DeviceManager
from app.managers.setpoint_manager import SetpointManager


class ScreenManager:
    def __init__(
        self,
        device: DeviceManager,
        setpoint_manager: SetpointManager,
        ambients_manager: AmbientsManager,
    ) -> None:
        self.lcd = device.lcd
        self.humidity_sensors = device.humidity_sensors
        self.setpoint_manager = setpoint_manager
        self.ambients_manager = ambients_manager

    def clear(self) -> None:
        self.lcd.set_message([], clear=True)

    def show_data(self) -> None:
        number_length = 6
        data = self.ambients_manager.get()

        if data.humidity == 0.0:
            humidity = "N/A   "
        else:
            humidity = ("%4.1f %%" % data.humidity)[0:number_length]

        if data.temperature == 0.0:
            temperature = "N/A   "
        else:
            temperature = ("%4.1f C" % data.temperature)[0:number_length]

        self.lcd.set_message(
            [
                f"H: {humidity}",
                f"T: {temperature}",
            ]
        )

    def show_config(self) -> None:
        self.lcd.set_message(
            [
                "Set Humidity",
                f"{self.setpoint_manager.get_setpoint()}%",
            ]
        )

    def set_brightness(self, brightness: float) -> None:
        self.lcd.set_brightness(brightness)
