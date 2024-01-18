def is_acceptable_error(
    real_price: float, calculated_price: float, pip_value: float
) -> bool:
    """
    Check whether the calculation is acceptable or not
        - Acceptable if the difference is less than 3 pips
        - Otherwise not acceptable

    Parameters
    ----------
    real_price : float
        The real price on chart
    calculated_price : float
        The calculated price from formulas
    pip_value : float
        The value of 1 pip on real market

    Returns
    -------
    bool
        Whether the error is acceptable or not
    """

    return abs(real_price - calculated_price) < pip_value * 3
