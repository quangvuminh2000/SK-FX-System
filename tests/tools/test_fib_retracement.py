import pytest as pt
import logging

from sk_fx.tools.fib_retracement import FibRetracement
from sk_fx.utils.test_utils import is_acceptable_error


@pt.mark.fib_retracement
class TestCalculationFibRetracement:
    """
    Class for testing for calculation logic of fibonacci retracement
    """

    def test_case_USOIL_downtrend_retracement(self):
        """
        Test retracement for USOIL market

        Settings:
        - Start Price : 121.336
        - High Price : 112.782
        - Low Price : 101.122
        - Downtrend
        """

        # INPUT
        start_price = 121.473
        high_price = 112.782
        low_price = 101.122
        is_increase = False

        logging.info(
            f"""
            Input values:
                - Start Price : 121.336
                - High Price : 112.782
                - Low Price : 101.122
                - Downtrend
            """
        )

        # OUTPUT
        fib_extension_tool = FibExtension()
        fib_extend_dict = fib_extension_tool.fib_level_price(
            start_price=start_price,
            low_price=low_price,
            high_price=high_price,
            is_increase=is_increase,
        )

        logging.debug(f"Fibonacci values: {list(fib_extend_dict.items())}")

        real_value_dict = {
            0: 112.782,
            1: 92.430,
            1.272: 86.894,
            1.382: 84.656,
            1.618: 79.853,
            1.809: 75.965,
            2: 72.078,
        }
        pip_value = 0.001

        for fib_level, fib_price in fib_extend_dict.items():
            assert is_acceptable_error(
                real_value_dict[fib_level], fib_price, pip_value
            ), f"Level {fib_level} has wrong value: {fib_price}, expected {real_value_dict[fib_level]}"

    def test_case_XAUUSD_uptrend_extension(self):
        """
        Test extension for GOLD market

        Settings:
        - Start Price : 1616.52
        - High Price : 1786.23
        - Low Price : 1725.85
        - Uptrend
        """

        # INPUT
        start_price = 1616.52
        high_price = 1786.23
        low_price = 1725.85
        is_increase = True

        logging.info(
            f"""
            Input values:
                - Start Price : {start_price}
                - High Price : {high_price}
                - Low Price : {low_price}
                - Uptrend
            """
        )

        # OUTPUT
        fib_extension_tool = FibExtension()
        fib_extend_dict = fib_extension_tool.fib_level_price(
            start_price=start_price,
            low_price=low_price,
            high_price=high_price,
            is_increase=is_increase,
        )

        logging.debug(f"Fibonacci values: {list(fib_extend_dict.items())}")

        real_value_dict = {
            0: 1725.85,
            1: 1895.56,
            1.272: 1941.72,
            1.382: 1960.38,
            1.618: 2000.44,
            1.809: 2032.85,
            2: 2065.26,
        }
        pip_value = 0.01

        for fib_level, fib_price in fib_extend_dict.items():
            assert is_acceptable_error(
                real_value_dict[fib_level], fib_price, pip_value
            ), f"Level {fib_level} has wrong value: {fib_price}, expected {real_value_dict[fib_level]}"
