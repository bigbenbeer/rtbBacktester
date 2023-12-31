import pandas as pd
from TickerBaseclass import Ticker, TickerClassification, TickerDataSource
import datetime

class Apple(Ticker):
    """
    A class to represent the Apple stock ticker.
    """

    def __init__(self, startDate: datetime.date, endDate: datetime.date):
        """
        Creates a new Apple ticker.
        """
        super().__init__(
            symbol="AAPL",
            classification=TickerClassification.STOCKS,
                        startDate=startDate,
            endDate=endDate
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
