import os
import cv2
import argparse

def extract_frames(video_path, output_dir, frame_rate=1, start_count=1):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = int(fps * frame_rate)
    frame_count = 0
    image_count = start_count
    success = True

    print(f" * {video_path}")

    while success:
        success, frame = cap.read()
        if frame_count % frame_interval == 0 and success:
            frame_filename = os.path.join(output_dir, f"{image_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            image_count += 1
        frame_count += 1

    cap.release()
    return image_count

def walk_directory_and_extract_frames(input_dir, output_dir, frame_rate=1):
    image_count = 1
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(root, file)
                image_count = extract_frames(video_path, output_dir, frame_rate, image_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from videos at a specified rate.")
    parser.add_argument("-i", "--input", required=True, help="Input directory containing videos.")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save frames.")
    parser.add_argument("-r", "--rate", type=int, default=1, help="Frame extraction rate in seconds (default: 1 frame per second).")

    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output
    frame_rate = args.rate

    os.makedirs(output_directory, exist_ok=True)
    walk_directory_and_extract_frames(input_directory, output_directory, frame_rate)
