import logging
import os
from datetime import datetime

from simple_logs.files import LoggingFile


class TimedRotatingFileHandler(logging.FileHandler):
    """
    Handler for log files that rotates them based on time or date, facilitating log management.

    This class is designed to manage log files efficiently by creating a new log file
    at regular time intervals, ensuring old logs are appropriately backed up or removed.
    The rotation is determined using a timestamp suffix format. It supports customization
    of backup count, file encoding, file mode, and error handling. Ensures the directory
    for the log files exists and properly manages the rolling over of files when necessary.

    Attributes:
        _directory (str): Directory path where log files are stored.
        _suffix (str): Time or date format used as a suffix in filenames.
        _backup_count (int): Maximum number of old log files to keep.
        _handler (LoggingFile): Internal handler for file operations.
        _filename (str): Name of the currently active log file.
    """

    def __init__(
        self,
        directory: str,
        suffix: str = "%Y-%m-%d",
        backup_count: int = 14,
        mode: str = "a",
        encoding: str | None = None,
        delay: bool = False,
        errors: str | None = None,
    ):
        self._directory = directory
        self._suffix = suffix
        self._backup_count = backup_count
        self._handler = LoggingFile(
            self._directory,
            self._suffix,
            self._backup_count,
        )
        self._filename = self.init_file()
        super().__init__(self._filename, mode, encoding, delay, errors)

    def init_file(self) -> str:
        """
        Ensures that the log directory exists and initializes the current log file.

        Returns:
            str: The name of the initialized log file.
        """
        self._handler.directory_exist()
        return self.get_filename()

    def get_filename(self) -> str:
        """
        Constructs the log file name based on the current date and suffix.

        This method generates a file name by formatting the current date using the
        specified suffix and appending it to the directory path.

        Returns:
            str: The constructed log file name.
        """
        try:
            current_date = datetime.now().strftime(self._suffix)
        except ValueError:
            current_date = datetime.now().strftime("%Y-%m-%d")
        filename = str(self._directory) + "/" + str(current_date)
        return filename

    def rename_file(self, filename: str):
        """
        Updates the internal reference to the current log file.

        Args:
            filename (str): The new log file name to set.
        """
        filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)

    def do_rollover(self, filename: str):
        """
        Rolls over to a new log file by closing the current file, setting up the new file,
        and optionally managing file stream creation.

        Args:
            filename (str): The name of the new log file to roll over to.
        """
        if self.stream:
            self.stream.close()
            self.stream = None  # type: ignore[assignment]
        self.rename_file(filename)
        if not self.delay:
            self.stream = self._open()

    def emit(self, record):
        """
        Logs a record to the current log file, performing a log file rollover if necessary.

        Args:
            record: The log record to be logged.
        """
        try:
            filename = self.get_filename()
            if not self._handler.file_exist(filename):
                self._handler.file_to_delete()
                self.do_rollover(filename)
            super().emit(record)
        except Exception:
            self.handleError(record)
            super().emit(record)
