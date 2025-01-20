from dataclasses import dataclass
from queue import Queue
from typing import cast

import board
import digitalio

from app.devices.io.io_write_process import IoWriteProcess


@dataclass
class RelayData:
    state: bool


class Relay(IoWriteProcess[RelayData]):
    def __init__(self):
        self.relay = digitalio.DigitalInOut(board.D21)
        self.relay.direction = digitalio.Direction.OUTPUT
        self.queue: Queue[RelayData] = cast(Queue[RelayData], Queue())
        super().__init__(self.queue)

    def set_relay(self, state: bool) -> None:
        self.queue.put(RelayData(state))

    def first_tick(self) -> None:
        self._apply_relay(False)

    def tick(self, data: RelayData) -> None:
        self._apply_relay(data.state)

    def _apply_relay(self, state: bool) -> None:
        self.relay.value = state

    def stop(self) -> None:
        super().stop()
        self._apply_relay(False)
