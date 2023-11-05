import rtbbacktester
import inspect

if __name__ == '__main__':
    # Initialize ticker
    # ticker = rtbbacktester.Ticker("AAPL")

    ticker = rtbbacktester.TickerImportManager.Stocks.AAPL

    # Initialize indicator manager
    indicatorManager = rtbbacktester.IndicatorManager()

    # Get an indicator import manager
    indicatorImportManager = rtbbacktester.IndicatorImportManager

    # Set the confirmation indicators
    indicatorManager.setConfirmationIndicators(
        indicatorImportManager.Confirmation.devList(
            num_indicators=2
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
    print("Combinations: ", combinations)

    # Initialize backtester
    backtester = rtbbacktester.Backtester(
        ticker = ticker.value,
        indicator_manager=indicatorManager
    )

    # # # Run backtest
    # # print(backtester.backtest())
