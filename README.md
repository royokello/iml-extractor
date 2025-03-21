# IML Extractor

This Python script extracts frames from videos with two primary extraction modes:

- **Time-based extraction:** Extract a specified number of frames per time unit (second, minute, or hour).  
  *Defaults:* 1 frame per second (`-f 1 -t second`).

- **Random extraction:** Randomly extract a given number of frames from each video.  
  *Usage:* Enable with `--random` and specify the number with `--random_counter`.

Additionally, you can choose how the extracted images are organized:

- **Collate mode (`--collate` flag):** All images from all videos are stored directly in the output directory.
- **Default mode:** A subdirectory is created for each video (named after the video) to store its frames.

**Note:** All extracted frames are saved as PNG files for lossless quality.

---

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

- **Time-based frame extraction:** Specify frames per second, minute, or hour.
- **Random frame extraction:** Randomly select a specified number of frames from each video.
- **Collation options:** Either collate all extracted frames into one directory or organize them into subdirectories by video.
- **Batch processing:** Processes all video files within an input directory (including subdirectories).
- **PNG output:** Uses lossless PNG format for extracted frames, preserving image quality.

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
python extract_frames.py -i <input_directory> -o <output_directory> -f <frames> -t <time> [--random] [--random_counter <number>] [--collate]
```

**Notes:**
- The `-f`/`--frames` flag specifies the number of frames to extract per time unit in time-based mode (default: `1`).
- The `-t`/`--time` flag specifies the time unit for extraction. Options: `second`, `minute`, or `hour` (default: `second`).
- The `--random` flag enables random extraction mode.
- When `--random` is set, you **must** provide `--random_counter` to specify how many random frames to extract per video.
- The `--collate` flag, when set, stores all images directly in the output directory. When not set, a subdirectory is created for each video using its name.

---

## Command-Line Arguments

| **Option**              | **Description**                                                                                                                                      | **Default**     |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `-i, --input`           | **Required.** Directory containing videos (searched recursively).                                                                                  | *None*          |
| `-o, --output`          | **Required.** Directory where the extracted frames will be saved.                                                                                  | *None*          |
| `-f, --frames`          | Number of frames to extract per specified time unit (used in time-based mode).                                                                        | `1`             |
| `-t, --time`            | Time unit for frame extraction. Options: `second`, `minute`, or `hour`.                                                                              | `second`        |
| `--random`              | If set, extracts frames randomly instead of using fixed intervals.                                                                                 | `False`         |
| `--random_counter`      | Number of random frames to extract from each video (required if `--random` is set).                                                                    | *None*          |
| `--collate`             | If set, all images are saved directly into the output directory. If not set, a subdirectory is created for each video (named after the video).      | `False`         |

---

## Examples

1. **Time-based extraction (default):** Extract 1 frame per second with separate folders per video.
    ```bash
    python extract_frames.py -i my_videos -o frames_output
    ```
2. **Extract 2 frames per second** with separate subdirectories:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 2 -t second
    ```
3. **Random extraction:** Extract 5 random frames per video into separate folders:
    ```bash
    python extract_frames.py -i my_videos -o frames_output --random --random_counter 5
    ```
4. **Collated extraction:** Extract 1 frame per minute and store all images in the same output directory:
    ```bash
    python extract_frames.py -i my_videos -o frames_output -f 1 -t minute --collate
    ```

---

## How It Works

1. **Directory Scanning:**  
   The script recursively searches the input directory for video files with extensions `.mp4`, `.avi`, `.mov`, or `.mkv`.

2. **Output Organization:**
   - **Collate Mode (`--collate`):**  
     All extracted frames from all videos are stored in the specified output directory using a global counter.
   - **Default Mode:**  
     For each video, a subdirectory (named after the video file, without extension) is created inside the output directory, and frame numbering starts from 1 for each video.

3. **Frame Extraction Modes:**
   - **Time-based Mode:**  
     - Reads the video’s frames per second (FPS) using OpenCV.
     - Calculates the total number of frames in the specified time unit.
     - Computes an interval to evenly distribute the extraction of the specified number of frames.
   - **Random Mode:**  
     - Retrieves the total frame count.
     - Randomly selects the specified number of unique frame indices (sorted for efficient reading).
     - Seeks to each selected frame index to extract and save the frame.

4. **Saving Frames:**  
   Extracted frames are saved as PNG files, ensuring lossless quality. Their filenames are sequential numbers, either global (in collated mode) or local to each video’s subdirectory.

---

## License

This script is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify, distribute, or use it in your projects.

---

**Happy extracting!**  
If you have any suggestions or encounter issues, please open an issue or submit a pull request.
