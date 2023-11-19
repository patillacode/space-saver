import os
import tempfile
import unittest

from unittest.mock import patch

import ffmpeg

from utils.video import convert_single_file, convert_to_H265_codec


class VideoUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("utils.video.logger")
    @patch("utils.video.convert_single_file")
    @patch("utils.video.check_file_type")
    def test_convert_to_H265_codec(
        self, mock_check_file_type, mock_convert_single_file, mock_logger
    ):
        # Mock the return values and behavior of the dependencies
        mock_check_file_type.return_value = True
        mock_convert_single_file.return_value = 100  # Simulate space saved

        # Create test files with different extensions
        test_files = ["file1.mp4", "file2.mkv", "file3.avi"]
        for file in test_files:
            file_path = os.path.join(self.temp_dir.name, file)
            open(file_path, "w").close()

        # Call the function under test
        convert_to_H265_codec(
            self.temp_dir.name, [".mp4", ".mkv"], dry_run=False, crf=23, quiet=True
        )

        # Assert the expected behavior
        self.assertEqual(
            mock_check_file_type.call_count, 3
        )  # Check file type for each file
        self.assertEqual(mock_convert_single_file.call_count, 3)  # Convert each file
        self.assertEqual(mock_logger.info.call_count, 4)  # Log messages

    def test_convert_single_file_successful_conversion(self):
        input_file_path = "input_file.mp4"
        with open(input_file_path, "wb") as f:
            f.seek(1023)
            f.write(b"\0")
            f.close()
        output_file_path = "output_file.mp4"
        quiet = True
        crf = 23
        dry_run = False

        with patch("utils.video.logger") as mock_logger, patch(
            "utils.video.check_video_stream", return_value=True
        ), patch("utils.video.ffmpeg_convert") as mock_ffmpeg_convert, patch(
            "utils.video.after_conversion_clean_up"
        ) as mock_after_conversion_clean_up:
            original_size = 1024
            start_time = 0
            end_time = 10
            mock_ffmpeg_convert.return_value = (start_time, end_time)
            mock_after_conversion_clean_up.return_value = 500

            result = convert_single_file(
                input_file_path, output_file_path, quiet, crf, dry_run
            )

            mock_logger.info.assert_not_called()
            mock_ffmpeg_convert.assert_called_with(
                input_file_path, output_file_path, quiet, crf
            )
            mock_after_conversion_clean_up.assert_called_with(
                input_file_path,
                original_size,
                output_file_path,
                start_time,
                end_time,
            )
            self.assertEqual(result, 500)

        os.remove(input_file_path)

    def test_convert_single_file_conversion_error(self):
        input_file_path = "input_file.mp4"
        open(input_file_path, "w").close()
        output_file_path = "output_file.mp4"
        open(output_file_path, "w").close()
        quiet = True
        crf = 23
        dry_run = False

        with patch("utils.video.logger"), patch(
            "utils.video.check_video_stream", return_value=True
        ), patch(
            "utils.video.ffmpeg_convert",
            side_effect=ffmpeg.Error("Conversion error", None, None),
        ), self.assertRaises(
            ffmpeg.Error
        ):
            convert_single_file(input_file_path, output_file_path, quiet, crf, dry_run)

        os.remove(input_file_path)
        os.remove(output_file_path)
