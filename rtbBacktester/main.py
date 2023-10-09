import rtbbacktester

if __name__ == '__main__':
    # Initialize ticker
    ticker = rtbbacktester.Ticker("AAPL")
    
    # Initialize indicator manager
    indicatorManager = rtbbacktester.IndicatorManager()

    # Set the indicators
    indicatorManager.add_indicator("EMA")
    indicatorManager.add_indicator("MACD")

    # Initialize backtester
    backtester = rtbbacktester.Backtester(ticker, indicatorManager)

    # Run backtest
    print(backtester.backtest())