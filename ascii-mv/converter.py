import cv2
import numpy as np

ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(frame, width=100):
    #Convert an OpenCV frame into ASCII art.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, original_width = gray.shape
    aspect_ratio = height / original_width
    new_height = int(width * aspect_ratio * 0.5)
    new_height = max(new_height, 1)
    resized = cv2.resize(
        gray,
        (width, new_height),
        interpolation=cv2.INTER_AREA
    )
    lines = []
    for row in resized:
        line = ""
        for pixel in row:
            index = int(
                pixel / 255 * (len(ASCII_CHARS) - 1)
            )
            line += ASCII_CHARS[index]
        lines.append(line)
    return lines


def ascii_to_image(ascii_lines, font_scale=0.5):
    #Convert ASCII lines into an OpenCV image.
    char_width = 10
    char_height = 18

    image_height = len(ascii_lines) * char_height
    image_width = len(ascii_lines[0]) * char_width

    image = np.zeros(
        (image_height, image_width, 3),
        dtype=np.uint8
    )
    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line):
            if char != " ":
                cv2.putText(
                    image,
                    char,
                    (
                        x * char_width,
                        (y + 1) * char_height
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA
                )

    return image