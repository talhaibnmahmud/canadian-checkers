import logging

from .custom_logger import setup_logging


setup_logging()
logger = logging.getLogger(__package__)
logger.info('Custom logger loaded')
