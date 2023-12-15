from dataclasses import dataclass
from .rtb_Indicators import Indicators


@dataclass
class IndicatorCombination:
    """
    A dataclass to hold a single combination of indicators
    """

    # Primary confirmation indicator
    c1: Indicators.Indicator

    # Secondary confirmation indicator
    c2: Indicators.Indicator

    # Baseline indicator
    baseline: Indicators.Indicator

    # Volume indicator
    volume: Indicators.Indicator

    # Property to denote if a combination has an exit indicator
    hasExit: bool = False
