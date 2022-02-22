import cv2
import time
import sys
sys.path.append('/vision/tools')

from configmanager import ConfigurationManager
from cameraparameters import CameraParameters
from datetime import datetime
from drawopencv import DrawingOpencv
import os
import glob
import copy
import sys


class VideoCapture:
    """
    Video üzerindeki tüm işlemlerin yapıldığı sınıftır.
    """

    def __init__(self, print_showing=False, pure_frame_save=False, vision_frame_save=True):
        """
        Parameters
        -----------
        print_showing: Boolean - sınıf içerisindeki çıktıların terminalde görünmesini/gizlenmesini sağlar
        pure_frame_save: Boolean - videonun orjinalinin/üzerine birşey yazılmamış halini seçili kamera parametrelerine göre kaydedilmesini sağlar.
        vision_frame_save: Boolean - videonun üzerine hesaplamalar yapılmış son halinin seçili kamere parametrelerine göre kaydedilmesini sağlar.

        Returns
        ----------
        return: None
        """
        self.cfg = ConfigurationManager()
        self.drawopencv = DrawingOpencv()

        self.camera_parameters = CameraParameters("webcam")

        self.class_id = int(self.cfg.config_readable['selected_class_id'])
        video_true_webcam_false = eval(self.cfg.config_readable['video_true_webcam_false'])

        if video_true_webcam_false:
            video_path = os.path.dirname(sys.argv[0]) + self.cfg.config_readable['video_path_file']
        else:
            video_path = 0

        self.video_capture = cv2.VideoCapture(video_path)
        self.frame_width = int(self.video_capture.get(3))
        self.frame_height = int(self.video_capture.get(4))

        self.frame_fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))

        self.frame_number = 0
        self.print_showing = print_showing
        self.id = os.path.splitext(os.path.basename(video_path))[0]

        self.resizing = True
        self.new_width = 0
        self.new_height = 0

        self.selecetROI = False
        self.box = None

        if self.frame_width != self.camera_parameters.width:
            if self.resizing:
                self.scale = self.frame_width / self.camera_parameters.width
                self.new_width = self.camera_parameters.width
                self.new_height = int(self.frame_height / self.scale)
            else:
                self.new_width = self.frame_width
                self.new_height = self.frame_height


        self.pure_frame_save = pure_frame_save
        if self.pure_frame_save:
            self.pure_frame_save_out = cv2.VideoWriter(os.path.dirname(sys.argv[0]) +self.cfg.config_readable['video_save_path_folder']+str(datetime.now().strftime('%Y_%m_%d_%H%M%S'))+'_pure.avi',cv2.VideoWriter_fourcc(*'XVID'), self.frame_fps, (self.new_width,self.new_height))

        self.vision_frame_save = vision_frame_save
        if self.vision_frame_save:
            self.vision_frame_save_out = cv2.VideoWriter(os.path.dirname(sys.argv[0]) +self.cfg.config_readable['video_save_path_folder']+str(datetime.now().strftime('%Y_%m_%d_%H%M%S'))+'_vision.avi',cv2.VideoWriter_fourcc(*'XVID'), self.frame_fps, (self.new_width,self.new_height))
            
        
        directory = self.id
        parent_dir = os.path.dirname(sys.argv[0] + self.cfg.config_readable['video_save_path_folder'])
        path = os.path.join(parent_dir, directory)

        
        try:
            self.frame_number = int(self.cfg.config_changeable['last_frame'])
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
            #print(latest_file)
        except:
            print("exception_videocapture_init")
            pass


    def save_pure_frame_save(self, frame):
        if self.pure_frame_save:
            try:
                self.pure_frame_save_out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            except:
                    pass
    def save_vision_frame_save(self, frame):
        if self.vision_frame_save:
            try:
                self.vision_frame_save_out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            except:
                    pass
    
    def get_image(self):
        """
        video dan sırası gelen frame i alan kısımdır, aynı zaman da bölge seçmek, ekran görüntüsü almak gibi kısımlar da burada yapılır.
        
        Parameters
        -----------
        None:
        Returns
        -----------
        None:
        """
        
        start_read_frame = time.time()
        self.ret, self.img = self.video_capture.read()

        self.frame_number = self.frame_number + 1
        
        if self.ret == False:
            cv2.destroyAllWindows()
            self.img = None
            return
        
        if self.frame_width != self.camera_parameters.width:
            if self.resizing:
                self.img = cv2.resize(self.img, (self.new_width, self.new_height))
        
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        self.img_orj = copy.deepcopy(self.img)

        try:
            directory = self.id
            parent_dir = os.path.dirname(sys.argv[0]) + self.cfg.config_readable['video_save_path_folder']
            path = os.path.join(parent_dir, directory)
            text_name = path + "/" + str(self.frame_number) + "__" + str(self.id) + ".txt"
            
            if os.path.exists(text_name) == True:
                infile = open(text_name, 'r').readlines()
                for index,line in enumerate(infile):
                    try:
                        index = int(line.split(" ")[0])
                        yolo_x = int(float(line.split(" ")[1]) * self.new_width)
                        yolo_y = int(float(line.split(" ")[2]) * self.new_height)
                        yolo_w = int(float(line.split(" ")[3]) * self.new_width)
                        yolo_h = int(float(line.split(" ")[4]) * self.new_height)
                        
                        x1 = yolo_x - int((yolo_w/2))
                        y1 = yolo_y - int((yolo_h/2))
                        self.drawopencv.drawing_rectangle(self.img, class_id=index, x1_y1=(x1, y1), x2_y2=(x1 + yolo_w, y1 + yolo_h), color=self.drawopencv.color_red)
                    except:
                        pass
        except:
            print("Çizimden dolayı hata oluştu!!! (Sistemin durmasına gerek yok) . videocapture get_image")
            pass
        self.drawopencv.drawing_time_stamp_text(self.img, selected_class=self.class_id)
        self.drawopencv.drawing_frame_number_text(self.img, self.frame_number, self.frame_fps)

        key = cv2.waitKey(1) & 0xFF

        if (key == 27 or key == ord("q")):
            self.ret = False

        if key == ord("s"):
            try:
                cv2.imwrite(os.path.dirname(sys.argv[0]) + self.cfg.config_readable['video_screenshots_path_folder']+str(time.time())+".png", cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR))
            except:
                print("Exception Video Capture cv2.imwrite")
                pass
        
        if key == ord("r"):
            self.box = cv2.selectROI(self.cfg.config_readable['cv_imshow_title'], cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR), fromCenter=False)
            if self.box[0] == 0 and self.box[1] == 0 and self.box[2] == 0 and self.box[3] == 0:
                self.selecetROI = False
            else:
                self.selecetROI = True

        if self.selecetROI == False:
            self.box = cv2.selectROI(self.cfg.config_readable['cv_imshow_title'], cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR), fromCenter=False)
            if self.box[0] == 0 and self.box[1] == 0 and self.box[2] == 0 and self.box[3] == 0:
                self.selecetROI = False
            else:
                self.selecetROI = True
        
        self.read_frame_time = time.time() - start_read_frame
        if self.print_showing:
            print("Video Capture get_image time: ",self.read_frame_time)