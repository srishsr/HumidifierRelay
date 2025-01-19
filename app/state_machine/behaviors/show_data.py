from app.container import Container
from app.state_machine.behavior import Behavior
from app.state_machine.keys.transition_event import TransitionEvent


class ShowDataBehavior(Behavior):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.screen_manager = self.container.screen_manager
        self.button_manager = self.container.button_manager

    def initialize(self) -> None:
        self.screen_manager.clear()
        self.screen_manager.set_brightness(1.0)

    def tick(self) -> TransitionEvent | None:
        self.screen_manager.show_data()
        if events := self.button_manager.get_events():
            first_event = events[0]
            return first_event
        if self.button_manager.is_idle():
            return TransitionEvent.IDLE_NO_INPUT
        return None

    def deinitalize(self) -> None:
        pass
