import pandas as pd
import pytest as pt
import logging

import yfinance as yf

from sk_fx.indicators.oscillators.divergence_oscillator import ChaikinOscillator
from sk_fx.indicators.idtypes import TimeFrame


@pt.mark.chaikin_oscillator
class TestCalculationChaikinOscillator:
    """
    Class for testing for calculation logic of chaikin oscillator
    """

    def test_case_AAPL_chaikin_oscillator(self):
        """
        Test oscillator for AAPL prices
        """

        # INPUT
        logging.info(
            f"""
            Input values:
                - Market : AAPL
                - Name : Apple Inc.
                - Time frame : daily
            Oscillator settings:
                - Fast length : 5
                - Slow length : 20
            """
        )

        # Loading data
        market_data: pd.DataFrame = yf.download("AAPL", period="max", interval="1d")
        market_data.columns = ["open", "high", "low", "close", "adjclose", "volume"]

        # OUTPUT
        chaikin_osc = ChaikinOscillator(
            ohlcv=market_data, time_frame=TimeFrame.D1, fast_length=5, slow_length=20
        )

        logging.debug(f"Latest price series: {list(market_data['close'][-5:])}")
        logging.debug(f"Latest oscillator series: {list(chaikin_osc.calculate()[-5:])}")

        assert True

    def test_case_BTCUSD_chaikin_oscillator(self):
        """
        Test oscillator for BTCUSD prices
        """

        # INPUT
        logging.info(
            f"""
            Input values:
                - Market : BTC USD
                - Name : Bitcoin USD
                - Time frame : daily
            Oscillator settings:
                - Fast length : 5
                - Slow length : 20
            """
        )

        # Loading data
        market_data: pd.DataFrame = yf.download("BTC-USD", period="max", interval="1d")
        market_data.columns = ["open", "high", "low", "close", "adjclose", "volume"]

        # OUTPUT
        chaikin_osc = ChaikinOscillator(
            ohlcv=market_data, time_frame=TimeFrame.D1, fast_length=5, slow_length=20
        )

        logging.debug(f"Latest price series: {list(market_data['close'][-5:])}")
        logging.debug(f"Latest volume series: {list(market_data['volume'][-5:])}")
        logging.debug(f"Latest oscillator series: {list(chaikin_osc.calculate()[-5:])}")
        logging.debug(
            f"Latest normalized oscillator series: {list(chaikin_osc.calculate(normalized=True)[-5:])}"
        )

        assert True

    def test_case_GOLD_chaikin_oscillator(self):
        """
        Test oscillator for GOLD prices
        """

        # INPUT
        logging.info(
            f"""
            Input values:
                - Market : GC=F
                - Name : GOLD
                - Time frame : daily
            Oscillator settings:
                - Fast length : 5
                - Slow length : 20
            """
        )

        # Loading data
        market_data: pd.DataFrame = yf.download("GC=F", period="max", interval="1d")
        market_data.columns = ["open", "high", "low", "close", "adjclose", "volume"]

        # OUTPUT
        chaikin_osc = ChaikinOscillator(
            ohlcv=market_data, time_frame=TimeFrame.D1, fast_length=5, slow_length=20
        )

        logging.debug(f"Latest price series: {list(market_data['close'][-5:])}")
        logging.debug(f"Latest volume series: {list(market_data['volume'][-5:])}")
        logging.debug(f"Latest oscillator series: {list(chaikin_osc.calculate()[-5:])}")
        logging.debug(
            f"Latest normalized oscillator series: {list(chaikin_osc.calculate(normalized=True)[-5:])}"
        )

        assert True
