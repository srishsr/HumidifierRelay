from app.state_machine.behavior import Behavior
from app.state_machine.keys.state_key import StateKey
from app.state_machine.keys.transition_event import TransitionEvent


class State:
    def __init__(
        self,
        key: StateKey,
        behavior: Behavior,
        event_transitions: dict[TransitionEvent, StateKey],
    ) -> None:
        self.key = key
        self.behavior = behavior
        self.event_transitions = event_transitions

    def initialize(self) -> None:
        self.behavior.initialize()

    def tick(self) -> TransitionEvent | None:
        return self.behavior.tick()

    def deinitalize(self) -> None:
        self.behavior.deinitalize()

    def get_next_key(self, event: TransitionEvent) -> StateKey | None:
        return self.event_transitions.get(event)
