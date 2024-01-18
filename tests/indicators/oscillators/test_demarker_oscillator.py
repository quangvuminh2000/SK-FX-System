import pandas as pd
import pytest as pt
import logging

import yfinance as yf

from sk_fx.indicators.oscillators.divergence_oscillator import DeMarkerOscillator
from sk_fx.indicators.idtypes import TimeFrame


@pt.mark.demarker_oscillator
class TestCalculationDeMarkerOscillator:
    """
    Class for testing for calculation logic of DeMarker Oscillator
    """

    def test_case_AAPL_demarker_oscillator(self):
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
                - Period : 14
            """
        )

        # Loading data
        market_data: pd.DataFrame = yf.download("AAPL", period="max", interval="1d")
        market_data.columns = ["open", "high", "low", "close", "adjclose", "volume"]

        # OUTPUT
        demarker_osc = DeMarkerOscillator(
            ohlcv=market_data, time_frame=TimeFrame.D1, period=14
        )

        logging.debug(f"Latest price series: {list(market_data['close'][-5:])}")
        logging.debug(
            f"Latest oscillator series: {list(demarker_osc.calculate()[-5:])}"
        )

        assert True
