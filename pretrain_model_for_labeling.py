import warnings
warnings.filterwarnings("ignore")

from semi_labeling import SingleObjectTracking

import numpy as np
import pandas as pd
import torch
import cv2
import os
import datetime
import time
import argparse

import sys
sys.path.append('tools')
from configmanager import ConfigurationManager
from drawopencv import DrawingOpencv
from videocapture import VideoCapture

sys.path.append('../')
from deep_sort_realtime.deepsort_tracker import DeepSort


class ModelPredForLabeling:
    """
    Prediction yapildigi siniftir.
    Etiketlenen framelerin ve txtlerin yazildigi kisimdir.
    classes.txt bu sinifta da yaratilir ve kontrol edilir.
    """

    def __init__(self,  video_id="none_name"):
        self.configurationManager = ConfigurationManager()

        self.video_id = video_id

        path = "../data-preprocessing_cv-skills/_models/yolov5_demo_agust22/Demo_August_Port10.pt"

        self.model = torch.hub.load(self.configurationManager.config_readable['model_main_yolov5'], 'custom', path=path, source='local')  # local model

        self.classes = ["port_s_daire", "port_s_kare", "port_anakare","sim_port","sim_aircar"]
        
        temp_model_name = str(path)
        if temp_model_name.find("demo")!=-1:
            self.classes = ["-", "port", "person","rust","--", "--"]

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.single_object_tracking = SingleObjectTracking(video_id=self.video_id)

        self.deepsort=False
    
        if self.deepsort:
            self.tracker = DeepSort(max_age=10)
            self.colors_tracker = np.random.uniform(0, 255, size=(255, 3))

        self.data_collection_for_distance = True

        if self.data_collection_for_distance:
            self.data_frame_data_collection_for_distance = pd.DataFrame()
            parent_dir = os.path.dirname(sys.argv[0]) + self.configurationManager.config_readable['video_save_path_folder']
            self.path_distance_csv = os.path.join(parent_dir,  datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y-%H-%M-%S")+".csv")
            

    def pred_labeling(self, frame, frame_orj, frame_number):
        """
        modele göre tahmin yapılıp etıketlendıgı yerdir.

        Parameters
        -----------
        None:

        Returns
        -----------
        None:
        """

        org_frame = frame_orj

        results = self.model(frame)
        rows = len(results.xyxy[0])


        CONFIDENCE_THRESHOLD = 0.5
        dets = []

        for r in range(rows):
            xmin,ymin,xmax,ymax,confidence,class_id=results.xyxy[0][r]

            xmin=int(xmin)
            ymin=int(ymin)
            xmax=int(xmax)
            ymax=int(ymax)

            confidence=float(confidence)
            class_id=int(class_id)

            
            if confidence >= CONFIDENCE_THRESHOLD:
                label = str(self.classes[class_id])
                color = self.colors[class_id]

                DrawingOpencv.drawing_rectangle(frame=frame, class_id=label, x1_y1=(xmin, ymin), x2_y2=(xmax, ymax), color=color)
                
                box = [xmin,ymin, (xmax-xmin), (ymax-ymin)]
                self.single_object_tracking.yolo_format(box=box, frame=org_frame, frame_number=frame_number, selected_class_id=class_id)

                dets.append( (box, confidence, label) )


            try:
                
                if self.data_frame_data_collection_for_distance is not None:
                    class_type = 0
                    distance = 10
                    self.data_frame_data_collection_for_distance = self.data_frame_data_collection_for_distance.append({'xmin': str(xmin),
                                                                        'ymin': str(ymin),
                                                                        'xmax': str(xmax),
                                                                        'ymax': str(ymax),
                                                                        'class_type': str(class_type),
                                                                        'width': str(xmax-xmin),
                                                                        'height': str(ymax-ymin),
                                                                        'time': str(datetime.datetime.utcnow()),
                                                                        'zloc': str(distance),
                                                                        }, ignore_index=True, verify_integrity=False,
                                                                                sort=None)
                    self.data_frame_data_collection_for_distance.to_csv(self.path_distance_csv)

            except:
                print('distance')


        try:
            if self.tracker is not None:
                self.tracks = self.tracker.update_tracks(dets, frame=frame)

                for track in self.tracks:
                    if not track.is_confirmed():
                        continue
                    track_id = track.track_id
                    ltrb = track.to_ltrb()
                    xmin=int(ltrb[0])
                    ymin=int(ltrb[1])
                    xmax=int(ltrb[2])
                    ymax=int(ltrb[3])

                    color = self.colors_tracker[int(str(track_id))]
                    DrawingOpencv.drawing_rectangle(frame=frame, class_id=str(track_id), x1_y1=(xmin, ymin), x2_y2=(xmax, ymax), color=color)
                    
        except:
            b = 5
            #print('track')




def main():
    """
    İslemin basladigi ana siniftir.                  
    """

    model_pred_for_labeling = ModelPredForLabeling(video_id=video_capture.id)
    video_capture.selecetROI = True

    

    while True:
        
        video_capture.get_image()

        if (video_capture.ret == False):
            break
 
        video_capture.save_pure_frame_save(video_capture.img)

        model_pred_for_labeling.pred_labeling(frame=video_capture.img, frame_orj=video_capture.img_orj, frame_number=video_capture.frame_number)

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
    
    
    video_capture = VideoCapture(vision_frame_save=False)

    main()