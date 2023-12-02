from ast import List
from enum import Enum, auto
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG
from numpy import cross

from rtbbacktester.rtb_Indicators.Indicators.Other.ATRIndicator import ATRIndicator

from .IndicatorCombination import IndicatorCombination
from .BacktesterOptions import BacktesterOptions
from .StrategyStates import StrategyStates


class rtbStrategy(Strategy):
    """
    rtbStrategy class to define the strategy that will be used in the backtest. The backtester 
    controls the backtesting process, this class controls the algorithm that will be backtested.
    """
    n1 = 10
    n2 = 20

    # The indicator combination to use for this run
    indicatorCombination: IndicatorCombination = None  # type: ignore

    # The options to use for this run
    options: BacktesterOptions = None  # type: ignore

    # The state of the strategy
    state: StrategyStates = StrategyStates.NONE

    def init(self):
        # C1 indicator
        self.c1 = self.I(
            self.indicatorCombination.c1.calculate_signals, self.data.df)

        # C2 indicator
        self.c2 = self.I(
            self.indicatorCombination.c2.calculate_signals, self.data.df)

        # Baseline indicator
        self.baseline = self.I(
            self.indicatorCombination.baseline.calculate_signals, self.data.df)

        # Volume indicator
        self.volume = self.I(
            self.indicatorCombination.volume.calculate_signals, self.data.df)

        # ATR indicator
        self.ATR = self.I(ATRIndicator().calculate_values, self.data.df)


        

    def next(self):
        stateLog = []
        # print(f"Date: {self.data.index.max()}")

        # The warm up date is the date at which the indicators can be used
        WarmUpDate = (self.options.startDate + self.options.warmUpPeriod.value)

        # Check if we are past the warm up date
        if (self.data.index.max() >= WarmUpDate):

            # C1 Entry
            c1_entry = crossover(self.c1, 0) or crossover(  # type: ignore
                0, self.c1)  # type: ignore

            if (c1_entry or self.state == StrategyStates.C1_1Candle_WAITING):
                # Check if the entry is a Long or a Short
                positionType = (
                    lambda c1: {
                        1: StrategyStates.C1_LONG,
                        -1: StrategyStates.C1_SHORT,
                    }.get(c1, StrategyStates.NONE)
                )(self.c1[-1])
                stateLog.append(positionType)

                # Check if the baseline confirms the signal
                BaselineConfirmation = self.baseline[-1] == self.c1[-1]

                if (BaselineConfirmation):
                    # Check if there is a very large candle
                    FuCandleConfirmation = (
                        lambda positionType: {
                            StrategyStates.C1_LONG: self.data.Close[-1] <= self.baseline[-1] + self.ATR[-1],
                            StrategyStates.C1_SHORT: self.data.Close[-1] >= self.baseline[-1] - self.ATR[-1],
                        }.get(positionType, False)
                    )(positionType)

                    if (FuCandleConfirmation):
                        C2Confirmation = self.c2[-1] == self.c1[-1]

                        if (C2Confirmation):
                            # Check if this is a continuation trade
                            continuationTrade = False

                            # Check if there are any closed trades, if there are none then a
                            # continuation trade is not possible
                            if (len(self.closed_trades) > 0):

                                # Get the date of the last time the baseline flipped from its current value
                                baselineFlipDate = next(
                                    (self.data.index[-(i+1)]
                                     for i in range((self.data.index.max() - WarmUpDate).days)
                                     if self.baseline[-(i+1)] != self.baseline[-1]
                                     ), None)

                                # Check if there have been any trades since the baseline flipped
                                if (not baselineFlipDate == None):
                                    for trade in self.closed_trades:

                                        # Do a type check
                                        if (type(trade.entry_time) == type(baselineFlipDate)):
                                            condition1 = trade.entry_time > baselineFlipDate  # type: ignore
                                            # type: ignore
                                            condition2 = trade.exit_time <= self.data.index[-1]
                                            # type: ignore
                                            if (condition1 and condition2):
                                                continuationTrade = True
                                                stateLog.append(
                                                    StrategyStates.CONTINUATION)
                                                break

                            # No continuation trade condition
                            if (not continuationTrade):
                                volumeConfirmation = self.volume[-1] == self.c1[-1]

                                if (volumeConfirmation):
                                    self.state = StrategyStates.ENTER_TRADE

                                elif (not volumeConfirmation):
                                    # Check if this is the first time the signal is confirmed
                                    if (not self.state == StrategyStates.C1_1Candle_WAITING):
                                        # Log the confirmation
                                        stateLog.append(
                                            StrategyStates.VOLUME_SINGLE_REJECTION)

                                        # Set the state to waiting for the next candle
                                        self.state = StrategyStates.C1_1Candle_WAITING

                                    # Check if we are already in a 1 Candle waiting situation
                                    elif (self.state == StrategyStates.C1_1Candle_WAITING):
                                        # Clear the state
                                        self.state = StrategyStates.NONE

                                        # Log the confirmation
                                        stateLog.append(
                                            StrategyStates.VOLUME_DOUBLE_REJECTION)
                                        stateLog.append(
                                            StrategyStates.NO_TRADE)

                            # Continuation trade condition
                            elif (continuationTrade):
                                self.state = StrategyStates.ENTER_TRADE

                        # Handle the C2 rejection cases
                        elif (not C2Confirmation):
                            # Check if this is the first time the signal is confirmed
                            if (not self.state == StrategyStates.C1_1Candle_WAITING):
                                # Log the confirmation
                                stateLog.append(
                                    StrategyStates.C2_SINGLE_REJECTION)

                                # Set the state to waiting for the next candle
                                self.state = StrategyStates.C1_1Candle_WAITING

                            # Check if we are already in a 1 Candle waiting situation
                            elif (self.state == StrategyStates.C1_1Candle_WAITING):
                                # Clear the state
                                self.state = StrategyStates.NONE

                                # Log the confirmation
                                stateLog.append(
                                    StrategyStates.C2_DOUBLE_REJECTION)
                                stateLog.append(StrategyStates.NO_TRADE)

                    # Handle the FU Candle rejection cases
                    elif (not FuCandleConfirmation):
                        # Check if this is the first time the FU Candle rejects the signal
                        if (not self.state == StrategyStates.C1_1Candle_WAITING):
                            # Log the rejection
                            stateLog.append(StrategyStates.FU_SINGLE_REJECTION)

                            # Set the state to waiting for the next candle
                            self.state = StrategyStates.C1_1Candle_WAITING

                        # Check if we are already in a 1 Candle waiting situation
                        elif (self.state == StrategyStates.C1_1Candle_WAITING):
                            # Clear the state
                            self.state = StrategyStates.NONE

                            # Log the rejection
                            stateLog.append(StrategyStates.FU_DOUBLE_REJECTION)
                            stateLog.append(StrategyStates.NO_TRADE)

                # Handle the baseline rejection cases
                elif (not BaselineConfirmation):
                    # Check if this is the first time the baseline rejects the signal
                    if (not self.state == StrategyStates.C1_1Candle_WAITING):
                        # Log the rejection
                        stateLog.append(
                            StrategyStates.BASELINE_SINGLE_REJECTION)

                        # Set the state to waiting for the next candle
                        self.state = StrategyStates.C1_1Candle_WAITING

                    # Check if we are already in a 1 Candle waiting situation
                    elif (self.state == StrategyStates.C1_1Candle_WAITING):
                        # Clear the state
                        self.state = StrategyStates.NONE

                        # Log the rejection
                        stateLog.append(
                            StrategyStates.BASELINE_DOUBLE_REJECTION)
                        stateLog.append(StrategyStates.NO_TRADE)

        else:
            # The warm up period is still going on
            self.state = StrategyStates.WARMUP_PERIOD

        #  Ignore the following, its just example code
        if crossover(self.c1, self.c2):  # type: ignore
            self.buy()
        elif crossover(self.c2, self.c1):  # type: ignore
            self.sell()

        # TODO Handle trade entry here.
        if(self.state == StrategyStates.ENTER_TRADE):
            pass
