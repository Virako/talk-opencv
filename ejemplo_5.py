import cv2
import numpy as np
 
capture = cv2.VideoCapture(1)

valid, frame = capture.read()
if not valid:
    exit()
h, w, c = frame.shape
MAX_PERIMETER = h / 2
MIN_AREA = (h / 20) ** 2
canny1 = 30
canny2 = 30
 
while(1):

    valid, frame = capture.read()
    if not valid:
        continue
    frame =  cv2.flip(frame, 1)
 
    tecla = cv2.waitKey(10) & 0xFF
    if tecla == 27:
        break
    key = chr(tecla)
    if key == 'j':
        canny1 -= 1
    elif key == 'k':
        canny1 += 1
    elif key == 'J':
        canny2 -= 1
    elif key == 'K':
        canny2 += 1
    print(canny1, canny2, MIN_AREA)

    canny = cv2.Canny(frame, canny1, canny2)
    img, contours, hier = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.1*cv2.arcLength(contour, True), True)
        area = cv2.contourArea(approx)
        lenght = cv2.arcLength(approx, True)
        # TODO: without restriction
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
        if len(approx) == 4 and area > MIN_AREA and lenght < MAX_PERIMETER:
            cv2.drawContours(frame, [approx], 0, (0, 0, 255), 2)

    cv2.imshow('canny', canny)
    cv2.imshow('frame', frame)
 
cv2.destroyAllWindows()
capture.release()
