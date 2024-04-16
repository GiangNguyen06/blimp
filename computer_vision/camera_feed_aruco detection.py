import cv2
import urllib.request
import numpy as np
import cv2.aruco as aruco


url = "http://192.168.2.191/capture?"
feed = cv2.VideoCapture(url)

aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)

while True:
    img_response = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_response.read()), dtype = np.uint8) 
    
    frame = cv2.imdecode (imgnp, -1)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict)
    
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
    
    cv2.imshow("Live Cam test", frame)
    key = cv2.waitKey(5)
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()