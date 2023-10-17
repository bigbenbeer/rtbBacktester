from enum import Enum
from .rtb_Indicators import Indicators

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class IndicatorImportManager:
    """
    Helper class to import indicators    
    """

    class Baseline(ExtendedEnum):
        """
        Baseline indicators
        """
        EMA = Indicators.Baseline.EMACustomIndicator()
        ICHIMOKU_KIJUN_SEN = Indicators.Baseline.ichimoku_indicator()
        KAMA = Indicators.Baseline.Kama_indicator()
        PSAR = Indicators.Baseline.psar_indicator()

    class Confirmation(ExtendedEnum):
        ADX = Indicators.Confirmation.ADXCustomIndicator()
        AROON = Indicators.Confirmation.AroonCustomIndicator()
        AWESOME_OSCILLATOR = Indicators.Confirmation.Awesome_Oscillator()
        BOLLINGER_BANDS = Indicators.Confirmation.BollingerBandsCustomIndicator()
        CCI = Indicators.Confirmation.CCICustomIndicator()
        DONCHIAN_CHANNEL = Indicators.Confirmation.DonchianChannelCustomIndicator()
        DPO = Indicators.Confirmation.DPOCustomIndicator()
        ICHIMOKU_KIJUN_SEN = Indicators.Confirmation.ichimoku_kijun_sen()
        ICHIMOKU_TENKAN = Indicators.Confirmation.ichimoku_tenkan()
        KAMA_WITH_MA = Indicators.Confirmation.KAMA_with_ma()
        KAMA = Indicators.Confirmation.KAMACustomIndicator()
        KELTNER_CHANNEL = Indicators.Confirmation.KeltnerChannelCustomIndicator()
        KST = Indicators.Confirmation.KSTCustomIndicator()
        MACD = Indicators.Confirmation.MACDIndicator()
        MI = Indicators.Confirmation.MICustomIndicator()
        PPO_TWOLINE = Indicators.Confirmation.PPO_twoline_indicator()
        PPO_ZERO = Indicators.Confirmation.PPO_zero_indicator()
        PSAR = Indicators.Confirmation.psar_confirmation_indicator()
        PVO = Indicators.Confirmation.PVO_Confirmation_Indicator()
        STC = Indicators.Confirmation.STC_Confirmation_Indicator()
        TRIX = Indicators.Confirmation.TRIX_Confirmation_Indicator()
        ULCER_INDEX = Indicators.Confirmation.UlcerIndex_Confirmation_Indicator()
        VORTEX = Indicators.Confirmation.Vortex_Confirmation_Indicator()
        VORTEX_II = Indicators.Confirmation.vortex_indicator_II()
        VI = Indicators.Confirmation.Vortex_Confirmation_Indicator()

    class Continuation(ExtendedEnum):
        PSAR = Indicators.Continuation.psar_continuation_indicator()

    class Other(ExtendedEnum):
        ATR = Indicators.Other.ATRIndicator()

    class Volume(ExtendedEnum):
        ADI = Indicators.Volume.ADI_Volume_Indicator()
        ADX = Indicators.Volume.ADX_Volume_Indicator()
        CMF = Indicators.Volume.CMF_Volume_Indicator()
        EOM = Indicators.Volume.EoM_Volume_Indicator()
        WAE = Indicators.Volume.WaddahAttar_Volume_Indicator()

