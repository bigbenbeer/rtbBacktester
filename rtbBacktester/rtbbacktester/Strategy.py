from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

from .IndicatorManager import IndicatorManager


class rtbStrategy(Strategy):
    n1 = 10
    n2 = 20
    indicatorManager: IndicatorManager = None

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

        print(self.indicatorManager)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()
