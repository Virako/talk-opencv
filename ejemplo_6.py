import cv2
import numpy as np
 
captura = cv2.VideoCapture(1)
dp = 1.5
param1 = 50
param2 = 50

valid, frame = captura.read()
if not valid:
    exit()
h, w, c = frame.shape
MIN_DIST = (h / 20)
MIN_R = int(MIN_DIST * 0.7)
MAX_R = int(MIN_DIST * 1.3)

while(1):
 
    tecla = cv2.waitKey(10) & 0xFF
    if tecla == 27:
        break

    key = chr(tecla)
    if key == 'j':
        dp += 0.1
    elif key == 'k':
        param1 += 1
    elif key == 'l':
        param2 += 1
    elif key == 'J':
        dp -= 0.1
    elif key == 'K':
        param1 -= 1
    elif key == 'L':
        param2 -= 1
    print(dp, param1, param2)

    valid, frame = captura.read()
    if not valid:
        continue
    frame =  cv2.flip(frame, 1)

    blur = cv2.medianBlur(frame, 3)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, MIN_DIST,\
            param1=param1, param2=param2, minRadius=MIN_R, maxRadius=MAX_R)

    # Examples: min, max
    cv2.circle(frame, (int(w / 2), int(h / 2)), MIN_R, (255, 0, 0), 3)
    cv2.circle(frame, (int(w / 2), int(h / 2)), MAX_R, (255, 0, 0), 3)

    if circles is not None:
        # convert the coordinates and radius to integers
        circles = np.round(circles[0, :]).astype("int")
     
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

    cv2.imshow('gray', gray)
    cv2.imshow('frame', frame)

 
cv2.destroyAllWindows()
capture.release()
