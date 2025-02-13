import logging.config
import os

from simple_logs.config import ConfigLogging

LOG_DIR = os.path.join(os.path.dirname(__file__), "dog")

logger = None


def config_logger(name_logger: str = "dog", directory: str = LOG_DIR):
    config = ConfigLogging()
    config.add_default_formatter()
    config.add_console_handler()
    config.add_file_handler(directory)
    config.add_default_logger(name_logger)
    logging.config.dictConfig(config)  # type: ignore[arg-type]
    global logger
    logger = logging.getLogger(name_logger)


def dog(name_logger: str = "dog", directory: str = LOG_DIR):
    config_logger(name_logger=name_logger, directory=directory)
    logger.info("I like dogs better, but don't tell that to my cat Mia.")  # type: ignore[union-attr]
    logger.info("I don't have a dog!")  # type: ignore[union-attr]
    logger.info("Who do you like more, a cat or a dog?")  # type: ignore[union-attr]


dog()
