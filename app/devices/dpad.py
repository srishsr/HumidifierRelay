import time
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import cast

import board
import digitalio

from app.devices.io.io_read_process import IoReadProcess


class ButtonName(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


@dataclass
class ButtonData:
    name: ButtonName
    is_pressed: bool


@dataclass
class DpadData:
    buttons: list[ButtonData]


class Dpad(IoReadProcess[DpadData]):
    def __init__(self):
        self.poll_interval = 0.1
        queue: Queue[DpadData] = cast(Queue[DpadData], Queue())

        self.north = digitalio.DigitalInOut(board.D26)
        self.east = digitalio.DigitalInOut(board.D20)
        self.south = digitalio.DigitalInOut(board.D16)
        self.west = digitalio.DigitalInOut(board.D19)
        self.buttons = [self.north, self.east, self.south, self.west]
        for button in self.buttons:
            self._setup_button(button)
        self.prev_state = []

        super().__init__(queue)

    def _setup_button(self, button: digitalio.DigitalInOut) -> None:
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP

    def first_tick(self) -> None:
        pass

    def tick(self) -> DpadData | None:
        all_data = []
        for index, button in enumerate(self.buttons):
            is_pressed = not button.value
            all_data.append(ButtonData(ButtonName(index), is_pressed))
        time.sleep(self.poll_interval)
        if all_data == self.prev_state:
            return None
        self.prev_state = all_data
        return DpadData(all_data)
