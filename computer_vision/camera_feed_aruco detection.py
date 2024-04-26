import cv2 as cv
import numpy as np

URL = "http://192.168.2.191:81/stream"

cap = cv.VideoCapture(URL)

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_50)

while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from the stream")
            break
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray, aruco_dict)
    
    if ids is not None:
        cv.aruco.drawDetectedMarkers(frame, corners, ids)
    
    cv.imshow("Live Cam test", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
    
cv.destroyAllWindows()
