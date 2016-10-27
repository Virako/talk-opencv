import cv2
import numpy as np
import time
from random import randint


FPS = 50
TIMEOUT = 30 # seconds
CAMERA = 1
MARGIN = 50
SMARGIN = 25
SPAWN = 3 # seconds


def difference(img1, img2):
    res = np.zeros(img1.shape, np.uint8)
    cv2.absdiff(img1, img2, res)
    return res


def putText(img, text, position=(0, 0), color=(255, 255, 255), size=1, thinkness=1):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, position, font, size, color, thinkness, cv2.LINE_AA)


class Enemy:
    def __init__(self, img):
        h, w, c = img.shape
        self.etype = randint(0, 3)
        self.image = self.get_img()
        ih, iw, ic = self.image.shape
        self.pos_x = randint(0, w - iw)
        self.pos_y = randint(0, h - ih)
        self.is_dead = False
        self.time_start = time.time()

    def get_img(self):
        if self.etype == 0:
            filename = 'assets/cactus.png'
        else:
            filename = 'assets/beer.png'
        return cv2.imread(filename, -1)

    def get_rect(self):
        h, w, c = self.image.shape
        return ((self.pos_y, self.pos_y + h), (self.pos_x, self.pos_x + w))

    def is_touched(self, diff):
        if time.time() - self.time_start >= SPAWN:
            self.is_dead = True
            return False
        total = sum(diff[self.pos_y, self.pos_x][0:3])
        return total >= 50

    def get_score(self):
        if self.etype == 0:
            res = -5
        else:
            res = 1
        return res



scores = 0
status = 'MENU' # 'MENU', 'GAME'

cam = cv2.VideoCapture(CAMERA) # Load video
if cam.isOpened():
    HEIGHT = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    WIDTH = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
else:
    raise "Camera not found"

while 1:
    # Manage keypress
    ascii_key = cv2.waitKey(FPS) & 0xFF
    if ascii_key == 27: # ESC
        break
    elif ascii_key == 10:
        key = 'ENTER'
    else:
        key = chr(ascii_key)

    # manage status
    if status == 'MENU':
        img = np.zeros((HEIGHT, WIDTH, 4), np.uint8)
        putText(img, "ENTER FOR START", position=(MARGIN, MARGIN), size=2, thinkness=2)
        if scores:
            putText(img, "LAST SCORES: " + str(scores), (MARGIN, MARGIN * 2))
        if key == 'ENTER': # New game
            scores = 0
            status = 'GAME'
            prev_img = None
            enemy = None
            continue
    elif status == 'GAME':
        result, img = cam.read() # read frame in image
        if result:
            img = cv2.flip(img, 1)
            if prev_img == None:
                prev_img = img.copy()
                t0 = time.time()
        else:
            raise "Frame not found"

        # create/update/remove enemy
        if enemy == None:
            enemy = Enemy(img)
        diff = difference(prev_img, img)
        prev_img = img.copy()
        if enemy.is_touched(diff):
            scores += enemy.get_score()
            enemy = None
        elif enemy.is_dead:
            enemy = None
        else:
            ((y1, y2), (x1, x2)) = enemy.get_rect()
            for x in range(x1, x2):
                for y in range(y1, y2):
                    alpha = enemy.image[y - y1, x - x1]
                    if alpha[3] != 0:
                        img[y, x] = alpha[:3]


        t1 = time.time() - t0
        if TIMEOUT < t1:
            status = 'MENU'
            continue
        # Show scores and timer
        timer = TIMEOUT - t1
        height, width, channels = img.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        putText(img, str(scores), position=(int(width / 2), SMARGIN), thinkness=2)
        putText(img, "{:.2f}".format(timer), position=(int(width / 2), height - SMARGIN), thinkness=2)

    cv2.imshow("Video", img) # show image

cam.release()
cv2.destroyAllWindows()
