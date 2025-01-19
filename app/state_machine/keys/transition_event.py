from enum import Enum, auto


class TransitionEvent(Enum):
    DONE = auto()
    NORTH_PRESSED = auto()
    EAST_PRESSED = auto()
    SOUTH_PRESSED = auto()
    WEST_PRESSED = auto()
    IDLE_NO_INPUT = auto()
