import cv2
import requests
import argparse
import os
from inference_sdk import InferenceHTTPClient


def parse_args():
    parser = argparse.ArgumentParser(description="Process video and extract insights")
    parser.add_argument("--dataset_id", help="Dataset ID (required)")
    parser.add_argument("--version_id", default="1", help="Version ID (default: 1)")
    parser.add_argument("--video_path", help="Path to the video (required)")
    parser.add_argument("--interval_seconds", type=int, default=5, help="Interval in seconds)")
    parser.add_argument("--max_samples", type=int, default=10, help="Hack: set max samples since I don't have a GPU, set to 0 to disable")
    return parser.parse_args()


def extract_frames(video_path, interval_seconds, max_samples):
    cap = cv2.VideoCapture(video_path)
    frames = []
    timestamps = []
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    interval_frames = (fps * interval_seconds)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % interval_frames == 0:
            print(f'Processing frame {len(frames)}')
            frames.append(frame)
            timestamps.append(frame_count / fps)
        frame_count += 1

        if max_samples > 0 and len(frames) >= max_samples:
            break

    cap.release()
    return frames, timestamps


def fetch_predictions(base_url, frames, timestamps, dataset_id, version_id, api_key, confidence=0.5):
    headers = {"Content-Type": "application/json"}
    CLIENT = InferenceHTTPClient(
        api_url = "http://localhost:9001",
        api_key = api_key
    )

    rows = []
    for idx, frame in enumerate(frames):

        res = CLIENT.run_workflow(
            workspace_name="workspace-vxpni",
            workflow_id="detect-and-classify",

            images={ "image": frame, },
        )

        res_predictions = res[0]["detection"]['predictions']

        row = {
            "timestamp": f"{int(timestamps[idx] // 60)}:{int(timestamps[idx] % 60):02}",
            "preds": [],
         }

        for pred in res_predictions:
            row["preds"].append({
                "class": pred["class"],
                "confidence": pred["confidence"],
                "x": pred["x"],
                "y": pred["y"],
                "width": pred["width"],
                "height": pred["height"],
            })

        rows.append(row)

    return rows

def main():
    args = parse_args()
    base_url = "http://localhost:9001"
    video_path = args.video_path
    dataset_id = args.dataset_id
    version_id = args.version_id
    api_key = "RUHhY3ldcnTXhaA5DY7m"  # TODO(kv) Crappy!
    interval_seconds = args.interval_seconds

    frames, timestamps = extract_frames(video_path, interval_seconds, args.max_samples)

    df = fetch_predictions(base_url, frames, timestamps, dataset_id, version_id, api_key)

    # Output
    print("-----------------------")
    print("Output")
    print("")
    for row in df:
        print(row)

if __name__ == "__main__":
    main()
