from app.managers.settings_manager import SettingsManager
import time

class SetpointManager:
    def __init__(self, settings_manager: SettingsManager) -> None:
        self._humidity_setpoint = 0.0
        self.settings_manager = settings_manager
        self.change_state_interval = settings_manager.config.change_state_interval
        self.change_timer = self.get_now()

    def initialize(self) -> None:
        self._humidity_setpoint = self.settings_manager.settings.humidity_setpoint

    def set_setpoint(self, humidity_setpoint: float) -> None:
        self._humidity_setpoint = max(0.0, min(100.0, humidity_setpoint))
        print(f"Setting humidity setpoint to {humidity_setpoint}%")
        self.settings_manager.settings.humidity_setpoint = self._humidity_setpoint
        self.settings_manager.save()

    def get_setpoint(self) -> float:
        return self._humidity_setpoint

    def get_now(self) -> float:
        return time.monotonic()

    def can_set_state(self) -> float:
        now = self.get_now()
        expected_change_time = self.change_timer + self.change_state_interval
        return  now >= expected_change_time

    def set_change_timer(self) -> None:
        self.change_timer = self.get_now()
