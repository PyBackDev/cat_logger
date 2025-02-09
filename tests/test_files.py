import unittest
from typing import List
from unittest.mock import patch

from simple_logs.files import LoggingFile


class TestLoggingFile(unittest.TestCase):
    """
    Unit test suite for verifying the functionality of the LoggingFile class.

    This class provides tests to ensure that all core methods within the LoggingFile
    class work as expected. The tests cover file name retrieval, sorting by datetime,
    and file deletion logic ensuring the backup count is maintained. Mocking is used
    to simulate behavior of file system interactions.

    Attributes:
        logging_file (LoggingFile): An instance of the LoggingFile class initialized
            in the test setup with test-specific parameters.
    """

    def setUp(self) -> None:
        self.logging_file = LoggingFile(
            directory="test_directory", suffix="%Y-%m-%d", backup_count=3
        )

    @patch("os.listdir")
    def test_get_file_names(self, mock_listdir) -> None:
        """
        Tests the functionality of the `get_file_names` method by mocking the `os.listdir`
        method to simulate the presence of specific file names in a directory. Ensures
        that the method correctly retrieves and returns the list of file names as expected.

        Args:
            mock_listdir (): Mock object that substitutes the `os.listdir` method, allowing
                test-specific directory content to be simulated.
        """
        mock_listdir.return_value = ["2023-01-01", "2023-01-02", "2023-01-03"]
        self.assertEqual(
            self.logging_file.get_file_names(),
            ["2023-01-01", "2023-01-02", "2023-01-03"],
        )

    def test_filename_datetime(self) -> None:
        """
        Tests the `filename_datetime` method for sorting filenames containing date strings.

        This test case verifies the correctness of the `filename_datetime` method, ensuring
        it accurately filters and sorts filenames containing valid date strings in ascending
        order. Files with invalid date formats should be excluded from the output.

        Args:
            None: This is a method in a test class and does not take any arguments.

        Attributes:
            input_files (List[str]): A list of filenames where some contain valid date strings
                while others do not.
            expected_output (List[str]): The expected list of filenames with valid date strings,
                sorted in ascending order.

        Returns:
            None: The method asserts functionality without returning any value.

        Raises:
            AssertionError: If the expected output does not match the actual output generated
                by the `filename_datetime` method.
        """
        input_files: List[str] = [
            "2023-01-03",
            "invalid-file",
            "2023-01-01",
            "2023-01-02",
        ]
        expected_output: List[str] = ["2023-01-01", "2023-01-02", "2023-01-03"]
        self.assertEqual(
            self.logging_file.filename_datetime(input_files), expected_output
        )

    @patch.object(LoggingFile, "get_file_names")
    @patch.object(LoggingFile, "delete_file")
    def test_file_to_delete(self, mock_delete_file, mock_get_file_names) -> None:
        """
        Tests the `file_to_delete` method of the `LoggingFile` class. This test mocks
        the behavior of the `get_file_names` and `delete_file` methods to ensure that
        the `file_to_delete` method functions as expected. Specifically, it checks
        that the correct file is passed to the `delete_file` method and that it is
        called the expected number of times.

        This method uses `@patch.object` to mock the `delete_file` and
        `get_file_names` methods of the `LoggingFile` class. The mock works by
        substituting the real behavior of these methods with mock objects to
        test the logic in isolation.

        Args:
            mock_delete_file (MagicMock): A mock object that replaces the
                `delete_file` method during the test. This is used to verify if
                the method is called with the correct arguments and number of times.
            mock_get_file_names (MagicMock): A mock object that replaces the
                `get_file_names` method during the test. This is used to return
                a predefined list of file names for the `file_to_delete` method
                to process.
        """
        mock_get_file_names.return_value = [
            "2023-01-01",
            "2023-01-02",
            "2023-01-03",
            "2023-01-04",
            "2023-01-05",
        ]
        self.logging_file.file_to_delete()
        mock_delete_file.assert_called_with("2023-01-03")
        self.assertEqual(mock_delete_file.call_count, 3)

    @patch("os.remove")
    def test_delete_file(self, mock_remove) -> None:
        """
        Tests the `delete_file` method of the `LoggingFile` class to ensure that the correct file is
        being removed within the specified directory.

        Args:
            mock_remove (MagicMock): Mocked version of the `os.remove` function, used to simulate the
                behavior of file deletion without actually removing any files.
        """
        self.logging_file.delete_file("2023-01-01")
        mock_remove.assert_called_once_with("test_directory/2023-01-01")
