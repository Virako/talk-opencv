import cv2
import numpy as np

img1 = np.zeros((600, 800, 3), np.uint8)
img2 = cv2.imread("assets/beer-big.png")
cv2.imshow("ZERO", img1)
cv2.imshow("BEER", img2)
cv2.waitKey(0) # WAIT PRESS
cv2.destroyAllWindows()

capture = cv2.VideoCapture(1)
while 1:
    result, frame = capture.read()
    if not result:
        break

    ascii_key = cv2.waitKey(30) & 0xFF
    if ascii_key == 27: #ESC
        break

    cv2.imshow("FRAME", frame)

cv2.destroyAllWindows()
capture.release()
