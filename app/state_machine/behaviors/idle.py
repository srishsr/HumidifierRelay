from app.managers.container import Container
from app.state_machine.behavior import Behavior
from app.state_machine.keys.transition_event import TransitionEvent


class IdleBehavior(Behavior):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.screen_manager = self.container.screen_manager
        self.button_manager = self.container.button_manager

    def initialize(self) -> None:
        self.screen_manager.set_brightness(0.0)

    def tick(self) -> TransitionEvent | None:
        self.screen_manager.show_data()
        if events := self.button_manager.get_events():
            first_event = events[0]
            return first_event
        return None

    def deinitalize(self) -> None:
        pass
