class IndicatorManager:
    """
    Class to manage the indicators used during backtesting. Think of this as a container for indicators with some helper methods.
    """
    def __init__(self):
        self.baselineIndicators = []
        self.confirmationIndicators = []
        self.volumeIndicators = []

    def add_baseline_indicator(self, indicator):
        """
        Add a baseline indicator to the indicator manager.

        Args:
            indicator (Indicator): The baseline indicator to add. You can use the IndicatorImportManager to import indicators. 
        """
        self.baselineIndicators.append(indicator)

    def __str__(self):
        return f"IndicatorManager with indicators: {self.indicators}"