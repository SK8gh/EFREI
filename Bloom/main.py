"""
    Main file, requesting data, processing analytics
"""


from binance_wrapper import BinanceWrapper


if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT']

    data = BinanceWrapper().get_data(symbols=symbols,
                                     start_time='2025-08-08',
                                     end_time='2025-08-09',
                                     interval='1h')
