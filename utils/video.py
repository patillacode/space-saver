import os
import time

from pathlib import Path

import ffmpeg

from utils.logger import logger
from utils.misc import after_conversion_clean_up, check_file_type, convert_size


def convert_to_H265_codec(path, extensions, dry_run, crf, quiet=False):
    total_space_saved = 0
    for root, _, files in os.walk(path):
        for file in files:
            logger.info(f'Looking at file: "{file}"')
            if check_file_type(file, extensions):
                input_file_path = os.path.join(root, file)
                base_file_path = os.path.splitext(input_file_path)[0]
                output_file_path = f"{base_file_path}_H265.mp4"
                space_saved = convert_single_file(
                    input_file_path, output_file_path, quiet, crf, dry_run
                )
                total_space_saved += space_saved if space_saved else 0
    logger.info(f"Total space saved: {convert_size(total_space_saved)}")


def convert_single_file(input_file_path, output_file_path, quiet, crf, dry_run):
    original_size = os.path.getsize(input_file_path)

    if check_video_stream(input_file_path):
        if dry_run:
            logger.info(f"Would convert {input_file_path} to {output_file_path}")
            return 0
        try:
            start_time, end_time = ffmpeg_convert(
                input_file_path, output_file_path, quiet, crf
            )
        except ffmpeg.Error as err:
            logger.error(
                f"Error occurred while converting {input_file_path} to mp4: {err}"
            )
            raise
        else:
            return after_conversion_clean_up(
                input_file_path,
                original_size,
                output_file_path,
                start_time,
                end_time,
            )


def ffmpeg_convert(input_file_path, mp4_file_path, quiet, crf):
    start_time = time.time()
    logger.info(f"Converting {input_file_path} to mp4 with H.265 codec")
    ffmpeg.input(input_file_path).output(
        mp4_file_path,
        vcodec="libx265",
        crf=str(crf),
        acodec="aac",
        strict="experimental",
    ).overwrite_output().run(quiet=quiet)
    end_time = time.time()

    return start_time, end_time


def check_video_stream(input_file_path):
    try:
        probe = ffmpeg.probe(input_file_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )

        if video_stream is None:
            logger.warning(f"No video stream found in {input_file_path}")
            return False

        if video_stream["codec_name"] == "hevc":
            logger.warning(
                f'File "{Path(input_file_path).name}" already using H.265 codec, '
                "skipping conversion."
            )
            return False

        return True

    except ffmpeg.Error as err:
        logger.error(
            f"Error occurred while checking video stream of {input_file_path}: {err}"
        )
        raise
