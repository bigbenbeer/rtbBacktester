import pandas as pd
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TickerBaseclass import Ticker, TickerClassification, TickerDataSource
from ForexLotSizes import ForexLotSizes

class EURUSD(Ticker):
    """
    A class to represent the Apple stock ticker.
    """

    def __init__(
            self, 
            startDate: datetime.date, 
            endDate: datetime.date,
            smallestLotSize: ForexLotSizes = ForexLotSizes.NONE
            ):
        """
        Creates a new Apple ticker.
        """
        super().__init__(
            symbol="EURUSD=X",
            classification=TickerClassification.FOREX,
            startDate=startDate,
            endDate=endDate,
            smallestLotSize=smallestLotSize
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
    

# Create a main function
def main():
    ticker = EURUSD(
        startDate=datetime.date(year=2017, month=1, day=1),
        endDate=datetime.date(year=2022, month=12, day=31),
        smallestLotSize=ForexLotSizes.MICRO
    )

    print(ticker.symbol)

if __name__ == "__main__":
    main()
