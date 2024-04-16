# Import IntEnum for creating an enumerated type where members are also integers,
# and auto for automatic value assignment.
from enum import IntEnum, auto


# Enumerate game layers with automatic integer values for easy layer management.
class Layer(IntEnum):
    BACKGROUND = auto()
    OBSTACLE = auto()
    FLOOR = auto()
    PLAYER = auto()
    UI = auto()
