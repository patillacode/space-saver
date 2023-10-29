import argparse
import math
import os

import ffmpeg
from termcolor import colored


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def convert_single_file(input_file_path, mp4_file_path, quiet, crf):
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
        print(f"Converting {colored(input_file_path, 'yellow')} to mp4 with H.265 codec")
        ffmpeg.input(input_file_path).output(
            mp4_file_path,
            vcodec="libx265",
            crf=str(crf),
            acodec="aac",
            strict="experimental",
        ).overwrite_output().run(quiet=quiet)
    except ffmpeg.Error as err:
        print(
            f"Error occurred while converting {colored(input_file_path, 'yellow')} to "
            f"mp4: {colored(err, 'red')}"
        )
    else:
        # If the conversion was successful, delete the original file and change
        # permissions of the new file
        if os.path.isfile(input_file_path):
            os.remove(input_file_path)
            new_size = os.path.getsize(mp4_file_path)
            os.chmod(mp4_file_path, 0o755)
            space_saved = original_size - new_size
            print_file_sizes(original_size, new_size)
            return space_saved


def print_file_sizes(original_size, new_size):
    size_reduction = ((original_size - new_size) / original_size) * 100
    print(
        f"Original mkv file size: {colored(convert_size(original_size), 'magenta')}\n"
        f"New mp4 file size: {colored(convert_size(new_size), 'orange')}\n"
        f"Size reduction: {colored(int(size_reduction), 'orange')}%"
    )


def convert_to_H265_codec(path, format, dry_run, crf, quiet=False):
    total_space_saved = 0
    for root, _, files in os.walk(path):
        for file in files:
            print("Looking at file: ", file)
            if file.endswith(f".{format}") or file.endswith(f".{format.upper()}"):
                file_path = os.path.join(root, file)
                mp4_file_path = os.path.splitext(file_path)[0] + ".mp4"
                if dry_run:
                    print(f"Would convert {file_path} to {mp4_file_path}")
                else:
                    space_saved = convert_single_file(
                        file_path, mp4_file_path, quiet, crf
                    )
                    total_space_saved += space_saved if space_saved else 0
    print(colored(f"Total space saved: {convert_size(total_space_saved)}", "yellow"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert files to .mp4 with H.265 codec")
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help=(
            "Path to the directory containing the .\{format\} files to convert into "
            ".mp4 files with H.265 codec"
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        required=True,
        help="File formats to convert",
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
        help="Set the Constant Rate Factor (CRF) value for the ffmpeg command",
    )
    args = parser.parse_args()
    convert_to_H265_codec(args.path, args.format, args.dry_run, args.crf, args.quiet)
