from datetime import datetime, timedelta
import cv2 
import numpy as np
import os
from dataclasses import dataclass
from pathlib import Path
import math
from math import atan2, pi, cos, sin

@dataclass
class GeoLocation:
    name: str
    latitude: float
    longitude: float


class Utils:
    location_coefficient = 10000000
    camera_height_max = 2081
    camera_height_min = 480

class DrawingOpencv:
    """
    Tum ekrana cizim islemlerinin yapildigi siniftir.
    
    """

    visual_beacon_min_distance = 30
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF',
               'cv2.TM_SQDIFF_NORMED']
    methods_str = cv2.TM_CCOEFF_NORMED
    threshold_visual_vs_beacon = 3.09 # meter
    threshold_matching = 0.40 # %70
    max_match_template_corr_score = 1500111222
    min_match_template_corr_score =  200111222

    color_beacon = (255,0,0)
    color_text_beacon = (255,0,0)


    line_thick = 0.65
    color_blue = (0, 0, 255) #blue
    color_red = (255, 0, 0) #red
    color_pink = (240, 131, 244) #pink
    color_green = (7, 216, 17) #green

    def __init__(self):
        pass


    @staticmethod
    def angle_between(last_cage_left_top_corner, new_cage_left_top_corner, frame = None, visual_debug=False, camera_parameters=None):
        delta_x_image = new_cage_left_top_corner[0] - last_cage_left_top_corner[0]
        delta_y_image = new_cage_left_top_corner[1] - last_cage_left_top_corner[1]
        angle_rad = atan2(delta_x_image, delta_y_image)
        angle_deg = angle_rad * 180.0 / pi
        angle_deg = math.atan2(last_cage_left_top_corner[1] - new_cage_left_top_corner[1], last_cage_left_top_corner[0] - new_cage_left_top_corner[0]) * 180/math.pi
        delta_x = (delta_y_image * camera_parameters.pixel_in_centimeters)/100
        delta_y = -(delta_x_image * camera_parameters.pixel_in_centimeters)/100
       

        # # angle_rad = atan2(delta_x_image, delta_y_image)
        # # angle_deg = angle_rad * 180.0 / pi
        # # angle_deg = math.atan2(last_cage_left_top_corner[1] - new_cage_left_top_corner[1], last_cage_left_top_corner[0] - new_cage_left_top_corner[0]) * 180/math.pi
        # # angle_rad = math.atan2(new_cage_left_top_corner[1]- last_cage_left_top_corner[1] , (new_cage_left_top_corner[0]- last_cage_left_top_corner[0]) )
        # # angle_deg = math.degrees(angle_rad)
        
        # delta_x = (delta_y_image * camera_parameters.pixel_in_centimeters)/100
        # delta_y = -(delta_x_image * camera_parameters.pixel_in_centimeters)/100
        # angle_rad = math.atan2(delta_x, delta_y )
        # angle_deg = math.degrees(angle_rad)

        return angle_deg, angle_rad, delta_x, delta_y


    @staticmethod
    def drawing_beacon_rectangle(frame, top_left_corner=None, right_bottom_corner=None):
        try:
            cv2.rectangle(frame, top_left_corner, right_bottom_corner, DrawingOpencv.color_beacon, thickness=0)

            # First we crop the sub-rect from the image

            sub_img = frame[top_left_corner[1]:right_bottom_corner[1], top_left_corner[0]:right_bottom_corner[0]]
            white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

            res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)

            # Putting the image back to its position
            frame[top_left_corner[1]:right_bottom_corner[1], top_left_corner[0]:right_bottom_corner[0]] = res

            cv2.rectangle(frame, top_left_corner, right_bottom_corner, DrawingOpencv.color_beacon, thickness=0)

            center_rectangle =  (int(top_left_corner[0]+10), int((top_left_corner[1]+right_bottom_corner[1])/2))

            line_thick=0.30
            cv2.putText(frame, "Visual Beacon", center_rectangle, cv2.FONT_HERSHEY_DUPLEX, line_thick, DrawingOpencv.color_beacon, 1)
        except:
            pass

    @staticmethod
    def drawing_time_stamp_text(frame, selected_class):

        """
        Parameters
        -----------
        frame: image - o anki frame
        selected_class: integer - secili sinifin labeli

        Returns
        -----------
        None: geri donuse gerek yok gelen frame uzerine yaziliyor
        """

        ttemp_y = 3
        ttemp_y_end = 60
        sub_img = frame[ttemp_y:ttemp_y_end, 5:320]
        white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
        res = cv2.addWeighted(sub_img, 0.6, white_rect, 0.5, 1.0)
        frame[ttemp_y:ttemp_y_end, 5:320] = res


        time_stamp = str(datetime.now())[:-3]
        textsize = cv2.getTextSize(time_stamp, cv2.FONT_HERSHEY_COMPLEX_SMALL, DrawingOpencv.line_thick, 1)[0]
        textX = int(10)
        textY = 30 #int(textsize[1]) + int((ttemp_y_end+ttemp_y)/2)
        
        cv2.putText(frame, "Selected Class Id: "+ str(selected_class), (textX,textY), cv2.FONT_HERSHEY_COMPLEX_SMALL, DrawingOpencv.line_thick, DrawingOpencv.color_blue, 1, cv2.LINE_AA)

    @staticmethod
    def drawing_frame_number_text(frame, frame_number, frame_fps):
        """
        Parameters
        -----------
        frame:image - o anki frame
        frame_number: integer - o anki bulunan frame sayisi
        frame_fps: integer -

        Returns
        -----------
        None: geri donuse gerek yok gelen frame üzerine yaziliyor. 
        """

        time_stamp = "frame number: "+str(frame_number)
        textsize = cv2.getTextSize(time_stamp, cv2.FONT_HERSHEY_COMPLEX_SMALL, DrawingOpencv.line_thick, 1)[0]
        textX = int(10)
        textY = 5 + int(textsize[1])

        total_second = int(frame_number / frame_fps)
        microseconds = (total_second * 1000) + int(frame_number % frame_fps)
        conversion = timedelta(seconds=total_second, microseconds=microseconds)
        converted_time = str(conversion)

        time_stamp = time_stamp #+ " time:" + converted_time[:-2]

        cv2.putText(frame, time_stamp,(textX,textY), cv2.FONT_HERSHEY_COMPLEX_SMALL, DrawingOpencv.line_thick, DrawingOpencv.color_green, 1, cv2.LINE_AA)


    @staticmethod
    def drawing_rectangle(frame, class_id, x1_y1, x2_y2, color):
        """
        Parameters
        -----------
        frame:image - o anki frame
        class_id: integer -
        x1_y1: tuple - sol ust koordinat degerleri
        x2_y2: tuple - sag alt koordinat degerleri

        Returns
        -----------
        None: geri donuse gerek yok gelen frame üzerine yaziliyor.
        """

        x1_y1_text_padding = (x1_y1[0], x1_y1[1]-5)
        cv2.putText(frame, str(class_id), x1_y1_text_padding, cv2.FONT_HERSHEY_COMPLEX_SMALL, DrawingOpencv.line_thick, color, 1, cv2.LINE_AA)
        cv2.rectangle(frame, x1_y1, x2_y2, color, 1)

    @staticmethod
    def opencv_put_text(frame, string_text):
        """
        Parameters
        -----------
        frame:image - o anki frame
        string_text: string - yazilmasi istenilen text

        Returns
        -----------
        None: geri donuse gerek yok gelen frame uzerine yaziliyor.
        """
        
        cv2.putText(frame, string_text, (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, DrawingOpencv.color_red, 2)
        