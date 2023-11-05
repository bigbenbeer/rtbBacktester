from .ExtendedEnum import ExtendedEnum
from .rtbTickers import Tickers

class TickerImportManager:
    class Stocks(ExtendedEnum):
        AAPL = Tickers.Stocks.Apple()