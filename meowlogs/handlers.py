import fcntl
import logging
import os
from datetime import datetime

from meowlogs.enums import LoggingLevel
from meowlogs.files import LoggingFile


class TimedRotatingFileHandler(logging.FileHandler):
    """
    A logging handler for managing log files that rotate based on date.

    This handler writes log records to a file, rotating the log file
    based on the specified date suffix. It ensures proper file locking
    during writes, supports log file rollovers, and removes old log
    files based on the backup count.

    Attributes:
        _directory (str): The directory where log files will be created.
        _suffix (str): The date format suffix for log file rotation.
        _backup_count (int): The number of backup log files to retain.
        _handler (LoggingFile): A helper for handling file operations.
        _filename (str): The current log file's name.
        _level (int): The log level threshold for this logger.

    Methods:
        init_file(): Ensures log directory existence and initializes the log file.
        get_filename(): Constructs the log file name based on date and suffix.
        do_rollover(filename): Rolls over to a new log file.
        get_level_logging(level): Maps log level names to numeric log levels.
        write_record_to_file(record): Writes a formatted log record to the log file.
        emit(record): Writes a log record with log rotation if necessary.
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
        level: str = "INFO",
    ):
        self._directory: str = directory
        self._suffix: str = suffix
        self._backup_count: int = backup_count
        self._handler: LoggingFile = LoggingFile(
            self._directory,
            self._suffix,
            self._backup_count,
        )
        self._filename: str = self.init_file()
        self._level: int = self.get_level_logging(level)
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

    def do_rollover(self, filename: str):
        """
        Handles log file rollover to a new file.

        This method closes the current log file, updates the handler
        to use a new file specified by `filename`, and ensures that
        the new file is open for writing.

        Args:
            filename (str): The path to the new log file.
        """
        self.close()
        filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        self.stream = self._open()

    def get_level_logging(self, level: str) -> int:
        """
        Converts a log level from its string representation to its numeric value.

        Args:
            level (str): The name of the log level (e.g., 'INFO', 'DEBUG').

        Returns:
            int: The numeric value associated with the specified log level. Defaults to logging.INFO if the level name is not found.
        """
        if level in LoggingLevel.__members__.keys():
            return LoggingLevel[level].value
        return logging.INFO

    def write_record_to_file(self, record: logging.LogRecord):
        """
        Writes a formatted log record to the current log file, ensuring proper file locking.

        Args:
            record (LogRecord): The log record to be written to the file.
        """
        msg = self.format(record)
        stream = self.stream
        try:
            fcntl.flock(stream, fcntl.LOCK_EX)
            stream.write(msg + self.terminator)
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)
        self.flush()

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record and handle log file rotation if necessary.

        This method writes a log record to a file, checking if a log
        file rotation is required. If the current log file's name
        differs from the expected filename (based on the date suffix),
        it performs a rollover. The log record is only written
        if its log level meets or exceeds the handler's threshold.

        Args:
            record (LogRecord): The log record to be emitted.
        """
        try:
            if record.levelno >= self._level:
                filename = self.get_filename()
                if not self._handler.file_exist(filename):
                    self._handler.file_to_delete()
                if self._filename != filename:
                    self._filename = filename
                    self.do_rollover(filename)
                self.write_record_to_file(record)
        except Exception:
            self.handleError(record)
