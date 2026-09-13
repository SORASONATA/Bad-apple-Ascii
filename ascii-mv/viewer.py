import cv2

VIDEO_PATH = "output/ascii_mv.mp4"

def main():
    video = cv2.VideoCapture(VIDEO_PATH)

    if not video.isOpened():
        print("Cannot open output video.")
        return

    print("▶ Playing:", VIDEO_PATH)
    print("Press Q to quit.")

    while True:
        success, frame = video.read()

        if not success:
            break

        cv2.imshow("ASCII MV", frame)

        # 24 FPS ≈ 41.67 ms per frame
        key = cv2.waitKey(42) & 0xFF

        if key == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()