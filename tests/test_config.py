import unittest

from simple_logs.config import ConfigLogging


class TestConfigLogging(unittest.TestCase):
    """
    Test suite for the ConfigLogging class.

    This class contains unit tests for the ConfigLogging class, ensuring that
    the configuration methods work as expected.

    Attributes:
        config_logging (ConfigLogging): An instance of the ConfigLogging class used for testing.
    """

    def setUp(self) -> None:
        self.config_logging = ConfigLogging()

    def test_initial_configuration(self) -> None:
        """
        Tests the initial configuration of the logging settings to ensure it matches the
        default configuration.

        The configuration is compared against the `default_config` attribute of the
        logging configuration to verify the correct setup on initialization.

        Args:
            self: Instance of the test class.

        Returns:
            None
        """
        self.assertEqual(self.config_logging, self.config_logging.default_config)

    def test_getitem(self) -> None:
        """
        Tests the behavior of retrieving a value from the `config_logging` dictionary
        when the key exists, ensuring it resolves to `None` as expected.

        Ensures that the test case verifies the overwritten behavior correctly when
        retrieving a set key from the `self.config_logging` dictionary.

        Args:
            self: The instance of the test case.

        Returns:
            None
        """
        self.config_logging["key"] = "value"
        self.assertEqual(self.config_logging["key"], None)

    def test_setitem(self) -> None:
        """
        Tests the '__setitem__' behavior for the 'config_logging' dictionary.

        This test ensures that after modifying the specific key-value pair in the
        'config_logging' dictionary via '__setitem__', the changes do not reflect
        as expected due to specific internal logic or restrictions implemented
        within the tested dictionary-like structure. It verifies that the value
        set operation does not persist as expected by asserting inequality.

        Args:
            No arguments are taken by this method.

        Raises:
            This method does not explicitly raise any exceptions.

        Returns:
            None: This method does not return a value.
        """
        self.config_logging["key"] = "value"
        self.assertNotEqual(self.config_logging["key"], "value")

    def test_add_formatter(self) -> None:
        """
        Tests the addition of a formatter to the logging configuration.

        This unit test validates that the `add_formatter` method correctly adds a new
        formatter configuration to the logging configuration. It ensures that the
        formatter name is properly included in the formatters section and that its
        configuration matches the expected structure.

        Args:
            None

        Returns:
            None
        """
        formatter = {"format": "%(levelname)s:%(message)s"}
        self.config_logging.add_formatter("simple", formatter)
        self.assertIn("simple", self.config_logging["formatters"])
        self.assertEqual(self.config_logging["formatters"]["simple"], formatter)

    def test_add_default_formatter(self) -> None:
        """
        Tests the addition of a default formatter to the logging configuration.

        This method verifies that the `add_default_formatter` function successfully
        adds a default formatter to the logging configuration. It checks if the
        dictionary containing configuration details is updated with a new formatter
        entry, including the expected `formatter` and its associated `format`.

        Args:
            None

        Returns:
            None
        """
        self.config_logging.add_default_formatter()
        self.assertIn("formatter", self.config_logging["formatters"])
        self.assertIn("format", self.config_logging["formatters"]["formatter"])

    def test_add_default_django_formatter(self) -> None:
        """
        Tests the addition of the default Django formatter into the logging configuration.

        The method `test_add_default_django_formatter` ensures that the `add_default_django_formatter` function correctly
        adds a default formatter named `"formatter"` to the `formatters` section of the logging configuration. The formatter
        is expected to utilize the `"django.utils.log.ServerFormatter"` class.

        Args:
            self: Instance of the test case class.

        Returns:
            None
        """
        self.config_logging.add_default_django_formatter()
        self.assertIn("formatter", self.config_logging["formatters"])
        self.assertEqual(
            self.config_logging["formatters"]["formatter"]["()"],
            "django.utils.log.ServerFormatter",
        )

    def test_add_handler(self) -> None:
        """
        Tests adding a new handler to the logging configuration.

        This method verifies that a handler can be added to the logging
        configuration and ensures the handler is correctly stored and
        accessible within the configuration.

        Args:
            None

        Returns:
            None
        """
        handler = {"class": "logging.StreamHandler", "level": "INFO"}
        self.config_logging.add_handler("console", handler)
        self.assertIn("console", self.config_logging["handlers"])
        self.assertEqual(
            self.config_logging["handlers"]["console"],
            handler,
        )

    def test_add_console_handler(self) -> None:
        """
        Tests the addition of a console handler to the logging configuration.

        This test ensures that invoking the `add_console_handler` method successfully
        adds a console handler to the logging configuration. The existence and type
        of the added handler are then verified.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the console handler is not added to the logging
                configuration or the added handler has an incorrect class type.
        """
        self.config_logging.add_console_handler()
        self.assertIn("console", self.config_logging["handlers"])
        self.assertEqual(
            self.config_logging["handlers"]["console"]["class"],
            "logging.StreamHandler",
        )

    def test_add_file_handler(self) -> None:
        """
        Tests the addition of a file handler to the logging configuration.

        This test ensures that a file handler is correctly added to the logging
        configuration with the specified directory, and that the configuration
        reflects the changes accurately.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If the file handler is not added to the handlers or if
            the directory of the file handler is not set to the specified value.
        """
        self.config_logging.add_file_handler(directory="test_dir")
        self.assertIn("file", self.config_logging["handlers"])
        self.assertEqual(
            self.config_logging["handlers"]["file"]["directory"],
            "test_dir",
        )

    def test_add_logger(self) -> None:
        """Tests the functionality of adding a logger configuration.

        This method verifies that a logger configuration can be added successfully to the
        logging configuration and checks the integrity of the added logger's configuration.

        Args:
            self: Represents the instance of the test case class.

        Returns:
            None.

        Raises:
            AssertionError: If the logger is not found in the `config_logging` or its configuration
            does not match the expected value.
        """
        logger_config = {"handlers": ["console"], "level": "DEBUG"}
        self.config_logging.add_logger("test_logger", logger_config)
        self.assertIn("test_logger", self.config_logging["loggers"])
        self.assertEqual(
            self.config_logging["loggers"]["test_logger"],
            logger_config,
        )

    def test_add_default_logger(self) -> None:
        """
        Tests the addition of a default logger configuration.

        This test case ensures that the default logger is properly added
        to the logging configuration. It verifies that the logger is present
        in the configuration, its associated handlers and logging level are
        correctly set, and the logger's propagation attribute is properly
        configured.

        Args:
            self: The instance of the test case.

        Raises:
            AssertionError: If the logger configuration does not match
                the expected values.
        """
        self.config_logging.add_default_logger("default")
        self.assertIn("default", self.config_logging["loggers"])
        default_logger = self.config_logging["loggers"]["default"]
        self.assertEqual(default_logger[0]["handlers"], ("file", "console"))
        self.assertEqual(default_logger[0]["level"], "INFO")
        self.assertEqual(default_logger[0]["propagate"], False)

    def test_len(self) -> None:
        """
        Tests the length of the `config_logging` object.

        This test case verifies if the length of the `config_logging` object's attributes
        matches the expected value. The test ensures that the object contains the correct
        number of elements according to the expected configuration.

        Tests in this case help to ensure that the attributes within the object remain
        consistent after various operations on `config_logging`.

        Args:
            self: An instance of the unittest's test case class containing the
                test context.

        Returns:
            None
        """
        self.assertEqual(len(self.config_logging), 5)

    def test_iter(self) -> None:
        """
        Tests the iterator functionality for the `config_logging` dictionary.

        This method ensures that when the `config_logging` attribute is iterated
        upon, it yields the correct and expected sequence of keys. The equality
        between the produced list of keys and the expected list of keys is asserted.

        Raises:
            AssertionError: If the test fails and the list of keys from iteration does
                not match the expected list of keys.
        """
        keys = list(iter(self.config_logging))
        expected_keys = [
            "version",
            "disable_existing_loggers",
            "formatters",
            "handlers",
            "loggers",
        ]
        self.assertEqual(keys, expected_keys)
