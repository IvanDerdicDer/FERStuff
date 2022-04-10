from enum import Enum


class RobotStates(Enum):
    STOP = 1 << 0
    FORWARD = 1 << 1
    LEFT1 = 1 << 2
    LEFT2 = 1 << 3
    LEFT3 = 1 << 4
    RIGHT1 = 1 << 5
    RIGHT2 = 1 << 6
    RIGHT3 = 1 << 7


def decide_next_state(line_position: int) -> RobotStates:
    pass
