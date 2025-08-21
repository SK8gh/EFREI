#!/usr/bin/python3

from functools import wraps
import argparse
import logging
import time


# Storing run/debug configuration argument names
ARGUMENTS = ['api_key',     # API client
             'secret_key',  # API secret key
             'log'          # Logging level
             ]


def parse_arguments():
    """
    Parsing the run/debug configuration arguments, setting the logging configuration
    """
    parser = argparse.ArgumentParser()

    for args in ARGUMENTS:
        parser.add_argument('--' + args)

    arguments = parser.parse_args()

    # Setting logging level
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level='INFO')

    logging.info(f"Parsed arguments:")
    for arg_name, arg_value in sorted(vars(arguments).items()):
        # Hiding password
        arg_value = arg_value if arg_name != 'secret_key' else '*' * 10

        # Logging argument name/value
        logging.info(f"{arg_name}: {arg_value}")

    return arguments


def timing(func):
    """
    Decorator that measures the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # high-resolution timer

        result = func(*args, **kwargs)

        end = time.perf_counter()
        print(f"'{func.__name__}' executed in {end - start:.2f} seconds")

        return result
    return wrapper
