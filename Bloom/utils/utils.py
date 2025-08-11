#!/usr/bin/python3

import configuration as conf
import argparse
import logging


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

    # Defaulting logging level to 'INFO'
    arguments.log = arguments.log if arguments.log else conf.DEFAULT_LOGGING_LEVEL

    # Setting logging level
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=arguments.log)

    logging.info(f"Parsed arguments:")
    for arg_name, arg_value in sorted(vars(arguments).items()):
        # Hiding password
        arg_value = arg_value if arg_name != 'secret_key' else '*' * 10

        # Logging argument name/value
        logging.info(f"{arg_name}: {arg_value}")

    return arguments
