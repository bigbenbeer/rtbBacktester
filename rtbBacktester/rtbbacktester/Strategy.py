from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

from .IndicatorCombination import IndicatorCombination
from .BacktesterOptions import BacktesterOptions


class rtbStrategy(Strategy):
    """
    rtbStrategy class to define the strategy that will be used in the backtest. The backtester 
    controls the backtesting process, this class controls the algorithm that will be backtested.
    """
    n1 = 10
    n2 = 20

    # The indicator combination to use for this run
    indicatorCombination: IndicatorCombination = None  # type: ignore

    # The options to use for this run
    options: BacktesterOptions = None  # type: ignore

    """
    DEV NOTES:

    This strategy should be run only on a single ticker with a single indicator combination.
    

    TODO: Continue here. Now you need to take the large flow chart and actually implement it here.

    LFG
    """

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

        print(f"Indicator combination: {self.indicatorCombination} \n")

        # print(self.indicatorManager)

    def next(self):
        if crossover(self.sma1, self.sma2):  # type: ignore
            self.buy()
        elif crossover(self.sma2, self.sma1):  # type: ignore
            self.sell()
