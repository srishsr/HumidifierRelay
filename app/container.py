from app.managers.ambients_manager import AmbientsManager
from app.managers.button_manager import ButtonManager
from app.managers.device_manager import DeviceManager
from app.managers.relay_manager import RelayManager
from app.managers.screen_manager import ScreenManager
from app.managers.setpoint_manager import SetpointManager


class Container:
    def __init__(self) -> None:
        self.devices = DeviceManager()
        self.setpoint_manager = SetpointManager()
        self.button_manager = ButtonManager(self.devices)
        self.ambient_manager = AmbientsManager(self.devices)
        self.relay_manager = RelayManager(
            self.devices, self.setpoint_manager, self.ambient_manager
        )
        self.screen_manager = ScreenManager(
            self.devices,
            self.setpoint_manager,
            self.ambient_manager,
            self.relay_manager,
        )

    def initialize(self) -> None:
        self.devices.start()
        self.button_manager.initialize()

    def tick(self) -> None:
        self.relay_manager.update()

    def deinitialize(self) -> None:
        self.devices.stop()
