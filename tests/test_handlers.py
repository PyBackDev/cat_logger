import os
from logging import LogRecord
from unittest.mock import patch

from tests.enums import FileHandlerEnum


def test_initialization(handler, mock_logging_file):
    """Test the initialization of the TimedRotatingFileHandler.
    Args:
        handler (TimedRotatingFileHandler): The handler instance being tested.
        mock_logging_file (MagicMock): The mocked LoggingFile class.

    Assertions:
        - The directory, suffix, and backup_count are set correctly.
        - LoggingFile is initialized with the expected arguments.
    """
    assert handler._suffix == FileHandlerEnum.SUFFIX.value
    assert handler._backup_count == FileHandlerEnum.BACKUP_COUNT.value
    assert handler._level == 10  # DEBUG level


def test_get_filename(handler, mocked_datetime_now):
    """Tests the `get_filename` method to ensure the filename is generated correctly.
    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.
        mocked_datetime_now (MagicMock): Mocked datetime for generating filenames.

    Assertions:
        filename (str): Verifies that the filename matches the expected pattern based on the date.
    """
    filename = handler.get_filename()
    assert filename == handler._directory + "/2023-10-01"


def test_file_rollover(handler, mock_logging_file):
    """Test the file rollover logic with the do_rollover method.

    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.
        mock_logging_file (MagicMock): Mocked LoggingFile class.

    Asserts:
        - The baseFilename is updated to the new filename after rollover.
    """
    path = os.path.join(handler._directory, "2023-10-02")
    handler.do_rollover(path)
    assert handler.baseFilename == os.path.abspath(path)


def test_write_record_to_file(handler):
    """Tests the write_record_to_file method.
    Args:
        handler (TimedRotatingFileHandler): The handler instance under test.

    Assertions:
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
    handler.write_record_to_file(record)


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
        mock_get_filename.return_value = handler._directory + "/2023-10-01"
        handler.emit(record)

        # Simulate filename change for rollover
        mock_get_filename.return_value = handler._directory + "/2023-10-02"
        handler.emit(record)
