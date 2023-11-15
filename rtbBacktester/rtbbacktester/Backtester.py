from .rtbTickers.TickerBaseclass import Ticker
from .IndicatorManager import IndicatorManager
from .BacktesterOptions import BacktesterOptions

from .Strategy import rtbStrategy

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import inspect


class Backtester:
    def __init__(self,
                 ticker: Ticker,
                 indicator_manager: IndicatorManager,
                 options: BacktesterOptions
                 ):
        """
        Backtester class to backtest a ticker with a given indicator manager.

        Args:
            ticker (Ticker): The ticker to backtest.
            indicator_manager (IndicatorManager): The indicator manager to use during backtesting.
        """
        if not isinstance(indicator_manager, IndicatorManager):
            raise TypeError(
                "indicator_manager must be of type IndicatorManager.")
        
        if not isinstance(options, BacktesterOptions):
            raise TypeError("options must be of type BacktesterOptions.")

        self.ticker = ticker
        self.indicator_manager = indicator_manager
        self.options = options

        # Validate the ticker
        self.ticker.validate()


    def backtest(self) -> str:
        """
        Backtest the ticker with the indicator manager.
        """

        '''
        Dev Notes: In order to backtest, we need to run a backtest with the given ticker, for each of the combinations
        of indicators. We can get the combinations of indicators by calling indicator_manager.getCombinations(). This should ideally be run
        in parallel, but for now, we can run it sequentially. We can use the backtesting library to run the backtest. 
        
        Logic:

        Preconfig: Run the ticker validation

        1. COnstruct the backtest object
        2. Get all the indicator combinations
        3. For each combination, run the backtest

        TODO: Run the combinations in parallel using TQDM and some parallel processing library.

        '''

        # Validate the ticker


        bt = Backtest(
            GOOG,
            rtbStrategy,
            cash=10000,
            commission=.002,
            exclusive_orders=True)

        kwargs = {"indicatorManager": self.indicator_manager}
        output = bt.run(**kwargs)
        print(output)

        return f"Backtesting ticker: {self.ticker.symbol} with indicator manager: {self.indicator_manager}"
