from .Ticker import Ticker
from .IndicatorManager import IndicatorManager

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import inspect


class Backtester:
    def __init__(self,
                 ticker: Ticker,
                 indicator_manager: IndicatorManager
                 ):
        """
        Backtester class to backtest a ticker with a given indicator manager.

        Args:
            ticker (Ticker): The ticker to backtest.
            indicator_manager (IndicatorManager): The indicator manager to use during backtesting.
        """
        self.ticker = ticker
        self.indicator_manager = indicator_manager

    def backtest(self) -> str:
        """
        Backtest the ticker with the indicator manager.
        """

        class _strategy(Strategy):
            n1=10
            n2=20
            indicatorManager:IndicatorManager = None
            
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

        bt = Backtest(
            GOOG,
            _strategy,
            cash=10000,
            commission=.002,
            exclusive_orders=True)

        kwargs = {"indicatorManager": self.indicator_manager}
        output = bt.run(**kwargs)
        print(output)

        return f"Backtesting ticker: {self.ticker.symbol} with indicator manager: {self.indicator_manager}"
