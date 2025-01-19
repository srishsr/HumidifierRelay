from enum import Enum, auto


class StateKey(Enum):
    DECREASE_SETPOINT = auto()
    IDLE = auto()
    INCREASE_SETPOINT = auto()
    SETPOINT_CONFIG = auto()
    SHOW_DATA = auto()
