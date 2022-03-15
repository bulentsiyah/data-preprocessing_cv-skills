import glob
import os
import argparse
from pydoc import text
import shutil

import sys
sys.path.append('tools')
from configmanager import ConfigurationManager

class SplitDataset:
    """
    Datasetin train ve valid diye ikiye bolundugu kisimdir.
    """

    def __init__(self):
        """
        config ve class cagrilirken ki kontrollerin yapildigi metotdur.
        
        Parameters
        -----------
        None:

        Returns
        -----------
        None:
        """
        self.configurationManager = ConfigurationManager()
        self.parser = argparse.ArgumentParser()

        config_percentage_valid = self.configurationManager.config_changeable['split_percentage_valid']
        config_split_type_yolov3_yolov5 = self.configurationManager.config_changeable['split_type_yolov3_yolov5']
        self.split_max_class_count = int(self.configurationManager.config_changeable['split_max_class_count'])

        self.parser.add_argument('-p', '--percentage_valid', help='yuzde kac valid icin', default=config_percentage_valid)
        self.parser.add_argument('-t', '--type_yolov3_yolov5', help='dosyalama türü yolov3(0) veya yolov5(1) göre ', default=config_split_type_yolov3_yolov5)

        args = self.parser.parse_args()

        self.percentage_valid = int(args.percentage_valid)
        self.configurationManager.set_split_percentage_valid(split_percentage_valid=self.percentage_valid)

        self.type_yolov3_yolov5 = int(args.type_yolov3_yolov5)
        self.configurationManager.set_split_type_yolov3_yolov5(split_type_yolov3_yolov5=self.type_yolov3_yolov5)


    def run(self):
        """
        Bolumleme isleminin yapildigi yerdir

        Parameters
        -----------
        None:

        Returns
        -----------
        None:
        """

        root_path = os.path.dirname(sys.argv[0])
        print("root_path", root_path)
        if "." in root_path:
            root_path = os.getcwd()+root_path.replace(".", "")
            print("root_path", root_path)
        
        video_id = os.path.splitext(os.path.basename(root_path + self.configurationManager.config_readable['video_path_file']))[0]
        output_dir = root_path + self.configurationManager.config_readable['video_save_path_folder']

        current_dir = os.path.join(output_dir, video_id)

        if self.type_yolov3_yolov5 == 0:
            videoid_yolo = "yolov3_"+video_id 
            yolo_output_dir = os.path.join(output_dir, videoid_yolo)
            os.mkdir(yolo_output_dir)

            file_train = open(yolo_output_dir+'/train.txt', 'w')
            file_test = open(yolo_output_dir+'/valid.txt', 'w')

            counter = 1
            index_test = round(100 / self.percentage_valid)
            for file in glob.iglob(os.path.join(current_dir, '*.png')):
                title, ext = os.path.splitext(os.path.basename(file))
                if counter == index_test:
                    counter = 1
                    file_test.write(current_dir + "/" + title + '.png' + "\n")
                else:
                    file_train.write(current_dir + "/" + title + '.png' + "\n")
                    counter = counter + 1

            
            file_train.close()
            file_test.close()
        else:
            yolo_output_dir = os.path.join(output_dir, "yolov5_"+ video_id )
            if os.path.exists(yolo_output_dir)==False:
                os.mkdir(yolo_output_dir)
            else:
                shutil.rmtree(yolo_output_dir)
                os.mkdir(yolo_output_dir)

            # bunlar resımler için
            images_yolo_output_dir = os.path.join(yolo_output_dir, "images")
            if os.path.exists(images_yolo_output_dir)==False:
                os.mkdir(images_yolo_output_dir)

            train_images_yolo_output_dir = os.path.join(images_yolo_output_dir, "train")
            if os.path.exists(train_images_yolo_output_dir)==False:
                os.mkdir(train_images_yolo_output_dir)

            val_images_yolo_output_dir = os.path.join(images_yolo_output_dir, "val")
            if os.path.exists(val_images_yolo_output_dir)==False:
                os.mkdir(val_images_yolo_output_dir)

            #bunlar etıketler ıcın
            labels_yolo_output_dir = os.path.join(yolo_output_dir, "labels")
            if os.path.exists(labels_yolo_output_dir)==False:
                os.mkdir(labels_yolo_output_dir)

            train_labels_yolo_output_dir = os.path.join(labels_yolo_output_dir, "train")
            if os.path.exists(train_labels_yolo_output_dir)==False:
                os.mkdir(train_labels_yolo_output_dir)

            val_labels_yolo_output_dir = os.path.join(labels_yolo_output_dir, "val")
            if os.path.exists(val_labels_yolo_output_dir)==False:
                os.mkdir(val_labels_yolo_output_dir)


            file_yaml = open(yolo_output_dir+'/custom_'+video_id+'.yaml', 'w')

            file_yaml.write("train: "+os.path.join(video_id,"images","train") + "\n")
            file_yaml.write("val: "+os.path.join(video_id,"images","val") + "\n")


            file_yaml.write("\n")
            file_yaml.write("\n")
            file_yaml.write("# number of classes"+"\n")
            file_yaml.write("nc: "+str(self.split_max_class_count+1))
            file_yaml.write("\n")
            file_yaml.write("\n")
            file_yaml.write("# class names"+ "\n")
            class_name = "names: [ "
            for i in range(int(self.split_max_class_count)+1):
                class_name = class_name+"'"+str(i)+"',"
            
            class_name = class_name +" ]"
            file_yaml.write(class_name+"\n")

            counter = 1
            index_test = round(100 / self.percentage_valid)
            for png_file in glob.iglob(os.path.join(current_dir, '*.png')):
                title, ext = os.path.splitext(os.path.basename(png_file))
                txt_file = os.path.join(current_dir, title+'.txt')
                if counter == index_test:
                    counter = 1
                    shutil.copy(png_file, val_images_yolo_output_dir)
                    shutil.copy(txt_file, val_labels_yolo_output_dir)
                else:
                    shutil.copy(png_file, train_images_yolo_output_dir)
                    shutil.copy(txt_file, train_labels_yolo_output_dir)
                    counter = counter + 1

            file_yaml.close()



if __name__ == '__main__':
    split_dataset = SplitDataset()
    split_dataset.run()