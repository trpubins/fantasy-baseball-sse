"""A utility for standardizing logging capabilities.
"""

# Standard modules
import logging
from typing import Union

# 3rd party modules
import coloredlogs


def get_logger(name: str, level: Union[int, str] = logging.DEBUG) \
               -> logging.Logger:
    """Configures a logger for modules by setting the log level
    and format. Colors the terminal output.

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
    format = '[%(asctime)s] %(hostname)s {%(name)s:%(lineno)d} %(levelname)s - %(message)s'
    date_format = '%m-%d %H:%M:%S'
    coloredlogs.install(level=level, logger=logger, fmt=format, datefmt=date_format)
    return logger
    