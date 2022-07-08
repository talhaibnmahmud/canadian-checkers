""" Custom logger module to log messages to file """

import logging
import logging.config
import os

import yaml


def setup_logging(
    default_path: str = 'logging.yml',
    default_level: int = logging.INFO,
    env_key: str = 'LOG_CFG'
):
    """ Setup logging configuration """

    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value

    if not os.path.exists('logs/'):
        os.makedirs('logs/')

    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                logger = logging.getLogger(__name__)
            except ValueError as ve:
                import traceback

                print('Error in Logging Configuration. Using default configs')
                print(ve.__traceback__)
                traceback.print_exc()

                logging.basicConfig(level=default_level)
            except Exception as e:
                import traceback

                print('Error in Logging Configuration. Using default configs')
                print(e.__traceback__)
                traceback.print_exc()

                logging.basicConfig(level=default_level)
            else:
                logger.info('Logging is successfully configured')
    else:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d-%m-%y %H:%M:%S %p',
            style='%',
            level=default_level,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logging.log', mode='w', encoding='utf-8')
            ],
            encoding='utf-8'
        )
