#--------------------------------------------------------------------
# Implements multiple objects motion prediction using Kalman Filter
#
# Author: https://github.com/SriramEmarose/Multi-Object-Motion-Prediction-With-KalmanFilter
#
#--------------------------------------------------------------------
import cv2
import numpy as np
import sys

sys.path.append('tools')
from drawopencv import DrawingOpencv

MAX_OBJECTS_TO_TRACK = 10


class SingleObjectTracking:
    """
    Tracking yapildigi siniftir.
    """

    def __init__(self, frame, tracker_type='MEDIANFLOW', box_selected=None):
        """
        Parameters
        -----------
        tracker_type: string -
        frame: 
        Returns
        -----------
        None:
        """
        if tracker_type == 'BOOSTING':
            self.tracker =  cv2.legacy.TrackerBoosting_create()
        if tracker_type == 'MIL':
            self.tracker =  cv2.legacy.TrackerMIL_create()
        if tracker_type == 'KCF':
            self.tracker = cv2.legacy.TrackerKCF_create()
        if tracker_type == 'TLD':
            self.tracker =cv2.legacy.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.legacy.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            self.tracker = cv2.legacy.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            self.tracker =cv2.legacy.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            self.tracker =  cv2.legacy.TrackerCSRT_create()

        self.tracker_state = self.tracker.init(frame, box_selected)


    def update_frame(self, frame):
        """
        Parameters
        -----------
        frame: image - 
        frame_orj: image -
        frame_number: int -
        Returns
        ------------
        return: Boolean
        """
        org_frame = frame

        success, box = self.tracker.update(frame)

        size_temp = len(box)

        if size_temp == 0:
            success = False

        #DrawingOpencv.opencv_put_Text(frame=frame, string_text=string_text)
        coords = []

        if success:
            (x, y, w, h) = [int(v) for v in box]
            DrawingOpencv.drawing_rectangle(frame=frame, class_id="1", x1_y1=(x, y), x2_y2=(x + w, y + h), color=DrawingOpencv.color_green)
        
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box_image = org_frame[y:y + h, x:x + w]
            #cv2.imshow("en sonki takip edebildigi box_image", cv2.cvtColor(box_image, cv2.COLOR_RGB2BGR))
            #if self.last_success_boxes is None:
            self.last_success_boxes=box_image
            #cv2.imshow("self.last_success_boxes", cv2.cvtColor(self.last_success_boxes, cv2.COLOR_RGB2BGR))
            center_x = int((x+x + w)/2)
            center_y = int((y+y + h)/2)

            coords.append((center_x,center_y))

            return True, coords 
        else:
            return False, coords 



# Instantiate OCV kalman filter
class KalmanFilter:

    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

    def Estimate(self, coordX, coordY):
        ''' This function estimates the position of the object'''
        measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        return predicted



#Performs required image processing to get ball coordinated in the video
class ProcessImage:

    def __init__(self):
        self.selecetROI = False

    def DetectObject(self):

        ball_or_drone = True

        if ball_or_drone:
            vid = cv2.VideoCapture("_videos/balls.mp4")

            if(vid.isOpened() == False):
                print('Cannot open input video')
                return

            width = int(vid.get(3))
            height = int(vid.get(4))

            # Create Kalman Filter Object
            kfObjs = []
            predictedCoords = []
            for i in range(MAX_OBJECTS_TO_TRACK):
                kfObjs.append(KalmanFilter())
                predictedCoords.append(np.zeros((2, 1), np.float32))

            while(vid.isOpened()):
                rc, frame = vid.read()

                if(rc == True):

                    coords = self.DetectBall(frame)

                    for i in range(len(coords)):
                        if(i > MAX_OBJECTS_TO_TRACK):
                            break

                        #print (' circle ',i, ' ', coords[i][0], ' ', coords[i][1])
                        predictedCoords[i] = kfObjs[i].Estimate(coords[i][0], coords[i][1])
                        frame = self.DrawPredictions(frame, coords[i][0], coords[i][1], predictedCoords[i])

                    cv2.imshow('Input', frame)

                    if (cv2.waitKey(300) & 0xFF == ord('q')):
                        break

                else:
                    break

        else:
            vid = cv2.VideoCapture("_videos/balls.mp4")

            if(vid.isOpened() == False):
                print('Cannot open input video')
                return

            width = 1280
            height = 720

            # Create Kalman Filter Object
            kfObjs = []
            predictedCoords = []

            kfObjs.append(KalmanFilter())
            predictedCoords.append(np.zeros((2, 1), np.float32))

            while(vid.isOpened()):
                rc, frame = vid.read()

                if(rc == True):
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    frame= cv2.resize(frame, (width, height))

                    if self.selecetROI == False:
                        box = cv2.selectROI("Kalman filters Estimation",  cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), fromCenter=False)
                        if box[0] == 0 and box[1] == 0 and box[2] == 0 and box[3] == 0:
                            self.selecetROI = False
                        else:
                            self.selecetROI = True
                            single_object_tracking = SingleObjectTracking(frame=frame,box_selected=box)

                    if self.selecetROI == True:
                        return_tracking, coords = single_object_tracking.update_frame(frame=frame)
                        if return_tracking == False:
                            self.selecetROI=False
                        else:
                            coords = coords
                            predictedCoords[0] = kfObjs[0].Estimate(coords[0][0], coords[0][1])
                            frame = self.DrawPredictions(frame, coords[0][0], coords[0][1], predictedCoords[0])

                        cv2.imshow("Kalman filters Estimation", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

                        if (cv2.waitKey(300) & 0xFF == ord('q')):
                            break

                else:
                    break


        vid.release()
        cv2.destroyAllWindows()

    # Segment the green ball in a given frame
    def DetectBall(self, frame):

        frameGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frameGrey = cv2.blur(frameGrey, (3, 3))

        circles = cv2.HoughCircles(frameGrey, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 30, minRadius = 1, maxRadius = 40)
        coords = []

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                coords.append((x,y))
            return coords

        return coords

    def DrawPredictions(self, frame, ballX, ballY, predictedCoords):
        # Draw Actual coords from segmentation
        cv2.circle(frame, (int(ballX), int(ballY)), 20, DrawingOpencv.color_green, 2, 8)
        cv2.line(frame, (int(ballX), int(ballY + 20)), (int(ballX + 50), int(ballY + 20)), DrawingOpencv.color_green, 2, 8)
        cv2.putText(frame, "Actual", (int(ballX + 50), int(ballY + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, DrawingOpencv.color_green)

        # Draw Kalman Filter Predicted output
        cv2.circle(frame, (int(predictedCoords[0]), int(predictedCoords[1])), 20, DrawingOpencv.color_red, 2, 8)
        cv2.line(frame, (int(predictedCoords[0]) + 16, int(predictedCoords[1]) - 15), (int(predictedCoords[0]) + 50, int(predictedCoords[1]) - 30), DrawingOpencv.color_red, 2, 8)
        cv2.putText(frame, "Predicted", (int(predictedCoords[0] + 50), int(predictedCoords[1] - 30)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, DrawingOpencv.color_red)
 

        return frame



#Main Function
def main():

    processImg = ProcessImage()
    processImg.DetectObject()


if __name__ == "__main__":
    main()

print('Program Completed!')