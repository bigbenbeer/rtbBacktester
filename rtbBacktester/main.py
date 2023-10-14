import rtbbacktester

if __name__ == '__main__':
    # Initialize ticker
    ticker = rtbbacktester.Ticker("AAPL")
    
    # Initialize indicator manager
    indicatorManager = rtbbacktester.IndicatorManager()

    # Get an indicator import manager
    indicatorImportManager = rtbbacktester.IndicatorImportManager

    # Set the indicators
    indicatorManager.add_baseline_indicator(indicatorImportManager.Baseline.EMA)

    # Initialize backtester
    backtester = rtbbacktester.Backtester(ticker, indicatorManager)

    # Run backtest
    print(backtester.backtest())