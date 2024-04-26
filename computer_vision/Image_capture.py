import cv2 as cv
import os


URL = "http://192.168.2.191:81/stream"

cap = cv.VideoCapture(URL)

folder_name = "update_calibration_images"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Initialize frame count and image count
frame_count = 0
image_count = 0

# Number of frames to skip before capturing an image
capture_interval = 30

while True:

    if cap.isOpened():
        ret, frame = cap.read()
    
    # Check if frame is valid
        if frame is not None:
            frame_count += 1
            
            # Save every capture_interval-th frame as an image
            if frame_count == capture_interval:
                image_count += 1
                file_path = os.path.join(folder_name, f"cal_image_{image_count}.jpg")
                cv.imwrite(file_path, frame)
                frame_count = 0
                
            text = f"Number of images taken: {image_count}"
            text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
            # Calculate the position of the text
            text_x = frame.shape[1] - text_size[0] - 20  # Right margin: 20 pixels
            text_y = frame.shape[0] - 20  # Bottom margin: 20 pixels
            cv.putText(frame, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display frame
            cv.imshow("Live Cam test", frame)
            
            # Check for key press to exit
            key = cv.waitKey(5)
            if key == ord("q"):
                break
        else:
            print("Error: Unable to decode frame.")
            break
    else:
        print("Error")
# Release resources
cv.destroyAllWindows()
