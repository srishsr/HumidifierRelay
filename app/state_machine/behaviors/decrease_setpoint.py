from app.managers.container import Container
from app.state_machine.behavior import Behavior
from app.state_machine.keys.transition_event import TransitionEvent


class DecreaseSetpointBehavior(Behavior):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.setpoint_manager = self.container.setpoint_manager

    def initialize(self) -> None:
        self.setpoint_manager.set_setpoint(self.setpoint_manager.get_setpoint() - 5)

    def tick(self) -> TransitionEvent | None:
        return TransitionEvent.DONE

    def deinitalize(self) -> None:
        pass
