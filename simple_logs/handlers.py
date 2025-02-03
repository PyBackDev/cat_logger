import logging
import os
from datetime import datetime

from simple_logs.files import LoggingFile


class TimedRotatingFileHandler(logging.FileHandler):
    """
    A handler for logging to files, rotating them at regular time intervals.

    This handler manages log files in a specified directory by creating a new file for each time period
    (determined by `suffix`) and managing backup files up to a specified limit (`backup_count`). When the
    current log file reaches its expiration, the handler deletes old files and begins logging to a new one.

    Args:
        directory (str): The directory where log files will be created.
        suffix (str): The suffix format for log file names using datetime formatting (e.g., "%Y-%m-%d").
                      Defaults to "%Y-%m-%d".
        backup_count (int): The maximum number of old log files to keep. Defaults to 14.
        mode (str): The file mode to use when opening the log file (e.g., "a" for append). Defaults to "a".
        encoding (str | None): The encoding to use for the log files. Defaults to None.
        delay (bool): Whether to delay the creation of the file until the first log record is emitted.
                      Defaults to False.
        errors (str | None): Determines how encoding errors are handled. Defaults to None.

    Methods:
        init_file(): Ensures the log directory exists and returns the current log file name.
        get_filename(): Constructs the log file name based on the current date and suffix.
        rename_file(filename): Updates the internal reference to the current log file.
        do_rollover(filename): Closes the current log file, deletes old files if necessary, and
                               starts a new log file.
        emit(record): Logs a record to the file, rolling over if the current log file needs to be replaced.
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
        """"""
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
