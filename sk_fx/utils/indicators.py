import pandas as pd


class TA:
    @staticmethod
    def ma(data: pd.DataFrame, length: int = 9, source: str = "close") -> pd.Series:
        """
        Generate the ma trend line based on the source of the data with given length

        Parameters
        ----------
        data : pd.DataFrame
            Input market data prices
        length : int, optional
            MA length, by default 9
        source : str, optional
            The source for MA, by default 'close'

        Returns
        -------
        pd.Series
            The series of the ma line
        """
        return (
            data[source]
            .rolling(window=length, min_periods=1)
            .mean()
            .fillna(method="backfill")
        )
