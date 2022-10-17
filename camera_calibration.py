import numpy as np
import cv2
import glob
import argparse

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# xx deneme 

def calibrate(dirpath, image_format, width=9, height=6):
    """ Apply camera calibration operation for images in the given directory path. """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)

    objp = np.zeros((1, width*height, 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    if dirpath[-1:] == '/':
        dirpath = dirpath[:-1]

    images = glob.glob(dirpath+'/' + '*.' + image_format)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return [ret, mtx, dist, rvecs, tvecs]
def save_coefficients(mtx, dist, path):
    """ Save the camera matrix and the distortion coefficients to given path/file. """
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()


def showUndistortion(dirpath, image_format,path, width=9, height=6):

    images = glob.glob(dirpath+'/' + '*.' + image_format)

    img = cv2.imread(images[0])
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, (width, height), None)
    
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret == True:
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (width, height), corners2,ret)
    
    cv2.imshow('original img', img)
    cv2.waitKey(0)

    
    # Refining the camera matrix using parameters obtained by calibration
    h,w = img.shape[:2]

    mtx, dist = load_coefficients(path)

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    method1_method2 = True
    # Method 1 to undistort the image

    if method1_method2:
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    else:
        # Method 2 to undistort the image
        mapx,mapy=cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

    # Displaying the undistorted image
    cv2.imshow("undistorted image",dst)
    cv2.waitKey(0)

def load_coefficients(path):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera calibration')
    parser.add_argument('--image_dir',  type=str,  help='image directory path',default= "./_images_must/camera_calibration/")
    parser.add_argument('--image_format', default="jpg",type=str,  help='image format, png/jpg')
    parser.add_argument('--width', default= 9,type=int, help='chessboard width size, default is 9')
    parser.add_argument('--height', default= 6,type=int, help='chessboard height size, default is 6')
    parser.add_argument('--save_file', default= "./_outputs/camera.yml",type=str, help='YML file to save calibration matrices')
    args = parser.parse_args()

    save_or_load = True

    if save_or_load:
        ret, mtx, dist, rvecs, tvecs = calibrate(args.image_dir,  args.image_format, args.width, args.height)
        save_coefficients(mtx, dist, args.save_file)
        print("Calibration is finished. RMS: ", ret)
    else:
        showUndistortion(args.image_dir,  args.image_format,args.save_file, args.width, args.height)


