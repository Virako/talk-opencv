import cv2
import numpy as np

print(""" HELP:
        p --> paint
        f -> flip hor
        F -> flip ver
        c --> gray color
        C --> hsv color
        d --> diff 
        r --> restart beer image
        b --> blur
        k --> canny
        t --> threshold""")

mode = None
img = cv2.imread("assets/beer-big.png")

while 1:
    if mode == 'p':
        img = np.zeros((600, 800, 3), np.uint8)
        WHITE = (255, 255, 255)
        cv2.circle(img, (50, 50), 25, WHITE, cv2.FILLED)
        cv2.circle(img, (300, 300), 50, WHITE, 3)
        cv2.rectangle(img,(100,100),(200,200), WHITE, 3)
    elif mode == 'f':
        img = cv2.flip(img, 1)
    elif mode == 'F':
        img = cv2.flip(img, 0)
    elif mode == 'c':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif mode == 'C':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif mode == 'd':
        aux_img = cv2.flip(img, 0)
        diff = img.copy()
        cv2.absdiff(aux_img, img, diff)
        cv2.imshow("prev", diff)
    elif mode == 'r':
        img = cv2.imread("assets/beer-big.png")
        cv2.destroyAllWindows()
    elif mode == 'b':
        img = cv2.blur(img, (5, 5))
    elif mode == 'k':
        img = cv2.Canny(img, 1, 2)
    elif mode == 't':
        img = cv2.imread("assets/beers.jpg")
        aux_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, orange1 = cv2.threshold(aux_img, 50, 255, cv2.THRESH_BINARY)
        ret, orange2 = cv2.threshold(aux_img, 150, 255, cv2.THRESH_BINARY)
        cv2.imshow("orange1", orange1)
        cv2.imshow("orange2", orange2)

    cv2.imshow("current", img)

    ascii_key = cv2.waitKey(0) & 0xFF
    if ascii_key == 27:
        break
    mode = chr(ascii_key)

cv2.destroyAllWindows()
