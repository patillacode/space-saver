# Space Saver

This project includes a script (`space_saver.py`) that converts video files to the H.265 codec, which provides more efficient encoding and results in smaller file sizes.

## Setup

1. Clone this repository.
2. Navigate to the project directory.
3. Run `make setup` to set up the project.

## Usage

Run `make run` to execute the script.

You can also run the script directly with `python space_saver.py -p <path> -f <format> [-d] [-q] [-c <crf>]`, where:

- `<path>` is the path to the directory containing the files to convert.
- `<format>` is the file format to convert.
- `-d` is an optional flag for a dry run without actually converting files.
- `-q` is an optional flag to keep the ffmpeg output to a minimum while converting.
- `<crf>` is an optional argument to set the Constant Rate Factor (CRF) value for the ffmpeg command (default is 23).

## Project Structure

- `space_saver.py`: The main script that converts video files to the H.265 codec.
- `requirements.txt`: A list of python dependencies required to run the script.
- `Makefile`: A makefile with commands for setting up the project, running the script, and cleaning up the project.
- `README.md`: This file.
