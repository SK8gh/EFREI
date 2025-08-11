#!/usr/bin/python3

from binance import Client
import pandas as pd
import logging
import ast

# Project configuration
import configuration as conf


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

        # Convert to Pandas Timestamp
        timestamp_pd = pd.to_datetime(timestamp_sec, unit='s')

        return timestamp_pd

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

    def get_ticker_data(self, symbol, start_time, end_time, interval):
        """
        Getting historical prices for given tickers, number of days, interval. Returns a pandas dataframe
        """
        try:
            # Sending request
            klines = self.client.get_historical_klines(symbol=symbol,
                                                       interval=interval,
                                                       start_str=start_time,
                                                       end_str=end_time)

        except Exception as e:
            logging.error(f"An error happened when requesting historical klines")
            raise e

        # Creating a dataframe with the API response
        data = pd.DataFrame(columns=conf.RESPONSE_COLUMNS, data=klines)

        for c in ['OPEN_TIMESTAMP', 'CLOSE_TIMESTAMP']:
            data[c] = self.convert_timestamp(data[c])

        return data

    def get_data(self, symbols, start_time, end_time, interval, gateway=False):
        """
        Requests products (one at a time)
        """
        if gateway:
            try:
                symbols = ast.literal_eval(symbols)
            except Exception as e:
                msg = f"Could not convert the inputted symbols into a list (gateway call)"
                logging.error(msg)
                raise ValueError(f"{msg}: {str(e)}")

        if not isinstance(symbols, list):
            raise TypeError(f"'symbols argument must be a list but has type : {type(symbols)}'")
        elif interval not in conf.VALID_INTERVALS:
            raise ValueError(f"Interval argument must be in {conf.VALID_INTERVALS}")

        # Initializing returned object
        data = {s: None for s in symbols}

        for s in symbols:
            df = self.get_ticker_data(symbol=s,
                                      start_time=start_time,
                                      end_time=end_time,
                                      interval=interval)

            data[s] = df

        return data


if __name__ == '__main__':
    binance_client = Client("API_KEY", "API_SECRET")
    price = binance_client.get_symbol_ticker(symbol="BTCUSDT")
    print(price)
