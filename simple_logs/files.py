import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass(repr=False, eq=False, frozen=True, slots=True, match_args=False)
class Directory:
    """
    Represents a directory and provides utility methods for directory operations.

    Attributes:
        directory (str): The path of the directory.

    Methods:
        directory_exist():
            Creates the directory if it doesn't already exist.
        join_directories(directory: str) -> str:
            Joins the base directory with another directory path.
    """

    directory: str

    def directory_exist(self) -> None:
        """
        Create the directory if it doesn't exist.

        Raises:
            PermissionError: If the process lacks permissions to create the directory.
            TypeError: If the provided path is not valid.
        """
        try:
            Path(self.directory).mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    def join_directories(self, directory: str) -> str:
        """
        Join the base directory with another directory path.

        Args:
            directory (str): The directory path to join with the base directory.

        Returns:
            str: The combined directory path.
        """
        return os.path.join(self.directory, directory)


@dataclass(repr=False, eq=False, frozen=True, slots=True, match_args=False)
class File(Directory):
    """
    Represents file operations based on a directory.

    Methods:
        delete_file(file: str) -> None:
            Deletes a specific file within the directory.

        get_file_names() -> list[str] | None:
            Retrieves a list of file names in the directory.

        file_exist(cls, filename: str) -> bool:
            Checks if a file exists at the given path.
    """

    def delete_file(self, file: str) -> None:
        """
        Deletes a specific file within the directory.

        Args:
            file (str): The name of the file to be deleted.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        try:
            os.remove(os.path.join(self.directory, file))
        except OSError:
            pass

    def get_file_names(self) -> list[str]:  # type: ignore[return]
        """
        Retrieves a list of file names in the directory.

        Returns:
            list[str]: A list of file names if the directory exists,
            otherwise None.

        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        try:
            return os.listdir(self.directory)
        except OSError:
            pass

    @classmethod
    def file_exist(cls, filename: str) -> bool:
        """
        Checks if a file exists at the given path.

        Args:
            filename (str): The path to the file.

        Returns:
            bool: True if the file exists and is a file, otherwise False.
        """
        return all((os.path.exists(filename), os.path.isfile(filename)))


@dataclass(repr=False, eq=False, frozen=True, slots=True, match_args=False)
class LoggingFile(File):
    """
    A class for handling logging operations with files in a specific directory.

    This class extends the `File` class and provides additional functionality
    to manage files with naming based on datetime suffixes and to enforce
    a limit on the number of backup files.

    Attributes:
        suffix (str): The datetime format suffix used in file names.
        backup_count (int): The maximum number of backup files to retain.

    Methods:
        filename_datetime(file_names: List[str]) -> List[str]:
            Extracts datetime-suffixed file names and sorts them in chronological order.
        file_to_delete() -> None:
            Deletes files exceeding the backup count.
    """

    suffix: str
    backup_count: int

    def filename_datetime(self, file_names: List[str]) -> List[str]:
        """
        Extracts and sorts file names based on their datetime suffix.

        Args:
            file_names (List[str]): A list of file names to process.

        Returns:
            List[str]: A list of file names with valid datetime suffixes,
            sorted in chronological order.

        Raises:
            ValueError: If a file name does not match the datetime suffix format,
            the file is deleted.
        """
        dates: List[datetime] = []
        for file in file_names:
            try:
                date = datetime.strptime(file, self.suffix)
                dates.append(date)
            except ValueError:
                self.delete_file(file)
        dates.sort()
        return [datetime.strftime(value, self.suffix) for value in dates]

    def file_to_delete(self) -> None:
        """
        Deletes files exceeding the specified backup count.

        This method retrieves file names from the directory, sorts them
        by their datetime suffix, and deletes the oldest files if the
        number of files exceeds the `backup_count` attribute.

        Returns:
            None
        """
        file_names: List[str] = self.get_file_names()
        if not file_names:
            return
        names: List[str] = self.filename_datetime(file_names)
        diff: int = len(names) - self.backup_count
        if diff >= 0:
            for file in names[0 : diff + 1]:
                self.delete_file(file)
