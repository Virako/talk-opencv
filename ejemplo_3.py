import cv2
import numpy as np
from random import randint


def putText(img, text, position=(0, 0), color=(0, 0, 0), size=1, thinkness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, position, font, size, color, thinkness, cv2.LINE_AA)


FPS = 20
SPAWN = 3 # seconds
RED = (0, 0, 255)

capture = cv2.VideoCapture(0)
result, frame = capture.read()
if not result:
    raise "Not frame found"
prev_img = frame.copy()
w, h, c = prev_img.shape
mode = ''
enemy = 0
scores = 0
max_scores = 0

while 1:
    result, frame = capture.read()
    if not result:
        break
    frame =  cv2.flip(frame, 1)

    res = frame.copy()
    if not enemy:
        enemy = True
        pos_x = randint(0, w - 1)
        pos_y = randint(0, h - 1)
        continue
    else:
        enemy += 1
        if enemy >= SPAWN * FPS:
            enemy = False
            scores = 0
            continue
        diff = np.zeros(frame.shape, np.uint8)
        diff = cv2.absdiff(prev_img, frame, diff)
        total = sum(diff[pos_x, pos_y][0:3])
        if total >= 50:
            cv2.circle(res, (pos_y, pos_x), 15, RED, cv2.FILLED)
            scores += 1
            if max_scores < scores:
                max_scores = scores
            enemy = False
    text_scores = "Scores: {0}   BEST: {1}".format(scores, max_scores)
    putText(res, text_scores, position=(int(w / 3), 25), thinkness=3)
    cv2.circle(res, (pos_y, pos_x), 15, RED, 5)

    prev_img = frame.copy()
    cv2.imshow("game", res)

    ascii_key = cv2.waitKey(FPS) & 0xFF
    if ascii_key == 27:
        break

capture.release()
cv2.destroyAllWindows()
