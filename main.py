import os
import cv2
import argparse
import random

def extract_frames(video_path, output_dir, frames_per_unit=1, time_unit='second', 
                   start_count=1, random_mode=False, random_counter=None):
    """
    Extract frames from a single video.

    In time-based mode (random_mode is False), it extracts a specified number of frames per
    given time unit (second, minute, or hour). In random mode (random_mode is True), it randomly
    selects 'random_counter' frames from the video.

    Parameters
    ----------
    video_path : str
        Path to the video file.
    output_dir : str
        Directory where the extracted frames are saved.
    frames_per_unit : int, optional
        Number of frames to extract per time unit (if random_mode is False). Defaults to 1.
    time_unit : {'second', 'minute', 'hour'}, optional
        Time unit for frame extraction (if random_mode is False). Defaults to 'second'.
    start_count : int, optional
        The starting index for naming the extracted frames. Defaults to 1.
    random_mode : bool, optional
        If True, randomly select frames instead of using time-based intervals. Defaults to False.
    random_counter : int or None, optional
        Number of random frames to extract (must be provided if random_mode is True).

    Returns
    -------
    int
        The next image count after extraction.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f" ! Cannot open video: {video_path}")
        return start_count

    image_count = start_count

    if random_mode:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            print(f" ! Skipping {video_path} (invalid frame count).")
            cap.release()
            return image_count

        if random_counter is None:
            print(" ! Random counter not provided for random mode.")
            cap.release()
            return image_count

        if random_counter > total_frames:
            print(f" ! random_counter ({random_counter}) is greater than total frames ({total_frames}). Adjusting to total frames.")
            random_counter = total_frames

        # Randomly sample unique frame indices and sort them for sequential access.
        random_indices = sorted(random.sample(range(total_frames), random_counter))
        print(f" * Random mode: Processing {video_path} | Extracting {random_counter} random frames.")

        for frame_index in random_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            success, frame = cap.read()
            if not success:
                print(f" ! Failed to read frame at index {frame_index} in {video_path}")
                continue
            frame_filename = os.path.join(output_dir, f"{image_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            image_count += 1

    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            print(f" ! Skipping {video_path} (cannot read FPS).")
            cap.release()
            return image_count

        # Determine the multiplier based on the time unit.
        if time_unit.lower() == 'minute':
            multiplier = 60
        elif time_unit.lower() == 'hour':
            multiplier = 3600
        else:  # default to 'second'
            multiplier = 1

        # Calculate the number of frames in one unit of time.
        frames_in_one_unit = fps * multiplier
        # Determine the interval to evenly distribute the frames.
        interval_float = frames_in_one_unit / frames_per_unit
        interval = max(int(round(interval_float)), 1)

        print(f" * Processing: {video_path} | {frames_per_unit} frame(s) per {time_unit} -> Interval={interval}")

        frame_count = 0
        success = True

        while success:
            success, frame = cap.read()
            if not success:
                break

            if frame_count % interval == 0:
                frame_filename = os.path.join(output_dir, f"{image_count}.jpg")
                cv2.imwrite(frame_filename, frame)
                image_count += 1

            frame_count += 1

    cap.release()
    return image_count

def walk_directory_and_extract_frames(input_dir, output_dir, frames_per_unit=1, time_unit='second', 
                                        random_mode=False, random_counter=None, collate=False):
    """
    Recursively walk through a directory to find video files and extract frames.

    Parameters
    ----------
    input_dir : str
        Directory containing video files (searches subdirectories).
    output_dir : str
        Directory to save extracted frames.
    frames_per_unit : int, optional
        Number of frames to extract per time unit (if random_mode is False). Defaults to 1.
    time_unit : {'second', 'minute', 'hour'}, optional
        Time unit for frame extraction (if random_mode is False). Defaults to 'second'.
    random_mode : bool, optional
        If True, extract frames randomly. Defaults to False.
    random_counter : int or None, optional
        Number of random frames to extract (required if random_mode is True).
    collate : bool, optional
        If True, all images are saved directly in the output directory. If False (default), a subdirectory 
        with the video's name is created inside the output directory to store that video's frames.
    """
    # Global image counter for collated output.
    global_image_count = 1
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(root, file)
                if collate:
                    video_output_dir = output_dir
                    image_count = global_image_count
                else:
                    # Create a subdirectory named after the video (without its extension)
                    video_name = os.path.splitext(file)[0]
                    video_output_dir = os.path.join(output_dir, video_name)
                    os.makedirs(video_output_dir, exist_ok=True)
                    image_count = 1

                new_count = extract_frames(
                    video_path,
                    video_output_dir,
                    frames_per_unit=frames_per_unit,
                    time_unit=time_unit,
                    start_count=image_count,
                    random_mode=random_mode,
                    random_counter=random_counter
                )

                if collate:
                    global_image_count = new_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract frames from videos either at a specific rate per time unit or randomly. " +
                    "Optionally collate all frames into one output directory or create subdirectories per video."
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
        help="Time unit for frame extraction (default: 'second')."
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="If set, extracts frames randomly instead of at fixed intervals."
    )
    parser.add_argument(
        "--random_counter",
        type=int,
        help="Number of random frames to extract from each video (required if --random is set)."
    )
    parser.add_argument(
        "--collate",
        action="store_true",
        help="If set, all images are saved directly into the output directory. " +
             "If not set (default), a subdirectory is created for each video."
    )

    args = parser.parse_args()

    if args.random and args.random_counter is None:
        parser.error("--random requires --random_counter to be provided.")

    input_directory = args.input
    output_directory = args.output
    frames_per_unit = args.frames
    time_unit = args.time
    random_mode = args.random
    random_counter = args.random_counter
    collate = args.collate

    os.makedirs(output_directory, exist_ok=True)
    walk_directory_and_extract_frames(
        input_directory,
        output_directory,
        frames_per_unit=frames_per_unit,
        time_unit=time_unit,
        random_mode=random_mode,
        random_counter=random_counter,
        collate=collate
    )
