import glob
import os
import shutil
from IPython.display import display, clear_output, HTML
from core.dataset import Dataset

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import cv2
import pandas as pd

from enum import Enum

class ObjectTypes(Enum):
    Airplane = 0
    Helicopter = 1
    Bird = 2
    Drone = 3
    Flock = 4
    Airborne = 5


class Main():

    def __init__(self):

        mantis_anapath='E:/Datasets/Mantis-Shrimp-Eye-s-Collision-Avoidance'

        self.video_out_path = mantis_anapath +"/videos"
        if os.path.exists(self.video_out_path)==False:
            print('created')
            os.mkdir(self.video_out_path)

        # part1 ve images path yolu

        self.part1_path = 'D:/'+'/airborne-detection-starter-kit/data/part1/'
        self.images_path = self.part1_path+'Images'

        # Klasördeki klasörlerin listesi
        self.folders = [f for f in os.listdir(self.images_path) if os.path.isdir(os.path.join(self.images_path, f))]

        #aws deki url ve yer
        self.dataset = Dataset(self.part1_path, 's3://airborne-obj-detection-challenge-training/part1/', partial=True, prefix='part1')

        #yolo pathleri
        self.yolo_output_dir = os.path.join(mantis_anapath, "yolo_dataset/" )

        #dnn pathleri
        self.dnn_output_dir = os.path.join(mantis_anapath, "dnn_dataset/" )

        #siamese pathleri
        self.siamese_output_dir = os.path.join(mantis_anapath, "siamese_dataset/" )

        #tüm train operasyonu ana dataframei
        self.path_ana_train_islemis_dataframe = mantis_anapath+'/ana_train_islemis_dataframe.csv'
        try:
            self.ana_train_islemis_dataframe =pd.read_csv(self.path_ana_train_islemis_dataframe)
        except:
            df_cols = ['flight_id', 'toplam_frame' , 'aldigimiz_background_sayisi', 'toplam_background_sayisi','all_objects']
            self.ana_train_islemis_dataframe = pd.DataFrame(columns=df_cols)

        self.video_out_path_train = self.video_out_path +"/train"
        if os.path.exists(self.video_out_path_train)==False:
            print('created')
            os.mkdir(self.video_out_path_train)

        #tüm test_background operasyonu ana dataframei
        self.path_ana_test_background_islemis_dataframe = mantis_anapath+'/ana_test_background_islemis_dataframe.csv'
        try:
            self.ana_test_background_islemis_dataframe =pd.read_csv(self.path_ana_test_background_islemis_dataframe)
        except:
            df_cols = ['flight_id', 'toplam_frame' ]
            self.ana_test_background_islemis_dataframe = pd.DataFrame(columns=df_cols)

        self.video_out_path_test_background = self.video_out_path +"/test_back_ground"
        if os.path.exists(self.video_out_path_test_background)==False:
            print('created')
            os.mkdir(self.video_out_path_test_background)


        self.height, self.width = 2048 , 2448 # 640 * 640 height 3 width 4 küçülüyor
        self.kucuk_obje_siniri = 0 # sinir ağına orjinalde 16*16 lıklar kabuldur, boyut 4/1 kuculebılır 
        self.fps = 10

        self.kac_kere_calissin = 50


    def run(self):

        kactayiz= 0
        for lucky_flight_folder in self.folders:
            
            self.lucky_flight_id = lucky_flight_folder

            #train dataframe daha once varsa pas geç 
            flight_id_var_mi = self.ana_train_islemis_dataframe['flight_id'].str.contains(self.lucky_flight_id).any()
            if flight_id_var_mi ==True:
                #print("flight_id_var: ",self.lucky_flight_id)

                #bır kereye mahsus taşıma 
                '''video_out_path = self.images_path+"/"+self.lucky_flight_id+"/"+self.lucky_flight_id+'.mp4'
                dest_video_path= self.video_out_path_train+"/"+self.lucky_flight_id+'.mp4'
                shutil.move(video_out_path, dest_video_path)'''
                continue


            #test backgorund dataframe daha once varsa pas geç 
            flight_id_var_mi = self.ana_test_background_islemis_dataframe['flight_id'].str.contains(self.lucky_flight_id).any()
            if flight_id_var_mi ==True:
                #print("flight_id_var: ",self.lucky_flight_id)
                continue

            self.lucky_flight = None
            try:
                self.lucky_flight = self.dataset.get_flight_by_id(self.lucky_flight_id)
            except:
                self.ucusBulunamadi()
                continue

            kactayiz = kactayiz+1

            if kactayiz>self.kac_kere_calissin:
                print("{}'de break durdurdu: ".format(kactayiz))
                break

            print("üzerine çalışılıyor: ",self.lucky_flight_id, " -----> kactayiz: ", kactayiz)

            temp_kac_object_var = 0
            temp_kac_framede_obje_var = 0
            temp_nesnenin_basladigi_yerler = []
            temp_nesnenin_bittigi_yerler = []
            for i in range (0,len(self.lucky_flight.valid_encounter)):
                temp_kac_object_var = temp_kac_object_var +1
                valid = self.lucky_flight.valid_encounter[i]
                temp_nesnenin_basladigi_yerler.append(valid['framemin'])
                temp_nesnenin_bittigi_yerler.append(valid['framemax'])
                temp_kac_framede_obje_var=temp_kac_framede_obje_var+valid['framecount']

            temp_kac_tane_background_lazim = temp_kac_framede_obje_var / 10 # 97 ise 10 tane-2.örnek ise 10 

            temp_kac_bas_var_kac_son_var = len(temp_nesnenin_basladigi_yerler)  + len(temp_nesnenin_bittigi_yerler) #2 dır-2.ornek ıcın 4 tur
            temp_kelle_basi_kac_resim = int(temp_kac_tane_background_lazim /temp_kac_bas_var_kac_son_var)
            hangi_frameleri_alayim = []

            for i in range (0,len(temp_nesnenin_basladigi_yerler)): 
                bulundugu_ilk_yer = temp_nesnenin_basladigi_yerler[i]  #229 --- varsa kus 100 --228-227-226-225
                for j in range(temp_kelle_basi_kac_resim,0,-1):
                    hangi_frameleri_alayim.append(bulundugu_ilk_yer -j) 

            for i in range (0,len(temp_nesnenin_bittigi_yerler)): 
                bulundugu_ilk_yer = temp_nesnenin_bittigi_yerler[i]  #325 --- varsa kus 350
                for j in range(0,temp_kelle_basi_kac_resim):
                    hangi_frameleri_alayim.append(bulundugu_ilk_yer +j+1) 



            '''self.mdPrint("List of Airborne Objects: ")
            for airborne_obj in self.lucky_flight.get_airborne_objects():
                self.mdPrint("- %s " % airborne_obj)'''

            all_keys = []
            all_keys_not_remove= []

            all_keys.extend([self.removeNumbers(k) for k in self.lucky_flight.detected_objects])
            all_keys_not_remove.extend([k for k in self.lucky_flight.detected_objects])

            #unique_keys = list(set(all_keys))
            #print('unique_keys',unique_keys)
            #print('unique_keys_not_remove',str(set(all_keys_not_remove)))

            rows_for_dnn = self.yoloTxtPreSiamese()

            toplam_frame,aldigimiz_background_sayisi, toplam_background_sayisi= self.yoloDatasetPreVideo(hangi_frameleri_alayim)

            #dnn  
            self.dnnDataset(rows_for_dnn)

            #dataframe kaydet

            self.ana_train_islemis_dataframe = self.ana_train_islemis_dataframe.append({'flight_id': str(self.lucky_flight_id),
                                                                        'toplam_frame': str(toplam_frame),
                                                                        'aldigimiz_background_sayisi': str(len(aldigimiz_background_sayisi)),
                                                                        'toplam_background_sayisi': str(toplam_background_sayisi),
                                                                        'all_objects': str(str(set(all_keys_not_remove)))}, 
                                                                        ignore_index=True, verify_integrity=False,
                                                                                sort=False)


        
            self.ana_train_islemis_dataframe.to_csv(self.path_ana_train_islemis_dataframe, index=False)

            

    def ucusBulunamadi(self,):

        print("ucus bulunamadi: ",self.lucky_flight_id)

        current_pure_images_dir = self.images_path+"/"+self.lucky_flight_id

        video_out_path = self.video_out_path_test_background+"/"+self.lucky_flight_id+'.mp4'

        if os.path.exists(video_out_path):
            vision_frame_save_out = None
        else:
            vision_frame_save_out = cv2.VideoWriter(video_out_path ,cv2.VideoWriter_fourcc(*'xvid'), self.fps, (self.width,self.height)) 

        toplam_frame=0
        for png_file in glob.iglob(os.path.join(current_pure_images_dir, '*.png')):
            toplam_frame = toplam_frame + 1
            try:
                frame = cv2.imread(png_file)
                if vision_frame_save_out is not None:
                    vision_frame_save_out.write(frame)
                    print("-------video olusturuluyor-----")
                else:
                    print("-------video pas geciyor-----")
                    pass
                    
            except:
                print("try-catch save_vision_frame_save")
                pass
            

        self.ana_test_background_islemis_dataframe = self.ana_test_background_islemis_dataframe.append({'flight_id': str(self.lucky_flight_id),
                                                                        'toplam_frame': str(toplam_frame)},
                                                                        ignore_index=True, verify_integrity=False,
                                                                                sort=False)


        
        self.ana_test_background_islemis_dataframe.to_csv(self.path_ana_test_background_islemis_dataframe, index=False)

    # keys
    def removeNumbers(self,s):
        return ''.join([i for i in s if not i.isdigit()])

    def mdPrint(self, text):
        display({
            'text/markdown': text,
            'text/plain': text
        }, raw=True)

    def dnnDataset(self,rows):

        if os.path.exists(self.dnn_output_dir)==False:
            print('created')
            os.mkdir(self.dnn_output_dir)

        df = pd.DataFrame(rows)
        df.columns = ['flight_id', 'object_type', 'object', 'frame_id', 
                    'left', 'top', 'width', 'height', 'area', 'image_path','range_distance']
        #print(df.head())
        df.to_csv(self.dnn_output_dir+str(self.lucky_flight_id)+".csv", index=False)


    def siameseDataset(self,object_type,obj_key,img_crop,temp_image_path_witout_ext):
        
        if os.path.exists(self.siamese_output_dir)==False:
            print('created')
            os.mkdir(self.siamese_output_dir)

        temp_object_type_folder =self.siamese_output_dir+"/"+object_type
        if os.path.exists(temp_object_type_folder)==False:
            print('created')
            os.mkdir(temp_object_type_folder)

        '''temp_flight_id_folder =self.siamese_output_dir+"/"+object_type
        if os.path.exists(temp_flight_id_folder)==False:
            print('created')
            os.mkdir(temp_flight_id_folder)'''

        temp_image_path = temp_object_type_folder+"/"+temp_image_path_witout_ext+"_"+str(obj_key)+".png"
        cv2.imwrite(temp_image_path,img_crop)
        

    def goruntuyuTasiVeyaOlcekliKopyala(self,png_file, val_images_yolo_output_dir, frame_resize, title):
        orjinalini_bozma =False

        if orjinalini_bozma:
            shutil.move(png_file, val_images_yolo_output_dir)
        else:
            cv2.imwrite(val_images_yolo_output_dir+"/"+title+".png", frame_resize)

    def yoloDatasetPreVideo(self,hangi_frameleri_alayim):

        if os.path.exists(self.yolo_output_dir)==False:
            print('created')
            os.mkdir(self.yolo_output_dir)
        
        current_dir = self.part1_path+'/Images/'+self.lucky_flight_id

        #video_out_path = current_dir+"/"+self.lucky_flight_id+'.mp4'
        video_out_path = self.video_out_path_train+"/"+self.lucky_flight_id+'.mp4'

        if os.path.exists(video_out_path):
            vision_frame_save_out = None
        else:
            vision_frame_save_out = cv2.VideoWriter(video_out_path ,cv2.VideoWriter_fourcc(*'xvid'), self.fps, (self.width,self.height)) 

        # bunlar resımler için
        train_yolo_output_dir = os.path.join(self.yolo_output_dir, "train"+"_"+str(self.lucky_flight_id))
        if os.path.exists(train_yolo_output_dir)==False:
            os.mkdir(train_yolo_output_dir)

        train_images_yolo_output_dir = os.path.join(train_yolo_output_dir, "images")
        if os.path.exists(train_images_yolo_output_dir)==False:
            os.mkdir(train_images_yolo_output_dir)

        train_labels_yolo_output_dir = os.path.join(train_yolo_output_dir, "labels")
        if os.path.exists(train_labels_yolo_output_dir)==False:
            os.mkdir(train_labels_yolo_output_dir)

        val_yolo_output_dir = os.path.join(self.yolo_output_dir, "val"+"_"+str(self.lucky_flight_id))
        if os.path.exists(val_yolo_output_dir)==False:
            os.mkdir(val_yolo_output_dir)

        val_images_yolo_output_dir = os.path.join(val_yolo_output_dir, "images")
        if os.path.exists(val_images_yolo_output_dir)==False:
            os.mkdir(val_images_yolo_output_dir)


        '''background_yolo_output_dir = os.path.join(self.yolo_output_dir, "background"+"_"+str(self.lucky_flight_id))
        if os.path.exists(background_yolo_output_dir)==False:
            os.mkdir(background_yolo_output_dir)'''


        #bunlar etıketler ıcın
        val_labels_yolo_output_dir = os.path.join(val_yolo_output_dir, "labels")
        if os.path.exists(val_labels_yolo_output_dir)==False:
            os.mkdir(val_labels_yolo_output_dir)

        split_max_class_count = len(ObjectTypes)

        temp_path_custom_yaml_file = self.yolo_output_dir+'custom.yaml'
        if os.path.exists(temp_path_custom_yaml_file)==False:
            
            file_yaml = open(temp_path_custom_yaml_file, 'w')

            file_yaml.write("path: "+str(self.yolo_output_dir)+ "\n" + "\n")

            file_yaml.write("train:  "+"\n")
            file_yaml.write("   "+"- train"+"_"+str(self.lucky_flight_id) + "\n")
            file_yaml.write("val: "+ "\n")
            file_yaml.write("   "+"- val"+"_"+str(self.lucky_flight_id) + "\n")

            file_yaml.write("\n")
            file_yaml.write("\n")
            file_yaml.write("# number of classes"+"\n")
            file_yaml.write("nc: "+str(split_max_class_count))
            file_yaml.write("\n")
            file_yaml.write("\n")
            file_yaml.write("# class names"+ "\n")

            class_name = "names: ["
            for i in range(int(split_max_class_count)):
                if i == split_max_class_count-1:
                    class_name = class_name+"'"+str(i)+"'"
                else:
                    class_name = class_name+"'"+str(i)+"',"
            class_name = class_name +"]"

            file_yaml.write(class_name+"\n")
            file_yaml.close()

        else:
            read_yaml = open(temp_path_custom_yaml_file, 'r').readlines()

            with open(temp_path_custom_yaml_file, 'w') as outfile:
                for index, line in enumerate(read_yaml):
                    try:
                        #index = int(line.split(" ")[0])
                        if line.strip() == str("train:  "+"\n").strip():
                            outfile.write(line)
                            outfile.write("   "+"- train"+"_"+str(self.lucky_flight_id) + "\n")
                        elif line.strip() == str("val:  "+"\n").strip():
                            outfile.write(line)
                            outfile.write("   "+"- val"+"_"+str(self.lucky_flight_id) + "\n")
                        else:
                            outfile.write(line)
                    except:
                        pass
    
                outfile.close()


        split_percentage_valid = 20

        counter = 1
        toplam_background_sayisi=0
        toplam_frame=0
        aldigimiz_background_sayisi = 0
        index_test = round(100 / split_percentage_valid)
        #black_img = np.zeros((self.height,self.width,3), dtype = np.uint8)
        for png_file in glob.iglob(os.path.join(current_dir, '*.png')):
            title, ext = os.path.splitext(os.path.basename(png_file))
            txt_file = os.path.join(current_dir, title+'.txt')
            toplam_frame = toplam_frame + 1

            back_icin = toplam_frame + 2 # TODO back icin anlamadıgımızdan elle gerı cektık

            try:
                frame = cv2.imread(png_file)
                if vision_frame_save_out is not None:
                    vision_frame_save_out.write(frame)
                    print("-------video olusturuluyor-----")
                else:
                    print("-------video pas geciyor-----")
                    pass
                    
            except:
                print("try-catch save_vision_frame_save")
                pass
        
            frame_resize = frame #cv2.resize(frame, (int(self.width/2),int(self.height/2)))
            
            if counter == index_test:
                counter = 1

                try:
                    shutil.move(txt_file, val_labels_yolo_output_dir)
                    self.goruntuyuTasiVeyaOlcekliKopyala(png_file, val_images_yolo_output_dir, frame_resize, title)
                    
                except:
                    #print("txt yok olabılır"+ext,title,ext)
                    toplam_background_sayisi = toplam_background_sayisi +1
                    if back_icin in hangi_frameleri_alayim:
                        self.goruntuyuTasiVeyaOlcekliKopyala(png_file, val_images_yolo_output_dir, frame_resize, title)
                        print("val a back koydum",toplam_frame," back_icin",back_icin)
                        aldigimiz_background_sayisi=aldigimiz_background_sayisi+1
                    else:
                        pass
                        #shutil.move(png_file, background_yolo_output_dir)
            else:
                try:
                    shutil.move(txt_file, train_labels_yolo_output_dir)
                    self.goruntuyuTasiVeyaOlcekliKopyala(png_file, train_images_yolo_output_dir, frame_resize, title)
                except:
                    #print("txt yok olabılır"+ext,title,ext)
                    toplam_background_sayisi = toplam_background_sayisi +1
                    if back_icin in hangi_frameleri_alayim:
                        self.goruntuyuTasiVeyaOlcekliKopyala(png_file, train_images_yolo_output_dir, frame_resize, title)
                        print("traine a background koydum",toplam_frame," back_icin",back_icin)
                        aldigimiz_background_sayisi=aldigimiz_background_sayisi+1
                    else:
                        pass
                        #shutil.move(png_file, background_yolo_output_dir)

                counter = counter + 1

            
            #cv2.imwrite(png_file, black_img)

        print('hangi_frameleri_alayimsayisi',str(hangi_frameleri_alayim))
        print('toplam_background_sayisi',toplam_background_sayisi)
        print('toplam_frame',toplam_frame)
        return toplam_frame, aldigimiz_background_sayisi, toplam_background_sayisi
            
    def yoloTxtPreSiamese(self,):

        # oncekı txtleri siler
        print_show = False
        tifCounter = 0
        myPath = self.part1_path+'/Images/'+self.lucky_flight_id

        if print_show:
            print(myPath)
        for root, dirs, files in os.walk(myPath):
            for file in files:    
                if file.endswith('.txt'):
                    #print(file)
                    os.remove(myPath+'/'+file)
                    tifCounter += 1

        rows = []
        
        resim_indir = 0
        for obj_key in self.lucky_flight.detected_objects:
            object_type = self.removeNumbers(obj_key)
            enum_value = ObjectTypes[object_type].value
            if enum_value==0 or enum_value==1:
                if print_show:
                    print('object_type',object_type)
                obj = self.lucky_flight.detected_objects[obj_key]

                if print_show:
                    print('obj',obj)
                
                for loc in obj.location:

                    resim_indir = resim_indir + 1
                    bbox = loc.bb.get_bbox()
                    #print('bbox',bbox)
                    frame_id = loc.frame.id
                    #print('frame_id',frame_id)
                    range_distance = loc.range_distance_m
                    #print('range_distance',range_distance)
                    image_path = loc.frame.image_path()
                    image_base_name=os.path.basename(loc.frame.image_path())
                    image_path = myPath + "/"+image_base_name
                    #print('image_path',image_path)
                    rows.append([self.lucky_flight_id, object_type, obj_key, frame_id,*bbox, bbox[-1]*bbox[-2], image_path, range_distance])

                    (x, y, w, h) = [int(v) for v in bbox]

                    center_x = (x + (x+w))/2
                    center_y = (y +(y+h))/2
                    yolo_x = format(center_x/self.width, '.6f')
                    yolo_y = format(center_y/self.height, '.6f')

                    yolo_w = format(w/self.width, '.6f')
                    yolo_h = format(h/self.height, '.6f')

                
                    yolo_line = '{0} {1} {2} {3} {4}'.format(enum_value, yolo_x, yolo_y, yolo_w, yolo_h)

                    en_kucuk_degerden_buyukmu = True

                    if w<= self.kucuk_obje_siniri or h<= self.kucuk_obje_siniri:
                        en_kucuk_degerden_buyukmu = False


                    temp_image_path_witout_ext = image_base_name.split(".")[0]
                    txt_path= image_path.split(".")[0]

                    if print_show:
                        print('image_path:', image_path)
                        print('1: ',txt_path)
                    txt_path=txt_path+".txt"
                    if os.path.exists(txt_path)==False:
                        file = open(txt_path, 'w')
                        file.close()


                    infile = open(txt_path,'r', encoding='utf-8').readlines()
                    with open(txt_path, 'w', encoding='utf-8') as outfile:
                        outfile.writelines(infile)
                        if en_kucuk_degerden_buyukmu:
                            outfile.writelines(yolo_line+"\n")


                    img_crop = cv2.imread(image_path)
                    img_crop = img_crop[y:y+h,x:x+w]
                    if en_kucuk_degerden_buyukmu:
                        self.siameseDataset(object_type,obj_key,img_crop,temp_image_path_witout_ext)
                    

                    if print_show:
                        print('--------------------------')



        return rows





if __name__ == '__main__':
    main = Main()
    main.run()
