"""A utility for standardizing logging capabilities.
"""

# Standard modules
import logging
from typing import Union


def get_logger(name: str, level: Union[int, str] = logging.DEBUG) \
               -> logging.Logger:
    """Configures a logger for modules by setting a
    formatter and adding a stream handler. Also, sets
    the log level.

    Parameters
    ----------
    name : str
        The name of the logger to retrieve.

    level : optional, logging._Level
        The logging level to set the logger.
        Default is `logging.DEBUG`.

    Returns
    -------
    logging.Logger
        The configured logger obj.
    """
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
    return logger
    