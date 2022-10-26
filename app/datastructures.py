from enum import Enum


class Base_States(str, Enum):
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"


class Repeat_States(str, Enum):
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"
    ONE = "one"


class Play_Modes(str, Enum):
    NORMAL = "normal"
    SHUFFLE_NOREPEAT = "shuffle_norepeat"
    SHUFFLE = "shuffle"
    REPEAT_ALL = "repeat_all"
    SHUFFLE_REPEAT_ONE = "shuffle_repeat_one"
    REPEAT_ONE = "repeat_one"
