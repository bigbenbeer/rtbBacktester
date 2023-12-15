from rtbbacktester import IndicatorImportManager
from rtbbacktester import IndicatorManager
from rtbbacktester import BacktesterOptions
from rtbbacktester.rtbTickers.ForexLotSizes import ForexLotSizes
from rtbbacktester.rtbTickers import Tickers
from rtbbacktester import Backtester
from datetime import datetime
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    """
    DEV NOTES:

    The flow of this program is as follows:
    1. Instantiate an indicator manager. The indicator manager is a container for all the 
    indicators that will be used in the backtest. It is responsible for generating the
    combinations of indicators that will be used in the backtest.

    2. Instantiate an indicator import manager. The indicator import manager is responsible
    for importing the indicators from the indicators directory. It is also responsible for
    creating the indicator classes.

    3. Set the confirmation indicators.

    4. Set the baseline indicators.

    5. Set the volume indicators.

    6. Configure the options for the backtester using the BacktesterOptions class. This class
    is responsible for holding the options for the backtester. If the option is not defined
    here then it should not be an option.

    7. Instantiate a ticker.
    """
    # Get an indicator import manager
    indicatorImportManager = IndicatorImportManager

    # Initialize indicator manager
    indicatorManager = IndicatorManager(
        # Set the confirmation indicators
        confirmationIndicators=indicatorImportManager.Confirmation.devList(
            num_indicators=2
        ),

        # Set the baseline indicators
        baselineIndicators=indicatorImportManager.Baseline.devList(
            num_indicators=1
        ),

        # Set the volume indicators
        volumeIndicators=indicatorImportManager.Volume.devList(
            num_indicators=1
        )
    )

    # # Print the number of combinations so that we can see it is doing something
    # if indicatorManager.combinations is not None:
    #     print("Number of combinations: ", len(indicatorManager.combinations))
    #     print("Combinations: ", indicatorManager.combinations)
    # else:
    #     print("No combinations found.")

    # Configure the options for the backtester:
    options = BacktesterOptions(
        # When to start the backtest
        start_date=datetime(year=2017, month=1, day=1),

        # When to end the backtest
        end_date=datetime(year=2022, month=12, day=31),

        # The warm up period for the backtest
        # warm_up_period=rtbbacktester.warmUpPeriod.SIX_MONTHS,

        # Whether to include pre and post market data
        prepost=False,

        # The amount of cash to start trading with
        cash=10_000,

        # Commission per trade. This value is a percentage value defined as float. E.G. 0.01 = 1%
        commission=0.0,

        # The risk percentage per trade. This value is a percentage value defined as float. E.G. 0.01 = 1%
        risk=0.02,

        smallestLotSize=ForexLotSizes.MICRO
    )

    # TODO Make sure the ticker is valid in the time period specified

    # Get the ticker
    ticker = Tickers.Forex.EURUSD(
        startDate=options.start_date,
        endDate=options.end_date,
        smallestLotSize = options.smallestLotSize
    )
    

    # Initialize backtester
    backtester = Backtester(
        ticker=ticker,
        indicator_manager=indicatorManager,
        options=options
    )

    # Run backtest
    try:
        backtester.backtest()
    except Exception as e:
        print(e)
        # Orint the stack trace
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
