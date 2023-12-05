from enum import Enum, auto

class StrategyStates(Enum):
    # No status
    NONE = auto()

    # Warmup period
    WARMUP_PERIOD = auto()

    # C1 Trade entry has occured and it is for a long position
    C1_LONG = auto()

    # C1 Trade entry has occured and it is for a short position
    C1_SHORT = auto()

    # C1 Signal rejected
    C1_REJECTED = auto()

    # Baseline Long Signal has occured
    BASELINE_LONG = auto()

    # Baseline Short Signal has occured
    BASELINE_SHORT = auto()

    # Signal blocked by baseline rejection for the first time
    BASELINE_SINGLE_REJECTION = auto()

    # Signal blocked by baseline rejection for the second time
    BASELINE_DOUBLE_REJECTION = auto()

    # Signal blocked by FU Candle rejection for the first time
    FU_SINGLE_REJECTION = auto()

    # Signal blocked by FU Candle rejection for the second time
    FU_DOUBLE_REJECTION = auto()

    # Signal blocked bt C2 rejection for the first time
    C2_SINGLE_REJECTION = auto()

    # Signal blocked bt C2 rejection for the second time
    C2_DOUBLE_REJECTION = auto()

    # Signal blocked by Volume rejection for the first time
    VOLUME_SINGLE_REJECTION = auto()

    # Signal blocked by Volume rejection for the second time
    VOLUME_DOUBLE_REJECTION = auto()

    # Something happened when a new C1 signal occured so now we wait for one candle
    C1_ENTRY_1Candle_WAITING = auto()

    # Something happened when a new Baseline signal occured so now we wait for one candle
    BASELINE_ENTRY_1Candle_WAITING = auto()

    # We are not interested in opening a trade because conditions have not been met
    NO_TRADE = auto()

    # We are interested in going into a trade
    ENTER_TRADE = auto()

    # A continuation trade  event has occured
    CONTINUATION = auto()

    # 7 Candle rejection
    SEVEN_CANDLE_REJECTION = auto()



