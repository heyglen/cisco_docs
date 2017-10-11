
import logging
import sys

import colorlog

from .configuration import configuration

verbose_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-2s%(reset)s %(name)-3s %(white)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)


def log_setup(name=None):
    name = name if name is not None else __name__.split('.')[0].lower()
    logger = logging.getLogger(name)
    logger.setLevel(configuration.log.level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(verbose_formatter)
    logger.addHandler(handler)
    return logger
