"""
Basic Oscillators based on basic OHCLV data

Currently supported oscillators:
    1. Chaikin Oscillator
    2. DeMarker Oscillator
    3. MACD
    4. Stochastic
    5. RSI
    6. Volume Oscillator
"""
from abc import abstractmethod
from typing import Tuple

import pandas as pd
from pandas.core.api import Series as Series

from sk_fx.indicators.oscillators.base_oscillator import Oscillator
from sk_fx.indicators.idtypes import TimeFrame


class DivergenceOscillator(Oscillator):
    name: str = "Divergence Oscillator"
    time_frame: TimeFrame = TimeFrame.D1

    def __init__(self, name: str = None, time_frame: TimeFrame = TimeFrame.D1) -> None:
        if name is not None:
            self.name = name
        self.time_frame = time_frame

        super(DivergenceOscillator, self).__init__(
            name=self.name, time_frame=self.time_frame
        )

    @abstractmethod
    def calculate(self) -> pd.Series:
        """
        Calculation of the oscillator

        Returns
        -------
        pd.Series
            The series returns as the result of the calculation

        Raises
        ------
        Exception
            When the function is not implemented in the derived class
        """
        raise Exception("Not implemented")


class ChaikinOscillator(DivergenceOscillator):
    ohlcv: pd.DataFrame
    fast_length: int = 3
    slow_length: int = 10

    def __init__(
        self,
        name: str = "Chaikin Oscillator",
        time_frame: TimeFrame = TimeFrame.D1,
        ohlcv: pd.DataFrame = None,
        fast_length: int = 3,
        slow_length: int = 10,
    ) -> None:
        super(ChaikinOscillator, self).__init__(name, time_frame)
        self.ohlcv = ohlcv
        self.fast_length = fast_length
        self.slow_length = slow_length

    # Override functions
    def _money_flow_multi(self, high: float, low: float, close: float) -> float:
        """
        Calculation of money flow multiplier -> Close Location Value (CLV)

        Parameters
        ----------
        high : float
            High price
        low : float
            Low price
        close : float
            Close price

        Returns
        -------
        float
            Money flow multiplier
        """
        clv = ((close - low) - (high - close)) / (high - low)
        return clv

    def calculate(self, normalized: bool = False) -> Series:
        # * Money Flow Multiplier -> CLV
        clv: pd.Series = self.ohlcv.apply(
            lambda row: self._money_flow_multi(row["high"], row["low"], row["close"]),
            axis="columns",
        )

        # * Money Flow Volume
        mfv: pd.Series = clv * self.ohlcv["volume"]

        # * Accumulation/Distribution Line -> ADL
        adl: pd.Series = mfv.cumsum()

        # * Chaikin Oscillator -> CO
        adl_ma_fast: pd.Series = adl.ewm(
            span=self.fast_length, adjust=False, ignore_na=True
        ).mean()
        adl_ma_slow: pd.Series = adl.ewm(
            span=self.slow_length, adjust=False, ignore_na=True
        ).mean()
        co_osc: pd.Series = adl_ma_fast - adl_ma_slow

        if normalized:
            co_osc = (co_osc - co_osc.mean()) / co_osc.std()

        return co_osc


class DeMarkerOscillator(DivergenceOscillator):
    ohlcv: pd.DataFrame
    period: int = 14

    def __init__(
        self,
        name: str = "Chaikin Oscillator",
        time_frame: TimeFrame = TimeFrame.D1,
        ohlcv: pd.DataFrame = None,
        period: int = 14,
    ) -> None:
        super(DeMarkerOscillator, self).__init__(name, time_frame)
        self.ohlcv = ohlcv
        self.period = period

    def calculate(self, average_demarker: bool = False) -> Series:
        # * DeMax, DeMin calculation
        demax = self.ohlcv["high"].diff(periods=1).clip(lower=0)
        demin = (self.ohlcv["low"].shift(1) - self.ohlcv["low"]).clip(lower=0)

        # * DeMax, DeMin with MA
        demax_ema = demax.ewm(span=self.period, adjust=False, ignore_na=True).mean()
        demin_ema = demin.ewm(span=self.period, adjust=False, ignore_na=True).mean()

        # * DeMarker Calculation
        demarker = demax_ema / (demax_ema + demin_ema)
        if average_demarker:
            demarker = demarker.ewm(
                span=self.period, adjust=False, ignore_na=True
            ).mean()

        return demarker


class MACD(DivergenceOscillator):
    ohlcv: pd.DataFrame
    fast_length: int = 12
    slow_length: int = 26
    signal_length: int = 9

    def __init__(
        self,
        name: str = None,
        time_frame: TimeFrame = TimeFrame.D1,
        ohlcv: pd.DataFrame = None,
        fast_length: int = 12,
        slow_length: int = 26,
        signal_length: int = 9,
    ) -> None:
        super(MACD, self).__init__(name, time_frame)
        self.ohlcv = ohlcv
        self.fast_length = fast_length
        self.slow_length = slow_length
        self.signal_length = signal_length

    def calculate(self) -> Tuple[Series, Series, Series]:
        # * Calculate EMA line
        fast_ema = (
            self.ohlcv["close"]
            .ewm(
                span=self.fast_length,
                adjust=False,
                ignore_na=True,
                min_periods=self.fast_length,
            )
            .mean()
        )
        slow_ema = (
            self.ohlcv["close"]
            .ewm(
                span=self.slow_length,
                adjust=False,
                ignore_na=True,
                min_periods=self.slow_length,
            )
            .mean()
        )

        # * Calculate macd, signal and difference lines
        macd = fast_ema - slow_ema
        macd_signal = macd.ewm(
            span=self.signal_length,
            adjust=False,
            ignore_na=True,
            min_periods=self.signal_length,
        ).mean()
        macd_diff = macd - macd_signal

        return macd, macd_signal, macd_diff


class StochasticOscillator(DivergenceOscillator):
    ohlcv: pd.DataFrame
    k_length: int = 14
    d_length: int = 3

    def __init__(
        self,
        name: str = None,
        time_frame: TimeFrame = TimeFrame.D1,
        ohlcv: pd.DataFrame = None,
        k_length: int = 14,
        d_length: int = 3,
    ) -> None:
        super(StochasticOscillator, self).__init__(name, time_frame)
        self.ohlcv = ohlcv
        self.k_length = k_length
        self.d_length = d_length

    def calculate(self) -> Series:
        # * Calculate high low in k periods
        n_high = self.ohlcv["high"].rolling(self.k_length).max()
        n_low = self.ohlcv["low"].rolling(self.k_length).min()

        # * Calculate the percentage using the min/max values
        percentage = (self.ohlcv["close"] - n_low) * 100 / (n_high - n_low)

        # * Calculate percentage sma ~ stochastic
        percentage_sma = percentage.rolling(self.d_length).mean()

        return percentage_sma


class RSIOscillator(DivergenceOscillator):
    ohlcv: pd.DataFrame
    period: int = 14

    def __init__(
        self,
        name: str = None,
        time_frame: TimeFrame = TimeFrame.D1,
        ohlcv: pd.DataFrame = None,
        period: int = 14,
    ) -> None:
        super(RSIOscillator, self).__init__(name, time_frame)
        self.ohlcv = ohlcv
        self.period = period

    def _gain_loss(self, diff: pd.Series) -> Tuple[pd.Series, pd.Series]:
        gain = diff.clip(lower=0).round(2)
        loss = diff.clip(upper=0).abs().round(2)

        return gain, loss

    def _avg_values(self, series: pd.Series) -> pd.Series:
        # Initial averages
        avg_series = series.rolling(window=self.period, min_periods=self.period).mean()

        # Get WMS averages
        for i, _ in enumerate(avg_series.iloc[self.period + 1 :]):
            avg_series.iloc[i + self.period + 1] = (
                avg_series.iloc[i + self.period] * (self.period - 1)
                + series.iloc[i + self.period + 1]
            ) / self.period

        return avg_series

    def _rsi_value(self, avg_gain: pd.Series, avg_loss: pd.Series) -> pd.Series:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate(self) -> Series:
        # Calculate diff
        diff = self.ohlcv["close"].diff(1)

        # Gain, Loss on close price
        gain, loss = self._gain_loss(diff)

        # Average gain, loss
        avg_gain = self._avg_values(gain)
        avg_loss = self._avg_values(loss)

        # RSI value
        rsi = self._rsi_value(avg_gain, avg_loss)

        return rsi
