import cv2
import numpy as np
import glob

chessboard_width = 8
chessboard_height = 5



#chessboard_square_size = 20

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboard_width * chessboard_height, 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_width, 0:chessboard_height].T.reshape (-1,2) #* chessboard_square_size


objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane


images = glob.glob('./calibration_images/*.jpg')  # Change this to the directory containing your images


for fname in images:
    
  
   img = cv2.imread(fname)
   
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


   ret, corners = cv2.findChessboardCorners(gray, (5,8), None)

   if ret == True:
        objpoints.append(objp)
        
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        
        imgpoints.append(corners2)


        cv2.drawChessboardCorners(img, (5,8), corners2, ret)
        cv2.imshow('Calibration images', img)
        cv2.waitKey(500)  
    
  
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Calibration Matrix: ")
print(mtx)
print("Disortion: ", dist )

print("dumping the data into one files using numpy ")
np.savez(
    "MultiMatrix",
    camMatrix=mtx,
    distCoef=dist,
    rVector=rvecs,
    tVector=tvecs,
)

print("-------------------------------------------")

print("loading data \n \n \n")

data = np.load("MultiMatrix.npz")

camMatrix = data["camMatrix"]
distCof = data["distCoef"]
rVector = data["rVector"]
tVector = data["tVector"]

print("loaded calibration data successfully")