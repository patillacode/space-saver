import argparse

from utils.logger import configure_logger, logger
from utils.video import convert_to_H265_codec


def examples():
    return """
    Examples:
        python space_saver.py -p /home/user/videos -e mp4 mkv
        python space_saver.py -p /home/user/videos -d
        python space_saver.py -p /home/user/videos -q
        python space_saver.py -p /home/user/videos -q -crf 28
    """


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="space_saver.py",
        description="Convert files to .mp4 with H.265 codec",
        epilog=examples(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help=(
            "Path to the directory containing the files to convert into "
            ".mp4 files with H.265 codec"
        ),
    )
    parser.add_argument(
        "-e",
        "--extensions",
        required=False,
        default=["mp4", "mkv", "avi", "mpg", "mpeg", "mov", "wmv", "flv", "webm"],
        nargs="*",
        type=str,
        help=r"Extensions to filter, default: %(default)s",
    )
    parser.add_argument(
        "-c",
        "--crf",
        type=int,
        default=23,
        help="Constant Rate Factor for the H.265 codec, scale is 0-51 (default: 23)",
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
        "-l",
        "--log",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    configure_logger(args.log)
    logger.info(f"Starting conversion process. {'(DRY RUN)' if args.dry_run else ''}")
    try:
        convert_to_H265_codec(
            args.path, args.extensions, args.dry_run, args.crf, args.quiet
        )
    except Exception as err:
        logger.error(f"An error occurred during conversion: {err}")
    else:
        logger.info("Conversion process finished.")
