import pandas as pd
from TickerBaseclass import Ticker, TickerClassification, TickerDataSource
from .ForexLotSizes import ForexLotSizes as LotSizes
import datetime

class EURUSD(Ticker):
    """
    A class to represent the Apple stock ticker.
    """

    def __init__(self, startDate: datetime.date, endDate: datetime.date):
        """
        Creates a new Apple ticker.
        """
        super().__init__(
            symbol="EURUSD=X",
            classification=TickerClassification.FOREX,
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
    
    # Set the lotSize property
    @property
    def lotSize(self) -> int:
        """
        The lot size of the ticker.

        Returns:
            The lot size of the ticker.
        """
        return LotSizes.MICRO.value
    

# Create a main function
def main():
    ticker = EURUSD()

    print(ticker.symbol)

if __name__ == "__main__":
    main()
