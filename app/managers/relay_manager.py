from app.managers.ambients_manager import AmbientsManager
from app.managers.device_manager import DeviceManager
from app.managers.setpoint_manager import SetpointManager


class RelayManager:
    def __init__(
        self,
        device: DeviceManager,
        setpoint_manager: SetpointManager,
        ambients_manager: AmbientsManager,
    ) -> None:
        self.relay = device.relay
        self.humidity_sensors = device.humidity_sensors
        self.setpoint_manager = setpoint_manager
        self.ambients_manager = ambients_manager
        self.is_relay_on = False

    def is_on(self) -> bool:
        return self.is_relay_on

    def update(self) -> None:
        setpoint = self.setpoint_manager.get_setpoint()
        humidity = self.ambients_manager.get().humidity
        is_relay_on = humidity > setpoint
        self.relay.set_relay(is_relay_on)
        self.is_relay_on = is_relay_on
