from TickerBaseclass import Ticker, TickerClassification


class Apple(Ticker):
    """
    A class to represent the Apple stock ticker.
    """

    def __init__(self):
        """
        Creates a new Apple ticker.
        """
        super().__init__(
            symbol="AAPL",
            classification=TickerClassification.STOCKS
        )