import cv2
import urllib.request
import numpy as np


url = "http://192.168.2.191/capture?"

# Initialize frame count and image count
frame_count = 0
image_count = 0

# Number of frames to skip before capturing an image
capture_interval = 31

while True:
    # Fetch image data from URL
    img_response = urllib.request.urlopen(url)
    img_array = np.array(bytearray(img_response.read()), dtype=np.uint8)
    
    # Decode image array into OpenCV image format
    frame = cv2.imdecode(img_array, -1)
    
    # Check if frame is valid
    if frame is not None:
        frame_count += 1
        
        # Save every capture_interval-th frame as an image
        if frame_count == capture_interval:
            image_count += 1
            cv2.imwrite(f"cal_image_{image_count}.jpg", frame)
            frame_count = 0
        
        # Display frame
        cv2.imshow("Live Cam test", frame)
        
        # Check for key press to exit
        key = cv2.waitKey(5)
        if key == ord("q"):
            break
    else:
        print("Error: Unable to decode frame.")
        break

# Release resources
cv2.destroyAllWindows()
