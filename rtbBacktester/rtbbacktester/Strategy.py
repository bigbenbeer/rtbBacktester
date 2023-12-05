from ast import List
from email.mime import base
from enum import Enum, auto
from stringprep import c22_specials
from turtle import st
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG
from numpy import cross

from rtbbacktester.rtb_Indicators.Indicators.Other.ATRIndicator import ATRIndicator

from .IndicatorCombination import IndicatorCombination
from .BacktesterOptions import BacktesterOptions
from .StrategyStates import StrategyStates

import datetime


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

    StrategyOutput = None  # type: ignore

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

    def handle_baseline_Rejection(self, state_log):
        """
        Helper function to handle the baseline rejection cases

        Args:
            state_log : The log of the states that have been passed through
        """
        # Check if this is the first time the baseline rejects the signal
        if not self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
            # Log the rejection
            state_log.append(StrategyStates.BASELINE_SINGLE_REJECTION)

            # Set the state to waiting for the next candle
            self.state = StrategyStates.C1_ENTRY_1Candle_WAITING

        # Check if we are already in a 1 Candle waiting situation
        elif self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
            # Clear the state
            self.state = StrategyStates.NONE

            # Log the rejection
            state_log.append(StrategyStates.BASELINE_DOUBLE_REJECTION)
            state_log.append(StrategyStates.NO_TRADE)

    def handle_FuCandle_Rejection(self, state_log, originState: StrategyStates) -> None:
        """
        Helper function to handle the FU Candle rejection cases

        Args:
            state_log : The log of the states that have been passed through

        Returns:
            None
        """
        if (originState == StrategyStates.C1_LONG or originState == StrategyStates.C1_SHORT):
            # Check if this is the first time the FU Candle rejects the signal
            if not self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
                # Log the rejection
                state_log.append(StrategyStates.FU_SINGLE_REJECTION)

                # Set the state to waiting for the next candle
                self.state = StrategyStates.C1_ENTRY_1Candle_WAITING

            # Check if we are already in a 1 Candle waiting situation
            elif self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
                # Clear the state
                self.state = StrategyStates.NO_TRADE

                # Log the rejection
                state_log.append(StrategyStates.FU_DOUBLE_REJECTION)
                state_log.append(StrategyStates.NO_TRADE)

        elif (originState == StrategyStates.BASELINE_LONG or originState == StrategyStates.BASELINE_SHORT):
            # Check if this is the first time the FU Candle rejects the signal
            if not self.state == StrategyStates.BASELINE_ENTRY_1Candle_WAITING:
                # Log the rejection
                state_log.append(StrategyStates.FU_SINGLE_REJECTION)

                # Set the state to waiting for the next candle
                self.state = StrategyStates.BASELINE_ENTRY_1Candle_WAITING

            # Check if we are already in a 1 Candle waiting situation
            elif self.state == StrategyStates.BASELINE_ENTRY_1Candle_WAITING:
                # Clear the state
                self.state = StrategyStates.NO_TRADE

                # Log the rejection
                state_log.append(StrategyStates.FU_DOUBLE_REJECTION)
                state_log.append(StrategyStates.NO_TRADE)

        # # Check if this is the first time the FU Candle rejects the signal
        # if not self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
        #     # Log the rejection
        #     state_log.append(StrategyStates.FU_SINGLE_REJECTION)

        #     # Set the state to waiting for the next candle
        #     self.state = StrategyStates.C1_ENTRY_1Candle_WAITING

        # # Check if we are already in a 1 Candle waiting situation
        # elif self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
        #     # Clear the state
        #     self.state = StrategyStates.NONE

        #     # Log the rejection
        #     state_log.append(StrategyStates.FU_DOUBLE_REJECTION)
        #     state_log.append(StrategyStates.NO_TRADE)

    def handle_C2_Rejection(self, state_log, originState: StrategyStates) -> None:
        """
        Helper function to handle the C2 rejection cases

        Args:
            state_log : The log of the states that have been passed through
        """
        if (originState == StrategyStates.C1_LONG or originState == StrategyStates.C1_SHORT):
            # Check if this is the first time the signal is confirmed
            if not self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
                # Log the confirmation
                state_log.append(StrategyStates.C2_SINGLE_REJECTION)

                # Set the state to waiting for the next candle
                self.state = StrategyStates.C1_ENTRY_1Candle_WAITING

            # Check if we are already in a 1 Candle waiting situation
            elif self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
                # Clear the state
                self.state = StrategyStates.NO_TRADE

                # Log the confirmation
                state_log.append(StrategyStates.C2_DOUBLE_REJECTION)
                state_log.append(StrategyStates.NO_TRADE)

        elif (originState == StrategyStates.BASELINE_LONG or originState == StrategyStates.BASELINE_SHORT):
            state_log.append(StrategyStates.C2_SINGLE_REJECTION)
            self.state = StrategyStates.NO_TRADE

    def handle_Volume_Rejection(self, state_log, originState: StrategyStates) -> None:
        """
        Helper function to handle the Volume rejection cases

        Args:
            state_log : The log of the states that have been passed through
        """
        if (originState == StrategyStates.C1_LONG or originState == StrategyStates.C1_SHORT):
            # Check if this is the first time the signal is confirmed
            if not self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
                # Log the confirmation
                state_log.append(StrategyStates.VOLUME_SINGLE_REJECTION)

                # Set the state to waiting for the next candle
                self.state = StrategyStates.C1_ENTRY_1Candle_WAITING

            # Check if we are already in a 1 Candle waiting situation
            elif self.state == StrategyStates.C1_ENTRY_1Candle_WAITING:
                # Clear the state
                self.state = StrategyStates.NONE

                # Log the confirmation
                state_log.append(StrategyStates.VOLUME_DOUBLE_REJECTION)
                state_log.append(StrategyStates.NO_TRADE)

        elif (originState == StrategyStates.BASELINE_LONG or originState == StrategyStates.BASELINE_SHORT):
            state_log.append(StrategyStates.VOLUME_SINGLE_REJECTION)
            self.state = StrategyStates.NO_TRADE

    def next(self):
        stateLog = []

        # The warm up date is the date at which the indicators can be used
        WarmUpDate = (self.options.startDate + self.options.warmUpPeriod.value)

        # Check if we are past the warm up date
        if (self.data.index.max() >= WarmUpDate):

            # C1 Entry
            c1_entry = crossover(self.c1, 0) or crossover(  # type: ignore
                0, self.c1)  # type: ignore

            # Baseline Entry
            baseline_entry = crossover(self.baseline, 0) or crossover(  # type: ignore
                0, self.baseline)  # type: ignore

            # Handle the C1 entry cases
            if (c1_entry or self.state == StrategyStates.C1_ENTRY_1Candle_WAITING):
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
                                            con1 = trade.entry_time > baselineFlipDate  # type: ignore
                                            # type: ignore
                                            con2 = trade.exit_time <= self.data.index[-1]
                                            if (con1 and con2):
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
                                    self.handle_Volume_Rejection(stateLog, originState=positionType)

                            # Continuation trade condition
                            elif (continuationTrade):
                                self.state = StrategyStates.ENTER_TRADE

                        # Handle the C2 rejection cases
                        elif (not C2Confirmation):
                            self.handle_C2_Rejection(stateLog, originState=positionType)

                    # Handle the FU Candle rejection cases
                    elif (not FuCandleConfirmation):
                        self.handle_FuCandle_Rejection(
                            stateLog, originState=positionType)

                # Handle the baseline rejection cases
                elif (not BaselineConfirmation):
                    self.handle_baseline_Rejection(stateLog)

            # Handle the Baseline entry cases
            if (baseline_entry or self.state == StrategyStates.BASELINE_ENTRY_1Candle_WAITING):
                # Check if the entry is a Long or a Short
                positionType = (
                    lambda baseline: {
                        1: StrategyStates.BASELINE_LONG,
                        -1: StrategyStates.BASELINE_SHORT,
                    }.get(baseline, StrategyStates.NONE)
                )(self.baseline[-1])
                stateLog.append(positionType)

                # Check if C1 agrees
                c1_confirmation = self.c1[-1] == self.baseline[-1]

                # Handle C1 confirmation
                if (c1_confirmation):
                    # Check if the C1 signal is newer than 7 candles
                    # This is the 7 Candle Rule
                    c1FlipDate = next(
                        (self.data.index[-(i+1)]
                         for i in range(7)
                         if self.c1[-(i+1)] != self.c1[-1]
                         ), None)

                    # Check if the C1 signal is newer than 7 candles
                    if (c1FlipDate != None):
                        FuCandleConfirmation = (
                            lambda positionType: {
                                StrategyStates.C1_LONG: self.data.Close[-1] <= self.baseline[-1] + self.ATR[-1],
                                StrategyStates.C1_SHORT: self.data.Close[-1] >= self.baseline[-1] - self.ATR[-1],
                            }.get(positionType, False)
                        )(positionType)

                        # Handle the FU Candle confirmation cases
                        if (FuCandleConfirmation):
                            c2_confirmation = self.c2[-1] == self.c1[-1]

                            # Handle the C2 confirmation cases
                            if (c2_confirmation):
                                volumeConfirmation = self.volume[-1] == self.c1[-1]

                                # Handle the Volume confirmation cases
                                if (volumeConfirmation):
                                    self.state = StrategyStates.ENTER_TRADE
                                    stateLog.append(
                                        StrategyStates.ENTER_TRADE)

                                # Handle the Volume rejection cases
                                elif (not volumeConfirmation):
                                    self.handle_Volume_Rejection(
                                        stateLog, originState=positionType)

                            # Handle the C2 rejection cases
                            elif (not c2_confirmation):
                                self.handle_C2_Rejection(
                                    stateLog, originState=positionType)

                        # Handle the FU Candle rejection cases
                        elif (not FuCandleConfirmation):
                            self.handle_FuCandle_Rejection(
                                stateLog, originState=positionType)

                    # If C1 Candle is older than 7 candles then we don't train
                    elif (c1FlipDate == None):
                        stateLog.append(StrategyStates.SEVEN_CANDLE_REJECTION)
                        self.state = StrategyStates.NO_TRADE

                # Handle C1 rejection
                elif (not c1_confirmation):
                    stateLog.append(StrategyStates.C1_REJECTED)
                    self.state = StrategyStates.NO_TRADE

        else:
            # The warm up period is still going on
            self.state = StrategyStates.WARMUP_PERIOD

        #  Ignore the following, its just example code
        if crossover(self.c1, self.c2):  # type: ignore
            self.buy()
        elif crossover(self.c2, self.c1):  # type: ignore
            self.sell()

        # TODO Handle trade entry here.
        if (self.state == StrategyStates.ENTER_TRADE):
            print(
                f"Date: {self.data.index.max()} | State: {self.state} | Log: {stateLog}")

        # Add new row to self.StrategyOutput
        self.StrategyOutput.append({
            'Date': self.data.index.max(),
            'Open': self.data.Open[-1],
            'High': self.data.High[-1],
            'Low': self.data.Low[-1],
            'Close': self.data.Close[-1],
            'Volume': self.data.Volume[-1],
            'C1': self.c1[-1],
            'C2': self.c2[-1],
            'Baseline': self.baseline[-1],
            'Volume': self.volume[-1],
            'ATR': self.ATR[-1],
            'State': self.state,
            'Log': stateLog
        })
