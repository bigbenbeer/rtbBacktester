from enum import Enum
from .rtb_Indicators import Indicators

class IndicatorImportManager(Enum):
    """
    Helper class to import indicators    
    """

    class Baseline(Enum):
        """
        Baseline indicators
        """
        EMA = Indicators.Baseline.EMACustomIndicator()
        ICHIMOKU_KIJUN_SEN = Indicators.Baseline.ichimoku_indicator()
        KAMA = Indicators.Baseline.Kama_indicator()
        PSAR = Indicators.Baseline.psar_indicator()

    class Confirmation(Enum):
        pass
