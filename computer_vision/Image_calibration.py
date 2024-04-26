import glob
import cv2 as cv
import numpy as np

chessboard_width = 8
chessboard_height = 5



#chessboard_square_size = 20

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboard_width * chessboard_height, 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_width, 0:chessboard_height].T.reshape (-1,2) #* chessboard_square_size


objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane


images = glob.glob('./update_calibration_images/*.jpg')  # Change this to the directory containing your images


for fname in images:
    
  
   img = cv.imread(fname)
   
   gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


   ret, corners = cv.findChessboardCorners(gray, (5,8), None)

   if ret == True:
        objpoints.append(objp)
        
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        
        imgpoints.append(corners2)


        cv.drawChessboardCorners(img, (5,8), corners2, ret)
        cv.imshow('Calibration images', img)
        cv.waitKey(500)  
    
  
cv.destroyAllWindows()
print("Drawing done! Waiting for the results!")

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

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
