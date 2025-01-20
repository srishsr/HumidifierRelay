from app.managers.settings_manager import SettingsManager


class SetpointManager:
    def __init__(self, settings_manager: SettingsManager) -> None:
        self._humidity_setpoint = 0.0
        self.settings_manager = settings_manager

    def initialize(self) -> None:
        self._humidity_setpoint = self.settings_manager.settings.humidity_setpoint

    def set_setpoint(self, humidity_setpoint: float) -> None:
        self._humidity_setpoint = max(0.0, min(100.0, humidity_setpoint))
        print(f"Setting humidity setpoint to {humidity_setpoint}%")
        self.settings_manager.settings.humidity_setpoint = self._humidity_setpoint
        self.settings_manager.save()

    def get_setpoint(self) -> float:
        return self._humidity_setpoint
