# Space Saver

`space_saver.py` converts video files to .mp4 format with H.265 codec.
The script *walks through* a given directory and its subdirectories looking for files with a given
extension (or all files if no extension is given), and converts them to .mp4 with
H.265 codec.

The original file is deleted if the conversion is successful,
and the new file is given permissions of 755.
The script also calculates the space saved by the conversion and prints it at the end.

## Setup

1. Clone this repository.
2. Navigate to the project directory.
3. Run `make install` to set up the project.

## Test

To run the tests: `make test`

## Usage

```bash
usage: space_saver.py [-h] -p PATH [-e [EXTENSIONS ...]] [-c CRF] [-d] [-q] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Convert files to .mp4 with H.265 codec

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the directory containing the files to convert
  -e [EXTENSIONS ...], --extensions [EXTENSIONS ...]
                        Extensions to filter, default: ['mp4', 'mkv', 'avi', 'mpg', 'mpeg', 'mov', 'wmv', 'flv', 'webm']
  -c CRF, --crf CRF     Constant Rate Factor for the H.265 codec, scale is 0-51 (default: 23)
  -d, --dry-run         Perform a dry run without actually converting files
  -q, --quiet           Keep the ffmpeg output to a minimum while converting
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level (default: INFO))

    Examples:
        python space_saver.py -p /home/user/videos -e mp4 mkv
        python space_saver.py -p /home/user/videos -d
        python space_saver.py -p /home/user/videos -q
        python space_saver.py -p /home/user/videos -q -crf 28
        python space_saver.py -p /home/user/videos -q -l DEBUG
```

