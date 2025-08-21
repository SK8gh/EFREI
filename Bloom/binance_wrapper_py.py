#!/usr/bin/python3

"""
    Implements the data acquisition part of the project
"""

from analytics_py import Analytics
import matplotlib.pyplot as plt
from datetime import datetime
from binance import Client
import pandas as pd
import logging

# Project configuration
import configuration_py as conf


class BinanceWrapper:
    """
    Wrapping up the Binance API
    """
    def __init__(self, api_key=None, secret_key=None):
        # Creating a Binance client
        client = Client(api_key, secret_key)
        self.client = client

    @staticmethod
    def convert_timestamp(timestamp_ms):
        """
        Convert a Unix timestamp in milliseconds to a Pandas timestamp
        """
        # Convert milliseconds to seconds
        timestamp_sec = timestamp_ms / 1000

        # Converting to Pandas Timestamp
        return pd.to_datetime(timestamp_sec, unit='s')

    def get_symbols(self):
        """
        Gets every possible crypto ticker provided by the API
        """
        # Get tickers from client
        all_symbols = self.client.get_all_tickers()
        tickers_usdt = []

        # Only return tickers that end with "USDT"
        for s in all_symbols:
            s = s['symbol']

            if s.endswith('USDT'):
                tickers_usdt.append(s)

        return tickers_usdt

    def get_ticker_data(self, symbol: str, start_time: str, end_time: str, interval: str):
        """
        Getting historical prices for given tickers, number of days, interval. Returns a pandas dataframe
        """
        logging.info(f"Requesting data for symbol: {symbol}")

        try:
            # Sending request
            klines = self.client.get_historical_klines(symbol=symbol,
                                                       interval=interval,
                                                       start_str=start_time,
                                                       end_str=end_time)

        except Exception as e:
            logging.error(f"An error happened when requesting historical klines for ticker: {symbol}")
            raise e

        # Creating a dataframe with the API response
        data = pd.DataFrame(columns=conf.RESPONSE_COLUMNS, data=klines)

        for c in ['OPEN_TIMESTAMP', 'CLOSE_TIMESTAMP']:
            data[c] = self.convert_timestamp(data[c])

        for c in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']:
            data[c] = data[c].astype(float)

        return data

    def get_data(self, symbols: list, start_time: str, end_time: str, interval: str):
        """
        Performs Binance API requests for input products on required time period with a given interval
        """
        if interval not in conf.VALID_INTERVALS:
            raise ValueError(f"Interval argument must be in {conf.VALID_INTERVALS}")

        for d in (start_time, end_time):
            try:
                datetime.strptime(d, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Start and end time must have appropriate format: yyyy-mm-dd")

        # Initializing returned object
        data_d = {s: None for s in symbols}

        for s in symbols:
            df = self.get_ticker_data(symbol=s,
                                      start_time=start_time,
                                      end_time=end_time,
                                      interval=interval)

            # Dropping useless columns
            df.drop(columns=conf.IGNORE_COLUMNS, errors="ignore", inplace=True)

            data_d[s] = df

        return data_d


def correlation_matrix(data: dict, column: str):
    """
    Computing the correlations of products based on a certain column
    """
    # Extract closing prices into a single DataFrame
    values = {}

    for symbol, df in data.items():
        values[symbol] = df[column]

    prices = pd.concat(
        values,
        axis=1
    )

    # Compute returns
    returns = prices.dropna(axis=1).pct_change().dropna()

    # Correlation matrix
    corr = returns.corr()

    return corr


if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']
    symbols = ('BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT')

    data = BinanceWrapper().get_data(symbols=symbols,
                                     start_time='2025-08-08',
                                     end_time='2025-08-09',
                                     interval='1h')

    corr = correlation_matrix(data=data, column='CLOSE')

    print('ok')
