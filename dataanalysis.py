from calendar import c
import glob
import os
from this import d
from turtle import width
import pandas as pd
import argparse

import sys 
sys.path.append('tools')
from configmanager import ConfigurationManager
from cameraparameters import CameraParameters

class DataAnalysis:
    """
    Tüm etiketli txtlerin incelendiği siniftir.
    """

    def __init__(self):
        """
        config ve class cagrilirken ki kontrollerin yapildigi yerdir.

        Parameters
        -----------
        None:

        Returns
        -----------
        None:
        """
        self.configurationManager = ConfigurationManager()
        self.camera_parameters = CameraParameters("webcam")


    def run(self):
        """
        bolumleme islemenin yapildigi yerdir

        Parameters
        -----------
        None:

        Returns
        -----------
        None:
        """
        delete_it_has_volume_below_this_value = 10 #Bu piksel degerinden kucukleri sil
        bound_box_list = []
        deleted_bound_box_list = []

        video_path = os.path.dirname(sys.argv[0]) + self.configurationManager.config_readable['video_path_file']
        video_path = os.path.splitext(os.path.basename(video_path))[0]
        parent_dir = os.path.dirname(sys.argv[0]) + self.configurationManager.config_readable['video_save_path_folder']
        labeling_folder_path = os.path.join(parent_dir, video_path)

        list_of_files = glob.glob(labeling_folder_path+'/*.txt')

        dictionary = {}

        x_default = self.camera_parameters.width
        y_default = self.camera_parameters.height

        for file in list(list_of_files):
            infile = open(file)
            for index,line in enumerate(infile):
                try:
                    class_id = line.split(" ")[0]

                    try:
                        class_id_df = int(class_id)
                        x_df = float(line.split(" ")[1])
                        y_df = float(line.split(" ")[2])
                        w_df = float(line.split(" ")[3])
                        h_df = float(line.split(" ")[4])
                        center_x_df = float((x_df+x_df+w_df)/2)
                        center_y_df = float((y_df+y_df+h_df)/2)
                        area = w_df * h_df
                        region = 0
                        if center_x_df <= 0.5:
                            if center_y_df <= 0.5:
                                region = 4
                            else:
                                region = 3
                        else:
                            if center_y_df <= 0.5:
                                region = 1
                            else:
                                region = 2
                        
                        width_piksel = x_default * w_df
                        height_piksel = y_default * h_df

                        area_piksel = width_piksel * height_piksel

                        center_x_piksel = x_default * center_x_df
                        center_y_piksel = y_default * center_y_df

                        if area_piksel < delete_it_has_volume_below_this_value:
                            image_file = file[:-4]
                            image_file = image_file + ".png"
                            os.remove(file)
                            os.remove(image_file) + ".png"
                            deleted_bound_box_list.append([str(file),str(image_file)])
                        else:
                            bound_box_list.append([class_id_df, x_df, y_df, w_df, h_df, center_x_df, center_y_df, area, region])
                    except:
                        pass

                    
                    if class_id in dictionary.keys():
                        last_value = dictionary[class_id]
                        last_value = last_value + 1
                        dictionary[class_id] = last_value
                    else:
                        dictionary[class_id] = 1

                    
                except:
                    pass

        total = 0
        for x, y in dictionary.items():
            total = total + y


        df = pd.DataFrame(bound_box_list, columns= ["class_id", "x", "y", "w", "h", "center_x", "center_y", "area", "region"])
        df.to_csv(parent_dir+"/"+video_path+"__class_analysis.csv", index=False)

        print("total labeling images count: ", len(df.index))

        if len(deleted_bound_box_list)>0:
            df = pd.DataFrame(deleted_bound_box_list, columns = ["txt_filename", "img_filename"])
            df.to_csv(parent_dir+"/"+video_path+"__class_deleted.csv", index=False)

            print("total deleting file count: ", len(df.index))

if __name__ == '__main__':
    data_analysis = DataAnalysis()
    data_analysis.run()