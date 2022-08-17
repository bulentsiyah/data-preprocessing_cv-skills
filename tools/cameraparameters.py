class CameraParameters:
    """
    Kameralarin ozelliklerinin tanimlandigi kisimdir.
    """

    def __init__(self, camera_type='video_airbus'):
        """
        Parameters
        -----------
        camera_type: string 

        Returns
        -----------
        None:
        """
        self.camera_info = self.camera_types(camera_type.lower())
        self.width = self.camera_info["width"]
        self.height = self.camera_info["height"]
        self.center_x = int(self.width / 2)
        self.center_y = int(self.height / 2)


    def camera_types(self, camera_type):
        """
        Parameters
        -----------
        camera_type: string

        Returns
        -----------
        return: Json
        """

        list_of_camera = {"hd": {"width": 1920, "height": 1080},
                         "webcam": {"width": 1280, "height": 960},
                         "webcam2": {"width": 640, "height": 480},
                         "video_airbus"  : {"width": 1280, "height" : 720}
                         }
        if camera_type in list_of_camera.keys():
            return list_of_camera[camera_type]
        raise ValueError(f"Error: Input camera name is not defined. Please define it. Input camera name: {camera_type}")

    def __str__(self):
        return "width [{}] height [{}] center_x [{}] center_y [{}]".format(self.width,
                                                                               self.height,
                                                                               self.center_x,
                                                                               self.center_y)
