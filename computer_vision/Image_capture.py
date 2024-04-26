import cv2 as cv
import urllib.request
import numpy as np


URL = "http://192.168.2.191:81/stream"

cap = cv.VideoCapture(URL)

# Initialize frame count and image count
frame_count = 0
image_count = 0

# Number of frames to skip before capturing an image
capture_interval = 31

while True:
    # Fetch image data from URL
    if cap.isOpened():
        ret, frame = cap.read()
    
    # Check if frame is valid
        if frame is not None:
            frame_count += 1
            
            # Save every capture_interval-th frame as an image
            if frame_count == capture_interval:
                image_count += 1
                cv.imwrite(f"cal_image_{image_count}.jpg", frame)
                frame_count = 0
            
            # Display frame
            cv.imshow("Live Cam test", frame)
            
            # Check for key press to exit
            key = cv.waitKey(5)
            if key == ord("q"):
                break
        else:
            print("Error: Unable to decode frame.")
            break

# Release resources
cv.destroyAllWindows()
