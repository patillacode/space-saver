# Space Saver

`space_saver.py` converts video files to .mp4 format with H.265 codec.
It walks through a directory and its subdirectories looking for files with a given
extension (or all files if no extension is given), and converts them to .mp4 with
H.265 codec.

The original file is deleted if the conversion is successful,
and the new file is given permissions of 755.
The script also calculates the space saved by the conversion and prints it at the end.

## Setup

1. Clone this repository.
2. Navigate to the project directory.
3. Run `make install` to set up the project.

## Usage

```bash
usage: space_saver.py [-h] -p PATH -f FORMAT [-d] [-q] [-c CRF]

Convert files to .mp4 with H.265 codec

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the directory containing the .\{format\} files to convert
                        into .mp4 files with H.265 codec
  -f FORMAT, --format FORMAT
                        File formats to convert, if not given all files will be checked
  -d, --dry-run         Perform a dry run without actually converting files
  -q, --quiet           Keep the ffmpeg output to a minimum while converting
  -c CRF, --crf CRF     Set the Constant Rate Factor (CRF) value for the ffmpeg command
```

## Project Structure

- `space_saver.py`: The main script that converts video files to the H.265 codec.
- `requirements.txt`: A list of python dependencies required to run the script.
- `Makefile`: A makefile with commands for setting up the project, running the script, and cleaning up the project.
- `README.md`: This file.
