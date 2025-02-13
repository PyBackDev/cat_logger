import logging.config
import os

from simple_logs.config import ConfigLogging

LOG_DIR = os.path.join(os.path.dirname(__file__), "cat")


class CatLogger:

    def __init__(self, name_logger: str = "cat", directory: str = LOG_DIR):
        self.name_logger: str = name_logger
        self.directory: str = directory

    def __call__(self, *args, **kwargs):
        config = ConfigLogging()
        config.add_default_formatter()
        config.add_console_handler()
        config.add_file_handler(self.directory)
        config.add_default_logger(self.name_logger)
        logging.config.dictConfig(config)
        return logging.getLogger(self.name_logger)


def cat(name_logger: str = "cat", directory: str = LOG_DIR):
    logger = CatLogger(name_logger=name_logger, directory=directory)()
    logger.info("I love cats!")
    logger.info("My cat's name is Mia!")
    logger.info("Who do you like more, a cat or a dog?")


cat()
