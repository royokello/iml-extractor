import os
import cv2
import argparse
import math

def extract_frames(video_path, output_dir, frames_per_unit=1, time_unit='second', start_count=1):
    """
    Extract frames from a single video based on the specified number of frames
    per given time unit (second, minute, or hour).

    Parameters
    ----------
    video_path : str
        Path to the video file.
    output_dir : str
        Directory where the extracted frames are saved.
    frames_per_unit : int, optional
        How many frames to extract per specified time unit. Defaults to 1.
    time_unit : {'second', 'minute', 'hour'}, optional
        The time unit for frames extraction. Defaults to 'second'.
    start_count : int, optional
        The starting index for naming the extracted frames. Defaults to 1.
    """

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print(f" ! Skipping {video_path} (cannot read FPS).")
        return start_count

    # Determine how many frames (in the video) correspond to one time unit
    if time_unit.lower() == 'minute':
        multiplier = 60
    elif time_unit.lower() == 'hour':
        multiplier = 3600
    else:  # default to 'second'
        multiplier = 1

    # frames_in_one_unit = fps * multiplier
    # We want to distribute 'frames_per_unit' frames evenly in that many frames
    # So interval = total_frames_in_one_unit / frames_per_unit
    frames_in_one_unit = fps * multiplier
    interval_float = frames_in_one_unit / frames_per_unit

    # Ensure interval is at least 1 to avoid modulo zero or infinite loops
    interval = max(int(round(interval_float)), 1)

    frame_count = 0
    image_count = start_count
    success = True

    print(f" * Processing: {video_path} | {frames_per_unit} frame(s) per {time_unit} -> Interval={interval}")

    while success:
        success, frame = cap.read()
        if not success:
            break

        # If current frame index is divisible by the interval, save the frame
        if frame_count % interval == 0:
            frame_filename = os.path.join(output_dir, f"{image_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            image_count += 1

        frame_count += 1

    cap.release()
    return image_count

def walk_directory_and_extract_frames(input_dir, output_dir, frames_per_unit=1, time_unit='second'):
    """
    Recursively walk through a directory to find video files and extract frames.

    Parameters
    ----------
    input_dir : str
        Directory containing video files (searches subdirectories).
    output_dir : str
        Directory to save extracted frames.
    frames_per_unit : int, optional
        How many frames to extract per specified time unit. Defaults to 1.
    time_unit : {'second', 'minute', 'hour'}, optional
        The time unit for frames extraction. Defaults to 'second'.
    """
    image_count = 1
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(root, file)
                image_count = extract_frames(
                    video_path,
                    output_dir,
                    frames_per_unit=frames_per_unit,
                    time_unit=time_unit,
                    start_count=image_count
                )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract a certain number of frames per time unit from videos."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input directory containing videos."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory to save frames."
    )
    parser.add_argument(
        "-f", "--frames",
        type=int,
        default=1,
        help="Number of frames to extract per time unit (default: 1)."
    )
    parser.add_argument(
        "-t", "--time",
        choices=["second", "minute", "hour"],
        default="second",
        help="Time unit for frames extraction (default: 'second')."
    )

    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output
    frames_per_unit = args.frames
    time_unit = args.time

    os.makedirs(output_directory, exist_ok=True)
    walk_directory_and_extract_frames(
        input_directory, 
        output_directory, 
        frames_per_unit=frames_per_unit, 
        time_unit=time_unit
    )

