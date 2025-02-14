import os
from datetime import datetime
from logging import LogRecord
from unittest.mock import MagicMock, patch

import pytest  # type: ignore[import-not-found]

from simple_logs.handlers import TimedRotatingFileHandler


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
def mock_file_handler():
    with patch(
        "simple_logs.handlers.logging.FileHandler", autospec=True
    ) as MockFileHandler:
        MockFileHandler.return_value = MagicMock()
        yield MockFileHandler


@pytest.fixture
def handler(mock_file_handler, mock_logging_file, mocked_datetime_now):
    """Create a test instance of TimedRotatingFileHandler with mocked dependencies."""
    handler = TimedRotatingFileHandler(
        directory="/tmp/logs", suffix="%Y-%m-%d", backup_count=3, level="DEBUG"
    )
    return handler


def test_initialization(handler, mock_logging_file):
    """Test the initialization of the TimedRotatingFileHandler.

    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.
        mock_logging_file (MagicMock): Mocked LoggingFile class.

    Asserts:
        - The directory, suffix, and backup_count are set correctly.
        - LoggingFile is initialized with the correct arguments.
    """
    assert handler._directory == "/tmp/logs"
    assert handler._suffix == "%Y-%m-%d"
    assert handler._backup_count == 3
    assert handler._level == 10  # DEBUG level
    mock_logging_file.assert_called_once_with("/tmp/logs", "%Y-%m-%d", 3)


def test_get_filename(handler, mocked_datetime_now):
    """Test the get_filename method to ensure the filename is generated correctly.

    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.
        mocked_datetime_now (MagicMock): Mocked datetime for generating filenames.

    Asserts:
        - The filename matches the expected pattern based on the date.
    """
    filename = handler.get_filename()
    assert filename == "/tmp/logs/2023-10-01"


def test_file_rollover(handler, mock_logging_file):
    """Test the file rollover logic with the do_rollover method.

    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.
        mock_logging_file (MagicMock): Mocked LoggingFile class.

    Asserts:
        - The baseFilename is updated to the new filename after rollover.
    """
    new_filename = "/tmp/logs/2023-10-02"
    handler.do_rollover(new_filename)
    assert handler.baseFilename == os.path.abspath(new_filename)


def test_write_record_to_file(handler):
    """Test the write_record_to_file method to ensure log records are written correctly.

    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.

    Asserts:
        - The log message is written correctly to the stream.
        - File locking (fcntl) is used properly during the write.
    """
    record = LogRecord(
        name="test_logger",
        level=20,  # INFO
        pathname="test_path",
        lineno=10,
        msg="Test log message",
        args=None,
        exc_info=None,
    )
    with patch("fcntl.flock"):
        with patch.object(handler, "stream", MagicMock()) as mock_stream:
            handler.write_record_to_file(record)
            mock_stream.write.assert_called_once_with("Test log message\n")
            mock_stream.flush.assert_called_once()


def test_emit_with_rollover(handler, mock_logging_file):
    """Test the emit method, including log file rotation logic.

    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.
        mock_logging_file (MagicMock): Mocked LoggingFile class.

    Asserts:
        - The log record is written correctly if within the log level.
        - Log file rollover (do_rollover) is triggered when necessary.
    """
    record = LogRecord(
        name="test_logger",
        level=20,  # INFO
        pathname="test_path",
        lineno=10,
        msg="Test log message",
        args=None,
        exc_info=None,
    )
    with patch.object(handler, "get_filename") as mock_get_filename:
        with patch.object(handler, "do_rollover") as mock_do_rollover:
            with patch.object(handler, "write_record_to_file") as mock_write_record:
                mock_get_filename.return_value = "/tmp/logs/2023-10-01"
                handler.emit(record)
                mock_write_record.assert_called_once_with(record)
                mock_do_rollover.assert_not_called()

                # Simulate filename change for rollover
                mock_get_filename.return_value = "/tmp/logs/2023-10-02"
                handler.emit(record)
                mock_write_record.assert_called_with(record)
                mock_do_rollover.assert_called_once_with("/tmp/logs/2023-10-02")
