import os
import tempfile
import unittest

from unittest.mock import patch

from utils.misc import (
    after_conversion_clean_up,
    check_file_type,
    convert_size,
    print_file_sizes,
)


class MiscUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_convert_size(self):
        # Test with different file sizes
        self.assertEqual(convert_size(0), "0B")
        self.assertEqual(convert_size(1024), "1.0 KB")
        self.assertEqual(convert_size(1048576), "1.0 MB")
        self.assertEqual(convert_size(1073741824), "1.0 GB")

    def test_print_file_sizes(self):
        # Mock the logger
        with patch("utils.misc.logger") as mock_logger:
            # Call the function under test
            print_file_sizes(1000000, 500000)

            # Assert the expected behavior
            mock_logger.info.assert_called_with(
                "Original file size: 976.56 KB\n"
                "New mp4 file size: 488.28 KB\n"
                "Size reduction: 50%"
            )

    def test_check_file_type(self):
        # Test with valid file extensions
        self.assertTrue(check_file_type("file1.mp4", ["mp4", "mkv"]))
        self.assertTrue(check_file_type("file2.mkv", ["mp4", "mkv"]))

        # Test with invalid file extension
        with patch("utils.misc.logger") as mock_logger:
            self.assertFalse(check_file_type("file3.avi", ["mp4", "mkv"]))
            mock_logger.warning.assert_called_with(
                'Skipping file "file3.avi", it doesn\'t have a valid extension'
            )

    def test_after_conversion_clean_up(self):
        # Create temporary input and output files
        input_file_path = os.path.join(self.temp_dir.name, "input.mp4")
        output_file_path = os.path.join(self.temp_dir.name, "output.mp4")
        # create a file that weighs 976.56 KB
        with open(input_file_path, "wb") as f:
            f.seek(976555)
            f.write(b"\0")
            f.close()
        # create a file that weighs 488.28 KB
        with open(output_file_path, "wb") as f:
            f.seek(488555)
            f.write(b"\0")
            f.close()

        # Call the function under test
        space_saved = after_conversion_clean_up(
            input_file_path, 1000000, output_file_path, 0, 10
        )

        # Assert the expected behavior
        self.assertEqual(space_saved, 511444)

        # Check that the input file is deleted
        self.assertFalse(os.path.isfile(input_file_path))

        # Check that the output file has the correct permissions
        self.assertEqual(oct(os.stat(output_file_path).st_mode)[-3:], "755")
