import math
from math import atan2, pi
from geocalculation import GeoCalculation


class FrameGPSUpdater:

    @staticmethod
    def distance_bearing_calculator_using_parameters(destination_x, destination_y, source_x, source_y,
                                                     camera_parameters):
        analytical_coordinate_sourceY = camera_parameters.height - source_y
        analytical_coordinate_destinationY = camera_parameters.height - destination_y

        bearing = 90 - (180 / pi) * math.atan2(analytical_coordinate_destinationY - analytical_coordinate_sourceY,
                                               destination_x - source_x)

        bearing = bearing * (pi / 180)

        distance = math.sqrt(((analytical_coordinate_destinationY - analytical_coordinate_sourceY) ** 2) + (
                destination_x - source_x) ** 2)
        distance = (distance * camera_parameters.pixel_in_centimeters)/100 # dis * self.ratio__pixels_meters
        distance = distance / 1000

        return distance, bearing

    @staticmethod
    def calculate_top_left_corner_from_drone_gps(drone_gps_location, top_left_corner_xy_tuple, camera_parameters):
        distance, bearing = FrameGPSUpdater.distance_bearing_calculator_using_parameters(top_left_corner_xy_tuple[0],
                                                                                         top_left_corner_xy_tuple[1],
                                                                                         camera_parameters.center_x,
                                                                                         camera_parameters.center_y,
                                                                                         camera_parameters)
        top_left_corner_latitude, top_left_corner_longitude = GeoCalculation.calculate_new_gps_position(
            drone_gps_location.latitude,
            drone_gps_location.longitude,
            distance,
            bearing)
        return top_left_corner_latitude, top_left_corner_longitude


    @staticmethod
    def calculate_top_left_corner_from_drone_gps_2(drone_gps_location, top_left_corner_xy_tuple, camera_parameters):
        distance, bearing = FrameGPSUpdater.distance_bearing_calculator_using_parameters(top_left_corner_xy_tuple[0],
                                                                                         top_left_corner_xy_tuple[1],
                                                                                         camera_parameters.center_x,
                                                                                         camera_parameters.center_y,
                                                                                         camera_parameters)
        top_left_corner_latitude, top_left_corner_longitude = GeoCalculation.calculate_new_gps_position(
            drone_gps_location[0],
            drone_gps_location[1],
            distance,
            bearing)
        return top_left_corner_latitude, top_left_corner_longitude

    @staticmethod
    def calculate_drone_from_top_left_corner(top_left_corner_gps_location,
                                                 top_left_corner_xy,
                                                 camera_parameters):
        distance, bearing = FrameGPSUpdater.distance_bearing_calculator_using_parameters(camera_parameters.center_x,
                                                                                         camera_parameters.center_y,
                                                                                         top_left_corner_xy[0],
                                                                                         top_left_corner_xy[1],
                                                                                         camera_parameters)
        drone_latitude, drone_longitude = GeoCalculation.calculate_new_gps_position(
            top_left_corner_gps_location.latitude,
            top_left_corner_gps_location.longitude,
            distance,
            bearing)
        return drone_latitude, drone_longitude


    @staticmethod
    def calculate_drone_gps_from_beacon(image_beacon_gps_location,
                                                 image_beacon_xy,
                                                 camera_parameters):
        distance, bearing = FrameGPSUpdater.distance_bearing_calculator_using_parameters(camera_parameters.center_x,
                                                                                         camera_parameters.center_y,
                                                                                         image_beacon_xy[0],
                                                                                         image_beacon_xy[1],
                                                                                         camera_parameters)
        drone_latitude, drone_longitude = GeoCalculation.calculate_new_gps_position(
            image_beacon_gps_location.latitude,
            image_beacon_gps_location.longitude,
            distance,
            bearing)
        return drone_latitude, drone_longitude



    
    @staticmethod
    def calculate_cage_left_corner_from_beacon(top_left_beacon_gps_location,top_left_corner_beacon_xy,top_left_corner_cage_xy,camera_parameters):
        distance, bearing = FrameGPSUpdater.distance_bearing_calculator_using_parameters( top_left_corner_cage_xy[0],
                                                                                         top_left_corner_cage_xy[1],
                                                                                         top_left_corner_beacon_xy[0],
                                                                                         top_left_corner_beacon_xy[1],
                                                                                         camera_parameters)
        cage_latitude, cage_longitude = GeoCalculation.calculate_new_gps_position(
            top_left_beacon_gps_location.latitude,
            top_left_beacon_gps_location.longitude,
            distance,
            bearing)
        return cage_latitude, cage_longitude

