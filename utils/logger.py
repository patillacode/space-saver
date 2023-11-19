import logging


def configure_logger(log_level):
    if numeric_level := getattr(logging, log_level.upper(), None) is None:
        raise ValueError(f"Invalid log level: {log_level}")

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )


logger = logging.getLogger("space_saver")
