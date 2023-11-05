from enum import Enum
from abc import ABC

class TickerClassification(Enum):
    """
    An enum to represent the classification of a ticker.
    """
    FOREX = "FOREX"
    STOCKS = "STOCKS"

class Ticker(ABC):
    """
    An abstract base class to represent a ticker.

    A ticker has a symbol and a classification.
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
