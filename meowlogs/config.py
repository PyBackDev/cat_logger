from collections.abc import MutableMapping
from typing import Any


class ConfigLogging(MutableMapping):
    """
    A configuration manager class for logging settings, implementing a mutable mapping.

    This class allows you to manage logging formatters, handlers, and loggers dynamically
    through a dictionary-like interface. It defines default logging configurations and
    provides methods for adding and customizing various logging components.

    Attributes:
        default_config (dict): The default logging configuration containing the version,
            disable flag for existing loggers, and placeholders for formatters, handlers,
            and loggers.

    Methods:
        __getitem__(key): Retrieve the value associated with a given key in the configuration.
        __setitem__(key, value): Set the value for a specific key in the configuration.
        __delitem__(key): Remove the key-value pair from the configuration.
        __iter__(): Return an iterator over the configuration keys.
        __len__(): Return the number of key-value pairs in the configuration.
        add_formatter(name, formatter): Add a logging formatter to the configuration.
        add_default_formatter(): Add a predefined logging formatter to the configuration.
        add_default_django_formatter(): Add a Django-specific logging formatter.
        add_handler(name, handler): Add a logging handler to the configuration.
        add_console_handler(level, class_handler, formatter, stream): Add a console logging handler.
        add_file_handler(directory, level, class_handler, formatter): Add a file logging handler.
        add_logger(name, logger): Add a logger to the configuration.
        add_default_logger(name, handlers, level, propagate): Add a predefined logger with default handlers.
    """

    default_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {},
        "handlers": {},
        "loggers": {},
    }

    def __init__(self):
        self.__dict__.update(self.default_config)

    def __getitem__(self, key: Any):
        """
        Retrieve the value associated with a given key in the configuration.

        Args:
            key (Any): The key for the value to retrieve.

        Returns:
            Any: The value associated with the given key, or None if the key is not found.
        """
        return self.__dict__.get(key, None)

    def __delitem__(self, key: Any):
        """
        Doesn't do anything.

        Args:
            key (Any): The key to be removed from the configuration.
        """

    def __setitem__(self, key: Any, value: Any):
        """
        Set the value for a given key in the configuration.

        Args:
            key (Any): The key for which to set the value.
            value (Any): The value to associate with the given key.
        """
        if key in self.__dict__:
            self.__dict__[key] = value

    def __iter__(self):
        """
        Return an iterator over the configuration keys.

        Returns:
            Iterator: An iterator over the configuration keys.
        """
        return iter(self.__dict__)

    def __len__(self):
        """
        Return the number of key-value pairs in the configuration.

        Returns:
            int: The number of key-value pairs.
        """
        return len(self.__dict__)

    def __repr__(self):
        """
        Return a string representation of the configuration.

        Returns:
            str: The string representation of the configuration.
        """
        return self.__dict__.__repr__()

    def add_formatter(self, name: str, formatter: dict[str, Any]):
        """
        Add a logging formatter to the configuration.

        Args:
            name (str): The name of the formatter.
            formatter (dict): The formatter configuration.
        """
        self["formatters"][name] = formatter

    def add_default_formatter(self):
        """
        Add a predefined logging formatter to the configuration.
        """
        self["formatters"]["formatter"] = {
            "format": (
                "[%(name)s %(levelname)s %(asctime)s %(filename)s: %(lineno)d"
                " - %(funcName)s()] %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }

    def add_default_django_formatter(self):
        """
        Add a Django-specific logging formatter to the configuration.
        """
        self["formatters"]["formatter"] = {
            "()": "django.utils.log.ServerFormatter",
            "format": (
                "[%(name)s %(levelname)s %(asctime)s %(filename)s: %(lineno)d"
                " - %(funcName)s()] %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }

    def add_handler(self, name: str, handler: dict[str, Any]):
        """
        Add a logging handler to the configuration.

        Args:
            name (str): The name of the handler.
            handler (dict): The handler configuration.
        """
        self["handlers"][name] = handler

    def add_console_handler(
        self,
        level: str = "INFO",
        class_handler: str = "logging.StreamHandler",
        formatter: str = "formatter",
        stream: str = "ext://sys.stdout",
    ):
        """
        Add a console logging handler.

        Args:
            level (str): Logging level, default is "INFO".
            class_handler (str): Handler class, default is "logging.StreamHandler".
            formatter (str): Formatter name, default is "formatter".
            stream (str): Stream location, default is "ext://sys.stdout".
        """
        self["handlers"]["console"] = {
            "level": level,
            "class": class_handler,
            "formatter": formatter,
            "stream": stream,
        }

    def add_file_handler(
        self,
        directory: str,
        level: str = "INFO",
        class_handler: str = "meowlogs.handlers.TimedRotatingFileHandler",
        formatter: str = "formatter",
    ):
        """
        Add a file logging handler.

        Args:
            directory (str): Directory for the log files.
            level (str): Logging level, default is "INFO".
            class_handler (str): Handler class, default is "meowlogs.handlers.TimedRotatingFileHandler".
            formatter (str): Formatter name, default is "formatter".
        """
        self["handlers"]["file"] = {
            "level": level,
            "class": class_handler,
            "formatter": formatter,
            "directory": directory,
        }

    def add_logger(self, name: str, logger: dict[str, Any]):
        """
        Add a logger to the configuration.

        Args:
            name (str): The name of the logger.
            logger (dict): The logger configuration.
        """
        self["loggers"][name] = logger

    def add_default_logger(
        self,
        name: str,
        handlers: tuple[str, str] = ("file", "console"),
        level: str = "INFO",
        propagate: bool = False,
    ):
        """
        Add a predefined logger with default handlers.

        Args:
            name (str): The name of the logger.
            handlers (tuple[str, str], optional): Handlers associated with the logger. Defaults to ("file", "console").
            level (str, optional): Logging level. Defaults to "INFO".
            propagate (bool, optional): Specify whether to propagate log entries. Defaults to False.
        """
        self["loggers"][name] = {
            "handlers": handlers,
            "level": level,
            "propagate": propagate,
        }
