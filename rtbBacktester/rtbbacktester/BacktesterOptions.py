import datetime
from enum import Enum


class warmUpPeriod(Enum):
    """ An enum to denote specific warm up periods. """
    SIX_MONTHS = datetime.timedelta(days=180)
    NONE = datetime.timedelta(days=0)


class BacktesterOptions:
    """ A class to represent the backtester options. """

    def __init__(self,
                 startDate: datetime,
                 endDate: datetime,
                 warmUpPeriod: warmUpPeriod = warmUpPeriod.NONE,
                 prepost: bool = False
                 ) -> None:
        """
        Creates a new backtester options object.

        Args:
            startDate: The start date of the backtest.
            endDate: The end date of the backtest.
            warmUpPeriod: The warm up period of the backtest.
            prepost: Whether to include pre and post market data.
        """
        self.startDate = startDate
        self.endDate = endDate
        self.warmUpPeriod = warmUpPeriod
        self.prepost = prepost
        self._validate()

    def _validate(self) -> None:
        """ Validates the backtester options. """
        if not type(self.startDate) == datetime.datetime:
            raise TypeError("Start date must be a datetime.")

        if not type(self.endDate) == datetime.datetime:
            raise TypeError("End date must be a datetime.")

        if not isinstance(self.warmUpPeriod, warmUpPeriod):
            raise TypeError("Warm up period must be a warmUpPeriod.")

        if self.startDate > self.endDate:
            raise ValueError("Start date must be before end date.")

        if self.warmUpPeriod.value > (self.endDate - self.startDate):
            raise ValueError(
                "Warm up period must be less than the time between the start date and end date.")

    @property
    def startDate(self) -> datetime:
        """ The start date of the backtest. """
        return self._startDate

    @startDate.setter
    def startDate(self, startDate: datetime):
        """ Sets the start date of the backtest. """
        self._startDate = startDate

    @property
    def endDate(self) -> datetime:
        """ The end date of the backtest. """
        return self._endDate

    @endDate.setter
    def endDate(self, endDate: datetime):
        """ Sets the end date of the backtest. """
        self._endDate = endDate

    @property
    def warmUpPeriod(self) -> warmUpPeriod:
        """ The warm up period of the backtest. During the warm up period, no trades are made."""
        return self._warmUpPeriod

    @warmUpPeriod.setter
    def warmUpPeriod(self, warmUpPeriod: warmUpPeriod):
        """ Sets the warm up period of the backtest. """
        self._warmUpPeriod = warmUpPeriod

    @property
    def prepost(self) -> bool:
        """ Whether to include pre and post market data. """
        return self._prepost
    
    @prepost.setter
    def prepost(self, prepost: bool):
        """ Sets whether to include pre and post market data. """
        self._prepost = prepost
