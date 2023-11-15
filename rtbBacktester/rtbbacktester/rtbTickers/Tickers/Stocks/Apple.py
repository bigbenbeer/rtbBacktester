import pandas as pd
from TickerBaseclass import Ticker, TickerClassification, TickerDataSource


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

    # Set the dataSource property
    @property
    def dataSource(self) -> TickerDataSource:
        """
        The data source of the ticker.

        Returns:
            The data source of the ticker.
        """
        return TickerDataSource.YAHOO_FINANCE
