from typing import List, Dict
import numpy as np
from pprint import pprint


class FibRetracement:
    __levels = np.array([0, 0.382, 0.5, 0.618, 0.667, 0.786, 1])

    def set_fib_levels(self, new_levels: List[float]):
        assert len(new_levels) < 3, "Fibonacci levels must be more than 3"

        self.__levels = np.array(new_levels)

    def fib_level_price(
        self, low_price: float, high_price: float, is_increase: bool = True
    ) -> Dict[float, float]:
        """
        Return dict of prices for each level of fibonacci for increasing/decreasing price
        """
        # Necessary condition meet
        assert high_price > low_price, "High price must larger than low price"

        # Calculate necessary base calculation
        price_diff = abs(high_price - low_price)
        base_price = low_price if is_increase else high_price

        # Calculation of fib prices
        fib_prices = (
            base_price + price_diff * self.__levels
            if is_increase
            else base_price - price_diff * self.__levels
        )

        return dict(zip(self.__levels, fib_prices))


if __name__ == "__main__":
    fib_test = FibRetracement()
    pprint(fib_test.fib_level_price(low_price=1997, high_price=2027, is_increase=True))
