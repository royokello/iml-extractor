# IML Extractor

This Python script allows you to extract frames from videos in two modes:

- **Time-based extraction**: Extract a specified number of frames per given time unit (second, minute, or hour).  
  *Defaults*: 1 frame per second (`-f 1 -t second`).

- **Random extraction**: Randomly extract a given number of frames from each video. When using random mode, you must provide the `--random_counter` argument.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [License](#license)

---

## Features

- **Time-based frame extraction**: Specify frames per second, minute, or hour.
- **Random frame extraction**: Randomly select a specified number of frames from each video.
- **Batch processing**: Processes all video files within an input directory (including subdirectories).
- Automatically creates the output directory if it doesn’t exist.
- Supports popular video formats: `.mp4`, `.avi`, `.mov`, `.mkv`.

---

## Prerequisites

- **Python 3.6+**
- **OpenCV** for Python  
Install via:
```bash
pip install opencv-python
```

---

## Installation

1. **Clone or download** the script to your local machine.
2. Ensure you have Python 3.6+ installed.
3. Install the required dependencies as noted above.

---

## Usage

```bash
python extract_frames.py -i <input_directory> -o <output_directory> -f <frames> -t <time> [--random] [--random_counter <number>]
```

**Notes:**
- The `-f`/`--frames` flag specifies the number of frames to extract per time unit when not in random mode (default: `1`).
- The `-t`/`--time` flag specifies the time unit for extraction. Options: `second`, `minute`, or `hour` (default: `second`).
- The `--random` flag enables random frame extraction.
- When `--random` is set, you **must** provide `--random_counter` to specify how many random frames to extract per video.

---

## Command-Line Arguments

| **Option**              | **Description**                                                                                                                                      | **Default**     |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `-i, --input`           | **Required.** Directory containing videos. Recursively searches subdirectories for video files.                                                     | *None*          |
| `-o, --output`          | **Required.** Directory where the extracted frames will be saved.                                                                                  | *None*          |
| `-f, --frames`          | Number of frames to extract per specified time unit (used in time-based mode).                                                                        | `1`             |
| `-t, --time`            | Time unit for frame extraction. Options: `second`, `minute`, or `hour`.                                                                              | `second`        |
| `--random`              | If set, extracts frames randomly instead of using fixed intervals.                                                                                 | `False`         |
| `--random_counter`      | Number of random frames to extract from each video (required if `--random` is set).                                                                    | *None*          |

---

## Examples

1. **Time-based extraction** (default: 1 frame per second):
    ```bash
    python extract_frames.py -i my_videos -o frames_output
    ```
2. **Extract 2 frames per second**:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 2 -t second
    ```
3. **Extract 1 frame per minute**:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 1 -t minute
    ```
4. **Random frame extraction**: Extract 5 random frames per video:
    ```bash
    python extract_frames.py -i my_videos -o frames_output --random --random_counter 5
    ```

---

## How It Works

1. **Directory Scanning**:  
   The script recursively scans the specified input directory for video files with extensions `.mp4`, `.avi`, `.mov`, or `.mkv`.

2. **Frame Extraction Modes**:
   - **Time-based Mode**:  
     - Retrieves the video’s frames per second (FPS) using OpenCV.
     - Calculates the total number of frames in the chosen time unit (using a multiplier of 1 for seconds, 60 for minutes, or 3600 for hours).
     - Computes an interval so that the specified number of frames is evenly extracted.
   - **Random Mode**:  
     - Obtains the total frame count for the video.
     - Randomly selects the specified number of frame indices (ensuring they are unique) and sorts them.
     - Seeks to each frame index to extract and save the frame.

3. **Saving Frames**:  
   Extracted frames are saved sequentially (named using a running counter) in the designated output directory.

---

## License

This script is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify, distribute, or use it in your projects.

---

**Happy extracting!**  
If you have any suggestions or encounter issues, please open an issue or submit a pull request.