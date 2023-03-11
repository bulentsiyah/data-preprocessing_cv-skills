from ultralytics import YOLO
from PIL import Image
import cv2
import torch





video_path = 'E:/Datasets/AmazonAirPrime/airborne-detection-starter-kit/data/part1/Images/00bb96a5a68f4fa5bc5c5dc66ce314d2/00bb96a5a68f4fa5bc5c5dc66ce314d2.mp4'
video_path = 'E:/Datasets/AmazonAirPrime/airborne-detection-starter-kit/data/part1/Images/0001ba865c8e410e88609541b8f55ffc/0001ba865c8e410e88609541b8f55ffc.mp4'

model = YOLO("E:/Codes/data-preprocessing_cv-skills/runs/detect/yolov8x_custom_imgsz_1024/weights/best.pt")


print('cuda_avail:', torch.cuda.is_available())
print('cuda_device:', torch.cuda.device_count())

'''

>>> torch.cuda.is_available()
True

>>> torch.cuda.device_count()
1

>>> torch.cuda.current_device()
0

>>> torch.cuda.device(0)
<torch.cuda.device at 0x7efce0b03be0>

>>> torch.cuda.get_device_name(0)
'GeForce GTX 950M'


'''



# Bir video nesnesi oluşturulur, bu durumda videoyu bir dosyadan okuyoruz
'''
vid_capture = cv2.VideoCapture(0) web kamerası
vid_capture = cv2.VideoCapture(1) normal kamera"
vid_capture = cv2.VideoCapture('Resources/Image_sequence/Cars%04d.jpg') >>> (Cars0001.jpg, Cars0002.jpg, Cars0003.jpg,...)
gibi bir görüntü dizinini okumaya yarar 
'''
vid_capture = cv2.VideoCapture(video_path)

height, width = 2048 , 2448 

if (vid_capture.isOpened() == False):
  print("Error opening the video file")

# fps ve kare sayısı okunur
else:
  # Kare hızı bilgilerini almak 
  # 5'i CAP_PROP_FPS ile de değiştirebilirsiniz, bunlar numaralandırmadır
  fps = vid_capture.get(5)
  print('Frames per second : {} FPS'.format(fps))

 # Kare sayısını almak
 # 7'yi CAP_PROP_FRAME_COUNT ile de değiştirebilirsiniz, bunlar numaralandırmadır
  frame_count = vid_capture.get(7)
  print('Frame count : ', frame_count)

while(vid_capture.isOpened()):
  # vid_capture.read() bir tuple döndürür, ilk eleman bool ve ikincisi frame
  ret, frame = vid_capture.read()
  if ret == True:

    frame = cv2.resize(frame, (int(width/2),int(height/2)))


    results = model.predict(source=frame, save=True, show=True, device=0)

    #cv2.imshow('Frame',frame)

    # waitKey() pencereyi kapatmak için bir tuşa basılmasını bekler ve 20 milisaniye cinsindendir
    key = cv2.waitKey(20)

    if key == ord('q'):
      break
  else:
    break

# Video capture nesnesini serbest bırakın
vid_capture.release()
cv2.destroyAllWindows()



