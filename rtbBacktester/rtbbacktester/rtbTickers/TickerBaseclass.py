from enum import Enum, auto
from abc import ABC, abstractmethod
import pandas as pd
import datetime
import yfinance as yf


class TickerClassification(Enum):
    """
    An enum to represent the classification of a ticker.
    """
    FOREX = "FOREX"
    STOCKS = "STOCKS"
    METALS = "METALS"


class TickerDataSource(Enum):
    YAHOO_FINANCE = auto()


class Ticker(ABC):
    """
        An abstract base class to represent a financial ticker.

        Attributes:
            symbol (str): The symbol of the ticker.
            classification (TickerClassification): The classification of the ticker.
            startDate (datetime): The start date for retrieving data.
            endDate (datetime): The end date for retrieving data.
            dataSource (TickerDataSource): The data source for fetching ticker data.

        Methods:
            getDataframe(): Retrieves the ticker data as a pandas DataFrame.
            validate(): Validates the ticker's start and end dates.
            ...
    """

    def __init__(
        self,
        symbol: str,
        classification: TickerClassification
    ):
        """
        Creates a new ticker.

        Args:
            symbol: The symbol of the ticker.
            classification: The classification of the ticker. Must be one of `TickerClassification.FOREX` or `TickerClassification.STOCKS`.
        """

        self.symbol = symbol
        self.classification = classification

    @property
    def symbol(self) -> str:
        """
        The symbol of the ticker.

        Returns:
            A string representing the symbol of the ticker.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str):
        """
        Sets the symbol of the ticker.

        Args:
            symbol: The new symbol of the ticker.
        """

        # Validate the symbol
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")

        self._symbol = symbol

    @property
    def classification(self) -> TickerClassification:
        """
        The classification of the ticker.

        Returns:
            A `TickerClassification` enum value representing the classification of the ticker.
        """
        return self._classification

    @classification.setter
    def classification(self, classification: TickerClassification):
        """
        Sets the classification of the ticker.

        Args:
            classification: The new classification of the ticker. Must be one of `TickerClassification.FOREX` or `TickerClassification.STOCKS`.
        """

        # Validate the classification
        if not isinstance(classification, TickerClassification):
            raise TypeError("Classification must be a TickerClassification.")

        self._classification = classification

    @property
    def startDate(self) -> datetime.date:
        """
        The start date of the ticker.

        Returns:
            A datetime representing the start date of the ticker.
        """
        return self._startDate

    @startDate.setter
    def startDate(self, startDate: datetime.date):
        """
        Sets the start date of the ticker.

        Args:
            startDate: The new start date of the ticker.
        """

        # Validate the start date
        if not isinstance(startDate, datetime.date):
            raise TypeError("Start date must be a datetime.")

        self._startDate = startDate

    @property
    def endDate(self) -> datetime.date:
        """
        The end date of the ticker.

        Returns:
            A datetime representing the end date of the ticker.
        """
        return self._endDate

    @endDate.setter
    def endDate(self, endDate: datetime.date):
        """
        Sets the end date of the ticker.

        Args:
            endDate: The new end date of the ticker.
        """

        # Validate the end date
        if not isinstance(endDate, datetime.date):
            raise TypeError("End date must be a datetime.")

        self._endDate = endDate

    @property
    def dataSource(self) -> TickerDataSource:
        """
        The data source of the ticker.

        Returns:
            A `TickerDataSource` enum value representing the data source of the ticker.
        """
        return self._dataSource

    @dataSource.setter
    def dataSource(self, dataSource: TickerDataSource):
        """
        Sets the data source of the ticker.

        Args:
            dataSource: The new data source of the ticker.
        """

        # Validate the data source
        if not isinstance(dataSource, TickerDataSource):
            raise TypeError("Data source must be a TickerDataSource.")

        self._dataSource = dataSource

    def validate(self) -> None:
        # Check if the start date and end date have been set
        if self.startDate is None:
            raise ValueError("Start date must be set.")

        if self.endDate is None:
            raise ValueError("End date must be set.")

        # Check if the start date is before the end date
        if self.startDate > self.endDate:
            raise ValueError("Start date must be before the end date.")

    def getDataframe(self) -> pd.DataFrame:
        """
        Retrieves the ticker data as a pandas DataFrame from the specified data source.

        Returns:
            pd.DataFrame: A pandas DataFrame containing ticker data.

        Raises:
            ValueError: If start date or end date is not set.
            NotImplementedError: If the data source is not recognized.
        """
        # Validate the ticker
        self.validate()

        if (self.dataSource == TickerDataSource.YAHOO_FINANCE):
            return self._getYahooFinanceDataframe()
        else:
            raise NotImplementedError("Data source not recognized.")

    def _getYahooFinanceDataframe(self) -> pd.DataFrame:
        startDate = self.startDate.strftime("%Y-%m-%d")
        endDate = self.endDate.strftime("%Y-%m-%d")

        data = yf.download(
            tickers=self.symbol,
            interval="1d",
            start=startDate,
            end=endDate,
            auto_adjust=True,
            repair=True,
            progress=False
        )

        return data
