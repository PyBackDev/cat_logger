import os
from datetime import datetime

from simple_logs.files import Directory, File, LoggingFile


# Tests for Directory class
def test_directory_exist(temp_dir):
    """Tests the creation of a directory using the `directory_exist` method.

    Args:
        temp_dir (str): Path to the temporary directory.
    """
    dir_path = os.path.join(temp_dir, "new_directory")
    directory = Directory(dir_path)
    directory.directory_exist()
    assert os.path.exists(dir_path) and os.path.isdir(dir_path)


def test_join_directories(temp_dir):
    """Tests the joining of a base directory path with a subdirectory.

    Args:
        temp_dir (str): Path to the temporary directory.
    """
    directory = Directory(temp_dir)
    combined_path = directory.join_directories("subdir")
    assert combined_path == os.path.join(temp_dir, "subdir")


# Tests for File class
def test_delete_file(temp_dir, temp_files):
    """Tests the deletion of a file in the directory using the `delete_file` method.

    Args:
        temp_dir (str): Temporary directory path.
        temp_files (list[str]): List of temporary file names in the directory.
    """
    file = File(temp_dir)
    target_file = temp_files[0]
    file.delete_file(target_file)
    assert not os.path.exists(os.path.join(temp_dir, target_file))


def test_get_file_names(temp_dir, temp_files):
    """Tests retrieval of file names in the directory using the `get_file_names` method.

    Args:
        temp_dir (str): Temporary directory path.
        temp_files (list[str]): List of temporary file names in the directory.
    """
    file = File(temp_dir)
    files = file.get_file_names()
    assert sorted(files) == sorted(temp_files)


def test_file_exist(temp_dir):
    """Tests the check for file existence using the `file_exist` method.

    Args:
        temp_dir (str): Temporary directory path.
    """
    temp_file_path = os.path.join(temp_dir, "test.txt")
    with open(temp_file_path, "w") as f:
        f.write("Test file content")
    assert File.file_exist(temp_file_path)
    os.remove(temp_file_path)
    assert not File.file_exist(temp_file_path)


# Tests for LoggingFile class
def test_filename_datetime(temp_dir, temp_files):
    """Tests sorting and filtering of file names based on datetime suffix.

    Args:
        temp_dir (str): Temporary directory path.
        temp_files (list[str]): List of temporary file names in the directory.
    """
    suffix = "%Y-%m-%d"
    logging_file = LoggingFile(temp_dir, suffix, backup_count=5)

    # Creating files with correct and incorrect suffix formats
    valid_files = [
        f"2023-11-{str(i).zfill(2)}" for i in range(1, 6)
    ]  # Files with valid suffix
    for file_name in valid_files:
        with open(os.path.join(temp_dir, file_name), "w") as f:
            f.write("Log file")

    # Attempt to sort and exclude invalid files
    sorted_files = logging_file.filename_datetime(
        temp_files + valid_files
    )  # Includes temp_files + valid suffix files
    assert sorted_files == sorted(
        valid_files, key=lambda x: datetime.strptime(x, suffix)
    )
    assert all(
        file not in os.listdir(temp_dir) for file in temp_files
    )  # Invalid files should be deleted


def test_file_to_delete(temp_dir):
    """Tests the deletion of old files exceeding the backup count.

    Args:
        temp_dir (str): Temporary directory path.
    """
    suffix = "%Y-%m-%d"
    logging_file = LoggingFile(temp_dir, suffix, backup_count=3)

    # Create 5 files with valid suffixes
    valid_files = [f"2023-11-{str(i).zfill(2)}" for i in range(1, 6)]
    for file_name in valid_files:
        with open(os.path.join(temp_dir, file_name), "w") as f:
            f.write("Log file")

    # Ensure it only keeps the most recent 3 files
    logging_file.file_to_delete()
    remaining_files = logging_file.get_file_names()  # Only 3 newest files
    assert remaining_files == valid_files[3:]
