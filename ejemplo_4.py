import cv2
import numpy as np


def get_range_hsv(bgr_color):
    hsv = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
    hue = hsv[0][0][0]
    lower_color = np.array([hue - 10, 50, 50])
    upper_color = np.array([hue + 10, 255, 255])
    return lower_color, upper_color


capture = cv2.VideoCapture(0)
mode = ''

color = [200, 200, 200] # WHITE

while 1:
    result, frame = capture.read()
    if not result:
        break

    # BGR
    if mode == 'r': # RED
        color = [30, 30, 110]
    elif mode == 'g': # GREEN
        color = [0, 100, 0]
    elif mode == 'b': # BLUE
        color = [150, 60, 20]
    elif mode == 'y': # YELLOW
        color = [0, 255, 255]
    elif mode == 'p': # PURPLE
        color = [35, 15, 60]
    elif mode == 'w': # GRAY
        color = [120, 120, 120]

    lower_color, upper_color = get_range_hsv(color)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("orig", frame)
    cv2.imshow("hsv", hsv)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    ascii_key = cv2.waitKey(30) & 0xFF
    if ascii_key == 27:
        break
    mode = chr(ascii_key)

cv2.destroyAllWindows()
