from app.state_machine.keys.state_key import StateKey
from app.state_machine.state import State


class StateMachine:
    def __init__(self, first_state_key: StateKey, states: list[State]) -> None:
        self.active_state: State | None = None
        self.states = {state.key: state for state in states}
        self.first_state_key = first_state_key

    def _activate_state(self, state: State) -> None:
        if self.active_state:
            self.active_state.deinitalize()
        self.active_state = state
        self.active_state.initialize()

    def initialize(self) -> None:
        self._activate_state(self.states[self.first_state_key])

    def tick(self) -> None:
        if not self.active_state:
            return
        if event := self.active_state.tick():
            if next_key := self.active_state.get_next_key(event):
                print(f"{self.active_state.key}: {event} -> {next_key}")
                self._activate_state(self.states[next_key])

    def deinitalize(self) -> None:
        if self.active_state:
            self.active_state.deinitalize()
        self.active_state = None
