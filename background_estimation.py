'''
https://learnopencv.com/simple-background-estimation-in-videos-using-opencv-c-python/

'''
import numpy as np
import cv2
from skimage import data, filters
 
# Videoyu okuyun
cap = cv2.VideoCapture('_videos/backg_esti.mp4')
 
# Rastgele 25 kare seçin
frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)
 
# Seçilen kareleri bir array de sakla
frames = []
for fid in frameIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    frame= cv2.resize(frame, (640, 480))
    frames.append(frame)
 
# Zaman ekseni boyunca medyanı hesaplayın
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)   

# Median frame i göster
cv2.imshow('frame', medianFrame)
cv2.waitKey(0)

# Frame numarasını sıfırla
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
 
# Arka planı gri tonlamaya dönüştür
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
 
# Tüm frame ler üzerinde döngü
ret = True
while(ret):
 
  # Frame i oku
  ret, frame = cap.read()

  if ret == False:
    break
  # Geçerli çerçeveyi gri tonlamaya dönüştür
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  frame= cv2.resize(frame, (640, 480))
  # Geçerli frame ve median frame in mutlak farkını hesaplayın
  dframe = cv2.absdiff(frame, grayMedianFrame)
  # Treshold to binarize
  th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
  # Resmi görüntüle
  cv2.imshow('frame', dframe)
  cv2.waitKey(20)
 
# Video nesnesini serbest bırak
cap.release()

cv2.destroyAllWindows()