import cv2
import numpy as np
from myutils import get_colors


def get_range_hsv(bgr_color):
    hsv = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
    hue = hsv[0][0][0]
    lower_color = np.array([hue - 10, 50, 50])
    upper_color = np.array([hue + 10, 255, 255])
    return lower_color, upper_color


while 1:
    colors = get_colors()
    if len(colors) > 0:
        break

color = colors[0]
capture = cv2.VideoCapture(1)

while 1:
    result, frame = capture.read()
    if not result:
        break
    frame = cv2.flip(frame, 1)

    ascii_key = cv2.waitKey(30) & 0xFF
    if ascii_key == 27:
        break
    mode = chr(ascii_key)

    # BGR
    if mode.isdigit():
        color = colors[int(mode) % len(colors)]

    lower_color, upper_color = get_range_hsv(color)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)

    i = 0
    for c in colors:
        cv2.rectangle(frame, (i*20, 0), ((i+1)*20, 20), c, -1)
        i += 1

    #cv2.imshow("hsv", hsv)
    cv2.imshow("orig", frame)
    cv2.imshow("mask", mask)

cv2.destroyAllWindows()
capture.release()
