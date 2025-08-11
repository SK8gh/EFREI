"""
    Implements the data analytics part of the project
"""


import pandas as pd


class Analytics:
    @staticmethod
    def moving_average(df: pd.DataFrame, column: str, window: int) -> pd.DataFrame:
        """
        Compute simple moving average (SMA) over the 'close' price.
        """
        if column not in df.columns:
            raise ValueError(f"The column {column} does not appear in {list(df.columns)}")

        df[f"MA{window}_{column}"] = df[column].rolling(window=window).mean()
        return df

    @staticmethod
    def exponential_ma(df: pd.DataFrame, column: str, window: int) -> pd.DataFrame:
        """
        Compute exponential moving average (EMA) over the 'column' price.
        """
        if column not in df.columns:
            raise ValueError(f"The column {column} does not appear in {list(df.columns)}")

        df[f"EMA{window}_{column}"] = df[column].ewm(span=window, adjust=False).mean()
        return df

    @staticmethod
    def bollinger_bands(df: pd.DataFrame, column: str, window: int, factor: float = 2) -> pd.DataFrame:
        """
        Compute Bollinger Bands (middle, upper, lower) over the 'column' price.
        """
        if column not in df.columns:
            raise ValueError(f"DataFrame must contain a {column} column")

        ma = df[column].rolling(window=window).mean()
        std = df[column].rolling(window=window).std()

        df[f"BB_MA_{window}"] = ma
        df[f"BB_Upper_{window}"] = ma + (std * factor)
        df[f"BB_Lower_{window}"] = ma - (std * factor)

        return df
