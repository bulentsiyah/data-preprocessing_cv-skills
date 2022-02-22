import glob
import os
import argparse
from pydoc import text

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
        self.parser.add_argument('-p', '--percentage_valid', help='yuzde kac valid icin', default=config_percentage_valid)

        args = self.parser.parse_args()

        self.percentage_valid = int(args.percentage_valid)
        self.configurationManager.set_split_percentage_valid(split_percentage_valid=self.percentage_valid)


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
        
        video_path = root_path + self.configurationManager.config_readable['video_path_file']
        video_id = os.path.splitext(os.path.basename(video_path))[0]
        parent_dir = root_path + self.configurationManager.config_readable['video_save_path_folder']
        current_dir = os.path.join(parent_dir, video_id)

        file_train = open(parent_dir+'/train.txt', 'w')
        file_test = open(parent_dir+'/valid.txt', 'w')

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

if __name__ == '__main__':
    split_dataset = SplitDataset()
    split_dataset.run()