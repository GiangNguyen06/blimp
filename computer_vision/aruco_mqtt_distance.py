import cv2 as cv

import numpy as np
import cv2.aruco as aruco
from paho.mqtt import client as mqtt_client
import random
import json
import time

broker = 'localhost'
port = 1883
topic = "aruco"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# load in the calibration data
calib_data_path = "MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 1.2  # centimeters (measure your printed marker size)

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

param_markers = aruco.DetectorParameters()

URL = "http://192.168.2.191:81/stream"

cap = cv.VideoCapture(URL)



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect to return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def ensure_mqtt_client(client):
    if client is None or not client.is_connected():
        client = connect_mqtt()
        client.loop_start()
        print("MQTT client connected")
    return client


def publish(client, message):
    msg = json.dumps(message)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent '{msg}' to '{topic}'")



def run():
    
    client = connect_mqtt() 
    
    start_time = time.time()
    frame_count = 0
    
    while True:
       
        
        if cap.isOpened():
            ret, frame = cap.read()
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, marker_dict)
                                    
            if marker_corners:
                rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                    marker_corners, MARKER_SIZE, cam_mat, dist_coef
                )
                total_markers = range(0, marker_IDs.size)
                for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                    cv.polylines(
                        frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                    )
                    corners = corners.reshape(4, 2)
                    corners = corners.astype(int)
                    top_right = corners[0].ravel()
                    top_left = corners[1].ravel()
                    bottom_right = corners[2].ravel()
                    bottom_left = corners[3].ravel()
            
                    # Calculating the distance
                    distance = np.sqrt(
                        tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
                    )
                    # Draw the pose of the marker
                    point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
                    cv.putText(
                        frame,
                        f"id: {ids[0]} Dist: {round(distance, 2)}",
                        top_right,
                        cv.FONT_HERSHEY_PLAIN,
                        1.3,
                        (0, 0, 255),
                        2,
                        cv.LINE_AA,
                    )
                    cv.putText(
                        frame,
                        f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                        bottom_right,
                        cv.FONT_HERSHEY_PLAIN,
                        1.0,
                        (0, 0, 255),
                        2,
                        cv.LINE_AA,
                    )
                    
                    print(f"Detected ArUco marker with ID: {ids[0]} and the distance is {distance}!")
                
                for marker_id in marker_IDs:
                   message = {}
                   if marker_id == 0:
                       message["direction"] = "go up"
                   elif marker_id == 1:
                       message["direction"] = "go down"
                   else:
                       message["direction"] = "unknown direction"
                 
                   publish(client, message)
                   
        cv.putText(frame, f"FPS: {frame_count / (time.time() - start_time):.2f}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)
      
        frame_count += 1
        
        cv.imshow("Camera display", frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break

    cv.destroyAllWindows()
    
if __name__ == '__main__':
     run()   
    