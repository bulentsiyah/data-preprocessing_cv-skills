import math
from geopy.distance import great_circle, geodesic ,vincenty

class GeoCalculation:

    @staticmethod
    def distance_between_positions_vincenty(lat1, lon1, lat2, lon2):
         return vincenty((lat1, lon1), (lat2, lon2)).meters

    @staticmethod
    def distance_between_positions_geodesic(lat1, lon1, lat2, lon2):
        l_10_7  = 10000000
        return geodesic((lat1/l_10_7, lon1/l_10_7), (lat2/l_10_7, lon2/l_10_7)).meters

    @staticmethod
    def distance_between_positions_great_circle(lat1, lon1, lat2, lon2, video_source=False):
        l_10_7  = 10000000
        if video_source:
            l_10_7 =1
        return great_circle((lat1/l_10_7, lon1/l_10_7), (lat2/l_10_7, lon2/l_10_7)).meters

    @staticmethod
    def calculate_new_gps_position(lat1, lon1, distance, bearing):
        R = 6378.1  # Radius of the Earth
        # bearing 1.57 #Bearing is 90 degrees converted to radians.
        # distance  # 0.100 #Distance in km

        lat1 = math.radians(lat1)  # Current lat point converted to radians
        lon1 = math.radians(lon1)  # Current long point converted to radians

        lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) +
                         math.cos(lat1) * math.sin(distance / R) * math.cos(bearing))

        lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat1),
                                 math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)

        # lat2 = (lat2 * 1.00000025853   ) #1,000000258535925‬  * 1.145 # 0.8781204112# 1.327291695
        # lon2 = (lon2 * 0.99999993388   ) #0,9999999338833232 * 1.145 # 0.8824914944 #1.327291695

        return lat2, lon2
