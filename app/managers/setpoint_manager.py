class SetpointManager:
    def __init__(self) -> None:
        self._humidity_setpoint = 0.0

    def set_setpoint(self, humidity_setpoint: float) -> None:
        self._humidity_setpoint = humidity_setpoint

    def get_setpoint(self) -> float:
        return self._humidity_setpoint
