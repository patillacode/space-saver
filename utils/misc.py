import math
import os

from pathlib import Path

from utils.logger import logger


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def print_file_sizes(original_size, new_size):
    size_reduction = ((original_size - new_size) / original_size) * 100
    logger.info(
        f"Original file size: {convert_size(original_size)}\n"
        f"New mp4 file size: {convert_size(new_size)}\n"
        f"Size reduction: {int(size_reduction)}%"
    )


def check_file_type(file, extensions):
    file_extension = Path(file).suffix.lower()[1:]
    if file_extension not in extensions:
        logger.warning(
            f'Skipping file "{Path(file).name}", it doesn\'t have a valid extension'
        )
        return False
    return True


def after_conversion_clean_up(
    input_file_path, original_size, output_file_path, start_time, end_time
):
    if os.path.isfile(input_file_path):
        new_size = os.path.getsize(output_file_path)

        if original_size < new_size:
            os.remove(output_file_path)
            logger.warning(
                "The converted file is larger than the original file, "
                "keeping the original file, removing the converted file"
            )
            return 0

        logger.warning(
            "The original file is larger than the converted file, "
            "keeping the converted file, removing the original file"
        )
        os.remove(output_file_path)
        os.chmod(output_file_path, 0o755)
        space_saved = original_size - new_size
        print_file_sizes(original_size, new_size)
        hours, rem = divmod(end_time - start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        formatted_time = "{:0>2}:{:0>2}:{:05.2f}".format(
            int(hours), int(minutes), seconds
        )
        logger.info(f"Time elapsed: {formatted_time}")
        return space_saved
