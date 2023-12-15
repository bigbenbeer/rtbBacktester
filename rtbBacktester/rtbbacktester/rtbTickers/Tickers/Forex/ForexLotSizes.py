from enum import Enum


class ForexLotSizes(Enum):
    STANDARD = 100000
    MINI = 10000
    MICRO = 1000
    NANO = 100
    NONE = 0