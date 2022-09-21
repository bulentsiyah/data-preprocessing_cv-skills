from drawopencv import Utils

class CameraParameters:
    def __init__(self, camera_type='video_airbus'):                
        self.camera_info = self.camera_types(camera_type.lower())   
        self.camera_type =  camera_type    
        self.pixel_in_centimeters = self.camera_info["pixel_in_centimeters"]        
        self.width = self.camera_info["width"]
        self.height = self.camera_info["height"]                
        self.center_x = int(self.width / 2)
        self.center_y = int(self.height / 2)
        self.scale = 1

        if self.height >= Utils.camera_height_max:
            self.scale = int(self.height/Utils.camera_height_min) + 1
            self.height = int(self.height/self.scale)
            self.width = int(self.width/self.scale)
            self.center_x = int(self.center_x/self.scale)
            self.center_y = int(self.center_y/self.scale)
            self.pixel_in_centimeters = self.pixel_in_centimeters * self.scale
    
    def camera_types(self,camera_type):

        list_of_camera = {"default" : {"width": 1280, "height" : 720, "pixel_in_centimeters" :6.8 }, 
                          "webcam"  : {"width": 640, "height" : 480, "pixel_in_centimeters" :20.0 },
                          "logitech"  : {"width": 640, "height" : 480, "pixel_in_centimeters" : 16 }, #15.83 },
                          "airsim"  : {"width": 640, "height" : 480, "pixel_in_centimeters" :32.5 },
                          "raspberry"  : {"width": 320, "height" : 240, "pixel_in_centimeters" :20.0 },
                          "raspberry_video"  : {"width": 640, "height" : 480, "pixel_in_centimeters" :20.0 },
                          "video"  : {"width": 1280, "height" : 960, "pixel_in_centimeters" :10.0 },
                          "video_dji"  : {"width": 3840, "height" : 2160, "pixel_in_centimeters" :4.0 },
                          "video_xiaomi"  : {"width": 1920, "height" : 1080, "pixel_in_centimeters" :8.695},
                           "video_dji_web_1"  : {"width": 854, "height" : 480, "pixel_in_centimeters" :8.0},
                           "video_dji_web_2"  : {"width": 1280, "height" : 720, "pixel_in_centimeters" :10.0},
                           "video_airbus"  : {"width": 1280, "height" : 720, "pixel_in_centimeters" :2.5}
                         }
        if camera_type in list_of_camera.keys():
            return list_of_camera[camera_type]        
        raise ValueError(f"Error: Input camera name is not defined. Please define it. input camera_name : {camera_type}")
    def __str__(self):
        return "width [{}] height [{}] center_x [{}] center_y [{}]".format(self.width,
                                                                           self.height,
                                                                           self.center_x,
                                                                           self.center_y)