from .rtbTickers.TickerBaseclass import Ticker
from .IndicatorManager import IndicatorManager
from .BacktesterOptions import BacktesterOptions


from .Strategy import rtbStrategy

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import inspect
import time

import pandas as pd

import concurrent.futures
import time
from tqdm import tqdm

import multiprocessing



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

        with tqdm(total=len(self.indicator_manager.combinations)) as pbar:
            def update(*_):
                pbar.update()

            # Run the loop in parallel
            num_threads = multiprocessing.cpu_count()
            # num_threads = 1
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(self.process_combination, combination) for combination in self.indicator_manager.combinations]
                for future in concurrent.futures.as_completed(futures):
                    update()

        return f"Backtesting ticker: {self.ticker.symbol} with indicator manager: {self.indicator_manager}"

    def process_combination(self, combination):
        # print(f"Running backtest with combination: {combination}\n")

        bt = Backtest(
            data=self.ticker.getDataframe(),
            strategy=rtbStrategy,
            cash=self.options.cash,
            commission=self.options.commission,
            exclusive_orders=True,
            trade_on_close=True, # Trade on close of current candle
            hedging=False
        )

        StrategyOutput = []
        # Define the additional inputs to provide.
        kwargs = {
            "indicatorCombination": combination,
            "options": self.options,
            "StrategyOutput": StrategyOutput
        }

        try:
            start_time = time.time()  # Start timing

            output = bt.run(**kwargs)
            end_time = time.time()  # End timing
            elapsed_time_ms = (end_time - start_time) * 1000
            print(f"Elapsed time: {elapsed_time_ms:.2f} ms\n")
        
        except Exception as e:
            print(f"Error in backtesting with combination: {combination}")
            print(e)

        # Calculate elapsed time in milliseconds


        # resultspd = pd.DataFrame(StrategyOutput)
        # print(resultspd)

        # Save resultspd to a csv file with the name of self.ticker.symbol
        # resultspd.to_csv(f"results/{self.ticker.symbol}.csv")
