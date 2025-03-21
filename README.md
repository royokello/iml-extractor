
# IML Extractor

A Python script that extracts a specified number of frames per given time unit—**second**, **minute**, or **hour**. Great for creating datasets, thumbnails, or sampling large numbers of videos at flexible rates.

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

- **Batch processing** of all videos in a given directory (and its subdirectories).
- **Flexible extraction rate**:
  - Example: Extract **2 frames per second** or **5 frames per minute** or **1 frame per hour**.
- Automatically **creates the output directory** if it doesn’t exist.
- **Supports multiple video formats**: `.mp4`, `.avi`, `.mov`, `.mkv`.

---

## Prerequisites

- **Python 3.6+** (recommended)
- **OpenCV** for Python. Install via:
  ```bash
  pip install opencv-python
  ```

---

## Installation

1. **Clone** or **download** this script to your local machine.
2. Ensure you have Python 3.6+ installed.
3. Install the required Python packages (see above).

---

## Usage

```bash
python extract_frames.py -i <input_directory> -o <output_directory> -f <frames_per_unit> -t <time_unit>
```

---

## Command-Line Arguments

| **Option**        | **Description**                                                                                                               | **Default** |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------|------------:|
| `-i, --input`     | **Required.** Path to the input directory containing videos. Recursively searches subdirectories for video files.             |      *None* |
| `-o, --output`    | **Required.** Path to the directory where extracted frames will be saved.                                                     |      *None* |
| `-f, --frames`    | **Integer.** Number of frames to extract *per* chosen time unit.                                                               |          `1` |
| `-t, --time`      | **Time unit.** Must be one of: `second`, `minute`, `hour`.                                                                    |  `second` |

**Defaults**: `-f 1 -t second` = **Extract 1 frame per second**.

---

## Examples

1. **Extract 1 frame per second** (default usage):
    ```bash
    python extract_frames.py -i my_videos -o frames_output
    ```
2. **Extract 2 frames per second**:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 2 -t second
    ```
3. **Extract 5 frames per minute**:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 5 -t minute
    ```
4. **Extract 3 frames per hour**:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 3 -t hour
    ```

---

## How It Works

1. **Directory Walk**: Scans the input directory (and subdirectories) for video files with `.mp4`, `.avi`, `.mov`, `.mkv`.
2. **Open & Read Video**:
   - Gets the video’s FPS using OpenCV’s `VideoCapture`.
   - Determines the total number of frames in the chosen time unit (e.g., `fps * 60` for `minute`).
   - Calculates the interval based on the requested frames per time unit, ensuring at least an interval of 1 frame.
3. **Frame Extraction**:
   - Iterates through the video frames.
   - Every time the current frame index is divisible by `interval`, it saves that frame as a `.jpg` file.
4. **Repeat** for every matching video found.

---

## License

This script is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use it in commercial or personal projects, modify, or distribute.

---

**Happy extracting!** If you have questions or suggestions, feel free to open an issue or submit a pull request.