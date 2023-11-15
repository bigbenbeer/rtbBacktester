import rtbbacktester
import datetime

if __name__ == '__main__':
    # Initialize indicator manager
    indicatorManager = rtbbacktester.IndicatorManager()

    # Get an indicator import manager
    indicatorImportManager = rtbbacktester.IndicatorImportManager

    # Set the confirmation indicators
    indicatorManager.setConfirmationIndicators(
        indicatorImportManager.Confirmation.devList(
            num_indicators=5
        )
    )

    # Set the baseline indicators
    indicatorManager.setBaselineIndicators(
        indicatorImportManager.Baseline.devList(
            num_indicators=1
        )
    )

    # Set the volume indicators
    indicatorManager.setVolumeIndicators(
        indicatorImportManager.Volume.devList(
            num_indicators=1
        )
    )

    # Get the combinations of indicators
    combinations = indicatorManager.getCombinations()

    print("Number of combinations: ", len(indicatorManager.getCombinations()))
    # print("Combinations: ", combinations)

    # Configure the options for the backtester:
    options = rtbbacktester.BacktesterOptions(
        # When to start the backtest
        startDate=datetime.datetime(year=2017, month=1, day=1),

        # When to end the backtest
        endDate=datetime.datetime(year=2022, month=12, day=31),

        # The warm up period for the backtest
        warmUpPeriod=rtbbacktester.warmUpPeriod.SIX_MONTHS,

        # Whether to include pre and post market data
        prepost=False
    )

    # TODO Make sure the ticker is valid in the time period specified

    ticker = rtbbacktester.TickerImportManager.Stocks.AAPL.value
    ticker.startDate = options.startDate
    ticker.endDate = options.endDate

    print(ticker.getDataframe())

    # print(ticker.startDate)
    # print(ticker.endDate)

    # Initialize backtester
    # backtester = rtbbacktester.Backtester(
    #     ticker = ticker,
    #     indicator_manager=indicatorManager,
    #     options=options
    # )

    # # # Run backtest
    # # print(backtester.backtest())
