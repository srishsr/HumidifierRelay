class SetpointManager:
    def __init__(self) -> None:
        self._humidity_setpoint = 0.0

    def set_setpoint(self, humidity_setpoint: float) -> None:
        self._humidity_setpoint = max(0.0, min(100.0, humidity_setpoint))

    def get_setpoint(self) -> float:
        return self._humidity_setpoint
