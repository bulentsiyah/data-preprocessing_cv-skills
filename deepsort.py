import numpy as np

import sys
sys.path.append('tools')
from drawopencv import DrawingOpencv

import sys
sys.path.append('../')
from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSortTracker:
    """

    """

    def __init__(self, max_age ):

        self.tracker = DeepSort(max_age=max_age)
        self.colors_tracker = np.random.uniform(0, 255, size=(255, 3))

    def update_tracks(self,dets,frame):
        try:
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