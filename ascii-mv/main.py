import cv2
import os
import subprocess

from converter import frame_to_ascii, ascii_to_image


VIDEO_PATH = "examples/bad_apple.mp4"
OUTPUT_PATH = "output/ascii_mv.mp4"
TEMP_VIDEO_PATH = "output/ascii_mv_no_audio.mp4"

ASCII_WIDTH = 100

def main():

    # Open input video
    video = cv2.VideoCapture(VIDEO_PATH)

    if not video.isOpened():
        print("Cannot open video.")
        return

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print("Video opened successfully.")
    print(f"FPS: {fps}")
    print(f"Frames: {frame_count}")

    os.makedirs("output", exist_ok=True)

    # Read first frame
    success, frame = video.read()

    if not success:
        print("Cannot read video.")
        video.release()
        return

    # Convert first frame to ASCII
    ascii_lines = frame_to_ascii(
        frame,
        width=ASCII_WIDTH
    )

    output_frame = ascii_to_image(ascii_lines)
    output_height, output_width = output_frame.shape[:2]

    print(
        f"Output size: "
        f"{output_width}x{output_height}"
    )

    # Create temporary video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        TEMP_VIDEO_PATH,
        fourcc,
        fps,
        (output_width, output_height)
    )

    if not writer.isOpened():
        print("Cannot create output video.")
        video.release()
        return

    # Process first frame
    writer.write(output_frame)
    processed = 1

    # Process remaining frames
    while True:
        success, frame = video.read()
        if not success:
            break
        ascii_lines = frame_to_ascii(
            frame,
            width=ASCII_WIDTH
        )
        output_frame = ascii_to_image(ascii_lines)
        writer.write(output_frame)
        processed += 1
        if processed % 100 == 0 or processed == frame_count:
            progress = processed / frame_count * 100

            print(
                f"\rProcessing: "
                f"{processed}/{frame_count} "
                f"({progress:.1f}%)",
                end=""
            )

    video.release()
    writer.release()

    print()
    print()
    print("ASCII video generated.")
    print("Adding original audio...")

    # Add original audio using FFmpeg

    command = [
        "ffmpeg",
        "-y",
        # ASCII video
        "-i",
        TEMP_VIDEO_PATH,
        # Original video containing audio
        "-i",
        VIDEO_PATH,
        # Use video from first input
        "-map",
        "0:v:0",
        # Use audio from original video
        "-map",
        "1:a:0",
        # Copy video without re-encoding
        "-c:v",
        "copy",
        # Encode audio
        "-c:a",
        "aac",
        # Stop when the shortest stream ends
        "-shortest",
        OUTPUT_PATH
    ]
    try:
        subprocess.run(
            command,
            check=True
        )
    except FileNotFoundError:
        print("FFmpeg is not installed.")
        print("Install it with:")
        print("brew install ffmpeg")
        print(
            f"The video without audio is still available at:"
            f"\n{TEMP_VIDEO_PATH}"
        )
        return

    except subprocess.CalledProcessError:
        print()
        print("FFmpeg failed.")
        return

    # Remove temporary video
    if os.path.exists(TEMP_VIDEO_PATH):
        os.remove(TEMP_VIDEO_PATH)

    print()
    print("DONE!")
    print(f"Final video: {OUTPUT_PATH}")
    print("Original audio included.")


if __name__ == "__main__":
    main()