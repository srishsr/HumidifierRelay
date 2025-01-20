import time
from pathlib import Path

from app.config.config import load_config
from app.managers.container import Container
from app.state_machine.behaviors.decrease_setpoint import DecreaseSetpointBehavior
from app.state_machine.behaviors.idle import IdleBehavior
from app.state_machine.behaviors.increase_setpoint import IncreaseSetpointBehavior
from app.state_machine.behaviors.setpoint_config import SetpointConfigBehavior
from app.state_machine.behaviors.show_data import ShowDataBehavior
from app.state_machine.keys.state_key import StateKey
from app.state_machine.keys.transition_event import TransitionEvent
from app.state_machine.state import State
from app.state_machine.state_machine import StateMachine


class Runner:
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config.toml"
        self.config = load_config(config_path)
        self.tick_delay = 0.01
        self.container = Container(self.config)

        self.state_machine = StateMachine(
            StateKey.SHOW_DATA,
            states=[
                State(
                    StateKey.SHOW_DATA,
                    ShowDataBehavior(self.container),
                    event_transitions={
                        TransitionEvent.IDLE_NO_INPUT: StateKey.IDLE,
                        TransitionEvent.NORTH_PRESSED: StateKey.INCREASE_SETPOINT,
                        TransitionEvent.SOUTH_PRESSED: StateKey.DECREASE_SETPOINT,
                        TransitionEvent.EAST_PRESSED: StateKey.SETPOINT_CONFIG,
                        TransitionEvent.WEST_PRESSED: StateKey.IDLE,
                    },
                ),
                State(
                    StateKey.IDLE,
                    IdleBehavior(self.container),
                    event_transitions={
                        TransitionEvent.NORTH_PRESSED: StateKey.SHOW_DATA,
                        TransitionEvent.EAST_PRESSED: StateKey.SHOW_DATA,
                        TransitionEvent.SOUTH_PRESSED: StateKey.SHOW_DATA,
                        TransitionEvent.WEST_PRESSED: StateKey.SHOW_DATA,
                    },
                ),
                State(
                    StateKey.SETPOINT_CONFIG,
                    SetpointConfigBehavior(self.container),
                    event_transitions={
                        TransitionEvent.IDLE_NO_INPUT: StateKey.IDLE,
                        TransitionEvent.WEST_PRESSED: StateKey.SHOW_DATA,
                        TransitionEvent.NORTH_PRESSED: StateKey.INCREASE_SETPOINT,
                        TransitionEvent.SOUTH_PRESSED: StateKey.DECREASE_SETPOINT,
                    },
                ),
                State(
                    StateKey.INCREASE_SETPOINT,
                    IncreaseSetpointBehavior(self.container),
                    event_transitions={TransitionEvent.DONE: StateKey.SETPOINT_CONFIG},
                ),
                State(
                    StateKey.DECREASE_SETPOINT,
                    DecreaseSetpointBehavior(self.container),
                    event_transitions={TransitionEvent.DONE: StateKey.SETPOINT_CONFIG},
                ),
            ],
        )

    def start(self) -> None:
        self.state_machine.initialize()
        self.container.initialize()

    def tick(self) -> None:
        self.state_machine.tick()
        self.container.tick()

    def run(self) -> None:
        while True:
            self.tick()
            time.sleep(self.tick_delay)

    def stop(self) -> None:
        self.state_machine.deinitalize()
        self.container.deinitialize()
