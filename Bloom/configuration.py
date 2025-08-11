#!/usr/bin/python3

# Valid intervals that can be used to query product data to the API
VALID_INTERVALS = {
    '1m': '1 minute',
    '3m': '3 minutes',
    '5m': '5 minutes',
    '15m': '15 minutes',
    '30m': '30 minutes',
    '1h': '1 hour',
    '2h': '2 hours',
    '4h': '4 hours',
    '6h': '6 hours',
    '8h': '8 hours',
    '12h': '12 hours',
    '1d': '1 day',
    '3d': '3 days',
    '1w': '1 week',
    '1M': '1 month'
}

RESPONSE_COLUMNS = ['OPEN_TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'CLOSE_TIMESTAMP', 'QUOTE_ASSET_VOLUME',
                    'TRADES_NUMBER', 'TAKER_BUY_BASE_ASSET_VOLUME', 'TAKER_BUY_QUOTE_ASSET_VOLUME', 'IGNORE']

DEFAULT_LOGGING_LEVEL = 'INFO'
