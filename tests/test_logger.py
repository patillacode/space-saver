import unittest

from unittest.mock import patch

from utils.logger import configure_logger


class LoggerUtilsTestCase(unittest.TestCase):
    @patch("utils.logger.logging.basicConfig")
    def test_configure_logger_valid_log_level(self, mock_basic_config):
        # Call the function under test
        configure_logger("info")
        # Assert the expected behavior
        mock_basic_config.assert_called_once()

    def test_configure_logger_invalid_log_level(self):
        # Call the function under test and assert the expected exception
        with self.assertRaises(ValueError):
            configure_logger("invalid_log_level")
