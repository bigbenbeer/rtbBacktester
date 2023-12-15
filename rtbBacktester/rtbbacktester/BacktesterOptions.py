from dataclasses import dataclass
import datetime
from enum import Enum
from .rtbTickers.Tickers.Forex.ForexLotSizes import ForexLotSizes


class warmUpPeriod(Enum):
    SIX_MONTHS = datetime.timedelta(days=180)
    NONE = datetime.timedelta(days=0)


@dataclass
class BacktesterOptions:
    # The start date of the backtest run
    start_date: datetime.date

    # The end date of the backtest run
    end_date: datetime.date

    # The warm up period for the backtest run in which no trading takes places
    warm_up_period: warmUpPeriod = warmUpPeriod.NONE

    # Prepost trading is trading that occurs before and after the market opens and closes
    prepost: bool = False

    # The amount of cash to start trading with
    cash: float = 10_000

    # Commission per trade. This value is a percentage value defined as float. E.G. 0.01 = 1%
    commission: float = 0.0

    #  The risk percentage per trade. This value is a percentage value defined as float. E.G. 0.01 = 1%
    risk: float = 0.02

    # The stop loss multiple of the ATR
    stopLossATRMultiple: float = 1.5

    # The take profit multiple of the ATR
    takeProfitATRMultiple: float = 1.0

    # Smallest lot size for FOREX
    smallestLotSize: ForexLotSizes = ForexLotSizes.MINI