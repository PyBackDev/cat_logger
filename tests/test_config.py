def test_initial_configuration(config_logging):
    """Test the default configuration of ConfigLogging."""
    assert config_logging["version"] == 1
    assert config_logging["disable_existing_loggers"] is True
    assert config_logging["formatters"] == {}
    assert config_logging["handlers"] == {}
    assert config_logging["loggers"] == {}


def test_set_and_get_item(config_logging):
    """Test setting and getting configuration items."""
    config_logging["version"] = 2
    config_logging["test_key"] = "test_value"
    assert config_logging["version"] == 2
    assert config_logging["test_key"] is None


def test_del_item(config_logging):
    """Test that deleting an item does not change the configuration."""
    # __delitem__ doesn't perform any operation
    del config_logging["version"]
    assert "version" in config_logging


def test_iter_keys(config_logging):
    """Test iterating over configuration keys."""
    expected_keys = [
        "version",
        "disable_existing_loggers",
        "formatters",
        "handlers",
        "loggers",
    ]
    assert list(config_logging.__iter__()) == expected_keys


def test_len(config_logging):
    """Test the length of the configuration (number of keys)."""
    assert len(config_logging) == len(config_logging.__dict__)


def test_repr(config_logging):
    """Test the string representation of the configuration."""
    assert repr(config_logging) == repr(config_logging.__dict__)


def test_add_formatter(config_logging):
    """Test adding a formatter to the configuration."""
    formatter = {"format": "%(asctime)s - %(message)s"}
    config_logging.add_formatter("custom_formatter", formatter)
    assert "custom_formatter" in config_logging["formatters"]
    assert config_logging["formatters"]["custom_formatter"] == formatter


def test_add_default_formatter(config_logging):
    """Test adding the default formatter."""
    config_logging.add_default_formatter()
    assert "formatter" in config_logging["formatters"]
    assert (
        "format" in config_logging["formatters"]["formatter"]
    )  # Check that default format exists


def test_add_default_django_formatter(config_logging):
    """Test adding the default Django-specific formatter."""
    config_logging.add_default_django_formatter()
    formater = {
        "()": "django.utils.log.ServerFormatter",
        "format": (
            "[%(name)s %(levelname)s %(asctime)s %(filename)s: %(lineno)d"
            " - %(funcName)s()] %(message)s"
        ),
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
    assert "formatter" in config_logging["formatters"]
    assert config_logging["formatters"]["formatter"] == formater


def test_add_handler(config_logging):
    """Test adding a handler to the configuration."""
    handler = {"class": "logging.StreamHandler", "level": "DEBUG"}
    config_logging.add_handler("custom_handler", handler)
    assert "custom_handler" in config_logging["handlers"]
    assert config_logging["handlers"]["custom_handler"] == handler


def test_add_console_handler(config_logging):
    """Test adding a console logging handler to the configuration."""
    config_logging.add_console_handler()
    assert "console" in config_logging["handlers"]
    handler = config_logging["handlers"]["console"]
    assert handler["level"] == "INFO"
    assert handler["class"] == "logging.StreamHandler"
    assert handler["formatter"] == "formatter"
    assert handler["stream"] == "ext://sys.stdout"


def test_add_file_handler(config_logging):
    """Test adding a file logging handler to the configuration."""
    directory = "/logs/"
    config_logging.add_file_handler(directory)
    assert "file" in config_logging["handlers"]
    handler = config_logging["handlers"]["file"]
    assert handler["level"] == "INFO"
    assert handler["class"] == "simple_logs.handlers.TimedRotatingFileHandler"
    assert handler["formatter"] == "formatter"
    assert handler["directory"] == directory


def test_add_logger(config_logging):
    """Test adding a logger to the configuration."""
    logger = {"level": "DEBUG", "handlers": ["console"]}
    config_logging.add_logger("custom_logger", logger)
    assert "custom_logger" in config_logging["loggers"]
    assert config_logging["loggers"]["custom_logger"] == logger


def test_add_default_logger(config_logging):
    """Test adding a default logger to the configuration."""
    config_logging.add_default_logger("default_logger")
    assert "default_logger" in config_logging["loggers"]
    logger = config_logging["loggers"]["default_logger"]
    assert logger["handlers"] == ("file", "console")
    assert logger["level"] == "INFO"
    assert logger["propagate"] is False
