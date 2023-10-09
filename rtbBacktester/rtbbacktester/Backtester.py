from .Ticker import Ticker
from .IndicatorManager import IndicatorManager

class Backtester:
    def __init__(self, 
                 ticker: Ticker, 
                 indicator_manager: IndicatorManager
                 ):
        self.ticker = ticker
        self.indicator_manager = indicator_manager

    def backtest(self) -> str:
        return f"Backtesting ticker: {self.ticker.symbol} with indicator manager: {self.indicator_manager}"
