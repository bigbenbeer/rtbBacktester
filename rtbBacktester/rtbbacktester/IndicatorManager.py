class IndicatorManager:
    """
    Class to manage the indicators used during backtesting. Think of this as a container for indicators with some helper methods.
    """

    def __init__(self):
        self.baselineIndicators = []
        self.confirmationIndicators = []
        self.volumeIndicators = []

    def getCombinations(self):
        """
        Returns all the combinations of indicators that can be used during backtesting.

        Returns:
            list: A list of tuples containing all the combinations of indicators that can be used during backtesting.
        """

        try:
            self._validate_Indicators()

            combinations = []
            for i in range(len(self.confirmationIndicators) - 1):
                for j in range(i + 1, len(self.confirmationIndicators)):
                    for volumeIndicator in self.volumeIndicators:
                        for baselineIndicator in self.baselineIndicators:
                            combinations.append(
                                (
                                    self.confirmationIndicators[i],
                                    self.confirmationIndicators[j],
                                    volumeIndicator,
                                    baselineIndicator
                                )
                            )
            return combinations
        except Exception as e:
            print(e)
    
    def _validate_Indicators(self):
        # Check that there are at least two confirmation indicators
        if len(self.confirmationIndicators) < 2:
            raise Exception("There must be at least two confirmation indicators.")
        
        if len(self.baselineIndicators) < 1:
            raise Exception("There must be at least one baseline indicator.")
        
        if len(self.volumeIndicators) < 1:
            raise Exception("There must be at least one volume indicator.")

    def setConfirmationIndicators(self, confirmationIndicators):
        """
        Sets the confirmation indicators.

        Args:
            confirmationIndicators (list): A list of confirmation indicators.
        """

        self.confirmationIndicators = confirmationIndicators

    def setBaselineIndicators(self, baselineIndicators):
        """
        Sets the baseline indicators.

        Args:
            baselineIndicators (list): A list of baseline indicators.
        """

        self.baselineIndicators = baselineIndicators

    def setVolumeIndicators(self, volumeIndicators):
        """
        Sets the volume indicators.

        Args:
            volumeIndicators (list): A list of volume indicators.
        """

        self.volumeIndicators = volumeIndicators

    def __str__(self):
        return f"IndicatorManager with baselines: {self.baselineIndicators}, confirmation indicators: {self.confirmationIndicators}, and volume indicators: {self.volumeIndicators}"


if __name__ == '__main__':
    # Initialize ticker
    # Initialize indicator manager
    indicatorManager = IndicatorManager()

    