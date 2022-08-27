import sys
sys.path.append('tools')
from configmanager import ConfigurationManager
from drawopencv import DrawingOpencv
from singleobjecttracker import SingleObjectTracking

import numpy as np

import torch
import cv2

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

        self.model = torch.hub.load(self.configurationManager.config_readable['model_main_yolov5'], 'custom', path=self.configurationManager.config_readable['model_yolo_v5_weight_filename'], source='local')  # local model

        self.classes = ["port_s_daire", "port_s_kare", "port_anakare","sim_port","sim_aircar"]
        
        temp_model_name = str(self.configurationManager.config_readable['model_yolo_v5_weight_filename'])
        if temp_model_name.find("demo")!=-1:
            self.classes = ["-", "port", "person","rust","--", "--"]

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.single_object_tracking = SingleObjectTracking(video_id=self.video_id)

        self.deepsort=False

        if self.deepsort:
            self.tracker = DeepSort(max_age=10)
            self.colors_tracker = np.random.uniform(0, 255, size=(255, 3))

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
                    bb =4
        except:
            print('track')


if __name__ == '__main__':
    model_pre_for_labeling = ModelPredForLabeling()
    model_pre_for_labeling.pred_labeling()