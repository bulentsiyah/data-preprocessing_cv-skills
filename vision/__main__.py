import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append('vision/tools')
from configmanager import ConfigurationManager
from singleobjecttracker import SingleObjectTracking, TrackerTypes
from videocapture import VideoCapture

import cv2
import time
import argparse

def main():
    """
    İşlemin başladığı ana sınıftır.
    """
    configurationManager = ConfigurationManager()
    parser = argparse.ArgumentParser()
    
    class_id = configurationManager.config_readable['selected_class_id']
    last_frame = configurationManager.config_changeable['last_frame']

    parser.add_argument('-c', '--selected_class_id', help="Seçilecek class id", default=class_id)
    parser.add_argument('-l', '--last_frame', help="Başlanılması istenen frame numarası", default=last_frame)
    
    args = parser.parse_args()

    video_capture.class_id = str(args.selected_class_id)
    video_capture.frame_number = int(args.last_frame)

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

            return_tracking = single_object_tracking.update_frame(frame=video_capture.img, frame_orj=video_capture.img_orj, frame_number=video_capture.frame_number)
            if return_tracking == False:
                video_capture.selecetOI=False

        # End Region Context
        video_capture.save_vision_frame_save(video_capture.img)
        cv2.imshow(configurationManager.config_readable['cv_imshow_title'], cv2.cvtColor(video_capture.img, cv2.COLOR_RGB2BGR))

        if video_capture.selecetROI == True:
            time.sleep(0.05)


if __name__ == '__main__':
    configurationManager = ConfigurationManager()
    video_capture = VideoCapture()

    main()