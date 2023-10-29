"""
This script converts video files to .mp4 format with H.265 codec.
It walks through a directory and its subdirectories looking for files with a given
extension (or all files if no extension is given), and converts them to .mp4 with
H.265 codec.

The original file is deleted if the conversion is successful,
and the new file is given permissions of 755.
The script also calculates the space saved by the conversion and prints it at the end.
"""

import argparse
import math
import os
import sys
import time

import ffmpeg

from termcolor import colored


def convert_size(size_bytes):
    """
    Converts the given size in bytes to a human-readable format.

    Args:
        size_bytes (int): The size in bytes.

    Returns:
        str: The size in a human-readable format.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def convert_single_file(input_file_path, mp4_file_path, quiet, crf, extension):
    """
    Converts a single video file to .mp4 format with H.265 codec.

    Args:
        input_file_path (str): The path to the input file.
        mp4_file_path (str): The path to the output .mp4 file.
        quiet (bool): Whether to keep the ffmpeg output to a minimum while converting.
        crf (int): The Constant Rate Factor (CRF) value for the ffmpeg command.
        extension (str): The extension of the input file.

    Returns:
        int: The space saved by the conversion, in bytes.
    """
    original_size = os.path.getsize(input_file_path)
    probe = ffmpeg.probe(input_file_path)
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
    )
    if video_stream is None:
        print(f"No video stream found in {colored(input_file_path, 'red')}")
        return
    if video_stream["codec_name"] == "hevc":
        print(f"{input_file_path} is already using H.265 codec, skipping conversion")
        return
    try:
        print(
            f"Converting {colored(input_file_path, 'yellow')} to mp4 with H.265 codec"
        )
        start_time = time.time()
        ffmpeg.input(input_file_path).output(
            mp4_file_path,
            vcodec="libx265",
            crf=str(crf),
            acodec="aac",
            strict="experimental",
        ).overwrite_output().run(quiet=quiet)
        end_time = time.time()
    except ffmpeg.Error as err:
        print(
            f"Error occurred while converting {colored(input_file_path, 'yellow')} to "
            f"mp4: {colored(err, 'red')}"
        )
        sys.exit()
    else:
        # If the conversion was successful, delete the original file and change
        # permissions of the new file
        if os.path.isfile(input_file_path):
            os.remove(input_file_path)
            new_size = os.path.getsize(mp4_file_path)
            os.chmod(mp4_file_path, 0o755)
            space_saved = original_size - new_size
            print_file_sizes(original_size, new_size, extension)
            hours, rem = divmod(end_time - start_time, 3600)
            minutes, seconds = divmod(rem, 60)
            formatted_time = "{:0>2}:{:0>2}:{:05.2f}".format(
                int(hours), int(minutes), seconds
            )
            print(f"Time elapsed: {colored(formatted_time, 'white')}")
            return space_saved


def print_file_sizes(original_size, new_size, extension):
    """
    Prints the original and new file sizes, and the space saved by the conversion.

    Args:
        original_size (int): The size of the original file, in bytes.
        new_size (int): The size of the new file, in bytes.
        extension (str): The extension of the original file.
    """
    size_reduction = ((original_size - new_size) / original_size) * 100
    print(
        f"Original {extension} file size: "
        f"{colored(convert_size(original_size), 'magenta')}\n"
        f"New mp4 file size: {colored(convert_size(new_size), 'cyan')}\n"
        f"Size reduction: {colored(int(size_reduction), 'cyan')}%"
    )


def convert_to_H265_codec(path, extension, dry_run, crf, quiet=False):
    """
    Converts all video files in the given directory and its subdirectories to .mp4 format
    with H.265 codec.

    Args:
        path (str): The path to the directory containing the video files to convert.
        extension (str): The extension of the video files to convert, or None to convert
                         all files.
        dry_run (bool): Whether to perform a dry run without actually converting files.
        crf (int): The Constant Rate Factor (CRF) value for the ffmpeg command.
        quiet (bool): Whether to keep the ffmpeg output to a minimum while converting.
    """
    total_space_saved = 0
    for root, _, files in os.walk(path):
        for file in files:
            print("Looking at file: ", file)
            if (
                extension is None
                or file.endswith(f".{extension}")
                or file.endswith(f".{extension.upper()}")
            ):
                file_path = os.path.join(root, file)
                base_file_path = os.path.splitext(file_path)[0]
                mp4_file_path = f"{base_file_path}_H265.mp4"
                if dry_run:
                    print(f"Would convert {file_path} to {mp4_file_path}")
                else:
                    space_saved = convert_single_file(
                        file_path, mp4_file_path, quiet, crf, extension
                    )
                    total_space_saved += space_saved if space_saved else 0
    print(colored(f"Total space saved: {convert_size(total_space_saved)}", "yellow"))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert files to .mp4 with H.265 codec"
    )
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help=(
            r"Path to the directory containing the .\{format\} files to convert into "
            ".mp4 files with H.265 codec"
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        required=False,
        help="File formats to convert, if not given all files will be checked",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Perform a dry run without actually converting files",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Keep the ffmpeg output to a minimum while converting",
    )
    parser.add_argument(
        "-c",
        "--crf",
        type=int,
        default=23,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    convert_to_H265_codec(args.path, args.format, args.dry_run, args.crf, args.quiet)
