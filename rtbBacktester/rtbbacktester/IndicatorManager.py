from .IndicatorCombination import IndicatorCombination


class IndicatorManager:
    """
    Class to manage the indicators used during backtesting. Think of this as a container for indicators with some helper methods.
    """
    combinations: list[IndicatorCombination] = []

    def __init__(
            self,
            confirmationIndicators: list = [],
            baselineIndicators: list = [],
            volumeIndicators: list = []
    ):
        self.baselineIndicators = baselineIndicators
        self.confirmationIndicators = confirmationIndicators
        self.volumeIndicators = volumeIndicators

        # Build the combinations
        self._buildCombinations()

    def _buildCombinations(self):
        """
        Builds all the combinations of indicators that can be used during backtesting.
        """
        try:
            self._validate_Indicators()

            for i in range(len(self.confirmationIndicators) - 1):
                for j in range(i + 1, len(self.confirmationIndicators)):
                    for volumeIndicator in self.volumeIndicators:
                        for baselineIndicator in self.baselineIndicators:
                            self.combinations.append(
                                IndicatorCombination(
                                    c1=self.confirmationIndicators[i],
                                    c2=self.confirmationIndicators[j],
                                    baseline=baselineIndicator,
                                    volume=volumeIndicator
                                )
                            )
        except Exception as e:
            print(e)

    def _validate_Indicators(self):
        # Check that there are at least two confirmation indicators
        if len(self.confirmationIndicators) < 2:
            raise Exception(
                "There must be at least two confirmation indicators.")

        if len(self.baselineIndicators) < 1:
            raise Exception("There must be at least one baseline indicator.")

        if len(self.volumeIndicators) < 1:
            raise Exception("There must be at least one volume indicator.")

    def __str__(self):
        return f"IndicatorManager with baselines: {self.baselineIndicators}, confirmation indicators: {self.confirmationIndicators}, and volume indicators: {self.volumeIndicators}"