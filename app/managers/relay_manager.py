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

    def update(self) -> None:
        setpoint = self.setpoint_manager.get_setpoint()
        humidity = self.ambients_manager.get().humidity
        self.relay.set_relay(humidity > setpoint)
