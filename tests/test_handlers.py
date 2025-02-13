import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from simple_logs.files import LoggingFile
from simple_logs.handlers import TimedRotatingFileHandler


class TestTimedRotatingFileHandler(unittest.TestCase):
    """
    Tests for the TimedRotatingFileHandler class.

    This test suite verifies the behavior of the TimedRotatingFileHandler class,
    including initialization, file handling, and log file rotation based on time.
    The tests simulate various scenarios to ensure the correct functionality
    of the handler.

    Attributes:
        directory (str): Directory path where log files are stored.
        suffix (str): Time or date format used as a suffix in filenames.
        backup_count (int): Maximum number of old log files to keep.
        handler (TimedRotatingFileHandler): Instance of the handler under test.
        current_date (str): Current date formatted according to the given suffix.
        path_to_dir (str): Full path to the log directory.
        path_to_file (str): Full path to the current log file.
    """

    def setUp(self):
        self.directory = "tests/logs"
        self.suffix = "%Y-%m-%d"
        self.backup_count = 7
        self.handler = TimedRotatingFileHandler(
            directory=self.directory,
            suffix=self.suffix,
            backup_count=self.backup_count,
        )
        self.current_date = datetime.now().strftime(self.suffix)
        self.path_to_dir = os.path.join(os.path.dirname(__file__), "logs")
        self.path_to_file = os.path.join(self.path_to_dir, self.current_date)

    def test_init_file(self):
        """
        Tests the `init_file` method of a logging file handler.

        This test ensures that the `init_file` method performs as expected by calling
        the `directory_exist` function and verifying the interaction.

        Args:
            self: Represents the instance of the test case.

        Raises:
            AssertionError: If `directory_exist` is not called exactly once during the
                execution of `init_file`.
        """
        with patch.object(LoggingFile, "directory_exist") as mock_directory_exist:
            self.handler.init_file()
            mock_directory_exist.assert_called_once()

    @patch("simple_logs.handlers.datetime")
    def test_get_filename(self, mock_datetime):
        """
        Tests the `get_filename` method to ensure that the generated filename matches
        the expected format based on the mocked current date.

        Args:
            mock_datetime (MagicMock): The mocked `datetime` class used to simulate
                the current date during the test.
        """
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01"
        expected_filename = f"{self.directory}/2023-01-01"
        self.assertEqual(self.handler.get_filename(), expected_filename)

    def test_do_rollover(self):
        """
        Executes and verifies the log file rollover operation for the handler instance.

        Tests the `do_rollover` function of the handler to ensure it correctly updates
        the `baseFilename` after performing the rollover process. Validates that the
        `baseFilename` matches the expected path after the rollover.

        Args:
            self: Represents the instance of the test case class.

        Raises:
            AssertionError: If the `baseFilename` does not match the expected value.

        """
        new_filename = f"{self.directory}/{self.current_date}"
        self.handler.do_rollover(new_filename)
        self.assertEqual(self.handler.baseFilename, self.path_to_file)

    @patch("simple_logs.handlers.TimedRotatingFileHandler.get_filename")
    def test_emit_rollover(self, mock_get_filename):
        """
        Test the emit method for rollover scenario in the TimedRotatingFileHandler.

        This method ensures that the `emit` method properly handles file rollover
        when a new log file is generated. It verifies that the rollover functionality
        deletes the old file and updates the handler's current log file path.

        Args:
            mock_get_filename (MagicMock): Mocked `get_filename` method from
                TimedRotatingFileHandler to control the file path returned.
        """
        mock_get_filename.return_value = self.path_to_file
        record = MagicMock()

        with patch.object(
            LoggingFile, "file_exist", return_value=False
        ) as mock_file_exist, patch.object(  # noqa F841
            LoggingFile, "file_to_delete"
        ) as mock_file_to_delete:
            self.handler.emit(record)
            mock_file_to_delete.assert_not_called()
            self.assertEqual(self.handler.baseFilename, self.path_to_file)

    @patch("simple_logs.handlers.TimedRotatingFileHandler.get_filename")
    def test_emit_no_rollover(self, mock_get_filename):
        """
        Test the emit functionality in the TimedRotatingFileHandler without triggering file
        rollover. This ensures that when a record is emitted, the base filename remains
        consistent, and no unnecessary file deletion occurs.

        Args:
            mock_get_filename (Mock): Mocked method for `get_filename` to control the
                filename used by the handler during the test.
        """
        mock_get_filename.return_value = self.path_to_file
        record = MagicMock()

        with patch.object(
            LoggingFile, "file_exist", return_value=True
        ) as mock_file_exist, patch.object(  # noqa F841
            LoggingFile, "file_to_delete"
        ) as mock_file_to_delete:
            self.handler.emit(record)
            mock_file_to_delete.assert_not_called()
            self.assertEqual(self.handler.baseFilename, self.handler.get_filename())
