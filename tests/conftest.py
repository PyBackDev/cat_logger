import os
import tempfile
from datetime import datetime
from unittest.mock import patch

import pytest  # type: ignore[import-not-found]

from simple_logs.config import ConfigLogging
from simple_logs.handlers import TimedRotatingFileHandler
from tests.enums import FileHandlerEnum


@pytest.fixture
def config_logging():
    # Initializes an instance of ConfigLogging for use in multiple tests
    return ConfigLogging()


@pytest.fixture
def temp_dir():
    """Creates a temporary directory for testing and ensures cleanup after the test."""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for directory in dirs:
            os.rmdir(os.path.join(root, directory))
    os.rmdir(dir_path)


@pytest.fixture
def temp_files(temp_dir):
    """Creates temporary files in the provided directory for testing.

    Args:
        temp_dir (str): Path to the temporary directory.

    Returns:
        list[str]: A list of created temporary file names.
    """
    filenames = ["file1.txt", "file2.txt", "invalid_name"]
    for name in filenames:
        with open(os.path.join(temp_dir, name), "w") as f:
            f.write("Sample content")
    return filenames


@pytest.fixture
def mocked_datetime_now():
    """Mock the datetime.now method to return a fixed value."""
    with patch("simple_logs.handlers.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1)
        mock_datetime.strftime = datetime.strftime
        yield mock_datetime


@pytest.fixture
def mock_logging_file():
    """Mock the LoggingFile class to emulate file handling behavior."""
    with patch("simple_logs.handlers.LoggingFile") as mock_file:
        yield mock_file


@pytest.fixture
def handler(temp_dir, mock_logging_file, mocked_datetime_now):
    """Create a test instance of TimedRotatingFileHandler with mocked dependencies."""
    handler = TimedRotatingFileHandler(
        directory=temp_dir,
        suffix=FileHandlerEnum.SUFFIX.value,
        backup_count=FileHandlerEnum.BACKUP_COUNT.value,
        level=FileHandlerEnum.LEVEL.value,
    )
    return handler
