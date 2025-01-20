import time

from app.devices.dpad import ButtonName
from app.managers.device_manager import DeviceManager
from app.state_machine.keys.transition_event import TransitionEvent


def now() -> float:
    return time.monotonic()


class ButtonManager:
    def __init__(self, device: DeviceManager) -> None:
        self.dpad = device.dpad
        self.events = {
            ButtonName.NORTH: TransitionEvent.NORTH_PRESSED,
            ButtonName.EAST: TransitionEvent.EAST_PRESSED,
            ButtonName.SOUTH: TransitionEvent.SOUTH_PRESSED,
            ButtonName.WEST: TransitionEvent.WEST_PRESSED,
        }
        self.idle_timeout = 60.0
        self.init_delay_time = 0.1
        self.reset_timer()
        self.prev_states = {
            ButtonName.NORTH: False,
            ButtonName.EAST: False,
            ButtonName.SOUTH: False,
            ButtonName.WEST: False,
        }

    def reset_timer(self) -> None:
        self.last_input_time = now()

    def initialize(self) -> None:
        while True:
            if buttons := self.dpad.get():
                for button_data in buttons.buttons:
                    self.prev_states[button_data.name] = button_data.is_pressed
                return
            else:
                time.sleep(self.init_delay_time)

    def get_events(self) -> tuple[TransitionEvent, ...]:
        if not (dpad_data := self.dpad.get()):
            return ()
        events = []
        for button_data in dpad_data.buttons:
            button_name = button_data.name
            is_pressed = button_data.is_pressed
            if is_pressed != self.prev_states[button_name]:
                self.prev_states[button_name] = is_pressed
                if is_pressed:
                    events.append(self.events[button_name])
                    self.reset_timer()
        return tuple(events)

    def time_since_last_input(self) -> float:
        return now() - self.last_input_time

    def is_idle(self) -> bool:
        return self.time_since_last_input() > self.idle_timeout
