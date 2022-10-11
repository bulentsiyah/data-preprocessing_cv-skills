import warnings
warnings.filterwarnings("ignore")
from turtle import width
from enum import Enum
import os
import numpy as np
import cv2
import time
import argparse

import sys
sys.path.append('tools')
from configmanager import ConfigurationManager
from videocapture import VideoCapture
from drawopencv import DrawingOpencv

class TrackerTypes(Enum):
    BOOSTING = 0,
    MIL = 1,
    KCF = 2,
    TLD = 3,
    MEDIANFLOW = 4,
    GOTURN = 5,
    MOSSE = 6,
    CSRT = 7,


class SingleObjectTracking:
    """
    Tracking yapildigi siniftir.
    Etiketlenen framelerin ve txtlerin yazildigi kisimdir.
    classes.txt bu sinifta yaratilir ve kontrol edilir.
    """

    def __init__(self, tracker_type=TrackerTypes.KCF.name, video_id="none_name"):
        """
        Parameters
        -----------
        tracker_type: Enum -
        video_id: string - secili videonun dosya adi

        Returns
        -----------
        None:
        """

        self.tracker_type = tracker_type
        self.selected_tracker(self.tracker_type)
        self.last_success_boxes = None

        self.configurationManager = ConfigurationManager()

        self.video_id = video_id

        self.class_id = int(self.configurationManager.config_readable['selected_class_id'])

    
    def selected_tracker(self, tracker_type):
        """
        Parameters
        -----------
        tracker_type: Enum - 

        Returns
        -----------
        None:
        """

        if tracker_type == 'BOOSTING':
            self.tracker = tracker = cv2.legacy.TrackerBoosting_create()
        if tracker_type == 'MIL':
            self.tracker = tracker = cv2.legacy.TrackerMIL_create()
        if tracker_type == 'KCF':
            self.tracker =tracker = cv2.legacy.TrackerKCF_create()
        if tracker_type == 'TLD':
            self.tracker =tracker = cv2.legacy.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            self.tracker =tracker = cv2.legacy.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            self.tracker =tracker = cv2.legacy.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            self.tracker =tracker = cv2.legacy.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            self.tracker = tracker = cv2.legacy.TrackerCSRT_create()

    
    def init_box_selected(self, frame, box_selected=None):
        """
        Parameters
        -----------
        frame: image -
        box_selected: tuple -

        Returns
        -----------
        None:
        """

        if box_selected is not None:
            tracker_state = self.tracker.init(frame, box_selected)

    def update_frame(self, frame, frame_orj, frame_number, selected_class_id):
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
        org_frame = frame_orj

        success, box = self.tracker.update(frame)

        size_temp = len(box)

        if size_temp == 0:
            success = False

        info = [("Tracker", self.tracker_type),
                ("Success", "Yes" if success else "No")]
        info = [("Success", "Yes" if success else "No")]

        string_text = ""

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            string_text = string_text + text + " "

        #DrawingOpencv.opencv_put_Text(frame=frame, string_text=string_text)

        if success:
            (x, y, w, h) = [int(v) for v in box]
            DrawingOpencv.drawing_rectangle(frame=frame, class_id=self.class_id, x1_y1=(x, y), x2_y2=(x + w, y + h), color=DrawingOpencv.color_green)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box_image = org_frame[y:y + h, x:x + w]
            self.yolo_format(box=box, frame=org_frame, frame_number=frame_number, selected_class_id=selected_class_id)
            #cv2.imshow("en sonki takip edebildigi box_image", cv2.cvtColor(box_image, cv2.COLOR_RGB2BGR))
            #if self.last_success_boxes is None:
            self.last_success_boxes=box_image
            #cv2.imshow("self.last_success_boxes", cv2.cvtColor(self.last_success_boxes, cv2.COLOR_RGB2BGR))
            return True
        else:
            return False

        
    def yolo_format(self, box, frame, frame_number, selected_class_id):
        """
        Parameters
        -----------
        frame: image
        box: tuple - (x, y, w, h)
        frame_number: int -
        selected_class_id: int -

        Returns
        -----------
        None:
        """

        #class_id x y width height
        (x, y, w, h) = [int(v) for v in box]

        height, width, c = frame.shape

        tt_x = (x + (x+w))/2
        tt_y = (y +(y+h))/2
        yolo_x = format(tt_x/width, '.6f')
        yolo_y = format(tt_y/height, '.6f')

        yolo_w = format(w/width, '.6f')
        yolo_h = format(h/height, '.6f')

        yolo_line = '{0} {1} {2} {3} {4}'.format(selected_class_id, yolo_x, yolo_y, yolo_w, yolo_h)

        directory = self.video_id
        parent_dir = os.path.dirname(sys.argv[0]) + self.configurationManager.config_readable['video_save_path_folder']
        path = os.path.join(parent_dir, directory)
        if os.path.exists(path)==False:
            os.mkdir(path)
        
        picture_name = path + "/" + str(frame_number) + "__" + str(self.video_id) + ".png"
        cv2.imwrite(picture_name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        text_name = path + "/" + str(frame_number) + "__" + str(self.video_id) + ".txt"
        if os.path.exists(text_name)==False:
            file = open(text_name, "w")
            file.close()

        infile = open(text_name, 'r').readlines()
        with open(text_name, 'w') as outfile:
            for index, line in enumerate(infile):
                try:
                    index = int(line.split(" ")[0])
                    outfile.write(line)
                except:
                    pass

            outfile.write(yolo_line+"\n")


        # Region classes.txt'nin yazildigi ve duzenlendigi yer       
        text_name = path + "/" + "classes.txt"
        if os.path.exists(text_name)==False:
            file = open(text_name, 'w')
            file.close()
        
        infile = open(text_name, 'r').readlines()
        with open(text_name, 'w') as outfile:
            last_class_id = -1
            for index,line in enumerate(infile):
                try:
                    last_class_id = int(line)
                except:
                    pass
        
            if selected_class_id > last_class_id:
                last_class_id = selected_class_id
            for class_id in range(0, last_class_id+1):
                if class_id != last_class_id:
                    outfile.write(str(class_id)+"\n")
                else:
                    outfile.write(str(class_id))

        self.configurationManager.set_split_max_class_count(split_max_class_count=str(class_id))
        # End Region


        self.configurationManager.set_last_frame(last_frame=frame_number)






def main():
    """
    İslemin basladigi ana siniftir.                  
    """

    while True:
        
        video_capture.get_image()

        if (video_capture.ret == False):
            break
 
        video_capture.save_pure_frame_save(video_capture.img)

        # Region Context
        if (video_capture.selecetROI==True):
            if video_capture.box is not None:
                single_object_tracking = SingleObjectTracking(TrackerTypes.BOOSTING.name, video_capture.id)
                single_object_tracking.init_box_selected(video_capture.img, video_capture.box)
                video_capture.box = None

            return_tracking = single_object_tracking.update_frame(frame=video_capture.img, frame_orj=video_capture.img_orj, frame_number=video_capture.frame_number, selected_class_id=video_capture.class_id)
            if return_tracking == False:
                video_capture.selecetOI=False


        # End Region Context
        video_capture.save_vision_frame_save(video_capture.img)
        cv2.imshow(configurationManager.config_readable['cv_imshow_title'], cv2.cvtColor(video_capture.img, cv2.COLOR_RGB2BGR))

        if video_capture.selecetROI == True:
            time.sleep(0.05)


if __name__ == '__main__':
    configurationManager = ConfigurationManager()
    
    parser = argparse.ArgumentParser()
    
    class_id = configurationManager.config_readable['selected_class_id']
    last_frame = configurationManager.config_changeable['last_frame']

    parser.add_argument('-c', '--selected_class_id', help="Secilecek class id", default=class_id)
    parser.add_argument('-l', '--last_frame', help="Baslanilmasi istenen frame numarasi", default=last_frame)
    
    args = parser.parse_args()
    
    
    configurationManager.set_selected_id(selected_id=str(args.selected_class_id))
    configurationManager.set_last_frame(last_frame=str(args.last_frame))

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--egitim_True_predticonandcheck_False', help="egitim_True_predticonandcheck_False", action='store_true')
    args = parser.parse_args()
    prepare(args)


    bb= eval(str(args.egitim_True_predticonandcheck_False))
    
    
    '''
    
    
    video_capture = VideoCapture(vision_frame_save=False)

    main()