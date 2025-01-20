from app.managers.ambients_manager import AmbientsManager
from app.managers.device_manager import DeviceManager
from app.managers.relay_manager import RelayManager
from app.managers.setpoint_manager import SetpointManager


class ScreenManager:
    def __init__(
        self,
        device: DeviceManager,
        setpoint_manager: SetpointManager,
        ambients_manager: AmbientsManager,
        relay_manager: RelayManager,
    ) -> None:
        self.lcd = device.lcd
        self.humidity_sensors = device.humidity_sensors
        self.setpoint_manager = setpoint_manager
        self.ambients_manager = ambients_manager
        self.relay_manager = relay_manager

    def clear(self) -> None:
        self.lcd.set_message([], clear=True)

    def show_data(self) -> None:
        number_length = 6
        data = self.ambients_manager.get()
        setpoint = self.setpoint_manager.get_setpoint()

        if data.humidity == 0.0:
            humidity_str = "N/A  "
        else:
            humidity_str = ("%4.1f%%" % data.humidity)[0:number_length]

        if data.temperature == 0.0:
            temperature_str = "N/A  "
        else:
            temperature_str = ("%4.1fC" % data.temperature)[0:number_length]

        setpoint_str = ("%4.1f%%" % setpoint)[0:number_length]
        relay_state = "\x00" if self.relay_manager.is_on() else "\x01"

        self.lcd.set_message(
            [
                f"H: {humidity_str} {relay_state}{setpoint_str}",
                f"T: {temperature_str}",
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
