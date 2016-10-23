import cv2
import numpy as np
from random import randint


def putText(img, text, position=(0, 0), color=(0, 0, 0), size=1, thinkness=3):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, position, font, size, color, thinkness, cv2.LINE_AA)


SIZE = (800, 600)
#SIZE = (1920, 1080)
FPS = 20
SPAWN = 3 # seconds
RED = (0, 0, 255)
THRESHOLD_DIFF = 50

capture = cv2.VideoCapture(1)
result, frame = capture.read()
if not result:
    raise "Not frame found"
prev_img = frame.copy()
w, h, c = prev_img.shape
enemy_timer = 0
scores = 0
max_scores = 0

while 1:
    result, frame = capture.read()
    if not result:
        break
    frame =  cv2.flip(frame, 1)

    if not enemy_timer: # enemy + timer + size
        enemy_timer = 1
        pos_x = randint(0, w - 1)
        pos_y = randint(0, h - 1)
        continue
    else:
        enemy_timer += 1
        if enemy_timer >= SPAWN * FPS:
            enemy_timer = 0
            scores = 0
            continue
        diff = np.zeros(frame.shape, np.uint8)
        diff = cv2.absdiff(prev_img, frame, diff)
        total = sum(diff[pos_x, pos_y][0:3])
        if total >= THRESHOLD_DIFF:
            scores += 1
            if max_scores < scores:
                max_scores = scores
            enemy_timer = 0

    prev_img = frame.copy()

    text_scores = "Scores: {0}   BEST: {1}".format(scores, max_scores)
    putText(frame, text_scores, position=(int(w / 3), 25))
    cv2.circle(frame, (pos_y, pos_x), 15, RED, enemy_timer)

    frame = cv2.resize(frame, SIZE, interpolation=cv2.INTER_CUBIC)
    cv2.imshow("game", frame)

    ascii_key = cv2.waitKey(FPS) & 0xFF
    if ascii_key == 27:
        break

cv2.destroyAllWindows()
capture.release()
