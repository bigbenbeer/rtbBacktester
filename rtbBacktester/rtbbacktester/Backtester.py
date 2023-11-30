from .rtbTickers.TickerBaseclass import Ticker
from .IndicatorManager import IndicatorManager
from .BacktesterOptions import BacktesterOptions


from .Strategy import rtbStrategy

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import inspect
import time


class Backtester:
    """
    Backtester class to backtest a ticker with a given indicator manager. This class contains all 
    the logic to run a backtest on a given ticker with a given indicator manager. This class however
    does not contain the logic for the strategy. The strategy is defined in the Strategy.py file. 
    """
    
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
            options (BacktesterOptions): The options to use during backtesting.
        """
        # Set the variables
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
        Dev Notes: In order to backtest, we need to run a backtest with the given ticker, for each 
        of the combinations of indicators. We can get the combinations of indicators by calling 
        indicator_manager.getCombinations(). This should ideally be run in parallel, but for now, 
        we can run it sequentially. We can use the backtesting library to run the backtest. 
            
        This class should see all the combinations, however, the strategy should only see one.
        '''

        # Construct the backtest object
        bt = Backtest(
            data = self.ticker.getDataframe(),
            strategy= rtbStrategy,
            cash=self.options.cash,
            commission=self.options.commission,
            exclusive_orders=True,
            trade_on_close=True,
            hedging=False
        )
            
        for combination in self.indicator_manager.combinations:
            print(f"Running backtest with combination: {combination} \n")

            # Define the additional inputs to provide.
            kwargs = {
                "indicatorCombination": combination,
                "options": self.options
            }

            start_time = time.time()  # Start timing
            output = bt.run(**kwargs)
            end_time = time.time()  # End timing

            elapsed_time_ms = (end_time - start_time) * 1000  # Calculate elapsed time in milliseconds
            print(f"Elapsed time: {elapsed_time_ms:.2f} ms\n")

            print("Output:")
            print(output)
            print("\n")

        return f"Backtesting ticker: {self.ticker.symbol} with indicator manager: {self.indicator_manager}"
