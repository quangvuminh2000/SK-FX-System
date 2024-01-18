from typing import List, Dict
import numpy as np
from pprint import pprint


class FibExtension:
    __levels = np.array([0, 1, 1.272, 1.382, 1.618, 1.809, 2])

    def set_fib_levels(self, new_levels: List[float]):
        assert len(new_levels) < 3, "Fibonacci levels must be more than 3"

        self.__levels = np.array(new_levels)

    def fib_level_price(
        self,
        start_price: float,
        low_price: float,
        high_price: float,
        is_increase: bool = True,
    ) -> Dict[float, float]:
        """
        Return dict of prices for each level of fibonacci for increasing/decreasing price
        """
        # Necessary condition meet
        assert high_price > low_price, "High price must larger than low price"

        # Calculate necessary base calculation
        price_diff = (
            abs(high_price - start_price)
            if is_increase
            else abs(start_price - low_price)
        )
        base_price = low_price if is_increase else high_price  # 0 level

        fib_prices = (
            base_price + price_diff * self.__levels
            if is_increase
            else base_price - price_diff * self.__levels
        )

        return dict(zip(self.__levels, fib_prices))


if __name__ == "__main__":
    fib_test = FibExtension()
    pprint(
        fib_test.fib_level_price(
            start_price=121.366,
            low_price=101.122,
            high_price=112.782,
            is_increase=False,
        )
    )
