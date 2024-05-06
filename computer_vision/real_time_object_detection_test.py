import cv2 as cv
from cv2 import aruco
import numpy as np
from ultralytics import YOLO


# Load camera calibration data
calib_data_path = "MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

# Marker size in centimeters (measure your printed marker size)
MARKER_SIZE = 1.2  

# ArUco marker dictionary and detector parameters
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

# YOLO model for object detection
model = YOLO("yolo-Weights/yolov8n.pt")

# Object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# Video stream URL
URL = "http://192.168.2.191:81/stream"
cap = cv.VideoCapture(URL)

while True:
    # Read frame from video stream
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect ArUco markers
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, marker_dict)
    
    if marker_corners:
        # Estimate pose for each detected marker
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cam_mat, dist_coef)
        total_markers = range(0, marker_IDs.size)
        
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
    
            # Calculating the distance
            distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)
            # Draw the pose of the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(frame, f"id: {ids[0]} Dist: {round(distance, 2)}", top_right, cv.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(frame, f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ", bottom_right, cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2, cv.LINE_AA)

    # Perform object detection using YOLO
    results = model(frame, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Extract box coordinates and class ID
            x1, y1, x2, y2 = box.xyxy[0]
            cls = int(box.cls[0])
            confidence = box.conf[0]  # Use 'conf' attribute instead of 'score'
            
            # Draw bounding box with rounded corners
            cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2, cv.LINE_AA)
            
            # Prepare label text
            label = f'{classNames[cls]}: {confidence:.2f}'
            
            # Calculate label position
            (label_width, label_height), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            label_x = int(x1)
            label_y = int(y1) - 5
            
            # Draw label background
            cv.rectangle(frame, (label_x, label_y - label_height), (label_x + label_width, label_y), (255, 0, 255), -1)
            
            # Draw label text
            cv.putText(frame, label, (label_x, label_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)



    # Display the annotated frame
    cv.imshow("Camera display", frame)
    if cv.waitKey(1) == ord("q"):
        break

# Release video capture and close all windows
cap.release()
cv.destroyAllWindows()
