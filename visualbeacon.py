import pandas as pd
import cv2
import json
from json import JSONEncoder
import os
import copy

import sys
sys.path.append('tools')
from geocalculation import GeoCalculation
from framebearingupdater import FrameGPSUpdater
from drawopencv import GeoLocation, DrawingOpencv, Utils
from cameraparameters2 import CameraParameters


class VisualBeaconContext:

    def __init__(self, data_frame_path=None, visual_beacon_list=None):
        self.data_frame_path = data_frame_path
        visual_beacon_list= VisualBeacon().visual_beacon_encoder()

        self.visual_beacon_list = visual_beacon_list
        self.data_frame_result = pd.DataFrame()

        self.beacon_drone_gps_location = None
        self.beacon_drone_gps_location_delta_x = None
        self.beacon_drone_gps_location_delta_y = None
        self.beacon_top_left_corner = None
        self.beacon_right_bottom_corner = None

        self.altitude = None
        self.image_taken_time = None

        self.correction = False
        self.diff_visual_vs_beacon = None

        self.gps_less_location_context_cage_left_top_corner = None
        self.beacon_cage_gps_location = None

        self.camera_parameters = CameraParameters("webcam") 

        


    def current_nearest_visual_beacon(self, last_gps_location):
        nearest_visual_beacon = self.visual_beacon_list[0]
        min_distance = GeoCalculation.distance_between_positions_great_circle(last_gps_location.latitude,
           last_gps_location.longitude,
           nearest_visual_beacon.latitude,
           nearest_visual_beacon.longitude)

        for item in self.visual_beacon_list:
           item_distance = GeoCalculation.distance_between_positions_great_circle(last_gps_location.latitude,
           last_gps_location.longitude,
           item.latitude,
           item.longitude)

           if min_distance > item_distance:
               min_distance = item_distance
               nearest_visual_beacon = item
                                                                        
        return nearest_visual_beacon, min_distance


    def run(self, frame, altitude, pixel_in_centimeters, visual_debug_hook=None, image_taken_time=None, last_gps_location=None, gps_less_location_context_cage_left_top_corner=None):
        self.correction = False
        self.gps_less_location_context_cage_left_top_corner = gps_less_location_context_cage_left_top_corner

        self.diff_visual_vs_beacon = 0
        self.altitude = altitude
        #self.pixel_in_centimeters = (pixel_in_centimeters * self.altitude / 100)
        self.image_taken_time = image_taken_time

        visual_beacon_selected, min_distance= self.current_nearest_visual_beacon(last_gps_location)
        if min_distance > DrawingOpencv.visual_beacon_min_distance:
            #print(" min_distance > DrawingOpencv.visual_beacon_min_distance",min_distance)
            return

        image_path = visual_beacon_selected.image_path
        img = cv2.cvtColor(cv2.imread(image_path, 1), cv2.COLOR_BGR2RGB)
        img_h, img_w = img.shape[:2]

        self.beacon_drone_gps_location = GeoLocation('Beacon', latitude=0, longitude=0)
        

        method = eval(DrawingOpencv.methods[0])
        # Apply template Matching
        res = cv2.matchTemplate(img, frame, DrawingOpencv.methods_str) #  method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + img_w, top_left[1] + img_h)

        match_template_corr_score =  DrawingOpencv.min_match_template_corr_score
        if self.camera_parameters.width >= 1000:
            match_template_corr_score = DrawingOpencv.max_match_template_corr_score

        print(" beacon, max_val",max_val)
        if max_val >= DrawingOpencv.threshold_matching:
        #if max_val >= match_template_corr_score:

            print(max_val)
            self.beacon_top_left_corner = top_left
            self.beacon_right_bottom_corner = bottom_right

            image_loc = GeoLocation('image',
                                    latitude=visual_beacon_selected.latitude,
                                    longitude=visual_beacon_selected.longitude)

            self.beacon_drone_gps_location.latitude, self.beacon_drone_gps_location.longitude = FrameGPSUpdater.calculate_drone_gps_from_beacon(
                image_beacon_gps_location=image_loc,
                image_beacon_xy=self.beacon_top_left_corner,
                camera_parameters=self.camera_parameters)

            _, _, delta_x, delta_y = DrawingOpencv.angle_between(last_cage_left_top_corner=self.beacon_top_left_corner,
            new_cage_left_top_corner=(self.camera_parameters.center_x,self.camera_parameters.center_y),
            camera_parameters=self.camera_parameters)

            self.beacon_drone_gps_location_delta_x = visual_beacon_selected.delta_x + delta_x
            self.beacon_drone_gps_location_delta_y = visual_beacon_selected.delta_y + delta_y

            self.beacon_cage_gps_location = GeoLocation('Cage Beacon', latitude=0, longitude=0)

            self.beacon_cage_gps_location.latitude, self.beacon_cage_gps_location.longitude =  FrameGPSUpdater.calculate_cage_left_corner_from_beacon(
                top_left_beacon_gps_location=image_loc,
                top_left_corner_beacon_xy=self.beacon_top_left_corner,
                top_left_corner_cage_xy=self.gps_less_location_context_cage_left_top_corner,
                camera_parameters=self.camera_parameters)
            

            self.diff_visual_vs_beacon = GeoCalculation.distance_between_positions_great_circle(last_gps_location.latitude,
                                                                                        last_gps_location.longitude,
                                                                                        self.beacon_drone_gps_location.latitude,
                                                                                        self.beacon_drone_gps_location.longitude,video_source=True)

            if visual_debug_hook:
                self.visual_debug_hook_(frame=frame)
                if self.diff_visual_vs_beacon >= DrawingOpencv.threshold_visual_vs_beacon:
                    self.correction = True


        if self.data_frame_path is not None:
            if self.beacon_drone_gps_location.latitude != 0:
                diff_distance = GeoCalculation.distance_between_positions_great_circle(self.beacon_drone_gps_location.latitude,
                self.beacon_drone_gps_location.longitude,
                last_gps_location.latitude,
                last_gps_location.longitude)
                self.data_frame_result = self.data_frame_result.append({'image_taken_time': str(self.image_taken_time),
                                                                        'altitude': str(self.altitude),
                                                                        'beacon_drone_gps_latitude': str(self.beacon_drone_gps_location.latitude),
                                                                        'beacon_drone_gps_longitude': str(self.beacon_drone_gps_location.longitude),
                                                                        'last_gps_latitude': str(last_gps_location.latitude),
                                                                        'last_gps_longitude': str(last_gps_location.longitude),
                                                                        'diff_distance': str(float("{0:.4f}".format(diff_distance))),
                                                                        }, ignore_index=True, verify_integrity=False,
                                                                       sort=None)
                self.data_frame_result.to_csv(self.data_frame_path)


    def __str__(self):
        return 'beacon_drone_gps_location:{self.beacon_drone_gps_location} \n ' \
               'altitude:{self.altitude} \n ' \
               'beacon_left_top_corner:{self.beacon_top_left_corner} \n ' \
               'beacon_right_bottom_corner:{self.beacon_right_bottom_corner} \n ' \
               .format(self=self)

    def visual_debug_hook_(self, frame=None):
            print(self.__str__())
            if frame is not None:
                DrawingOpencv.drawing_beacon_rectangle(frame=frame, top_left_corner=self.beacon_top_left_corner, right_bottom_corner=self.beacon_right_bottom_corner)


class VisualBeacon:
    def __init__(self, image_path=None, latitude=None, longitude=None, delta_x=None, delta_y=None):
        self.image_path = image_path
        self.latitude = latitude
        self.longitude = longitude
        self.delta_x = delta_x
        self.delta_y = delta_y

    def visual_beacon_encoder(self, path_folder_visual_beacon_file_name=None):
        #fileDir = os.path.join(os.path.dirname(os.path.realpath('__file__')), "source/visual beacon/")
        fileDir = "./_images_must/visual beacon/"
        path_folder_visual_beacon_file_name = os.path.join(fileDir, "airsim_capraz.json") 

        with open(path_folder_visual_beacon_file_name, 'r') as file_name:
            json_object = json.load(file_name)
            json_object = json.loads(json_object)
            visual_beacon_list = list()
            for i in range(len(json_object)):
                visual_beacon_list.append(VisualBeacon(**json_object[i]))

        for i in range(len(visual_beacon_list)):
            visual_beacon_list[i].image_path = fileDir+visual_beacon_list[i].image_path

        return visual_beacon_list


class VisualBeaconEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__




#Main Function
def main():
    visual_beacon_context = VisualBeaconContext()
    vid = cv2.VideoCapture("_videos/visual_beacon_sim.mp4")

    if(vid.isOpened() == False):
        print('Cannot open input video')
        return

    width = 640
    height = 480

    take_off_latitude = 41.1076638 * Utils.location_coefficient
    take_off_longitude = 28.9951060* Utils.location_coefficient

    drone_gps_location = GeoLocation('Drone',latitude=(take_off_latitude/Utils.location_coefficient), longitude=(take_off_longitude/Utils.location_coefficient))

    cage_left_top_corner_gps = (int(320), int(240))

    while(vid.isOpened()):
        rc, frame = vid.read()

        if(rc == True):
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame= cv2.resize(frame, (width, height))

            visual_beacon_context.run(frame=frame,
                                altitude=100,
                                pixel_in_centimeters=6.8,
                                visual_debug_hook=True,
                                image_taken_time=None,
                                last_gps_location=drone_gps_location,
                                gps_less_location_context_cage_left_top_corner=cage_left_top_corner_gps)

            cv2.imshow("Visual Beacon", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            if (cv2.waitKey(300) & 0xFF == ord('q')):
                break


    if visual_beacon_context.correction:
        print("sapma var")
        '''self.gps_less_location_context.state.cage_left_top_corner_gps.latitude = self.visual_beacon_context.beacon_cage_gps_location.latitude
        self.gps_less_location_context.state.cage_left_top_corner_gps.longitude = self.visual_beacon_context.beacon_cage_gps_location.longitude

        self.gps_less_location_context.state.drone_gps_location.latitude = self.visual_beacon_context.beacon_drone_gps_location.latitude
        self.gps_less_location_context.state.drone_gps_location.longitude = self.visual_beacon_context.beacon_drone_gps_location.longitude

        self.total_correction_meter  += self.visual_beacon_context.diff_visual_vs_beacon

        self.gps_less_location_context.state.delta_x = self.visual_beacon_context.beacon_drone_gps_location_delta_x
        self.gps_less_location_context.state.delta_y = self.visual_beacon_context.beacon_drone_gps_location_delta_y'''


if __name__ == "__main__":
    main()

print('Program Completed!')