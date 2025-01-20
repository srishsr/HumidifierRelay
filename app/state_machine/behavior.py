from app.managers.container import Container
from app.state_machine.keys.transition_event import TransitionEvent


class Behavior:
    def __init__(self, container: Container) -> None:
        self.container = container

    def initialize(self) -> None:
        pass

    def tick(self) -> TransitionEvent | None:
        pass

    def deinitalize(self) -> None:
        pass
